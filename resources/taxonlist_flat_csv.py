# csv...

import requests
from urlparse import urlparse
import urllib2

from resources.lists import taxonlistflat

from database.dbtaxonname import getAllTaxonNamesFromListFlat, getTaxonNameAllAcceptedNames
from database.dbprojects import getProject

from flask.ext import restful
from flask import Flask,g, request, render_template
from flask import url_for
from flask.ext.restful import Resource, fields, marshal_with
from flask import url_for, Response

class taxonlist_flat_csv(restful.Resource):
    def get(self, database, id):
        project = getProject('DiversityProjects_TNT', id)
        taxonnamelist = getAllTaxonNamesFromListFlat(database, id)
        for row in taxonnamelist:
            uri =  url_for('name', database=database, id = row['NameID'], _external=True)
            row['taxonID'] = uri
            if row['HierarchieNameParentID'] is not None and row['HierarchieNameParentID'] != -1:
                uri_parent = url_for('name', database=database, id = row['HierarchieNameParentID'], _external=True)
            else:
                uri_parent = None
            row['parentNameUsageID'] = uri_parent
            if row['AcceptedNameProject'] is None and row['SynonymieNameID'] is not None:
                synonym_is_accepted = getTaxonNameAllAcceptedNames(database, row['SynonymieNameID'])
                if len(synonym_is_accepted) > 0 and synonym_is_accepted[0]['NameID'] is not None:
                    uri_synonym = url_for('name', database=database, id = row['NameID'], _external=True)
                else:
                    uri_synonym = None
            else:
                uri_synonym = None
            row['acceptedNameUsageID'] = uri_synonym    
        response = Response(render_template("taxonlist_flat_csv.j2", database=database, id=id, taxonnames=taxonnamelist, project=project[0]) )
        response.headers['content-type'] = 'text/comma-separated-values'
        return response