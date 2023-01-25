from moviepy.editor import VideoFileClip
import os
import myUtilsModule
import sys

# start script execution
scriptStartTime = myUtilsModule.startExecution()

# get CLI arguments


# set parameters
#vidFolderPath = "/home/primaben/Downloads"
vidFolderPath = sys.argv[1]
#srcName = "test1.webm"
srcName = sys.argv[2]
startSec = sys.argv[3]
endSec = sys.argv[4]
overwrite = sys.argv[5]
targetExt = "gif"

# convert srcFile to target extension
myUtilsModule.convertToGif(vidFolderPath, srcName, targetExt, startSec, endSec, overwrite)

# parameter preparation
vidFullPath = os.path.join(vidFolderPath, srcName)
videoClip = VideoFileClip(vidFullPath)
#
# vidDuration = videoClip.duration
# print(f"duration: {vidDuration} ")

# clip1 = VideoFileClip(vidFullPath).subclip(10, 15)
# clip1.write_videofile("shortVersion.webm")

# end script execution
duration = myUtilsModule.endExecution(scriptStartTime)
