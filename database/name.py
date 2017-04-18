# database
# selections on the databases

#from app import get_db
#Open Connection to a Database and save the details in the App context
from flask import current_app

from database.management import get_db, getDBs, cleanDatabasename, diversitydatabase
from database.dbtaxonname import *


def getName(database, id):
    namelist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
#    dbList = getDBs('DiversityTaxonNames')
#    if not database in dbList:
#        return None
    namelist = getTaxonName(database, id)
    return namelist

def getTaxonNameListsForName(database, id):
    namelist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    namelist = getAllTaxonNameListForName(database, id)
    return namelist

def getAllNames():
    lists=[]
    dbList = getDBs('DiversityTaxonNames')
    for db in dbList:
        lists += getTaxonNames(db)
    return lists

def findName(namestring):
    lists=[]
    dbList = getDBs('DiversityTaxonNames')
    for db in dbList:
        lists += findTaxonNames(db, namestring)
    return lists


def findNameID(nameid):
    lists=[]
    dbList = getDBs('DiversityTaxonNames')
    for db in dbList:
        lists += getTaxonName(db, nameid)
    return lists

def findNamePartly(namestring):
    lists=[]
    dbList = getDBs('DiversityTaxonNames')
    for db in dbList:
        lists += findTaxonNamePartly(db, namestring)
    return lists


# sublists 

def getNameAllCommonNames(database, id):
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    #dbList = getDBs('DiversityTaxonNames')
    #if not database in dbList:
        #return None
    lists = getTaxonNameAllCommonNames(database,id)
    return lists

def getNameAllSynonyms(database, id):
    lists=[]
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    #dbList = getDBs('DiversityTaxonNames')
    #if not database in dbList:
        #return None
    lists = getTaxonNameAllSynonyms(database,id)
    return lists

def getNameAllAcceptednames(database, id):
    lists=[]
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    #dbList = getDBs('DiversityTaxonNames')
    #if not database in dbList:
        #return None
    lists = getTaxonNameAllAcceptedNames(database,id)
    return lists

def getNameAllHierarchies(database, id):
    lists=[]
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    #dbList = getDBs('DiversityTaxonNames')
    #if not database in dbList:
        #return None
    lists = getTaxonNameAllHierarchies(database,id)
    return lists

# Subitems

def getacceptedname(database, projectid, nameid,  ignore):
    lists=[]
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    #dbList = getDBs('DiversityTaxonNames')
    #if not database in dbList:
        #return None
    lists=getAcceptedName(database, projectid, nameid, ignore)
    return lists
    
def getsynonymy(database, projectid, nameid, synnameid, ignore):
    lists=[]
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    #dbList = getDBs('DiversityTaxonNames')
    #if not database in dbList:
        #return None
    lists = getSynonymy(database, projectid, nameid, synnameid, ignore)
    return lists
    
def gettaxonhierarchy(database, projectid, nameid, ignore):
    lists=[]
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    #dbList = getDBs('DiversityTaxonNames')
    #if not database in dbList:
        #return None
    lists = getTaxonHierarchy(database, projectid, nameid, ignore)
    return lists

def gettaxonhierachyfull(database,projectid, nameid, ignore):
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    lists=getTaxonHierarchyFull(database, projectid, nameid, ignore)
    return lists


# referencesearch
def getAllReferencingTaxonNames(referenceuri):
    lists=[]
    dbList = getDBs('DiversityTaxonNames')
    for db in dbList:
        lists += findTaxonnameWithReference(db, referenceuri)
    return lists


def getAllReferenceingAcceptedNames(referenceuri):
    lists=[]
    dbList = getDBs('DiversityTaxonNames')
    for db in dbList:
        lists += findTaxonAcceptednameWithReference(db, referenceuri)
    return lists


def getAllReferenceingSynonyms(referenceuri):
    lists=[]
    dbList = getDBs('DiversityTaxonNames')
    for db in dbList:
        lists += findTaxonSynonymWithReference(db, referenceuri)
    return lists


def getAllReferenceingHierarchies(referenceuri):
    lists=[]
    dbList = getDBs('DiversityTaxonNames')
    for db in dbList:
        lists += findTaxonHierarchyWithReference(db, referenceuri)
    return lists



