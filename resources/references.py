# agents
# REST interface to agents

from flask.ext import restful
from database.reference import getreferences, getreference, getreferencerelations, getreferencerelation
from database.dbreferences import makeReferenceURI, getReferenceChilds
from flask import url_for
#import urllib2

from database.agent import getAllReferenceingAgents
from database.analysis import getAllReferenceingCategories
from database.commonname import getAllReferenceingCommonNames
from database.list import getAllReferenceingTaxonLists
from database.name import getAllReferencingTaxonNames, getAllReferenceingAcceptedNames, getAllReferenceingSynonyms, getAllReferenceingHierarchies
from database.project import getAllProjectsWithReference

def makelink(label, name, the_uri):
    link = {}
    link['uri'] = the_uri
    link['type'] = 'uri'
    link['rel'] = name
    link['name'] = label
    return link

class references(restful.Resource):
    def get(self):
        referencelist = getreferences('DiversityReferences_TNT')
        for row in referencelist:
            links = []
            ref = url_for('reference', database='DiversityReferences_TNT', id=row['RefID'], _external=True)
            links.append(makelink('reference', 'details', ref))
            row['links'] = links
        return referencelist

class reference(restful.Resource):
    def get(self, database, id):
        referencelist = getreference(database, id)
        for row in referencelist:
            links = []
            links.append(makelink('relations', 'authors', url_for('referencerelations',  database=row['DatabaseName'], id=row['RefID'], _external=True)))
            links.append(makelink('referencing', 'links', url_for('referencingitems',  database=row['DatabaseName'], refid=row['RefID'], _external=True)))
            links.append(makelink('reference', 'childs', url_for('referencechilds',  database=row['DatabaseName'], refid=row['RefID'], _external=True)))
            if row['ParentRefID']:
                if (int(row['ParentRefID'])):
                    links.append(makelink('reference', 'parent', url_for('reference',  database=row['DatabaseName'], id=row['ParentRefID'], _external=True)))             
            row['links'] = links
        return referencelist

class referenceTNT(restful.Resource):
    def get(self,  id):
        referencelist = getreference('DiversityReferences_TNT', id)
        for row in referencelist:
            links = []
            links.append(makelink('relations', 'authors', url_for('referencerelations',  database='DiversityReferences_TNT', id=row['RefID'], _external=True)))
            links.append(makelink('referencing', 'links', url_for('referencingitems',  database='DiversityReferences_TNT', refid=row['RefID'], _external=True)))
            links.append(makelink('reference', 'childs', url_for('referencechilds',  database='DiversityReferences_TNT', refid=row['RefID'], _external=True)))
            if row['ParentRefID']:
                if (int(row['ParentRefID'])):
                    links.append(makelink('reference', 'parent', url_for('reference',  database='DiversityReferences_TNT', id=row['ParentRefID'], _external=True)))            
            row['links'] = links
        return referencelist    

class referencechilds(restful.Resource):
    def get(self, database, refid):
        referencelist = getReferenceChilds(database, refid)
        for row in referencelist:
            links = []
            links.append(makelink('reference', 'item', url_for('reference',  database=row['DatabaseName'], id=row['RefID'], _external=True)))
            row['links'] = links
        return referencelist

class referencetntchilds(restful.Resource):
    def get(self, id):
        referencelist = getReferenceChilds('DiversityReferences_TNT', id)
        for row in referencelist:
            links = []
            links.append(makelink('reference', 'item', url_for('reference',  database='DiversityReferences_TNT', id=row['RefID'], _external=True)))
            row['links'] = links
        return referencelist
    
class referencerelations(restful.Resource):
    def get(self, database, id):
        relationslist = getreferencerelations(database, id)
        for row in relationslist:
            links = []
            links.append(makelink('referenceRelation', 'details', url_for('referencerelation',  database=row['DatabaseName'], id=row['RefID'], role=row['Role'],sequence=row['Sequence'], _external=True)))
            row['links'] = links
        return relationslist
      
class referencerelation(restful.Resource):
    def get(self, database, id, role, sequence):
        relationslist = getreferencerelation(database, id, role, sequence)
        return relationslist

# items with references

class agentsreferencing(restful.Resource):    
    def get(self, database, refid):
        referenceuri = makeReferenceURI(database, refid)
        agentlist = getAllReferenceingAgents(referenceuri)
        for row in agentlist:
            links = []
            links.append(makelink('agent', 'item', url_for('agent',  database=row['DatabaseName'], id=row['AgentID'], _external=True)))
            row['links'] = links
        return agentlist
    
class agentsreferencingtnt(restful.Resource):    
    def get(self, database, refid):
        referenceuri = makeReferenceURI(database, refid)
        agentlist = getAllReferenceingAgents(referenceuri)
        for row in agentlist:
            links = []
            links.append(makelink('agent', 'item', url_for('agent',  database='DiversityAgents_TNT', id=row['AgentID'], _external=True)))
            row['links'] = links
        return agentlist
    
class analysiscategoriesreferencing(restful.Resource):
    def get(self, database, refid):
        referenceuri = makeReferenceURI(database, refid)
        analysislist = getAllReferenceingCategories(referenceuri)
        for row in analysislist:
            links = []
            if row['AnalysisID']:
                if int(row['AnalysisID'])>0:
                    ref = url_for('analysiscategorie', database=row['DatabaseName'], analysisid=row['AnalysisID'], _external=True)
                    links.append(makelink('analysiscategory', 'item', ref))
            row['links'] = links
        return analysislist


class commonnamesreferencing(restful.Resource):
    def get(self, database, refid):
        referenceuri = makeReferenceURI(database, refid)
        results = getAllReferenceingCommonNames(referenceuri)
        for row in results:
            links = []
            newid = u"[%s#%s#%s#%s]" % (row['CommonName'], row['LanguageCode'], row['CountryCode'], row['ReferenceTitle'])
            #newid = urllib2.quote(newid.encode('utf-8')) # no utf8 but %xx encoding in urls 
            #url = u"http://tnt.diversityworkbench.de/commonnames/%s/%s/%s" % (row['DatabaseName'], row['NameID'], newid )
            url = url_for('commonname', database=row['DatabaseName'], nameid=row['NameID'], cid=newid, _external=True)
            #print url
            links.append(makelink('commonnames','details', url))
            row['links'] = links
        return results 


class taxonlistsreferencing(restful.Resource):
    def get(self, database, refid):
        referenceuri = makeReferenceURI(database, refid)
        listlist = getAllReferenceingTaxonLists(referenceuri)
        for row in listlist:
            links = []
            links.append(makelink('listproject', 'detail', url_for('taxonlistproject',  database=row['DatabaseName'], id=row['ProjectID'], _external=True)))
            links.append(makelink('list', 'items', url_for('taxonlist',  database=row['DatabaseName'], id=row['ProjectID'], _external=True)))
            row['links'] = links
        return listlist
    
    
# referencing 
class namesreferencing(restful.Resource):    
    def get(self, database, refid):
        referenceuri = makeReferenceURI(database, refid)
        namelist = getAllReferencingTaxonNames(referenceuri)
        for row in namelist:
            links = []
            links.append(makelink('name', 'details', url_for('name',  database=row['DatabaseName'], id=row['NameID'], _external=True)))
            row['links'] = links
        return namelist
    
    
class acceptednamesreferencing(restful.Resource):    
    def get(self, database, refid):
        referenceuri = makeReferenceURI(database, refid)
        namelist = getAllReferenceingAcceptedNames(referenceuri)
        for row in namelist:
            links = []
            links.append(makelink('acceptedname', 'details', url_for('acceptedname', database=row['DatabaseName'], projectid=row['ProjectID'], nameid=row['NameID'], _external=True)))
            row['links'] = links
        return namelist


class synonymsreferencing(restful.Resource):    
    def get(self, database, refid):
        referenceuri = makeReferenceURI(database, refid)
        namelist = getAllReferenceingSynonyms(referenceuri)
        for row in namelist:
            links = []
            links.append(makelink('synonymname', 'details', url_for('name', database=row['DatabaseName'], id=row['SynNameID'], _external=True)))
            row['links'] = links
        return namelist


class hierarchiesreferencing(restful.Resource):    
    def get(self, database, refid):
        referenceuri = makeReferenceURI(database, refid)
        hlist = getAllReferenceingHierarchies(referenceuri)
        for row in hlist:
            links=[]
            links.append(makelink('hierarchy', 'details', url_for('hierarchy', database=row['DatabaseName'], projectid=row['ProjectID'], nameid=row['NameID'], _external=True)))
            row['links'] = links
        return hlist      
    

class projectsreferencing(restful.Resource):
    def get(self, database, refid):
        referenceuri = makeReferenceURI(database, refid)
        projectlist = getAllProjectsWithReference(referenceuri)
        for row in projectlist:
            links = []
            links.append(makelink('projects', 'item', url_for('project', id = row['ProjectID'], _external=True)))
            row['links'] = links
        return projectlist


    
class referencingitems(restful.Resource):
    def get(self, database, refid):
        referencingitemslist=[]
        referencingitem={}
        referencingitem['DatabaseName'] = database
        referencingitem['ReferenceID'] = refid
        referenceuri = makeReferenceURI(database, refid)
        referencingitem['ReferenceURI'] = referenceuri
        links =  []
        links.append(makelink('agents', 'referencing', url_for('agentsreferencing',  database=database, refid=refid, _external=True)))
        links.append(makelink('analysiscategories', 'referencing', url_for('analysiscategoriesreferencing',  database=database, refid=refid, _external=True)))
        links.append(makelink('commonnames', 'referencing', url_for('commonnamesreferencing',  database=database, refid=refid, _external=True)))
        links.append(makelink('taxonlists', 'referencing', url_for('taxonlistsreferencing',  database=database, refid=refid, _external=True)))
        links.append(makelink('taxonnames', 'referencing', url_for('namesreferencing',  database=database, refid=refid, _external=True)))
        links.append(makelink('acceptednames', 'referencing', url_for('acceptednamesreferencing',  database=database, refid=refid, _external=True)))        
        links.append(makelink('synonyms', 'referencing', url_for('synonymsreferencing',  database=database, refid=refid, _external=True)))        
        links.append(makelink('hierarchies', 'referencing', url_for('hierarchiesreferencing',  database=database, refid=refid, _external=True)))        
        links.append(makelink('projects', 'referencing', url_for('projectsreferencing',  database=database, refid=refid, _external=True)))        
        referencingitem['links'] = links
        referencingitemslist.append(referencingitem)
        return referencingitemslist
        
