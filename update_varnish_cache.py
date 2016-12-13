#!/bin/python
import requests
import datetime
import multiprocessing
import sys

# update primariy caches for modified lists
# Query all lists and dig to the full (broader) hierarchy for each name by following the links

def getList(listmemberlink):
    namedetails = requests.get(listmemberlink).json()
    for namedetail in namedetails: # only one...
        # save the name details somewhere now...
        defaultProject=namedetail["DefaultProjectID"]
        for namedetaillink in namedetail['links']:
            # here we query only hierarchies, extend this to synonyms, common names, acceptedname
            if namedetaillink['name'] == 'hierarchies':
                hierarchyselection = requests.get(namedetaillink['uri'])
                for hierarchydetails in hierarchyselection.json():
                    # if there are more hierarchies-projects use the defaultProjektID
                    if not defaultProject or defaultProject==hierarchydetails['ProjectID']:
                        for hierarchydetail in hierarchydetails['links']:
                            if hierarchydetail['name'] == 'hierarchy':
                                hierarchydescrtiption = requests.get(hierarchydetail['uri']).json()
                                for hierarchy in hierarchydescrtiption: # only one...
                                    for hlinks in hierarchy['links']:
                                        if hlinks['name'] == 'allparents':
                                            allparentmembers = requests.get(hlinks['uri']).json()
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
    pool = multiprocessing.Pool(processes=30)
    pool.map(getList, updateuris)
    pool.close()
    pool.join()    

    
                        
                        
                    
                                    
