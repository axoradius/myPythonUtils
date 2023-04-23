"""
works only for imgdb links
"""
import requests
import os
from bs4 import BeautifulSoup


def getHtmlFile(url):
    try:
        r = requests.get(url)
        return r
    except requests.exceptions.RequestException as err:
        print("html page does not exist")
        return False


def checkDirNew(myPath, verbose=False):
    if os.path.isdir(myPath):
        if verbose:
            print(f"path {myPath} exists already.")
        return False
    else:
        if verbose:
            print(f"path {myPath} has not been found.")
        return True


def downloadFile(url, destFolder=None, destName=None):
    print(f"check if dl is possible from {url}")
    try:
        r = requests.get(url)
        print(str(r.status_code))
    except requests.exceptions.RequestException as e:
        print("exception found")
        connectError = str(e)
        print(f"failed to connect {connectError}")
        raise SystemExit(e)
    print(f"start dl file from {url}")
    content = r.content
    destPath = destFolder + "/" + destName
    open(destPath, 'wb').write(content)


def fileNameFromUrl(url=None):
    if url is None:
        return None
    return os.path.basename(url)


baseUrl = "https://imgdb.net/"
baseDestinationPath = "/Users/bvds/Downloads/zzPython"
startRange = 10900
rangeNbr = 2
endRange = startRange + rangeNbr

destFolder = os.path.join(baseDestinationPath, str(startRange))
if checkDirNew(destFolder):
    os.mkdir(destFolder)

for i in range(startRange, endRange):
    url = baseUrl + str(i)
    r = getHtmlFile(url)
    if r != False:
        soup = BeautifulSoup(r.content, 'html5lib')

        # print(soup.prettify())
        img = soup.img.attrs
        print(img)

        subPath = img["src"]
        fullPath = "https://imgdb.net" + subPath
        print(fullPath)

        fileName = fileNameFromUrl(fullPath)
        print(fileName)

        downloadFile(fullPath, destFolder, fileName) # TODO make dlPath configurable; read configs from config file
