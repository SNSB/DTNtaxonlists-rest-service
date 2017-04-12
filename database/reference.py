# database
# selections on the databases

#from app import get_db
#Open Connection to a Database and save the details in the App context
from flask import current_app

from database.management import get_db, getDBs, cleanDatabasename, diversitydatabase
from database.dbreferences import *


def getreference(database, id):
    referencelist = []
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    #dbList = getDBs('DiversityAgents')
    #if not database in dbList:
        #return None
    referencelist = getReference(database, id)
    return referencelist

def getreferences(database):
    referencelist=[]
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    #dbList = getDBs('DiversityAgents')
    #if not database in dbList:
        #return None
    referencelist = getReferences(database)
    return referencelist


def getreferencerelations(database, id):
    referencelist=[]
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    #dbList = getDBs('DiversityAgents')
    #if not database in dbList:
        #return None
    referencelist = getReferenceRelations(database, id)
    return referencelist

    
#####

def getreferencerelation(database, id, role, sequence):
    referencelist=[]
    if not cleanDatabasename(database):
        return []
    database=diversitydatabase(database)
    #dbList = getDBs('DiversityAgents')
    #if not database in dbList:
        #return None
    referencelist = getReferenceRelation(database, id, role, sequence)
    return referencelist

#####
# get all items (links) which refer to this reference
# 
# fur jede Datenbank auszufuehren:
#
#select a.* from INFORMATION_SCHEMA.COLUMNS a inner join INFORMATION_SCHEMA.TABLES b 
#on a.TABLE_CATALOG=b.TABLE_CATALOG and a.TABLE_SCHEMA=b.TABLE_SCHEMA and a.TABLE_NAME=b.TABLE_NAME
#where b.TABLE_TYPE='BASE TABLE' and a.TABLE_CATALOG like 'Diversity%' and 
#(a.COLUMN_NAME = 'ReferenceURI' or a.COLUMN_NAME like '%Ref%URI') and not a.Table_Name like '%_log'
#
# woher bekommt man den link? /project_tnt/id, /agents/id, /commonnames/id
# TaxonNames:
#    TaxonCommonName
#    Taxonname
#    TaxonNameListAnalysis
# Projects:
#    ProjectReferences
# Agents: 
#     AgentReference
# ScientificNames_TNT:
#     TerminologyReference
#     TermReference 
#
    
