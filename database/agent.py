# database
# selections on the databases

#from app import get_db
#Open Connection to a Database and save the details in the App context
from flask import current_app

from database.management import get_db, getDBs, cleanDatabasename, diversitydatabase
from database.dbagents import *


def getagent(database, id):
    agentlist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
     #dbList = getDBs('DiversityAgents')
    #if not database in dbList:
        #return None
    agentlist = getAgent(database, id)
    return agentlist

def getagents(database):
    agentlist=[]
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    #dbList = getDBs('DiversityAgents')
    #if not database in dbList:
        #return None
    agentlist = getAgents(database)
    return agentlist

def getagentrelations(database, id):
    agentlist=[]
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    #dbList = getDBs('DiversityAgents')
    #if not database in dbList:
        #return None
    agentlist = getAgentRelations(database, id)
    return agentlist

    
