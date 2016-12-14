#!/bin/python
import requests
import datetime
import time
import multiprocessing
import sys

# update primariy caches for modified lists
# Query all lists and dig to the full (broader) hierarchy for each name by following the links

def getList(listmemberlink):
    namedetailsr = requests.get(listmemberlink)
    try:
        namedetails=namedetailsr.json()
    except:
        print(namedetailsr.text)
        time.sleep(2)
        return
    for namedetail in namedetails: # only one...
        # save the name details somewhere now...
        defaultProject=namedetail["DefaultProjectID"]
        for namedetaillink in namedetail['links']:
            # here we query only hierarchies, extend this to synonyms, common names, acceptedname
            if namedetaillink['name'] == 'hierarchies':
                hierarchyselectionr = requests.get(namedetaillink['uri'])
                try:
                    hierarchyselection = hierarchyselectionr.json()
                except:
                    print hierarchyselectionr.text
                    time.sleep(2)
                    return
                
                for hierarchydetails in hierarchyselection:
                    # if there are more hierarchies-projects use the defaultProjektID
                    if not defaultProject or defaultProject==hierarchydetails['ProjectID']:
                        for hierarchydetail in hierarchydetails['links']:
                            if hierarchydetail['name'] == 'hierarchy':
                                hierarchydescrtiptionr = requests.get(hierarchydetail['uri'])
                                try:
                                    hierarchydescrtiption=hierarchydescrtiptionr.json()
                                except:
                                    print(hierarchydescrtiptionr.text)
                                    time.sleep(2)
                                    return
                                for hierarchy in hierarchydescrtiption: # only one...
                                    for hlinks in hierarchy['links']:
                                        if hlinks['name'] == 'allparents':
                                            allparentmembersr = requests.get(hlinks['uri'])
                                            # save the hierarchy details somewhere now...


if __name__ == '__main__':
    updateuris = []
    u = requests.get("http://services.snsb.info/DTNtaxonlists/rest/v0.1/lists/")
    for list in u.json():
        # print(list['projectid'])
        if True or list['projectid'] in [1154, 701] :
            moddist = 1 # minimum age of project in days
            itemscount= 'unknown'
            #for listlink in list['links']:
                #if listlink['name'] == 'listproject':
                    #projecturi = listlink['uri'] + '/modificationdate'
                    #moddist = (datetime.datetime.now() - datetime.datetime.strptime(requests.get(projecturi).json().replace('T', ' ').split('.')[0], "%Y-%m-%d %H:%M:%S")).days
            if moddist <= 1:
                for listlink in list['links']:            
                    if listlink['name'] == 'taxonnamelist':
                        listlinkuri = listlink['uri']
                        namelist = requests.get(listlinkuri).json()
                        itemscount=len(namelist)
                        for listmember in namelist:
                            for listmemberlink in listmember['links']:
                                if  listmemberlink['name'] == 'taxonname':
                                    updateuris.append(listmemberlink['uri'])
            print("List %s is  %s days old with %s items" % (list['projectid'], moddist, itemscount))
    print("Updateable items: %s" % len(updateuris))
    #print(updateuris)
    pool = multiprocessing.Pool(processes=10)
    pool.map(getList, updateuris)
    pool.join()    
    pool.close()

    
                        
                        
                    
                                    
