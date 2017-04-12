from flask.ext import restful
from flask import url_for
from urlparse import urlparse

from database.analysis import getAllAnalysisCategories
from database.dbtaxonname import getAnalysisCategorie, getAnalysisCategorieChilds, getAnalysisValuesAll, getAnalysisValue, getAnalysisCategoriesforName
from database.dbtaxonname import getAnalysisInProject, getAnalysisAll, getAnalysisAllTaxRef, getAnalysis, getAnalysisfilter

from flask_restful import reqparse

def makelink(label, name, the_uri):
    link = {}
    link['uri'] = the_uri
    link['type'] = 'uri'
    link['rel'] = name
    link['name'] = label
    return link

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
    
def extractReferenceID(referenceuri):
    if referenceuri:
        parts = referenceuri.split('/')
        referenceid = parts[-1]
        if isInt(referenceid):
            return referenceid
    return None

class analysiscategories(restful.Resource):
    def get(self):
        analysiscategorylist = getAllAnalysisCategories()
        for row in analysiscategorylist:
            links = []
            if row['AnalysisID']:
                if int(row['AnalysisID'])>0:
                    ref = url_for('analysiscategorie', database=row['DatabaseName'], analysisid=row['AnalysisID'], _external=True)
                    links.append(makelink('analysiscategory', 'category', ref))
                    ref = url_for('analysiscategoryvalues', database=row['DatabaseName'], analysisid=row['AnalysisID'], _external=True)
                    links.append(makelink('analysiscategoryvalues', 'valueset', ref))
                    ref = url_for('analysiscategoriechilds', database=row['DatabaseName'], analysisid=row['AnalysisID'], _external=True)
                    links.append(makelink('analysiscategoriechilds', 'valueset', ref))
                    row['ReferenceURI'] = urlparse(row['ReferenceURI']).path
                    referenceid = extractReferenceID(row['ReferenceURI'])
                    if referenceid:
                        links.append(makelink('reference', 'related', url_for('referencetnt', id=referenceid, _external=True) ))
                    
            if row['AnalysisParentID']:
                if int(row['AnalysisParentID'])>0:
                    ref = url_for('analysiscategorie', database=row['DatabaseName'], analysisid=row['AnalysisParentID'], _external=True)
                    links.append(makelink('parent', 'category', ref))
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
                    links.append(makelink('parent', 'category', ref))
            if row['AnalysisID']:
                if int(row['AnalysisID'])>0:
                    ref = url_for('analysiscategoryvalues', database=row['DatabaseName'], analysisid=row['AnalysisID'], _external=True)
                    links.append(makelink('analysiscategoryvalues', 'valueset', ref))                    
                    ref = url_for('analysiscategoriechilds', database=row['DatabaseName'], analysisid=row['AnalysisID'], _external=True)
                    links.append(makelink('analysiscategoriechilds', 'valueset', ref))
                    row['ReferenceURI'] = urlparse(row['ReferenceURI']).path
                    referenceid = extractReferenceID(row['ReferenceURI'])
                    if referenceid:
                        links.append(makelink('reference', 'related', url_for('referencetnt', id=referenceid, _external=True) ))
            row['links'] = links
        return analysiscategorylist

class analysiscategoriechilds(restful.Resource):
    def get(self, database, analysisid):
        analysiscategorylist = getAnalysisCategorieChilds(database, analysisid)
        for row in analysiscategorylist:
            links = []
            if row['AnalysisParentID']:
                if int(row['AnalysisParentID'])>0:
                    ref = url_for('analysiscategorie', database=row['DatabaseName'], analysisid=row['AnalysisParentID'], _external=True)
                    links.append(makelink('parent', 'category', ref))
            if row['AnalysisID']:
                if int(row['AnalysisID'])>0:
                    ref = url_for('analysiscategoryvalues', database=row['DatabaseName'], analysisid=row['AnalysisID'], _external=True)
                    links.append(makelink('analysiscategoryvalues', 'valueset', ref))  
                    ref = url_for('analysiscategoriechilds', database=row['DatabaseName'], analysisid=row['AnalysisID'], _external=True)
                    links.append(makelink('analysiscategoriechilds', 'valueset', ref))
                    row['ReferenceURI'] = urlparse(row['ReferenceURI']).path
            row['links'] = links
        return analysiscategorylist    
    
class  analysiscategoryvalues(restful.Resource):
    def get(self, database, analysisid):
        analysiscategoryvalueslist = getAnalysisValuesAll(database, analysisid)
        for row in analysiscategoryvalueslist:
            links = []
            #if row['AnalysisID']:
                #if int(row['AnalysisID'])>0:
                    #ref = url_for('analysiscategorie', database=row['DatabaseName'], analysisid=row['AnalysisID'], _external=True)
                    #links.append(makelink('analysiscategory', 'category', ref))
            #ref = url_for('analysiscategoryvalues', database=row['DatabaseName'], analysisid=row['AnalysisID'], _external=True)
            #links.append(makelink('analysiscategoryvalues', 'valueset', ref))                    
            ref = url_for('analysisvalue', database=row['DatabaseName'], analysisid=row['AnalysisID'], analysisvalue=row['AnalysisValue'], _external=True)
            links.append(makelink('item', 'detail', ref))                    
            row['links'] = links
        return analysiscategoryvalueslist

class analysisvalue(restful.Resource):
    def get(self, database, analysisid, analysisvalue):
        analysiscategoryvaluelist = getAnalysisValue(database, analysisid, analysisvalue)
        for row in analysiscategoryvaluelist:
            links = []
            if row['AnalysisID']:
                if int(row['AnalysisID'])>0:
                    ref = url_for('analysiscategorie', database=database, analysisid=analysisid, _external=True)
                    links.append(makelink('analysiscategory', 'category', ref))
            ref = url_for('analysiscategoryvalues', database=database, analysisid=analysisid, _external=True)
            links.append(makelink('analysiscategoryvalues', 'valueset', ref))                    
            row['links'] = links
        return analysiscategoryvaluelist
    
 
class analysiscategoriesinproject(restful.Resource):
    def get(self, database, projectid):
        analysiscategorylist = getAnalysisInProject(database, projectid)
        for row in analysiscategorylist:
            links = []
            if row['AnalysisID']:
                if int(row['AnalysisID'])>0:
                    ref = url_for('analysiscategorie', database=database, analysisid=row['AnalysisID'], _external=True)
                    links.append(makelink('analysiscategory', 'category', ref))
                    ref = url_for('analysisinprojectfilter', database=database, projectid=projectid, analysisid=row['AnalysisID'], _external=True)
                    links.append(makelink('analysis', 'items', ref))
            row['links'] = links
        return analysiscategorylist
    

class analysisinproject(restful.Resource):
    def get(self, database, analysisid, projectid):
        analysislist = getAnalysisAll(database, projectid,  analysisid)
        for row in analysislist:
            links = []
            if row['NameID']:
                if int(row['NameID'])>0:
                    ref = url_for('analysis', database=database, analysisid=analysisid, projectid=projectid, nameid=row['NameID'], _external=True)
                    links.append(makelink('analysis', 'detail', ref))
            row['links'] = links
        return analysislist

class analysisinprojectequal(restful.Resource):
    def get(self, database, analysisid, projectid, analysisvalue):
        analysislist = getAnalysisfilter(database, projectid,  analysisid, -1, analysisvalue)
        for row in analysislist:
            links = []
            if row['NameID']:
                if int(row['NameID'])>0:
                    ref = url_for('analysis', database=database, analysisid=analysisid, projectid=projectid, nameid=row['NameID'], _external=True)
                    links.append(makelink('analysis', 'detail', ref))
            row['links'] = links
        return analysislist

class analysisinprojectlower(restful.Resource):
    def get(self, database, analysisid, projectid, analysisvalue):
        analysislist = getAnalysisfilter(database, projectid,  analysisid, -1, analysisvalue, "<")
        for row in analysislist:
            links = []
            if row['NameID']:
                if int(row['NameID'])>0:
                    ref = url_for('analysis', database=database, analysisid=analysisid, projectid=projectid, nameid=row['NameID'], _external=True)
                    links.append(makelink('analysis', 'detail', ref))
            row['links'] = links
        return analysislist

class analysisinprojectgreater(restful.Resource):
    def get(self, database, analysisid, projectid, analysisvalue):
        analysislist = getAnalysisfilter(database, projectid,  analysisid, -1, analysisvalue, ">")
        for row in analysislist:
            links = []
            if row['NameID']:
                if int(row['NameID'])>0:
                    ref = url_for('analysis', database=database, analysisid=analysisid, projectid=projectid, nameid=row['NameID'], _external=True)
                    links.append(makelink('analysis', 'detail', ref))
            row['links'] = links
        return analysislist


class analysisinprojectfilter(restful.Resource):
    def get(self, database, analysisid, projectid):
        analysislist = []
        parser =  reqparse.RequestParser()
        parser.add_argument('op') #, type=unicode
        parser.add_argument('value')
        parser.add_argument('refid', type=int)
        args = parser.parse_args()

        if args['value'] or args['value']=="":
            ALLOWD_OPERATORS = {'eq': "=",
            'lt': "<",
            'gt': ">",
            'le': "<=",
            'ge': ">=",
            'ne': "=",
            'notlike': "like",
            'like': "like"
            }
            op = "="
            notop = ""
            analysisvalue = args['value']
            if args['op']:
                op = ALLOWD_OPERATORS.get(args['op'], "=")
                if args['op'] in ['ne', 'notlike']:
                    notop = "not"
            if args['refid'] or args['refid'] == 0 :
                refid =  args['refid']
            else: 
                refid = -1
                
            if op == "like":
                analysisvalue = "%" + analysisvalue + "%"
            
            analysislist = getAnalysisfilter(database, projectid,  analysisid, refid, analysisvalue, op, notop)
        else:
            if args['refid'] or args['refid']==0:
                analysislist = getAnalysisAllTaxRef(database, projectid,  analysisid, args['refid'])
            else:
                analysislist = getAnalysisAll(database, projectid,  analysisid)
        for row in analysislist:
            links = []
            if row['NameID']:
                if int(row['NameID'])>0:
                    ref = url_for('analysis', database=database, analysisid=analysisid, projectid=projectid, nameid=row['NameID'], _external=True)
                    links.append(makelink('analysis', 'detail', ref))
            row['links'] = links
        return analysislist
    

    
class analysis(restful.Resource):
    def get(self, database, projectid, nameid, analysisid):
        analysislist = getAnalysis(database, projectid, nameid, analysisid, -1)
        for row in analysislist:
            links = []
            if row['AnalysisID']:
                if int(row['AnalysisID'])>0:
                    ref = url_for('analysiscategorie', database=database, analysisid=row['AnalysisID'], _external=True)
                    links.append(makelink('analysiscategory', 'category', ref))
            ref = url_for('analysiscategoryvalues', database=database, analysisid=analysisid, _external=True)
            links.append(makelink('analysiscategoryvalues', 'valueset', ref))
            projecturi = url_for('project', id=projectid, _external=True)
            links.append(makelink('listproject', 'related', projecturi))
            links.append(makelink('name', 'related', url_for('name', database=row['DatabaseName'], id=row['NameID'], _external=True) ))
            row['links'] = links
        return analysislist
    
class analysiscategoriesforname(restful.Resource):
    def get(self, database, projectid, nameid):
        analysislist = getAnalysisCategoriesforName(database, projectid, nameid)
        for row in analysislist:
            links = []
            if row['AnalysisID']:
                if int(row['AnalysisID'])>0:
                    ref = url_for('analysiscategorie', database=database, analysisid=row['AnalysisID'], _external=True)
                    links.append(makelink('analysiscategory', 'category', ref))
                    ref = url_for('analysis', database=database, projectid=projectid, nameid=nameid, analysisid=row['AnalysisID'], _external=True)
                    links.append(makelink('analysisvalues', 'details', ref))
            row['links'] = links
        return analysislist
