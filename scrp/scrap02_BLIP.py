"""
works only for imgdb links
pip install salesforce-lavis (contains the BLIP module)
"""
import requests
import os
from bs4 import BeautifulSoup
from lavis.models import model_zoo
from lavis.models import load_model_and_preprocess
import torch
from PIL import Image

# required to get the load model and preprocess to work, otherwise you get a certificate failed error message
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context


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
startRange = 10910
rangeNbr = 2
endRange = startRange + rangeNbr

destFolder = os.path.join(baseDestinationPath, str(startRange))
if checkDirNew(destFolder):
    os.mkdir(destFolder)


#print(model_zoo)


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

        fullDestPath = os.path.join(destFolder, fileName)
        downloadFile(fullPath, destFolder, fileName) # TODO make dlPath configurable; read configs from config file

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # load sample image
        print("... load image")
        raw_image = Image.open(fullDestPath).convert("RGB")

        print("... load model and preprocess")
        model, vis_processors, _ = load_model_and_preprocess(name="blip_caption", model_type="base_coco", is_eval=True,
                                                             device=device)
        # preprocess the image
        # vis_processors stores image transforms for "train" and "eval" (validation / testing / inference)
        print("... process image")
        image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)

        # generate caption
        print("... generate caption")
        print(model.generate({"image": image}))
        #print(model)




