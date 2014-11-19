# database
# selections on the databases

#from app import get_db
#Open Connection to a Database and save the details in the App context
from flask import current_app

from database.management import get_db, getDBs
from database.dbtaxonname import *


def getcommonname(database, nameid, commonname, languagecode, countrycode, referencetitle):
    cnamelist = []
    dbList = getDBs('DiversityTaxonNames')
    if not database in dbList:
        return None
    namelist = getCommonName(database, nameid, commonname, languagecode, countrycode, referencetitle)
    return namelist


    
