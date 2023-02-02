import os
import configparser
import myUtilsModule
import simple_term_menu
import subprocess
#TODO : how to import a module in a different relative folder?? 

# dictionary object with key as option, and value as command
myCommands = {
    "home": "/Users/benny.vandesompele/",
    "Documents": "/Users/benny.vandesompele/Documents",
    "goto src": "/Users/benny.vandesompele/Library/CloudStorage/OneDrive-ServiceNow/OneDrivesweagle/workspace/python/01test/goto",
    "exit": "exit"
}
cnt = True
# settingsFilePath = 'gotoSettings.ini'


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


def getMenuOptions(cfgFilePath="", verbose=True):
    confPars = configparser.ConfigParser()
    i = 0
    #workingPath = os.path
    #print("workingPath ", workingPath)
    #settingsFilePath = os.path.join(workingPath, settingsFile)
    if len(cfgFilePath) == 0:
        print(f"!!coding error: no file path provided!!")
        return False
    else:
        if checkFileExists(cfgFilePath, False):
            confPars.read(cfgFilePath)
            options = confPars.sections()
            for option in options:
                i += 1
                print(f"{i}: {option}")


def getSelectedMenuoption(myMenu={"", ""},myTitle=""):
    termMenu = simple_term_menu.TerminalMenu(myMenu,title=myTitle,clear_screen=False)
    selectedOptionIndex = termMenu.show() #returns the index of the listed menu options
    selectedOption = myMenuOptions[selectedOptionIndex] # lookup the menu name based upon its index in the list object
    return selectedOption


startTime = myUtilsModule.startExecution(False)
# options (list object) containing all the keys of the dictionary object
while cnt:
    myMenuOptions = list(myCommands)
    selectedOption = getSelectedMenuoption(myMenuOptions, "select a command to execute")
    selectedCmd = myCommands.get(selectedOption)
    if selectedCmd == "exit": 
        cnt =  False
        break
    returnCode = subprocess.run(["open", "-a", "Terminal", selectedCmd])
myUtilsModule.endExecution(startTime)
