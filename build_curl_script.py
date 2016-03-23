#!/usr/bin/python

import requests
import os

resp = requests.get('http://services.snsb.info/DTNtaxonlists/rest/v0.1/lists')
if resp.status_code == 200:
    print "Regenerating DWC script ..."
    with open("/root/curlscript.sh", "w") as tf:
        tf.write("#!/bin/bash\n")
        tf.write("cd /var/www/localhost/static/dwc\n")
        data = resp.json()
        for listitem in data :
            for link in listitem['links'] :
                if link['name'] == "taxonnamelist":
                    tf.write('curl -s -O -J -L '+ link['uri'] +'dwc_offline\n')
    print "Regenerating DWC-Archives"
    os.system('. /root/curlscript.sh')
else:
    print "Could not retrieve lists/"
                  
