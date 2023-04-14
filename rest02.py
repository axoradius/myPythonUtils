import requests
import subprocess
from requests.auth import HTTPBasicAuth
import json
import time

def connect(verbose=False):
    cfgFile = "rest02Config.json"
    read_file = open(cfgFile)
    connectDetails = json.load(read_file)
    if verbose:
        print(connectDetails)
    return connectDetails

def getExportContent(exportId):
    print("** start getExportContent")
    fullUrl = sncUrl + "/api/sn_cdm/applications/deployables/exports/" + exportId + "/content"
    print(f"full URL: {fullUrl}")
    print(f"authentication: {sncUsr}, {sncPwd}")
    print(f"content: {reqHeaders}")

    response = requests.get(fullUrl, headers=reqHeaders, auth=(sncUsr, sncPwd))

    print(response.json())

    if response.status_code == 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        #exit()

    print(response.json())

if __name__ == "__main__":
    subprocess.run("clear")
    connectDetails = connect()
    sncUrl = connectDetails["sncUrl"]
    sncUsr = connectDetails["sncUser"]
    sncPwd = connectDetails["sncPwd"]

    exporterName = "returnAllData-now"
    appName = "PRD1"
    deployableName = "devtest2"

    sncAuth = HTTPBasicAuth(sncUsr,sncPwd)
    reqHeaders = {'content-type' : 'application/json', "Accept":"application/json"}

    #response=$(curl -s "${sncUrl}/api/sn_cdm/applications/deployables/exports?deployableName=${deplName}&exporterName=${expName}&args=%7B%22keyName%22%3A%22${expArg1}%22%2C%22nodeName%22%3A%22${expArg2}%22%7D&appName=${appName}&dataFormat=${expFormat}" --request POST --header 'Accept:application/json' --user ${sncUser}:${sncPwd})
    fullUrl = sncUrl + "/api/sn_cdm/applications/deployables/exports?deployableName=" + deployableName + "&appName=" + appName + "&exporterName=" + exporterName + "&dataFormat=json"
    print(f"full URL: {fullUrl}")
    
    response = requests.post(fullUrl, headers=reqHeaders, auth=sncAuth)
    print(response)
    responseData = response.json()
    print(responseData)
    exportId = responseData['result']['export_id']
    #exportId = "035c8ed3870ea110dfeec91d8bbb35a4"
    print(f"exportID {exportId}")
    time.sleep(2)

    getExportContent(exportId)



#https://sweagleprd1.service-now.com/api/sn_cdm/applications/deployables/exports/77e84e5b87c6a1100c2440c80cbb35a5/content
#https://sweagleprd1.service-now.com/api/sn_cdm/applications/deployables/exports/77e84e5b87c6a1100c2440c80cbb35a5/content