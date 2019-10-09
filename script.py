import os
import time
import glob
from myPythonModules import other
import json 

properties = {}
class ForJson:
    def createJson(self):
        username = input("enter you windows username: ")
        properties ['username'] = username        
        properties["folder_to_track"] = "c:/users/" + properties["username"] + "/Downloads"

        properties['executable'] = {}
        properties["executable"]["folder_destination"] = properties["folder_to_track"] + "/exe/"
        properties["executable"]["extension"] = ['exe', 'msi', 'jar']

        properties["archives"] = {}
        properties["archives"]["folder_destination"] = properties["folder_to_track"] + "/archives/"
        properties["archives"]["extension"] = ['rar', 'iso', 'zip', '7z']

        properties["other"] = properties["folder_to_track"] + "/autres/"
        with open('./config.json','w') as f:
            json.dump(properties, f)


    def readJson(self):
        if(os.path.isfile("./config.json")):
            with open('./config.json', 'r') as f:
                global properties
                properties = json.load(f)
        else:
            ForJson.createJson(self)


def renameFilesIfAsExtension(folder_source, folder_destination, extension):
    os.chdir(folder_source)
    allFiles = glob.glob('*.*')
    if(extension != True):
        find = other.findStringArray(allFiles, extension, True)
        if(len(find) > 0):
            for i in range(len(find)):
                os.rename(allFiles[find[i]], folder_destination + allFiles[find[i]])
    else:
        for i in range(len(allFiles)):
            os.rename(allFiles[i], folder_destination + allFiles[i])


def findFile():
    for i in properties:
        if i != "username" and i != "folder_to_track" and i != "other":
            print(i)
            for extension in properties.get(i)["extension"]:
                renameFilesIfAsExtension(properties['folder_to_track'], properties[i]["folder_destination"], extension)    
    renameFilesIfAsExtension(
        properties['folder_to_track'], properties["other"], True)

useJson = ForJson()
useJson.readJson()
f1 = glob.glob('*.*')

try:
    while True:
        time.sleep(1)
        findFile()
except KeyboardInterrupt:
    print('exit')
