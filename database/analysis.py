from flask import current_app

from database.management import getDBs
from database.dbtaxonname import getAnalysisCategoriesAll

def getAllAnalysisCategories():
    lists=[]
    dbList = getDBs('DiversityTaxonNames')
    for db in dbList:
        lists += getAnalysisCategoriesAll(db)
    return lists
