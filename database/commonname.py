# database
# selections on the databases

#from app import get_db
#Open Connection to a Database and save the details in the App context
from flask import current_app

from database.management import get_db, getDBs, cleanDatabasename, diversitydatabase
from database.dbtaxonname import *


def getcommonname(database, nameid, commonname, languagecode, countrycode, referencetitle):
    cnamelist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    namelist = getCommonName(database, nameid, commonname, languagecode, countrycode, referencetitle)
    return namelist

def findCommonName(namestring):
    lists=[]
    dbList = getDBs('DiversityTaxonNames')
    for db in dbList:
        lists += findCommonNames(db, namestring)
    return lists

def getAllReferenceingCommonNames(referenceuri):
    lists=[]
    dbList = getDBs('DiversityTaxonNames')
    for db in dbList:
        print(len(lists))
        nl = findTaxonCommonnameWithReference(db, referenceuri)
        print(len(nl))
        lists += nl
    return lists
