import os
import time
import glob
import json
import platform
import locale

def findStringInArray(array, string, multiple = False):
    if multiple:
        r = []
    else:
        r = -1
    for i in range(len(array)):
        if(array[i].find(string) != -1):
            if multiple:
                r.append(i)
            else:
                r = i
    return r




properties = {}
class ForJson:
    def createJson(self):
        local_language = locale.getdefaultlocale()[0]
        print(local_language)
        username = input("enter your {} username: ".format(platform.system()))
        properties ['username'] = username
        if platform.system() == "Windows":
            properties["folder_to_track"] = "c:/users/" + properties["username"] + "/Downloads"
        elif platform.system() == "Linux":
            if local_language.find('en') != -1:
                properties["folder_to_track"] = "/home/" + properties["username"] + "/Downloads"
            elif local_language.find('fr') != -1:
                properties["folder_to_track"] = "/home/"+ properties["username"]+"/Téléchargements"
        properties['executable'] = {}
        properties["executable"]["folder_destination"] = properties["folder_to_track"] + "/exe/"
        properties["executable"]["extension"] = ['exe', 'msi', 'jar', "run"]

        properties["archives"] = {}
        properties["archives"]["folder_destination"] = properties["folder_to_track"] + "/archives/"
        properties["archives"]["extension"] = ['rar', 'iso', 'zip', '7z', "tar" , "tar.bz2"]

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
        find = findStringInArray(allFiles, extension, True)
        if(len(find) > 0):
            for i in range(len(find)):
                os.rename(allFiles[find[i]], folder_destination + allFiles[find[i]])
    else:
        for i in range(len(allFiles)):
            os.rename(allFiles[i], folder_destination + allFiles[i])


def findFile():
    for i in properties:
        if i != "username" and i != "folder_to_track" and i != "other":
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
