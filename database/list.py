# database
# selections on the databases

#from app import get_db
#Open Connection to a Database and save the details in the App context
from flask import current_app

from database.management import get_db, getDBs, cleanDatabasename, diversitydatabase
from database.dbtaxonname import *


def getList(database, id):
    namelist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    #dbList = getDBs('DiversityTaxonNames')
    #if not database in dbList:
        #return None
    namelist = getAllTaxonNamesFromList(database, id)
    return namelist

def getAllLists():
    lists=[]
    dbList = getDBs('DiversityTaxonNames')
    for db in dbList:
        lists += getTaxonNameLists(db)
    return lists

def getListProject(database, id):
    projecturi=None
    if not cleanDatabasename(database):
        return  projecturi  
    database=diversitydatabase(database)
    #dbList = getDBs('DiversityTaxonNames')
    #if not database in dbList:
        #return None
    projecturi=getTaxonNameListsProjectUri(database, id)
    return projecturi

    
def getAllReferenceingTaxonLists(referenceuri):
    lists=[]
    dbList = getDBs('DiversityTaxonNames')
    for db in dbList:
        lists += findTaxonnamelistWithReference(db, referenceuri)
    return lists
