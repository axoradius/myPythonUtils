"""
creates a caption for every image in a folder and writes the output to a file
"""

import os

# set variables
outputFileName = "catalog_caption.txt"
sourcePath = "/Users/bvds/Pictures"

def listAllFiles(srcPath, listExtensions=["jpg","jpeg","png"]):
    result = []
    if os.path.isdir(srcPath):
        allFiles = os.listdir(srcPath)
        for ext in listExtensions:
            for f in allFiles:
                if f.endswith(ext):
                    print(f"{f} has a valid extension {ext}")
                    result.append(f)
    else:
        print(f"ERROR: {srcPath} is not a valid path")
    return result

if __name__ == "__main__":
    print(f"::: start :::")
    res = listAllFiles(sourcePath)
    nbrFound = len(res)
    print(f"nbr found is {nbrFound}")