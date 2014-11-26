# lists
# REST interface to LISTS

from flask.ext import restful
from flask.ext.restful import fields, marshal_with
from flask import url_for, Response
from database.list import getList, getAllLists, getListProject
from urlparse import urlparse

from flask import Flask,g, request, render_template

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
            links.append(makelink('taxonname', 'related', uri))
            row['links'] = links
        return namelist

class taxonlistproject(restful.Resource):
    def get(self, database, id):
        return getListProject(database, id)
    
class taxonlists(restful.Resource):
    def get(self):
        listlist = getAllLists()
        for row in listlist:
            links = []
            listurl = url_for('taxonlist',  database=row['DatabaseName'], id=row['projectid'], _external=True)
            links.append(makelink('taxonnamelist', 'related', listurl)) #u"http://tnt.diversityworkbench.de/lists/%s/%s"  % (row['DatabaseName'], row['projectid'])
            row["projecturi"] = urlparse(row["projecturi"]).path
            projecturi = url_for('project', id=row['projectid'], _external=True)
            links.append(makelink('listproject', 'related', projecturi))
            row['links'] = links
        return listlist
    
class taxonlistwww(restful.Resource):
    def get(self, database, id):
        response = Response(render_template("taxonlist.html", database=database, id=id) )   
        response.headers['content-type'] = 'text/html'
        return response
