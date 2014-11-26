# database
# selections on the databases

#from app import get_db
#Open Connection to a Database and save the details in the App context
from flask import current_app

from database.management import get_db, getDBs, cleanDatabasename
from database.dbprojects import *


def getproject(database, id):
    projectlist = []
    if not cleanDatabasename(database):
        return []
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
#    dbList = getDBs('DiversityProjects')
#    if not database in dbList:
#        return None
    lists = getProjectAgents(database,id)
    return lists


