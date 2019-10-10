import os
import time
import glob
import json
import platform
import locale
import datetime
from zipfile import ZipFile

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
        properties["old"] = properties["folder_to_track"] + "/vieux/"
        with open('./config.json','w') as f:
            json.dump(properties, f)


    def readJson(self):
        if(os.path.isfile("./config.json")):
            with open('./config.json', 'r') as f: 
                global properties
                properties = json.load(f)
        else:
            ForJson().createJson()

class compress():
    def findOldestFile(self):
        files = compress.get_all_file_paths(self, properties["folder_to_track"])
        biggest = os.path.getctime(files[0])
        for i in range(1,len(files)):
            if os.path.getctime(files[i]) > biggest:
                biggest = os.path.getctime(files[i])
        month = time.strftime('%m', time.gmtime(biggest))
        return month

    def get_all_file_paths(self,directory):
            # initializing empty file paths list
        file_paths = []

        # crawling through directory and subdirectories
        for root, directories, files in os.walk(directory):
            for filename in files:
                # join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)
        # returning all file paths
        return file_paths


    def compress(self):
        files = compress().get_all_file_paths(properties["folder_to_track"])
        actual_date = datetime.date.today()
        past_month = 12 if actual_date.month == 1 else actual_date.month -1
        if past_month == compress().findOldestFile():
            print(actual_date.month)
            with ZipFile(properties['old'] + actual_date.month + "-" +actual_date.year + ".zip", "a") as zip:
                for file in files:
                    zip.write(file)




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
        if i != "username" and i != "folder_to_track" and i != "other" and i!= "old":
            for extension in properties.get(i)["extension"]:
                renameFilesIfAsExtension(properties['folder_to_track'], properties[i]["folder_destination"], extension)    
    renameFilesIfAsExtension(
        properties['folder_to_track'], properties["other"], True)

ForJson().readJson()
f1 = glob.glob('*.*')
try:
    while True:
        time.sleep(1)
        compress().compress()
        findFile()
except KeyboardInterrupt:
    print('exit')
