# names
# REST interface to names
# build up URIs and links

from flask.ext import restful
from flask.ext.restful import Resource, fields, marshal_with
from flask import url_for
import urllib2
from database.name import *

def makelink(label, name, the_uri):
    link = {}
    link['uri'] = the_uri
    link['type'] = 'uri'
    link['rel'] = name
    link['name'] = label
    return link

class names(restful.Resource):
    def get(self):
        namelist = getAllNames()
        for row in namelist:
            row['nameuri'] = url_for('name', database=row['DatabaseName'], id = row['NameID'])
        return namelist


#name_sublinks = {
    #'commonnames': fields.Url('nameCommonNames'),
    #'acceptednames': fields.Url('nameAcceptedNames'),
    #'synonyms': fields.Url('nameSynonyms'),
    #'hierarchies': fields.Url('nameHierarchies')
#}

#name_fields = {
    #'TaxonNameCache' : fields.String,
    #'links' : name_sublinks
    #}

class name(restful.Resource):
    #@marshal_with(name_fields)
    def get(self, database, id):
        nameinfo = getName(database, id)
        for row in nameinfo:
            links = []
            links.append(makelink('commonnames', 'related', url_for('namecommonnames', database=row['DatabaseName'], id=row['NameID']) ))
            links.append(makelink('acceptednames', 'related', url_for('nameacceptednames', database=row['DatabaseName'], id=row['NameID']) ))
            links.append(makelink('synonyms', 'related', url_for('namesynonyms', database=row['DatabaseName'], id=row['NameID']) ))
            links.append(makelink('hierarchies', 'related', url_for('namehierarchies', database=row['DatabaseName'], id=row['NameID']) ))
            row['links'] = links
        return nameinfo

class nameCommonNames(restful.Resource):
    def get(self, database, id):
        cnamelist =  getNameAllCommonNames(database, id)
        for row in cnamelist:
            links = []
            
            #print __file__ +" : "+row['CommonName']
            newid = u"[%s,%s,%s,%s]" % (row['CommonName'], row['LanguageCode'], row['CountryCode'], row['ReferenceTitle'])
            #newid = urllib2.quote(newid.encode('utf-8')) # no utf8 but %xx encoding in urls 
            #url = u"http://tnt.diversityworkbench.de/commonnames/%s/%s/%s" % (row['DatabaseName'], row['NameID'], newid )
            url = url_for('commonname', database=row['DatabaseName'], nameid=row['NameID'], cid=newid)
            #print url
            links.append(makelink('commonnames','related', url))
            row['links'] = links
            #print __file__ +" : " + row['commonnameuri']
        return cnamelist

class nameAcceptedNames(restful.Resource):
    def get(self, database, id):
        anlist = getNameAllAcceptednames(database, id)
        for row in anlist:
            links=[]
            links.append(makelink('acceptedname', 'related', url_for('acceptedname', database=row['DatabaseName'], projectid=row['ProjectID'], nameid=row['NameID'])))
            row['links'] = links
        return anlist        

class nameSynonyms(restful.Resource):
    def get(self, database, id):
        slist = getNameAllSynonyms(database, id)
        for row in slist:
            links = []
            links.append(makelink('synonymy', 'related',  url_for('synonymy', database=row['DatabaseName'], projectid=row['ProjectID'], nameid=row['NameID'], synnameid=row['SynNameID'])))
            row['links'] = links
        return slist        

class nameHierarchies(restful.Resource):
    def get(self, database, id):
        hlist = getNameAllHierarchies(database, id)
        for row in hlist:
            links=[]
            links.append(makelink('hierarchy', 'related', url_for('hierarchy', database=row['DatabaseName'], projectid=row['ProjectID'], nameid=row['NameID'])))
            row['links'] = links
        return hlist        

#name addittions
# getacceptedname(database, projectid, nameid,  ignore):
# getsynonymy(database, projectid, nameid, synnameid, ignore):
# gettaxonhierarchy(database, projectid, nameid, ignore):

class acceptedname(restful.Resource):
    def get(self, database, projectid, nameid):
        alist = getacceptedname(database, projectid, nameid, 0)
        for row in alist:
            links=[]
            links.append(makelink('project', 'related', url_for('project', id=row['ProjectID'])))
            row['links'] = links
        return alist
   
class synonymy(restful.Resource):
    def get(self, database, projectid, nameid, synnameid):
        slist = getsynonymy(database, projectid, nameid, synnameid, 0)
        for row in slist:
            links=[]
            links.append(makelink('synonymname', 'related', url_for('name', database=row['DatabaseName'], id=row['SynNameID'])))
            row['links'] = links
        return slist

class hierarchy(restful.Resource):
    def get(self, database, projectid, nameid):
        hlist = gettaxonhierarchy(database, projectid, nameid, 0)
        for row in hlist:
            links=[]
            links.append(makelink('parent', 'related', url_for('name', database=row['DatabaseName'], id=row['NameParentID'])))
            links.append(makelink('project', 'related', url_for('project', id=row['ProjectID'])))                     
            row['links'] = links
        return hlist
    
