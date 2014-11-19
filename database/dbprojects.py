# TaxonName-Database specific functions

from flask import current_app
from database.management import get_db, getDBs


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
    d= dict(data.items())
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
    query = u''' select ProjectID, ProjectParentID, Project, ProjectTitle, ProjectDescription, \
                 ProjectEditors, ProjectInstitution, ProjectNotes, ProjectCopyright, ProjectURL, \
                 ProjectSettings, ProjectRights, ProjectLicenseURI from [%s].[dbo].[Project] \
                 where ProjectID=%s''' % (database, projectid)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        tprojectlist = conn.execute(query)
        if tprojectlist != None:
            projectlist=R2L(tprojectlist)
    return projectlist

def getProjectAgents(database, projectid):
    agentlist=[]
    query = u''' select ProjectID, AgentName, AgentURI, AgentRole, Notes from [%s].[dbo].[ProjectAgent] \
                 where ProjectID=%s''' % (database, projectid)
    current_app.logger.debug("Query %s " % (query))
    with get_db().connect() as conn:
        tagentlist = conn.execute(query)
        if tagentlist != None:
            agentlist=R2L(tagentlist)
    return agentlist    


#