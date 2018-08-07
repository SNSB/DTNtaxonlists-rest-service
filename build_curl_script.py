#!/usr/bin/python

import requests
import os

resp = requests.get('http://services.snsb.info/DTNtaxonlists/rest/v0.1/lists')
if resp.status_code == 200:
    print "Regenerating DWC script ..."
    with open("/root/curlscript.sh", "w") as tf:
        tf.write("#!/bin/bash\n")
        tf.write("cd /var/www/localhost/static/dwc\n")
        tf.write("rm -f /var/www/localhost/static/dwc/*.zip\n")
        data = resp.json()
        for listitem in data :
            for link in listitem['links'] :
                if link['name'] == "taxonnamelist":
                    tf.write("curl -H 'Cache-Control: no-cache' -s -S -O -J -L "+ link['uri'] +'dwc_offline\n')
    print "Regenerating DWC-Archives"
    # invalidate dwc_offline urls
    os.system('''varnishadm 'ban req.url ~ ".*dwc_offline$"' ''')
    # recreate archives (they use direct DB-access only, no web-cacheing...)
    os.system('. /root/curlscript.sh')
    # invlaidate cahche for dwc redirection and zip-files
    os.system('''varnishadm 'ban req.url ~ ".*dwc$"' ''')
    os.system('''varnishadm 'ban req.url ~ ".*zip$"' ''')
else:
    print "Could not retrieve lists/"
