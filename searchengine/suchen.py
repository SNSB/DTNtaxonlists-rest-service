 
# searchengien whoosh interface
from whoosh.index import create_in
import whoosh.index as index
from whoosh.fields import *
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.query import FuzzyTerm, Every
from whoosh import query, qparser

import os, os.path
from database.name import *
from database.dbtaxonname import *
from flask import url_for
import six # unicode 

from flask import Response, render_template


def createindex():
    # creates the index and deltes an existing one.
    schema = Schema(name=TEXT(stored=True), # the latin name
                    name_part=TEXT(stored=True), # the name without the author
                    url=ID(stored=True), # the url of the name
                    commonname=TEXT(stored=True), # the common names, comma separated
                    project=TEXT(stored=True),
                    database=TEXT, # in which database
                    country=TEXT, # all countries, comma separated
                    tags=KEYWORD)
    if not os.path.exists("/var/www/localhost/index"):
       os.mkdir("/var/www/localhost/index")
    ix = create_in("/var/www/localhost/index", schema)
    writer = ix.writer()
    allnames=getAllNames()
    for item in allnames:
        if item['ProjectID'] in [701, 704, 1137, 855, 1143, 1144, 849, 1140, 1129, 853, 852, 851, 1154]:
            uri = u"" + url_for('name', database=item['DatabaseName'], id = item['NameID'], _external=True)
            commonnames=getTaxonNameAllCommonNames(item['DatabaseName'], item['NameID'])
            cn = u" "
            co = u" "
            for n in commonnames:
                cn += n['CommonName'] + u", "
                co += n['CountryCode'] + u", "
            if len(cn)>1:
                cn=cn.strip()
            namelist = getTaxonName_for_search_only(item['DatabaseName'], item['NameID'])
            taxonname = u""
            taxonname_part = u""
            keys = u""
            if len(namelist)>0:
                taxonname = namelist[0]['TaxonNameCache']
                taxonname_part = namelist[0]['TaxonName_for_search_only']
                keys = u",".join(filter(lambda l: isinstance(l, six.string_types), namelist[0].values()))
            #print("country: %s " % co)
            #print("commonname: %s " % cn)
            writer.add_document(name=taxonname, name_part=taxonname_part, url=uri, database=item['DatabaseName'], project=u"%s" % item['ProjectID'], commonname=cn, country=co, tags=keys)
    #        else:
    #          writer.add_document(name=taxonname, url=uri, database=item['DatabaseName'], tags=keys)
    writer.commit()
    
def indexquery(name,www):
    if name==None:
        return []
    #print("Name: %s" % name)        
    ix = index.open_dir("/var/www/localhost/index")
    qp = MultifieldParser(["commonname", "database", "tags", "name", "name_part", "country", "project", "url"], schema=ix.schema, termclass=FuzzyTerm)
    qp.add_plugin(qparser.FuzzyTermPlugin())
    q = qp.parse(name)
    #q = Every()
    tempvar=[]
    with ix.searcher() as searcher:
        results = searcher.search(q, limit=None)
        for hit in results:
            tempvar.append({'name':hit["name"], 'commonname':hit["commonname"] , 'url':hit["url"]})
    if  not www:
        return tempvar
    else:
        response = Response(render_template("searchresults.html", resultlist=tempvar) )
        response.headers['content-type'] = 'text/html'
        return response
       
        
    
            
        
    


