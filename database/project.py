# database
# selections on the databases

#from app import get_db
#Open Connection to a Database and save the details in the App context
from flask import current_app

from database.management import get_db, getDBs, cleanDatabasename, diversitydatabase
from database.dbprojects import *


def getproject(database, id):
    projectlist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
#    dbList = getDBs('DiversityProjects')
#    if not database in dbList:
#        return None
    projectlist = getProject(database, id)
    return projectlist


# sublists 

def getprojectagents(database, id):
    lists=[]
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
#    dbList = getDBs('DiversityProjects')
#    if not database in dbList:
#        return None
    lists = getProjectAgents(database,id)
    return lists

def getprojectagentroles(database, id, agentname, agenturl):
    lists=[]
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
#    dbList = getDBs('DiversityProjects')
#    if not database in dbList:
#        return None
    lists = getProjectAgentRoles(database,id, agentname, agenturl)
    return lists

def getprojectreferences(database, id):
    lists=[]
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
#    dbList = getDBs('DiversityProjects')
#    if not database in dbList:
#        return None
    lists = getProjectReferences(database,id)
    return lists

def getprojectlicense(database, id):
    lists=[]
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
#    dbList = getDBs('DiversityProjects')
#    if not database in dbList:
#        return None
    lists = getProjectLicense(database,id)
    return lists
    
def getprojectlastchange(database,id):
    lists=[]
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    mdate = getProjectLastChange(database, id)
    return mdate

def getAllProjectsWithReference(referenceuri):
    lists=[]
    dbList = getDBs('DiversityProjects')
    for db in dbList:
        lists += findProjectsWithReference(db, referenceuri)
    return lists
    
