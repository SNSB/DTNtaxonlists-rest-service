# webinterface...

import requests
from urllib.parse import urlparse
import urllib.request, urllib.error, urllib.parse

from database.commonname import getcommonname
from database.agent import getagents, getagent, getagentrelations
from database.project import getproject, getprojectagents
from database.name import *
from database.list import getList, getAllLists, getListProject

from resources.names import namecommonnames


import flask_restful as restful
from flask import Flask,g, request, render_template
from flask import url_for
from flask_restful import Resource, fields, marshal_with
from flask import url_for, Response

class wwwtaxonlist(restful.Resource):
    def get(self, database, id):
        taxonnamelist = getList(database, id)
        for nameitem in taxonnamelist:
            nameinfo = getName(nameitem['database'], nameitem['nameid'])
            commonnamesurl=url_for("namecommonnames", database=nameitem['database'], id=nameitem['nameid'], _external=True)
            nameinfo[0]['commonnamesurl']=commonnamesurl
            allcommonnames=getNameAllCommonNames(nameitem['database'], nameitem['nameid'])
            nameinfo[0]['commonnames']=allcommonnames
            nameitem['nameinfo']=nameinfo
        taxonlistproject = getproject('DiversityProjects_TNT',id)
        taxonlistagents = getprojectagents('DiversityProjects_TNT', id)
        response = Response(render_template("taxonlist_internal.html", database=database, id=id, taxonnames=taxonnamelist, taxonlistproject=taxonlistproject, taxonlistagents=taxonlistagents) )
        response.headers['content-type'] = 'text/html'
        return response
    