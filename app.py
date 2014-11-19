# restnames app

from flask import Flask,g, request, render_template
from flask.ext import restful


app = Flask(__name__)
api = restful.Api(app)


# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASESERVER='''mssql+pymssql://TNT:***REMOVED***@tnt.diversityworkbench.de:5432''',
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
    DEFAULTDBUSER='TNT',
    DEFAULTDBPORT=5432,
    DEFAULTDBPASSWORD='***REMOVED***',
    DEFAULTDBSERVER='tnt.diversityworkbench.de'
))

DIVERSITY_TAXON_NAMES='DiveristyTaxonNames'


app.config.from_envvar('FLASKR_SETTINGS', silent=True)

from resources.intro import intro
from resources.lists import taxonlist, taxonlistproject, taxonlists
from resources.names import *
from resources.agents import agent, agentsTNT, agentRelations, agentTNT, agentRelationsTNT
from resources.projects import project, projects, projectAgents
from resources.contacts import contact
from resources.commonnames import commonname, commonnames
import json
import urllib2, urlparse


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    serverlist = getattr(g, 'serverlist', dict())
    for c in serverlist.itervalues():
        connectstring='''mssql+pymssql://{userpass}@{server}'''.format(userpass=c.get('userpass'), server=c.get('server'))
        app.logger.debug("Closing connetion to %s" % connectstring)
        c.get('engine').dispose()
    serverlist.clear()        


#api.add_resource(intro, '/')   # statik baselinks to LISTS, NAMES, AGENTS, COMMONNAMES, PROJECTS

api.add_resource(taxonlists, '/lists/' )
api.add_resource(taxonlist, '/lists/<string:database>/<int:id>') # links to all LISTS or info on this list and link to _all_ AGENTS and links to _all_ NAMES
api.add_resource(taxonlistproject, '/lists/<string:database>/<int:id>/project') # link to the associated project

api.add_resource(names, '/names/' ) 
api.add_resource(name, '/names/<string:database>/<int:id>' ) # urls to all NAMES or info on this name including info and links to _all_ COMMONNAMES, PROJECTS, ACCEPTEDNAMES, HIERARCHIES, SYNONYMS
api.add_resource(nameCommonNames, '/names/<string:database>/<int:id>/commonnames') # urls to the common names
#api.add_resource(nameProjects, '/names/<string:database>/<int:id>/projects' ) # urls to PROJECTS
api.add_resource(nameAcceptedNames, '/names/<string:database>/<int:id>/acceptednames' ) # urls to ACCEPTEDNAMES,
api.add_resource(nameSynonyms, '/names/<string:database>/<int:id>/synonyms' ) # urls to SYNONYMS
api.add_resource(nameHierarchies, '/names/<string:database>/<int:id>/hierarchies' ) # urls to HIERARCHIES

api.add_resource(agentsTNT, '/agents/', '/Agents_TNT/')
api.add_resource(agent,  '/agents/<string:database>/<int:id>' ) # urls to all agents or info on this agent including links to _all_ CONTACTS
api.add_resource(agentRelations, '/agents/<string:database>/<int:id>/relations' ) 
api.add_resource(agentTNT,  '/Agents_TNT/<int:id>' ) # urls to all agents or info on this agent including links to _all_ CONTACTS
api.add_resource(agentRelationsTNT, '/Agents_TNT/<int:id>/relations' ) 

#api.add_resource(agentContacts,  '/names/<string:database>/<int:id>/contacts' ) # urls to  _all_ CONTACTS

api.add_resource(contact, '/contacts/<int:id>') # Info on that contacts

#api.add_resource(commonnames, '/commonnames/')
api.add_resource(commonname, u'/commonnames/<string:database>/<int:nameid>/<string:cid>') # links to all commonnames or info on this common name

api.add_resource(acceptedname, '/acceptednames/<string:database>/<int:projectid>/<int:nameid>')

api.add_resource(synonymy, '/synonymy/<string:database>/<int:projectid>/<int:nameid>/<int:synnameid>')

api.add_resource(hierarchy, '/hierarchy/<string:database>/<int:projectid>/<int:nameid>')


api.add_resource(projects, '/projects/')
api.add_resource(project, '/projects/<int:id>', '/Projects/<int:id>', '/Projects_TNT/<int:id>') # links to all projects or info on this project 
api.add_resource(projectAgents, '/projects/<int:id>/agents', '/Projects_TNT/<int:id>/agents')

#TODO: References einbauen



@app.route('/www/')
def frontMatter():
    urlroot=request.url_root
    return render_template('show_lists.html', urlroot=urlroot )


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)