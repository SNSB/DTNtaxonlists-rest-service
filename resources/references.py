# agents
# REST interface to agents

from flask.ext import restful
from database.reference import getreferences, getreference, getreferencerelations, getreferencerelation
from flask import url_for
#import urllib2

def makelink(label, name, the_uri):
    link = {}
    link['uri'] = the_uri
    link['type'] = 'uri'
    link['rel'] = name
    link['name'] = label
    return link

class references(restful.Resource):
    def get(self):
        referencelist = getreferences('DiversityReferences_TNT')
        for row in referencelist:
            links = []
            ref = url_for('reference', database='DiversityReferences_TNT', id=row['refID'], _external=True)
            links.append(makelink('self', 'related', ref))
            row['links'] = links
        return referencelist

class reference(restful.Resource):
    def get(self, database, id):
        referencelist = getreferences(database, id)
        for row in referencelist:
            links = []
            links.append(makelink('relations', 'related', url_for('referencerelations',  database=row['DatabaseName'], id=row['RefID'], _external=True)))
            row['links'] = links
        return referencelist
    
class referenceRelations(restful.Resource):
    def get(self, database, id):
        relationslist = getreferencerelations(database, id)
        return relationslist
      
class referenceRelation(restful.Resource):
    def get(self, database, id, role, sequence):
        relationslist = getreferencerelation(database, id, role, sequence)
        return relationslist


