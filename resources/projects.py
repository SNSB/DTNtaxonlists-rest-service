# projects
# REST interface to projects

from flask.ext import restful
from flask import url_for
from database.project import getproject, getprojectagents
from urlparse import urlparse
#import urllib2

def makelink(label, name, the_uri):
    link = {}
    link['uri'] = the_uri
    link['type'] = 'uri'
    link['rel'] = name
    link['name'] = label
    return link


class projects(restful.Resource):
    def get(self):
        pass
    
class project(restful.Resource):
    def get(self, id):
        projectlist = getproject('DiversityProjects_TNT', id)
        for row in projectlist:
            links = []
            links.append(makelink('agents', 'related', url_for('projectagents', id=row['ProjectID'])))
            row['links'] = links
        return projectlist
 
class projectAgents(restful.Resource):
    def get(self, id):
        projectagentlist = getprojectagents('DiversityProjects_TNT', id)
        for row in projectagentlist:
            links = []
            agenturi = urlparse(row['AgentURI']).path
            row['AgentURI']=agenturi #remove host
            agentdb, agentid = agenturi.strip(' /').split('/')
            links.append(makelink('agent', 'related', url_for('agenttnt', id=agentid)))
            row['links'] = links
        return projectagentlist

