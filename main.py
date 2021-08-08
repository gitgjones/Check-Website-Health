import requests
import json
from datetime import datetime
import csv

def getURL(strUrl):
    return requests.get(strUrl, allow_redirects=False)

def printResponseDetails(response):
    print ("Response took: " + str(response.elapsed.total_seconds()))
    #print ("Headers returned: " + str(response.headers))
    print ("Response status code: " + str(response.status_code))

with open('config.json') as json_data_file:
    appConfig = json.load(json_data_file)
    for sites in appConfig['sitesToCheck']:
        datetimeOfCheck = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        urlToCheck = sites['url']
        redirectUrl = sites['shouldRedirect']
        redirectSuccess = ""
        redirectResponseTime = ""
        urlSuccess = ""
        urlResponseTime = ""
        errorStage = ""
        response = getURL(urlToCheck)
        printResponseDetails(response)
        if sites['shouldRedirect'] == "True":
            if response.status_code == 301:
                if sites['redirectUrl'] == response.headers['Location']:
                    redirectSuccess = "True"
                    redirectResponseTime = response.elapsed.total_seconds()
                    redirectResponse = getURL(response.headers['Location'])
                    if redirectResponse.status_code == 200:
                        urlSuccess = "True"
                        urlResponseTime = redirectResponse.elapsed.total_seconds()
                    else:
                        urlSuccess = "False"
                        errorStage = "Failed to load redirect"
                else:
                    redirectSuccess = "False"
                    errorStage = "Incorrect redirect URL"
            else:
                redirectSuccess = "False"
                errorStage = "Expected 301 not received"
        else:
            if response.status_code == 200:
                urlSuccess = "True"
            else:
                urlSuccess = "False"
                errorStage = "Failed to load URL"

        fields=[datetimeOfCheck,urlToCheck,redirectUrl,redirectSuccess,redirectResponseTime,urlSuccess,urlResponseTime,errorStage]
        f = open("website-health.csv", "a")
        writer = csv.writer(f)
        writer.writerow(fields)
        f.close()
            
        

# CSV output
# Time of Check, URL, Redirect, Redirect Success, Redirect Response Time, URL Success, URL Response Time, Error