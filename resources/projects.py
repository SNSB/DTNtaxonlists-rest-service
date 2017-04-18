# projects
# REST interface to projects

from flask.ext import restful
from flask import url_for
from database.project import getproject, getprojectagents, getprojectreferences, getprojectlicense, getprojectlastchange
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
            links.append(makelink('agents', 'related', url_for('projectagents', id=row['ProjectID'], _external=True)))
            links.append(makelink('references', 'related', url_for('projectreferences', id=row['ProjectID'], _external=True)))            
            links.append(makelink('licenses', 'related', url_for('projectlicense', id=row['ProjectID'], _external=True)))            
            row['links'] = links
        return projectlist
    
class projectLicense(restful.Resource):
    def get(self, id):
        licenselist = getprojectlicense('DiversityProjects_TNT', id)
        for row in licenselist:
            links = []
            if row['IPRHolderAgentURI']:
                ipragenturi = urlparse(row['IPRHolderAgentURI']).path
                row['IPRHolderAgentURI']=ipragenturi #remove host
                agentdb, agentid = ipragenturi.strip(' /').split('/')
                links.append(makelink('agent', 'IPR', url_for('agenttnt', id=agentid, _external=True)))
            if row['CopyrightHolderAgentUri']:
                licenceagenturi = urlparse(row['CopyrightHolderAgentUri']).path
                row['CopyrightHolderAgentUri']=licenceagenturi #remove host
                agentdb, agentid = licenceagenturi.strip(' /').split('/')
                links.append(makelink('agent', 'copyright', url_for('agenttnt', id=agentid, _external=True)))
            if row['LicenseHolderAgentURI']:
                licenceagenturi = urlparse(row['LicenseHolderAgentURI']).path
                row['LicenseHolderAgentURI']=licenceagenturi #remove host
                agentdb, agentid = licenceagenturi.strip(' /').split('/')
                links.append(makelink('agent', 'license', url_for('agenttnt', id=agentid, _external=True)))
            row['links'] = links
        return licenselist
    
class projectAgents(restful.Resource):
    def get(self, id):
        projectagentlist = getprojectagents('DiversityProjects_TNT', id)
        for row in projectagentlist:
            links = []
            agenturi = urlparse(row['AgentURI']).path
            row['AgentURI']=agenturi #remove host
            agentdb, agentid = agenturi.strip(' /').split('/')
            links.append(makelink('agent', 'details', url_for('agenttnt', id=agentid, _external=True)))
            row['links'] = links
        return projectagentlist

class projectReferences(restful.Resource):
    def get(self, id):
        projectreferencelist = getprojectreferences('DiversityProjects_TNT', id)
        for row in projectreferencelist:
            links = []
            referenceuri = urlparse(row['ReferenceURI']).path
            row['ReferenceURI']=referenceuri #remove host
            referencedb, referenceid = referenceuri.strip(' /').split('/')
            row['DatabaseName']='DiversityProjects_TNT'
            row['RefID']=referenceid
            links.append(makelink('reference', 'details', url_for('reference', database=referencedb, id=referenceid, _external=True)))
            row['links'] = links
        return projectreferencelist

class projectLastChange(restful.Resource):
    def get(self, id):
        mdate = getprojectlastchange('DiversityProjects_TNT', id)
        return mdate


