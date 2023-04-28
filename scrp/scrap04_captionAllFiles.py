"""
creates a caption for every image in a folder and writes the output to a file
"""

import os
import json

# set variables
verbose = False
curDir = os.getcwd() # identify base path where this file is running from and compose the configFilePath
scriptName = os.path.basename(__file__).split(".")[0] # basename returns the filename. the split function with separator returns a list with substings. the first is the name without extension
configFileName = scriptName + "_cfg.json"
configFilePath = os.path.join(curDir, configFileName)
allConfigSettings = []


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
    res = listAllFiles(sourcePath, listExtensions,verbose)
    nbrFound = len(res)
    print(f"nbr of files with a relevant extension: {nbrFound}")


    # writeToFile(["hello1","hello2"],"/Users/benny.vandesompele/Pictures/catalog.txt")