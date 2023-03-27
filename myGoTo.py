import os
import shutil
import configparser
import simple_term_menu
import subprocess
import json
from datetime import datetime

configFile = "/Users/benny.vandesompele/myGoToConfig.json"
myCommands = {}

#TODO : how to import a module in a different relative folder?? 

def readJSONtoDictionary(fp, verbose=False):
    # dictionary object with key as option, and value as command
    myJSON = {}
    try:
        with open(fp) as json_file:
            try: 
                myJSON = json.load(json_file)
                if verbose: 
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

def cpFileToDestination(srcPath,destPath):
    print(f"copy {srcPath} to {destPath}")

    cp = shutil.copy2(srcPath,destPath) #copy2 copies the metadata as well. 
    print(cp)

def getSelectedMenuoption(myMenu={"", ""},myTitle=""):
    termMenu = simple_term_menu.TerminalMenu(myMenu,title=myTitle,clear_screen=False)
    selectedOptionIndex = termMenu.show() #returns the index of the listed menu options
    selectedOption = myMenuOptions[selectedOptionIndex] # lookup the menu name based upon its index in the list object
    return selectedOption

def writeHistory(msg, returnCode=0,verbose=False):
    curDateTime = datetime.now()
    myFile = open("gotoHistory.txt", "a") # append mode, will create the file if it does not exist or append in case exists
    #strftime is required to convert object from datetime to string + write method does not add a new line character, add it manually
    fullMsg = curDateTime.strftime("%Y/%m/%d %H:%M:%S") + "," + msg + "," + str(returnCode) + "\n"
    myFile.write(fullMsg)
    #myFile.write('\n') 
    myFile.close

def createReturnMsg(retObject): #converst the returnCode is a return msg for easier handling
    rtnMsg = "Successfull execution"
    rtCode = returnCode.returncode
    if rtCode != 0:
        rtnMsg = "!! error: " + rtCode + " : " + returnCode.args   
    return rtnMsg

# parameter containing the full json as a dict object
myCommands = readJSONtoDictionary(configFile, False)
cnt = True
selectedCmd = ""
selectedOption = ""
rtnMsg = ""

if isinstance(myCommands, dict): # check a valid dictionary object has been returned. If not, there was a problem reading the config file
    while cnt:
        #subprocess.run("clear")
        print("***********************************")
        print("**** welcome to myGoTo utility ****")
        print("***********************************")
        if selectedCmd: #should only be displayed if there was a command executed. So not upon first start
            print(f"last command executed: {selectedOption}")
            print(f"{rtnMsg}")

        myMenuOptions = list(myCommands) # list command puts all the keys in the dict into a list object
        selectedOption = getSelectedMenuoption(myMenuOptions, "select a command to execute")
        selectedCmd = myCommands.get(selectedOption)
        if selectedOption == "exit": 
            cnt =  False
        if selectedOption == "edit config file":
            returnCode = subprocess.run(["subl", "-w", selectedCmd]) #subprocess.run returns an object with args and returncode
            rtnMsg = createReturnMsg(returnCode)
            myCommands = readJSONtoDictionary(configFile, False) #reload the config file as things might have changed.
        if selectedOption == "push myGoTo.py to github":
            print("start copy file")
            cpFileToDestination("myGoTo.py",selectedCmd)
            rtnMsg = "successfull execution"
        else:
            returnCode = subprocess.run(["open", "-a", "Terminal", selectedCmd]) #this is not the right way to exit a sub process
            rtnMsg = createReturnMsg(returnCode)
        writeHistory(selectedCmd)
else:
    print(f"ERROR: {configFile} does not seem to be a valid JSON based configuration file")


