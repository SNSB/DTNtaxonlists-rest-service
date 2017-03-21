from flask.ext import restful
from flask import url_for

from database.analysis import getAllAnalysisCategories
from database.dbtaxonname import getAnalysisCategorie, getAnalysisValuesAll, getAnalysisValue
from database.dbtaxonname import getAnalysisInProject, getAnalysisAll, getAnalysis

def makelink(label, name, the_uri):
    link = {}
    link['uri'] = the_uri
    link['type'] = 'uri'
    link['rel'] = name
    link['name'] = label
    return link

class analysiscategories(restful.Resource):
    def get(self):
        analysiscategorylist = getAllAnalysisCategories()
        for row in analysiscategorylist:
            links = []
            if row['AnalysisParentID']:
                if int(row['AnalysisParentID'])>0:
                    ref = url_for('analysiscategorie', database=row['DatabaseName'], analysisid=row['AnalysisParentID'], _external=True)
                    links.append(makelink('parent', 'details', ref))
            ref = url_for('analysiscategoryvalues', database=row['DatabaseName'], analysisid=row['AnalysisID'], _external=True)
            links.append(makelink('items', 'details', ref))
            row['links'] = links
        return analysiscategorylist
    
class analysiscategorie(restful.Resource):
    def get(self, database, analysisid):
        analysiscategorylist = getAnalysisCategorie(database, analysisid)
        for row in analysiscategorylist:
            links = []
            if row['AnalysisParentID']:
                if int(row['AnalysisParentID'])>0:
                    ref = url_for('analysiscategorie', database=row['DatabaseName'], analysisid=row['AnalysisParentID'], _external=True)
                    links.append(makelink('parent', 'details', ref))
            ref = url_for('analysiscategoryvalues', database=row['DatabaseName'], analysisid=row['AnalysisID'], _external=True)
            links.append(makelink('items', 'details', ref))                    
            row['links'] = links
        return analysiscategorylist
    
class  analysiscategoryvalues(restful.Resource):
    def get(self, database, analysisid):
        analysiscategoryvalueslist = getAnalysisValuesAll(database, analysisid)
        return analysiscategoryvalueslist
