# projects
# REST interface to projects

import flask_restful as restful
from flask import url_for
from database.project import getproject, getprojectagents, getprojectreferences, getprojectlicense, getprojectlastchange, getprojectagentroles
from urllib.parse import urlparse, quote_plus, unquote_plus
import hashlib # python 3.6
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
                if ipragenturi:
                    agentdb, agentid = ipragenturi.strip(' /').split('/')
                    links.append(makelink('agent', 'IPR', url_for('agenttnt', id=agentid, _external=True)))
            if row['CopyrightHolderAgentUri']:
                licenceagenturi = urlparse(row['CopyrightHolderAgentUri']).path
                row['CopyrightHolderAgentUri']=licenceagenturi #remove host
                if licenceagenturi:
                    agentdb, agentid = licenceagenturi.strip(' /').split('/')
                    links.append(makelink('agent', 'copyright', url_for('agenttnt', id=agentid, _external=True)))
            if row['LicenseHolderAgentURI']:
                licenceagenturi = urlparse(row['LicenseHolderAgentURI']).path
                row['LicenseHolderAgentURI']=licenceagenturi #remove host
                if licenceagenturi:
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
            agentkey = '-'.join([str(id), row['AgentName'], row['AgentURI']]).encode()
            sh = hashlib.shake_128()
            sh.update(agentkey)
            agenthash = sh.hexdigest(64)
            row['AgentHash'] = agenthash
            if agenturi:
                agentdb, agentid = agenturi.strip(' /').split('/')
                if agentdb == 'Agents_TNT':
                    links.append(makelink('agent', 'details', url_for('agenttnt', id=agentid, _external=True)))
            links.append(makelink('projectroles', 'roles', url_for('projectagentroles', projectid=id, agenthash=agenthash, _external=True)))
            row['AgentURI']=agenturi #remove host
            if links:
                row['links'] = links
            
        return projectagentlist
    

class projectAgentRoles(restful.Resource):
    def get(self, projectid, agenthash):
        agentprojectroles = getprojectagentroles('DiversityProjects_TNT', projectid, agenthash)
        for row in agentprojectroles:
            links = []
            agenturi = urlparse(row['AgentURI']).path
            if agenturi:
                agentdb, agentid = agenturi.strip(' /').split('/')
                if agentdb == 'Agents_TNT':
                     row['AgentURI']=agenturi
                     links.append(makelink('agent', 'details', url_for('agenttnt', id=agentid, _external=True)))
            if links:
                row['links'] = links
        return agentprojectroles


class projectReferences(restful.Resource):
    def get(self, id):
        projectreferencelist = getprojectreferences('DiversityProjects_TNT', id)
        for row in projectreferencelist:
            links = []
            referenceuri = urlparse(row['ReferenceURI']).path
            row['ReferenceURI']=referenceuri #remove host
            if referenceuri:
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


