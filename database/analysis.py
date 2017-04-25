from flask import current_app

from database.management import getDBs
from database.dbtaxonname import getAnalysisCategoriesAll, findAnalysisCategoryWithReference, getProjectsHavingAnalysis

def getAllAnalysisCategories():
    lists=[]
    dbList = getDBs('DiversityTaxonNames')
    for db in dbList:
        lists += getAnalysisCategoriesAll(db)
    return lists

def getAllReferenceingCategories(referenceuri):
    lists=[]
    dbList = getDBs('DiversityTaxonNames')
    for db in dbList:
        lists += findAnalysisCategoryWithReference(db, referenceuri)
    return lists

def getAllProjectsReferencingAnalysisCategory(analysisid):
    lists=[]
    dbList = getDBs('DiversityTaxonNames')
    for db in dbList:
        lists += getProjectsHavingAnalysis(db, analysisid)
    return lists    
