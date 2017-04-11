# lists
# REST interface to LISTS

from flask.ext import restful
from flask.ext.restful import fields, marshal_with
from flask import url_for, Response
from database.list import getList, getAllLists, getListProject
from database.dbtaxonname import getAllTaxonNamesFromListFlat
from urlparse import urlparse
from flask import Flask,g, request, render_template

import requests

def makelink(label, name, the_uri):
    link = {}
    link['uri'] = the_uri
    link['type'] = 'uri'
    link['rel'] = name
    link['name'] = label
    return link

class taxonlist(restful.Resource):
    def get(self, database, id):
        namelist = getList(database, id)
        for row in namelist:
            links=[]
            uri =  url_for('name', database=database, id = row['nameid'], _external=True)
            links.append(makelink('taxonname', 'details', uri))
            row['links'] = links
        return namelist
    
class taxonlistflat(restful.Resource):
    def get(self, database, id):
        namelist = getAllTaxonNamesFromListFlat(database,id)
        for row in namelist:
            uri =  url_for('name', database=database, id = row['NameID'], _external=True)
            row['taxonID'] = uri
            if row['HierarchieNameParentID'] is not None and row['HierarchieNameParentID'] != -1:
                uri_parent = url_for('name', database=database, id = row['HierarchieNameParentID'], _external=True)
            else:
                uri_parent = None
            row['parentNameUsageID'] = uri_parent
            if row['SynonymieNameID'] is not None:
                uri_synonym = url_for('name', database=database, id = row['SynonymieNameID'], _external=True)
            else:
                uri_synonym = None
            row['acceptedNameUsageID'] = uri_synonym
            
            
        return namelist

class taxonlistproject(restful.Resource):
    def get(self, database, id):
        listlist = getListProject(database, id)
        for row in listlist:
            links=[]
            row["projecturi"] = urlparse(row["projecturi"]).path
            projecturi = url_for('project', id=id, _external=True)
            links.append(makelink('listproject', 'related', projecturi))
            row['links'] = links
        return listlist
    
class taxonlists(restful.Resource):
    def get(self):
        listlist = getAllLists()
        for row in listlist:
            links = []
            row["projecturi"] = urlparse(row["projecturi"]).path
            projecturi = url_for('project', id=row['projectid'], _external=True)
            links.append(makelink('listproject', 'related', projecturi))
            listurl = url_for('taxonlist',  database=row['DatabaseName'], id=row['projectid'], _external=True)
            links.append(makelink('taxonnamelist', 'elements', listurl)) #u"http://tnt.diversityworkbench.de/lists/%s/%s"  % (row['DatabaseName'], row['projectid'])
            links.append(makelink('analysiscategories', 'related', url_for('analysiscategoriesinproject',  database=row['DatabaseName'], projectid=row['projectid'], _external=True)))
            row['links'] = links
        return listlist
    
