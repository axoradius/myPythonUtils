import os
import configparser
import simple_term_menu
import subprocess
import json

configFile = "myGoToConfig.json"
myCommands = {}

# TODO : how to import a module in a different relative folder??


def readJSONtoDictionary(fp, verbose=False):
    # dictionary object with key as option, and value as command
    myJSON = {}
    try:
        with open(fp) as json_file:
            try: 
                myJSON = json.load(json_file)
                print("in function return type: ", type(myJSON))
                if isinstance(myJSON, dict):
                    return myJSON
                else:
                    error = "not a valid json"
                    return error
            except ValueError as error:
                #logger.error(error)
                if verbose: print(f"JSON error in file: {error} ")
                return error
    except IOError:
        error = "error in processing file " + fp
        if verbose: print(f"fatal error accessing {fp} : {error} ")
        return error


def checkFileExists(myPath="", verbose=False):
    """checks if a provided path exists - works for both a folder path as well as a file path"""
    checkForFile = False
    checkForRelPath = False
    checkForAbsPath = False
    if myPath != "":
        if os.path.basename(myPath):
            checkForFile = True
            if verbose: 
                print(f"{os.path.basename(myPath)} is a path to a file")
        else:
            if verbose: 
                print(f"{os.path.basename(myPath)} is a path to a folder")

        exists = os.path.exists(myPath)
        if verbose:
            if exists: 
                print(f"{myPath} exists.")
            else:
                print(f"ERROR: {myPath} cannot be found")
        return exists
    else:
        if verbose:
            print(f"!! CODING ERROR: no path was provided")
        return False


def getSelectedMenuoption(myMenu={"", ""},myTitle=""):
    termMenu = simple_term_menu.TerminalMenu(myMenu,title=myTitle,clear_screen=False)
    selectedOptionIndex = termMenu.show() #returns the index of the listed menu options
    selectedOption = myMenuOptions[selectedOptionIndex] # lookup the menu name based upon its index in the list object
    return selectedOption


# parameter containing the full json as a dict object
myCommands = readJSONtoDictionary(configFile, False)
cnt = True

# check a valid dictionary object has been returned. If not, there was a problem reading the config file
if isinstance(myCommands, dict): 
    while cnt:
        myMenuOptions = list(myCommands) # list command puts all the keys in the dict into a list object
        selectedOption = getSelectedMenuoption(myMenuOptions, "select a command to execute")
        selectedCmd = myCommands.get(selectedOption)
        if selectedCmd == "exit": 
            cnt =  False
        returnCode = subprocess.run(["open", "-a", "Terminal", selectedCmd])
else:
    print(f"ERROR: {configFile} does not seem to be a valid JSON based configuration file")


