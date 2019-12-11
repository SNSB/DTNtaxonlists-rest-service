# restnames app

from flask import Flask,g, request, render_template
from flask_restful import Api
from werkzeug.serving import run_simple
from flask_restful.representations import json
from flask_cors import CORS

from reverseproxy import ReverseProxied

from config import config

#from flask.ext.restful.representations.json import output_json
#output_json.func_globals['settings'] = {'ensure_ascii': False, 'encoding': 'utf8'}


app = Flask(__name__)
CORS(app)
app.wsgi_app = ReverseProxied(app.wsgi_app)

api = Api(app)

app.config["APPLICATION_ROOT"] = "/DTNtaxonlists"

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASESERVER='''mssql+pymssql://TNT:unknown@tnt.diversityworkbench.de:5432''',
    DEBUG=False,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
    DEFAULTDBUSER='TNT',
    DEFAULTDBPORT=5432,
    DEFAULTDBPASSWORD='unkown',
    DEFAULTDBSERVER='tnt.diversityworkbench.de'
))

config.config['RESTFUL_JSON'] = {'sort_keys': True,
                    'indent': 2}

app.config.update(config.config)

DIVERSITY_TAXON_NAMES='DiveristyTaxonNames'


app.config.from_envvar('FLASKR_SETTINGS', silent=True)


from resources.intro import intro
from resources.lists import taxonlist, taxonlistproject, taxonlists, taxonlistflat, getTaxonListAnalyisReferencingSUB
from resources.taxonlist_flat_csv import taxonlist_flat_csv, darwin_core_zip, darwin_core_offline
from resources.names import *
from resources.agents import agent, agentsTNT, agentRelations, agentTNT, agentRelationsTNT
from resources.projects import project, projects, projectAgents, projectReferences, projectLicense, projectLastChange, projectAgentRoles
from resources.contacts import contact
from resources.commonnames import commonname, commonnames
from resources.references import references, reference, referenceTNT, referencerelations, referencerelation
from resources.references import referencingitems, namesreferencing, acceptednamesreferencing, synonymsreferencing, hierarchiesreferencing, analysiscategoriesreferencing, commonnamesreferencing, taxonlistsreferencing, projectsreferencing, agentsreferencing
from resources.references import referencechilds, referencetntchilds, referenceschildsall
import json
import urllib.request, urllib.error, urllib.parse, urllib.parse

from resources.analysis import analysiscategories, analysiscategorie, analysiscategoryvalues, analysisvalue, analysiscategoriesinproject, analysiscategoriesforname, analysis
from resources.analysis import analysisinprojectfilter, analysiscategoriechilds, projectsreferencinganalysis, analysiscategoriechildsall


from resources.webinterface import wwwtaxonlist

from resources.apitest import testapi


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    serverlist = getattr(g, 'serverlist', dict())
    for c in serverlist.values():
        connectstring='''mssql+pymssql://{userpass}@{server}'''.format(userpass=c.get('userpass'), server=c.get('server'))
        app.logger.debug("Closing connetion to %s" % connectstring)
        c.get('engine').dispose()
    serverlist.clear()        


#api.add_resource(intro, '/')   # statik baselinks to LISTS, NAMES, AGENTS, COMMONNAMES, PROJECTS

api.add_resource(taxonlists, '/lists/' )
api.add_resource(taxonlist, '/lists/<string:database>/<int:id>/') # links to all LISTS or info on this list and link to _all_ AGENTS and links to _all_ NAMES
api.add_resource(wwwtaxonlist, '/lists/<string:database>/<int:id>/www/') # link to the associated project
api.add_resource(taxonlistproject, '/lists/<string:database>/<int:id>/project/') # link to the associated project
api.add_resource(taxonlistflat, '/lists/<string:database>/<int:id>/flat/') # all names of list in flat format
api.add_resource(taxonlist_flat_csv, '/lists/<string:database>/<int:id>/csv/') # all names of list in flat format
api.add_resource(darwin_core_zip, '/lists/<string:database>/<int:id>/dwc/') # all names of list in darwin core zip  format
api.add_resource(darwin_core_offline, '/lists/<string:database>/<int:id>/dwc_offline/') # precomputet darwin core zip format
api.add_resource(getTaxonListAnalyisReferencingSUB, '/lists/<string:database>/<int:projectid>/analysisfromreference/<int:referenceid>')
api.add_resource(names, '/names/' ) 
api.add_resource(name, '/names/<string:database>/<int:id>/' ) # urls to all NAMES or info on this name including info and links to _all_ COMMONNAMES, PROJECTS, ACCEPTEDNAMES, HIERARCHIES, SYNONYMS
api.add_resource(namewww, '/names/<string:database>/<int:id>/www/' ) # urls to all NAMES or info on this name including info and links to _all_ COMMONNAMES, PROJECTS, ACCEPTEDNAMES, HIERARCHIES, SYNONYMS
api.add_resource(namecommonnames, '/names/<string:database>/<int:id>/commonnames/') # urls to the common names
#api.add_resource(nameProjects, '/names/<string:database>/<int:id>/projects' ) # urls to PROJECTS
api.add_resource(nameAcceptedNames, '/names/<string:database>/<int:id>/acceptednames/' ) # urls to ACCEPTEDNAMES,
api.add_resource(nameSynonyms, '/names/<string:database>/<int:id>/synonyms/' ) # urls to SYNONYMS
api.add_resource(nameHierarchies, '/names/<string:database>/<int:id>/hierarchies/' ) # urls to HIERARCHIES
api.add_resource(namelistprojects, '/names/<string:database>/<int:id>/lists/' ) # urls to lists containing this name

api.add_resource(agentsTNT, '/agents/', '/Agents_TNT/')
api.add_resource(agent,  '/agents/<string:database>/<int:id>/' ) # urls to all agents or info on this agent including links to _all_ CONTACTS
api.add_resource(agentRelations, '/agents/<string:database>/<int:id>/relations/' ) 
api.add_resource(agentTNT,  '/Agents_TNT/<int:id>/' ) # urls to all agents or info on this agent including links to _all_ CONTACTS
api.add_resource(agentRelationsTNT, '/Agents_TNT/<int:id>/relations/' ) 

#api.add_resource(agentContacts,  '/names/<string:database>/<int:id>/contacts' ) # urls to  _all_ CONTACTS

api.add_resource(contact, '/contacts/<int:id>/') # Info on that contacts

api.add_resource(commonnames, '/commonnames/')
api.add_resource(commonname, '/commonnames/<string:database>/<int:nameid>/<string:cid>/') # links to all commonnames or info on this common name

api.add_resource(acceptedname, '/acceptednames/<string:database>/<int:projectid>/<int:nameid>/')

api.add_resource(synonymy, '/synonymy/<string:database>/<int:projectid>/<int:nameid>/<int:synnameid>/')

api.add_resource(hierarchy, '/hierarchy/<string:database>/<int:projectid>/<int:nameid>/')
api.add_resource(hierarchyfull, '/hierarchy/<string:database>/<int:projectid>/<int:nameid>/full/')
api.add_resource(hierarchynarrowerfull, '/hierarchy/<string:database>/<int:projectid>/<int:nameid>/fullnarrow/')


api.add_resource(projects, '/projects/')
api.add_resource(project, '/projects/<int:id>/', '/Projects/<int:id>/', '/Projects_TNT/<int:id>/') # links to all projects or info on this project 
api.add_resource(projectAgents, '/projects/<int:id>/agents/', '/Projects_TNT/<int:id>/agents/')
api.add_resource(projectAgentRoles, '/projects/<int:projectid>/agents/<string:agentname>/<string:agenturi>')
api.add_resource(projectReferences, '/projects/<int:id>/references/', '/Projects_TNT/<int:id>/references/')
api.add_resource(projectLicense, '/projects/<int:id>/licenses/', '/Projects_TNT/<int:id>/licenses/')
api.add_resource(projectLastChange, '/projects/<int:id>/modificationdate/', '/Projects_TNT/<int:id>/modificationdate/')


api.add_resource(references, '/references/')
api.add_resource(reference, '/references/<string:database>/<int:id>/')
api.add_resource(referenceTNT, '/References_TNT/<int:id>/')
api.add_resource(referencetntchilds, '/References_TNT/<int:id>/childs/')
api.add_resource(referencechilds, '/references/<string:database>/<int:refid>/childs/')
api.add_resource(referenceschildsall, '/references/<string:database>/<int:refid>/allchilds/')

api.add_resource(referencerelations, '/references/<string:database>/<int:id>/relations/' )
api.add_resource(referencerelation, '/referencerelation/<string:database>/<int:id>/<string:role>/<int:sequence>/')

api.add_resource(referencingitems, '/references/<string:database>/<int:refid>/referencing/')
api.add_resource(namesreferencing, '/references/<string:database>/<int:refid>/referencing/names/')
api.add_resource(acceptednamesreferencing, '/references/<string:database>/<int:refid>/referencing/acceptednames/')
api.add_resource(synonymsreferencing, '/references/<string:database>/<int:refid>/referencing/synonyms/')
api.add_resource(hierarchiesreferencing, '/references/<string:database>/<int:refid>/referencing/hierarchies/')
api.add_resource(analysiscategoriesreferencing, '/references/<string:database>/<int:refid>/referencing/analysis/')
api.add_resource(commonnamesreferencing, '/references/<string:database>/<int:refid>/referencing/commonnames/')
api.add_resource(taxonlistsreferencing, '/references/<string:database>/<int:refid>/referencing/taxonlists/')
api.add_resource(projectsreferencing, '/references/<string:database>/<int:refid>/referencing/projects/')
api.add_resource(agentsreferencing, '/references/<string:database>/<int:refid>/referencing/agents/')

api.add_resource(analysiscategories, '/analysiscategories/')
api.add_resource(analysiscategorie, '/analysiscategories/<string:database>/<int:analysisid>/')
api.add_resource(analysiscategoriechilds, '/analysiscategories/<string:database>/<int:analysisid>/childs/')
api.add_resource(analysiscategoriechildsall, '/analysiscategories/<string:database>/<int:analysisid>/allchilds/')
api.add_resource(projectsreferencinganalysis, '/analysiscategories/<string:database>/<int:analysisid>/projects/')

                 
api.add_resource(analysiscategoryvalues, '/analysiscategories/<string:database>/<int:analysisid>/valuedefinitions/')
api.add_resource(analysisvalue, '/analysiscategorievalues/<string:database>/<int:analysisid>/<string:analysisvalue>/')
api.add_resource(analysiscategoriesinproject, '/lists/<string:database>/<int:projectid>/analysis/')
api.add_resource(analysisinprojectfilter, '/lists/<string:database>/<int:projectid>/analysis/<int:analysisid>/')

api.add_resource(analysiscategoriesforname, '/analysis/<string:database>/<int:projectid>/<int:nameid>/')
api.add_resource(analysis, '/analysis/<string:database>/<int:projectid>/<int:nameid>/<int:analysisid>/')

api.add_resource(externalidentifiers, '/names/<string:database>/<int:nameid>/externalIdentifiers/')
api.add_resource(externalnamedatabase, '/externalnameservice/<string:database>/<int:externaldatabaseid>/')



api.add_resource(regenrateindex, '/indexneubauen' ) 


api.add_resource(testapi, '/apitest/')

@app.route('/www')
@app.route('/')

def frontMatter():
    urlroot=request.url_root
    return render_template('show_lists.html', urlroot=urlroot )


@app.route('/static/api-doc.html')
def apidoc():
    x = datetime.datetime.now()
    return render_template('api-doc.html', year = x.year)


# uwsgi --http 0.0.0.0:5000 --pyhome . --module app --callable app
# http://flask.pocoo.org/docs/0.10/deploying/mod_wsgi/

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    #run_simple('0.0.0.0', 5000, app, use_reloader=True, use_debugger=False, use_evalex=True)
    
    
# distribution:
#  run ./pack.sh in activated virtual environment (source bin/activate)
#  scp restnames.tar to server
#  tar -C /var/www/localhost -xvf restnames.tar
#  pip install -r requirements.txt
#  service httpd restart
#  rebuild index: http://webservice.../indexneubauen
# TODO: index kann nicht neu gebaut werden da apache keinen zugriff hat. -> SELINUX anpassen!
# search.py anpassen falls pfad sich aendert (/var/www/localhost/index)
# mkdir -p var/www/localhost/index
# chown -R apache:apache var/www/localhost/index
# fuer SELLINUX, damit geschrieben werden darf:
# chcon -t httpd_sys_content_rw_t /var/www/localhost/index
# chcon -t httpd_sys_content_rw_t /var/www/localhost/index/*
#
# to update the docs, simply modify the static/swagger.json file
# _host and _basePath in the json are for local testing. The comment in api_doc.html is also for testing.
# to enable debug comment out run_simple above and uncomment app.run.

