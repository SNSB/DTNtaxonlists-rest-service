# names
# REST interface to names
# build up URIs and links

from flask.ext import restful
from flask.ext.restful import Resource, fields, marshal_with
from flask import url_for, Response
import urllib2
from database.name import *
from flask import Flask,g, request, render_template
from flask_restful import reqparse
from searchengine.suchen import *

def makelink(label, name, the_uri):
    link = {}
    link['uri'] = the_uri
    link['type'] = 'uri'
    link['rel'] = name
    link['name'] = label
    return link

class regenrateindex(restful.Resource):
    def get(self):
        createindex()

class names(restful.Resource):
    def get(self):
        results = []
        parser =  reqparse.RequestParser()
        parser.add_argument('name') #, type=unicode
        parser.add_argument('www', type=bool)
        parser.add_argument('exactname')
        parser.add_argument('nameid', type=int)
        parser.add_argument('exactcommonname')
        parser.add_argument('exactnamepartwithoutauthorandyear')
        args = parser.parse_args()
        #createindex()
        if args['name']:
            results = indexquery(args['name'], args['www'])
        if args['exactname']:
            temp = findName(args['exactname'])
            for row in temp:
                temprow = {}
                commonnames=getTaxonNameAllCommonNames(row['DatabaseName'], row['NameID'])
                cn = u" "
                for n in commonnames:
                    cn += n['CommonName'] + u", "
                if len(cn)>1:
                    cn=cn.strip()
                temprow['commonname'] = cn
                temprow['name'] = row['TaxonNameCache']
                temprow['url'] = url_for('name', database=row['DatabaseName'], id = row['NameID'], _external=True)
                results.append(temprow)
        if args['nameid']:
            temp = findNameID(args['nameid'])
            for row in temp:
                temprow = {}
                commonnames=getTaxonNameAllCommonNames(row['DatabaseName'], row['NameID'])
                cn = u" "
                for n in commonnames:
                    cn += n['CommonName'] + u", "
                if len(cn)>1:
                    cn=cn.strip()
                temprow['commonname'] = cn
                temprow['name'] = row['TaxonNameCache']
                temprow['url'] = url_for('name', database=row['DatabaseName'], id = row['NameID'], _external=True)
                results.append(temprow)
        if args['exactnamepartwithoutauthorandyear']:
            temp = findNamePartly(args['exactnamepartwithoutauthorandyear'])
            for row in temp:
                temprow = {}
                commonnames=getTaxonNameAllCommonNames(row['DatabaseName'], row['NameID'])
                cn = u" "
                for n in commonnames:
                    cn += n['CommonName'] + u", "
                if len(cn)>1:
                    cn=cn.strip()
                temprow['commonname'] = cn
                temprow['name'] = row['TaxonNameCache']
                temprow['url'] = url_for('name', database=row['DatabaseName'], id = row['NameID'], _external=True)
                results.append(temprow)                
        return results
        #namelist = getAllNames()
        #for row in namelist:
            #row['nameuri'] = url_for('name', database=row['DatabaseName'], id = row['NameID'], _external=True)
        #return namelist


class findexactname(restful.Resource):
    def get(self):
        parser =  reqparse.RequestParser()
        parser.add_argument('exactname')
        args = parser.parse_args()
        results = findName(args['exactname'])
        for row in results:
            row['uri'] = url_for('name', database=row['DatabaseName'], id = row['NameID'], _external=True)
        return results
        

class findallnameid(restful.Resource):
    def get(self):
        parser =  reqparse.RequestParser()
        parser.add_argument('nameid', type=int)
        args = parser.parse_args()
        results = findNameID(args['nameid'])
        for row in results:
            row['uri'] = url_for('name', database=row['DatabaseName'], id = row['NameID'], _external=True)
        return results 

class findexactcommanname(restful.Resource):
    def get(self):
        parser =  reqparse.RequestParser()
        parser.add_argument('exactcommonname')
        args = parser.parse_args()
        results = findCommonName(args['exactcommonname'])
        for row in results:
            newid = u"[%s#%s#%s#%s]" % (row['CommonName'], row['LanguageCode'], row['CountryCode'], row['ReferenceTitle'])
            url = url_for('commonname', database=row['DatabaseName'], nameid=row['NameID'], cid=newid, _external=True)
            row['url'] = url
        return results



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
            links.append(makelink('commonnames', 'related', url_for('namecommonnames', database=row['DatabaseName'], id=row['NameID'], _external=True) ))
            links.append(makelink('acceptednames', 'related', url_for('nameacceptednames', database=row['DatabaseName'], id=row['NameID'], _external=True) ))
            links.append(makelink('synonyms', 'related', url_for('namesynonyms', database=row['DatabaseName'], id=row['NameID'], _external=True) ))
            links.append(makelink('hierarchies', 'related', url_for('namehierarchies', database=row['DatabaseName'], id=row['NameID'], _external=True) ))
            links.append(makelink('listproject', 'related', url_for('project', id=row['ProjectID'], _external=True) ))
            row['links'] = links
        return nameinfo

class namecommonnames(restful.Resource):
    def get(self, database, id):
        cnamelist =  getNameAllCommonNames(database, id)
        for row in cnamelist:
            links = []
            
            #print __file__ +" : "+row['CommonName']
            newid = u"[%s#%s#%s#%s]" % (row['CommonName'], row['LanguageCode'], row['CountryCode'], row['ReferenceTitle'])
            #newid = urllib2.quote(newid.encode('utf-8')) # no utf8 but %xx encoding in urls 
            #url = u"http://tnt.diversityworkbench.de/commonnames/%s/%s/%s" % (row['DatabaseName'], row['NameID'], newid )
            url = url_for('commonname', database=row['DatabaseName'], nameid=row['NameID'], cid=newid, _external=True)
            #print url
            links.append(makelink('commonnames','details', url))
            row['links'] = links
            #print __file__ +" : " + row['commonnameuri']
        return cnamelist

class nameAcceptedNames(restful.Resource):
    def get(self, database, id):
        anlist = getNameAllAcceptednames(database, id)
        for row in anlist:
            links=[]
            links.append(makelink('acceptedname', 'details', url_for('acceptedname', database=row['DatabaseName'], projectid=row['ProjectID'], nameid=row['NameID'], _external=True)))
            row['links'] = links
        return anlist        

class nameSynonyms(restful.Resource):
    def get(self, database, id):
        slist = getNameAllSynonyms(database, id)
        for row in slist:
            links = []
            links.append(makelink('synonymy', 'details',  url_for('synonymy', database=row['DatabaseName'], projectid=row['ProjectID'], nameid=row['NameID'], synnameid=row['SynNameID'], _external=True)))
            row['links'] = links
        return slist        

class nameHierarchies(restful.Resource):
    def get(self, database, id):
        hlist = getNameAllHierarchies(database, id)
        for row in hlist:
            links=[]
            links.append(makelink('hierarchy', 'details', url_for('hierarchy', database=row['DatabaseName'], projectid=row['ProjectID'], nameid=row['NameID'], _external=True)))
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
            links.append(makelink('project', 'related', url_for('project', id=row['ProjectID'], _external=True)))
            row['links'] = links
        return alist
   
class synonymy(restful.Resource):
    def get(self, database, projectid, nameid, synnameid):
        slist = getsynonymy(database, projectid, nameid, synnameid, 0)
        for row in slist:
            links=[]
            links.append(makelink('synonymname', 'related', url_for('name', database=row['DatabaseName'], id=row['SynNameID'], _external=True)))
            row['links'] = links
        return slist

class hierarchy(restful.Resource):
    def get(self, database, projectid, nameid):
        hlist = gettaxonhierarchy(database, projectid, nameid, 0)
        for row in hlist:
            links=[]
            if row['NameParentID']:
                if int(row['NameParentID'])>0:
                    links.append(makelink('parent', 'related', url_for('name', database=row['DatabaseName'], id=row['NameParentID'], _external=True)))
                    links.append(makelink('allparents', 'related', url_for('hierarchyfull', database=row['DatabaseName'], projectid=row['ProjectID'], nameid=row['NameID'], _external=True)))
                else:
                    row['NameParentID'] = None
            links.append(makelink('project', 'related', url_for('project', id=row['ProjectID'], _external=True))) 
            row['links'] = links
        return hlist

class hierarchyfull(restful.Resource):
    def get(self, database, projectid, nameid):
        hlist = gettaxonhierachyfull(database, projectid, nameid, 0)
        for row in hlist:
            links=[]
            if row['NameParentID']:
                if int(row['NameParentID'])>0:
                    links.append(makelink('parent', 'related', url_for('name', database=database, id=row['NameParentID'], _external=True)))
                else:
                    row['NameParentID'] = None
            links.append(makelink('project', 'related', url_for('project', id=row['ProjectID'], _external=True)))                     
            row['links'] = links
        return hlist
    
class namewww(restful.Resource):
    def get(self, database, id):
        response = Response(render_template("taxonname.html", database=database, id=id) )   
        response.headers['content-type'] = 'text/html'
        return response    

