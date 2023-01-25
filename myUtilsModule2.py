import os
import datetime  # import the toplevel module with all the methods to prevent confusion with the datetime class & type name. BAD design of this OOTB library
from moviepy.editor import *


def str2boolean(myStr):
    """returns a boolean True in case the string provided is either yes, true or 1"""
    return str(myStr).lower() in ("true", "yes", "1")
    # unbelievable there is no standard python method for this??


def startExecution(printHeader=True):
    """clears the screen, optionally does not print a header and returns the starting time stamp of the execution"""
    currT = datetime.datetime.now()
    os.system("clear")
    if str2boolean(printHeader): print(f"==== starting at {currT} ===")
    return currT


def endExecution(startTime=""):
    """print closing message and optionally the execution duration in seconds"""
    currT = datetime.datetime.now()
    if isinstance(startTime, (datetime.datetime,
                              datetime.date)):  # this ensures the provided value has a valid datetime stamp or a valid date stamp
        durationSeconds = (
                    currT - startTime).total_seconds()  # this calculation returns an object of type "timedelta". That type has methods such as total_seconds()
        print(f"==== ending execution at {currT} --> duration was {durationSeconds} seconds")
        return durationSeconds
    else:
        print(f"==== ending execution at {currT} ===")
        return None


def convertToGif(vidFolderPath, srcName, targetExt, startSec, endSec, overwrite=False):
    # parameter preparation
    vidFullPath = os.path.join(vidFolderPath, srcName)

    # check if src file exists
    if not (os.path.exists(vidFolderPath)):
        print(f"Error: Folder {vidFolderPath} does not exist")
        exit(1)

    if not (os.path.exists(vidFullPath)):
        print(f"Error: File {vidFullPath} does not exist")
        exit(1)

    # create video file clip object
    videoClip = VideoFileClip(vidFullPath)
    if endSec > startSec:
        print(f"start at {startSec}sec till {endSec}sec, overwrite is {overwrite}")
        videoClip = videoClip.subclip(startSec, endSec)

    # parameter helpers
    srcNameSplit = os.path.splitext(srcName)
    srcNameBase = srcNameSplit[0]
    srcNameExt = srcNameSplit[1]
    srcSize = round(os.path.getsize(vidFullPath) / 1024)
    targetName = srcNameBase + "." + targetExt
    targetFullPath = os.path.join(vidFolderPath, targetName)
    print(f"base name is {srcNameBase} with ext {srcNameExt} with size {srcSize} kb --> {targetName}")


    # video conversion to gif
    if os.path.exists(targetFullPath):
        if overwrite:
            os.remove(targetFullPath)
        else:
            print(f"skipping conversion to {targetExt} because {targetName} exists already")
    else:
        print(f"-- starting conversion from {srcNameExt} to {targetExt}")
        videoClip.write_gif(targetFullPath)

    # get conversion result
    if os.path.exists(targetFullPath):
        targetSize = round(os.path.getsize(targetFullPath) / 1024)
        print(f"conversion successful: {targetName} created with size {targetSize}kb ")
    else:
        print(f"Error: File {vidFullPath} does not exist")
        exit(1)
