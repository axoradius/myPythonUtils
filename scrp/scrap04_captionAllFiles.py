"""
creates a caption for every image in a folder and writes the output to a file
"""

import os
import json
from lavis.models import load_model_and_preprocess
import torch
from PIL import Image
import ssl
ssl._create_default_https_context = ssl._create_stdlib_context

# set variables
verbose = False
curDir = os.getcwd() # identify base path where this file is running from and compose the configFilePath
scriptName = os.path.basename(__file__).split(".")[0] # basename returns the filename. the split function with separator returns a list with substings. the first is the name without extension
configFileName = scriptName + "_cfg.json"
configFilePath = os.path.join(curDir, configFileName)
allConfigSettings = []
# method = "caption"
method = "vqa"

def getAllConfigValues(cfgPath=configFilePath, verbose=False):
    if verbose: print(f"start getAllConfigValues on {cfgPath}")
    with open(cfgPath) as json_file:
        allCfgSettings = json.load(json_file)
        if isinstance(allCfgSettings, dict):
            return allCfgSettings
        else:
            print(f"ERROR: {cfgPath} is not a valid JSON configuration file. Check the file.")
        

def createInitialCfg(cfgFilePath, verbose=False):    
    if os.path.isfile(cfgFilePath):
        if verbose: print(f"configuration file {cfgFilePath} exists already")
    else:
        writeToFile(['{'],configFilePath)
        writeToFile(['"sourcePath": "/Users/benny.vandesompele/Pictures",'],configFilePath)
        writeToFile(['"outputFileName": "catalog_caption.txt",'],configFilePath)
        writeToFile(['"listExtensions": ["jpg","jpeg","png"]'], configFilePath)
        writeToFile(['}'],configFilePath)
        if verbose: print(f"configuration file {cfgFilePath} has been created with default values. Please check the values.")


def listAllFiles(srcPath, listExtensions=["jpg","jpeg","png"], verbose=False):
    result = []
    i = 0
    if os.path.isdir(srcPath):
        allFiles = os.listdir(srcPath)
        for ext in listExtensions:
            i += 1
            if verbose: print(f"iteration {i}: for extension {ext}")
            for f in allFiles:
                if f.endswith(ext):
                    if verbose: print(f"{f} has a valid extension {ext}")
                    result.append(f)
    else:
        print(f"ERROR: {srcPath} is not a valid path")
    return result


def writeToFile(messages=[], filePath=""):
    for msg in messages:
        myFile = open(filePath,"a")
        myFile.write(msg)


if __name__ == "__main__":
    print(f"::: start :::")
    # checks if the cfg exists, if not creates a default file
    createInitialCfg(configFilePath)

    # get parameter values from cfg.json
    allConfigSettings = getAllConfigValues(configFilePath)
    sourcePath = allConfigSettings["sourcePath"]
    outputFileName = allConfigSettings["outputFileName"]
    listExtensions = []
    listExtensions = allConfigSettings["listExtensions"]
    if len(listExtensions) == 0: 
        print(f"ERROR: list of extensions in {configFilePath} is empty. Please check")
        exit
    if verbose: 
        print(f"sourcePath is {sourcePath}")
        print(f"outputFileName is {outputFileName}")
        print(f"list of extions to filter on is {listExtensions}")

    # create list of files at target location
    images = listAllFiles(sourcePath, listExtensions,verbose)
    nbrFound = len(images)
    catalogPath = os.path.join(sourcePath, "catalog.txt")
    print(f"nbr of files with a relevant extension: {nbrFound}")

    if method == "caption":
        # create caption for each image file
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # print("... load model and preprocess")
        model, vis_processors, _ = load_model_and_preprocess(name="blip_caption", model_type="base_coco", is_eval=True, device=device)
        for img in images:
            fp = os.path.join(sourcePath, img)
            if verbose: print(f"... image: {fp}")
            raw_image = Image.open(fp).convert("RGB")

            # preprocess the image
            # vis_processors stores image transforms for "train" and "eval" (validation / testing / inference)
            if verbose: print("... process image")
            image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)

            # generate caption
            if verbose: print("... generate caption")
            imageCaption = model.generate({"image": image})
            print(f"{img} : {imageCaption[0]}")
            writeToFile([img, ",", imageCaption[0]], catalogPath)

    if method == "vqa":
        print(images)
        img = input("for which file do you have a question? ")
        fp = os.path.join(sourcePath, img)


        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # print("... load model and preprocess")
        model, vis_processors, txt_processors = load_model_and_preprocess(name="blip_vqa", model_type="vqav2", is_eval=True, device=device)
        if verbose: print(f"... image: {fp}")
        raw_image = Image.open(fp).convert("RGB")

        # preprocess the image
        # vis_processors stores image transforms for "train" and "eval" (validation / testing / inference)
        if verbose: print("... process image")
        image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)

        cnt = True
        while cnt:
            question = input("what is your question? ")
            if question == "exit":
                cnt = False
            else:
                question = txt_processors["eval"](question)
                answer = model.predict_answers(samples={"image": image, "text_input": question}, inference_method="generate")
                print(f"answer: {answer}")