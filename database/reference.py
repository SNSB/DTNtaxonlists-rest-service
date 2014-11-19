# database
# selections on the databases

#from app import get_db
#Open Connection to a Database and save the details in the App context
from flask import current_app

from database.management import get_db, getDBs
from database.dbreferences import *


def getreference(database, id):
    referencelist = []
    #dbList = getDBs('DiversityAgents')
    #if not database in dbList:
        #return None
    referencelist = getReference(database, id)
    return referencelist

def getreferences(database):
    referencelist=[]
    #dbList = getDBs('DiversityAgents')
    #if not database in dbList:
        #return None
    referencelist = getReferences(database)
    return referencelist


def getreferencerelations(database, id):
    referencelist=[]
    #dbList = getDBs('DiversityAgents')
    #if not database in dbList:
        #return None
    referencelist = getReferenceRelations(database, id)
    return referencelist

    
#####

def getreferencerelation(database, id, role, sequence):
    referencelist=[]
    #dbList = getDBs('DiversityAgents')
    #if not database in dbList:
        #return None
    referencelist = getReferenceRelation(database, id, role, sequence)
    return referencelist