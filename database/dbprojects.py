# TaxonName-Database specific functions

from flask import current_app
from database.management import get_db, getDBs, cleanDatabasename, diversitydatabase
from datetime import datetime
from sqlalchemy import text
import hashlib # > python 3.6

DWB_MODULE='DiversityProjects'

def encoded_dict(in_dict):
    return in_dict
    #out_dict = {}
    #for k, v in in_dict.iteritems():
        #if isinstance(v, unicode):
            #v = v.decode('utf8')
        #elif isinstance(v, str):
            ## Must be encoded in UTF-8
            #v.encode('utf8')
        #out_dict[k] = v
    #return out_dict

def toDict(data):
    d= dict(list(data.items()))
    return encoded_dict(d)

def R2L(data):
    mydata = []
    for row in data:
        myrow = toDict(row)
        mydata.append(myrow)
    return mydata

def databasenameOK(databasename):
    dblists=getDBs('DiversityProjects')
    if not databasename in dblists:
        return False
    return True


###############################

def getProject(database, projectid):
    projectlist=[]
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    query = ''' select a.ProjectID, a.ProjectParentID, a.Project, a.ProjectTitle, a.ProjectDescription, \
                 a.ProjectEditors, a.ProjectInstitution, a.ProjectNotes, a.ProjectCopyright, a.ProjectURL, \
                 a.ProjectSettings, a.ProjectRights, a.ProjectLicenseURI \
                 from [%s].dbo.[Project] a \
                 where a.ProjectID=%s''' % (database, projectid)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        tprojectlist = conn.execute(query)
        if tprojectlist != None:
            projectlist=R2L(tprojectlist)
    return projectlist

def getProjectLicense(database, projectid):
    licenselist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    query = ''' select b.LicenseID, b.ProjectID, b.DisplayText as LicenseDisplayText, b.LicenseURI, b.LicenseType, b.LicenseHolder, \
                 b.LicenseHolderAgentURI, b.LicenseYear, b.Context as LicenseContext, \
                 b.IPR, b.IPRHolder, b.IPRHolderAgentURI, b.CopyrightStatement, b.CopyrightHolder, \
                 b.CopyrightHolderAgentUri, b.Notes as LicenseNotes \
                 from [%s].dbo.[ProjectLicense] b \
                 where b.ProjectID=%s''' % (database, projectid)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        tlicenselist = conn.execute(query)
        if tlicenselist != None:
            licenselist=R2L(tlicenselist)
    return licenselist
                 
def getProjectAgents(database, projectid):
    agentlist=[]
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    query = ''' select ProjectID, AgentName, AgentURI, AgentRole, AgentSequence, Notes from [%s].[dbo].[ProjectAgent] \
                 where ProjectID=%s order by AgentSequence''' % (database, projectid)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        tagentlist = conn.execute(query)
        if tagentlist != None:
            agentlist=R2L(tagentlist)
    return agentlist  

def getProjectAgentByHash(database, projectid, agenthash):
    theagent = []
    if not cleanDatabasename(database):
        return []
    if not cleanDatabasename(agenthash):
        return []
    agentlist = getProjectAgents(database, projectid)
    for row in agentlist:
        agentkey = '-'.join([str(projectid), row['AgentName'], row['AgentURI']]).encode()
        sh = hashlib.shake_128()
        sh.update(agentkey)
        thehash = sh.hexdigest(64)
        if thehash == agenthash:
            theagent.append(row)
            return theagent
    return theagent
       

def getProjectAgentRoles(database, projectid, agentname, agenturi):
    agentrolelist = []
    if not cleanDatabasename(database):
        return [] 
    query = text(f"select ProjectID, AgentName, AgentURI, AgentRole from [{database}].[dbo].[ProjectAgentRole] \
                 where ProjectID = :e1 and AgentName = :e2 and AgentURI = :e3")
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        tagentrolelist = conn.execute(query, e1=projectid, e2=agentname, e3=agenturi)
        if tagentrolelist != None:
            agentrolelist=R2L(tagentrolelist)
    return agentrolelist     

def getProjectReferences(database, projectid):
    referenceslist=[]
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    query = ''' select ProjectID, ReferenceTitle, ReferenceURI, ReferenceDetails, Notes, ReferenceType from [%s].[dbo].[ProjectReference] \
                 where ProjectID=%s''' % (database, projectid)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        tagentlist = conn.execute(query)
        if tagentlist != None:
            referenceslist=R2L(tagentlist)
    return referenceslist    

def getProjectLastChange(database, projectid):
    mdate=''
    if not cleanDatabasename(database):
        return ''
    database=diversitydatabase(database)
    query=''' DECLARE @ProjectID int; DECLARE @lastmodification datetime = NULL; set @ProjectID=%s; EXECUTE [%s].[dbo].[procLastProjectModification] @ProjectID,@lastmodification OUTPUT; select @lastmodification;''' % (projectid,database)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        q = conn.execute(query)
        if q:
            v = q.fetchone()
            current_app.logger.debug("Time %s " % (str(v)))
            mdate = v[0].isoformat()
    return mdate

def findProjectsWithReference(database, referenceurl):
    projectlists = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    query=''' select '%s' as DatabaseName, ProjectID from [%s].[dbo].[ProjectReference] where [ReferenceURI] = '%s'; ''' % (database, database, referenceurl)
    current_app.logger.debug("Query %s with refuri = '%s'" % (query, referenceurl))
    with get_db().connect() as conn:
        plist = conn.execute(query, refuri=referenceurl)
        if plist != None:
           projectlists = R2L(plist)
    return projectlists
