# agents
# REST interface to agents

from flask.ext import restful
from database.agent import getagents, getagent, getagentrelations
from flask import url_for
#import urllib2

def makelink(label, name, the_uri):
    link = {}
    link['uri'] = the_uri
    link['type'] = 'uri'
    link['rel'] = name
    link['name'] = label
    return link

class agentsTNT(restful.Resource):
    def get(self):
        agentlist = getagents('DiversityAgents_TNT')
        for row in agentlist:
            links = []
            agent = url_for('agent', database='DiversityAgents_TNT', id=row['AgentID'], _external=True)
            links.append(makelink('agent', 'details', agent))
            row['links'] = links
        return agentlist

class agent(restful.Resource):
    def get(self, database, id):
        agentlist = getagent(database, id)
        for row in agentlist:
            links = []
            links.append(makelink('relations', 'related', url_for('agentrelations',  database=row['DatabaseName'], id=row['AgentID'], _external=True)))
            if row['AgentParentID']:
                links.append(makelink('parent', 'related', url_for('agent', database=row['DatabaseName'], id=row['AgentParentID'], _external=True)))
            row['links'] = links
        return agentlist
    
class agentRelations(restful.Resource):
    def get(self, database, id):
        relationslist = getagentrelations(database, id)
        return relationslist
    
class agentTNT(restful.Resource):
    def get(self, id):
        agentlist = getagent('DiversityAgents_TNT', id)
        for row in agentlist:
            links = []
            links.append(makelink('relations', 'related', url_for('agentrelations',  database=row['DatabaseName'], id=row['AgentID'], _external=True)))
            if row['AgentParentID']:
                links.append(makelink('parent', 'related', url_for('agent', database=row['DatabaseName'], id=row['AgentParentID'], _external=True)))
            row['links'] = links
        return agentlist
    
class agentRelationsTNT(restful.Resource):
    def get(self, id):
        relationslist = getagentrelations('DiversityAgents_TNT', id)
        return relationslist




