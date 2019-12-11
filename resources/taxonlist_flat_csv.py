# csv...

import requests
from urllib.parse import urlparse
import urllib.request, urllib.error, urllib.parse

from resources.lists import taxonlistflat

from database.dbtaxonname import getAllTaxonNamesFromListFlat, getTaxonNameAllAcceptedNames, getAllCommonNamesFromListFlat
from database.dbprojects import getProject, getProjectAgents, getProjectLicense, getProjectReferences, getProjectAgentRoles
from database.dbagents import getAgent
from database.dbreferences import getReference
import flask_restful as restful
from flask import Flask,g, request, render_template
from flask import url_for
from flask_restful import Resource, fields, marshal_with
from flask import url_for, Response, redirect
from flask import current_app

class taxonlist_flat_csv(restful.Resource):
    def get(self, database, id):
        project = getProject('DiversityProjects_TNT', id)
        taxonnamelist = getAllTaxonNamesFromListFlat(database, id)
        if len(taxonnamelist) <= 0:
            restful.abort(404)
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
                    uri_synonym = url_for('name', database=database, id = synonym_is_accepted[0]['NameID'], _external=True)
                else:
                    uri_synonym = None
            else:
                uri_synonym = None
            row['acceptedNameUsageID'] = uri_synonym    
        response = Response(render_template("taxonlist_flat_csv.j2", database=database, id=id, taxonnames=taxonnamelist, project=project[0]) )
        response.headers['content-type'] = 'text/comma-separated-values'
        return response

import six
def quote_xml_string(myitem):
    if myitem:
        myitem=myitem.replace("&", "&amp;")
        myitem=myitem.replace('"', "&quot;")
        myitem=myitem.replace("'", "&apos;")
        myitem=myitem.replace('<', "&lt;")
        myitem=myitem.replace('>', "&gt;")
    return myitem
            
def quote_xml(mylist):
    if isinstance(mylist,six.string_types):
        mylist=quote_xml_string(mylist)
        return mylist
    if isinstance(mylist,list):
        for item in mylist:
           item=quote_xml(item)
        return mylist
    if isinstance(mylist, dict):
        for k,v in list(mylist.items()):
           v=quote_xml(v)
           mylist[k]=v
        return mylist
    
            
class  darwin_core_offline( restful.Resource ):
    def get(self, database, id):
        
        thisurl = url_for('darwin_core_zip', database=database, id = id, _external=True)
        
        project = getProject('DiversityProjects_TNT', id)
        taxonnamelist = getAllTaxonNamesFromListFlat(database, id)
        if len(taxonnamelist) <= 0:
            restful.abort(404)
        for row in taxonnamelist:
            uri =  url_for('name', database=database, id = row['NameID'], _external=True)
            row['taxonID'] = uri
            if row['HierarchieNameParentID'] is not None and row['HierarchieNameParentID'] != -1:
                # remove all parents which are not accepted
                parentisaccepted = False
                parentid = row['HierarchieNameParentID']
                for row2 in taxonnamelist:
                    if parentid == row2['NameID'] and row2['AcceptedNameProject'] is not None:
                        parentisaccepted = True
                        break;
                if parentisaccepted:
                    uri_parent = url_for('name', database=database, id = row['HierarchieNameParentID'], _external=True)
                else:
                    uri_parent = None 
            else:
                uri_parent = None
            row['parentNameUsageID'] = uri_parent
            if row['AcceptedNameProject'] is None and row['SynonymieNameID'] is not None:
                synonym_is_accepted = getTaxonNameAllAcceptedNames(database, row['SynonymieNameID'])
                if len(synonym_is_accepted) > 0 and synonym_is_accepted[0]['NameID'] is not None:
                    uri_synonym = url_for('name', database=database, id = synonym_is_accepted[0]['NameID'], _external=True)
                else:
                    uri_synonym = None
            else:
                uri_synonym = None
            row['acceptedNameUsageID'] = uri_synonym    
        taxon_csv = render_template("taxonlist_flat_csv.j2", database=database, id=id, taxonnames=taxonnamelist, project=project[0]) 

        taxoncommonnamelist = getAllCommonNamesFromListFlat(database, id)
        for row in taxoncommonnamelist:
            uri =  url_for('name', database=database, id = row['NameID'], _external=True)
            row['taxonID'] = uri
        taxoncommonname_csv = render_template("taxonlistcommonnames_flat_csv.j2", database=database, id=id, commonnames=taxoncommonnamelist, project=project[0]) 
        
        
        import time
        currentdate = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        
             
        citations=''
        gbifcitation=''
        restcitation=''
        projectreferences = getProjectReferences('DiversityProjects_TNT', id)
        for preference in projectreferences:
            if preference['ReferenceType'] == "GBIF":
               referenceuri = urlparse(preference['ReferenceURI']).path
               referencedb, referenceid = referenceuri.strip(' /').split('/')
               ref = getReference('DiversityReferences_TNT', referenceid)
               for row in ref:
                   gbifcitation = row["fullref"] + '. Accessed via ' + row['Weblinks'] + ', Data Publisher: ' +  row['Publisher'] + ', ' + row["UserDef1"]
            if preference['ReferenceType'] == "REST Api":
               referenceuri = urlparse(preference['ReferenceURI']).path
               referencedb, referenceid = referenceuri.strip(' /').split('/')
               ref = getReference('DiversityReferences_TNT', referenceid)
               for row in ref:
                   restcitation = row["fullref"] + '. Accessed via the REST service descibed at ' + row['Weblinks'] + ', Data Publisher: ' +  row['Publisher'] + '.'

        if len(gbifcitation) > 0:
            citation = gbifcitation
        else:
            citation = restcitation
        
        projectagentlist = getProjectAgents('DiversityProjects_TNT', id)
        for row in projectagentlist:
            agenturi = urlparse(row['AgentURI']).path
            agentroles = getProjectAgentRoles('DiversityProjects_TNT', id, row['AgentName'], row['AgentURI'])
            agent_roles = []
            for agentrole in agentroles:
                agent_roles.append(agentrole['AgentRole'])
            row['AgentRoles'] = agent_roles
            agentdb, agentid = agenturi.strip(' /').split('/')
            row['AgentURI']=url_for('agenttnt', id=agentid, _external=True)
            agent = getAgent('DiversityAgents_TNT', agentid)
            if len(agent) > 0:
                row['AgentID'] = agent[0]['AgentID']
                row['AgentTitle'] = agent[0]['AgentTitle']
                row['GivenName'] = agent[0]['GivenName']
                #row['GivenNamePostfix'] = agent[0]['GivenNamePostfix']
                #row['InheritedNamePrefix'] = agent[0]['InheritedNamePrefix']
                row['InheritedName'] = agent[0]['InheritedName']
                #row['InheritedNamePostfix'] = agent[0]['InheritedNamePostfix']
                row['Abbreviation'] = agent[0]['Abbreviation']
                row['AgentType'] = agent[0]['AgentType']
                
        projectlicencelist = getProjectLicense('DiversityProjects_TNT', id)
        quote_xml(projectlicencelist)
        quote_xml(projectagentlist)
        citation=quote_xml(citation)
        quote_xml(project[0])
        quote_xml(database)
        
        current_app.logger.debug("Licencelist: %s " % (projectlicencelist)) 
        current_app.logger.debug("Agentlist %s " % (projectagentlist))
        current_app.logger.debug("citation %s " % (citation))
        current_app.logger.debug("project %s " % (project[0]))
        current_app.logger.debug("project %s " % (database))
        taxonlist_eml = render_template("taxonlist_flat_eml.j2", database=database, id=id, agents=projectagentlist, project=project[0], licenses=projectlicencelist, currentdate=currentdate, thisurl=thisurl, citation=citation) 
        
        taxonlist_meta = render_template("meta.xml.j2", database=database, id=id, project=project[0], commonnamesexist=(len(taxoncommonnamelist) > 0) )
        
        from flask import Flask, Response
        from zipfile import ZipFile, ZIP_DEFLATED
        from io import BytesIO
        from werkzeug.wsgi import FileWrapper

        timestr = time.strftime("%Y%m%d-%H%M%S")

        inMemoryOutputFile = BytesIO()

        zipFile = ZipFile(inMemoryOutputFile, 'w', ZIP_DEFLATED) 
        zipFile.writestr('eml.xml', taxonlist_eml.encode('utf-8'))
        zipFile.writestr('meta.xml', taxonlist_meta.encode('utf-8'))
        zipFile.writestr('taxon.csv', taxon_csv.encode('utf-8'))
        if len(taxoncommonnamelist)>0:
            zipFile.writestr('common-names.csv', taxoncommonname_csv.encode('utf-8'))
        zipFile.close()

        inMemoryOutputFile.seek(0)
        # uWSGI: https://www.pythonanywhere.com/forums/topic/13570/
        wrappedFile = FileWrapper(inMemoryOutputFile)
        attachment_filename="".join(["DTNtaxonlist_",database, "_" , str(id) ,".zip"])

        response = Response(wrappedFile, mimetype =  'application/zip',  direct_passthrough=True)
        response.headers.set('Content-Disposition', 'attachment', filename=attachment_filename)
        return response

class darwin_core_zip( restful.Resource ):
    def get(self, database, id):        
        filename=url_for('static', filename="".join(["dwc/", "DTNtaxonlist_",database, "_" , str(id) ,".zip"]))
        return redirect(filename, code=302)
