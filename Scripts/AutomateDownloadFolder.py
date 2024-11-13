#! python3

import os
import time
import datetime as dt

def fileNameLimiter(file):
    if len(file) > 60:
        return file[:60]
    return file

def printDownloadList(downloadList):

    downloadList.sort(key=lambda x: x[1])       # Sort list by Date, the second value in the tuple

    print(f'{"Naam":<60}{"Date":>60}')
    print('-' * 120)                            # Print the header of the list      

    for item in downloadList:
        if item[1] != downloadList[downloadList.index(item)-1][1]: # Bundels files of same creation date
            print('\n')
            print(f'{downloadList.index(item)} {item[0]:<60}{item[1]:>60}')
        else:
            print(f'{downloadList.index(item)} {item[0]:<60}{item[1]:>60}')

downloadFolderPath = r'C:\Users\YClae\Downloads'

downloadFiles = os.listdir(downloadFolderPath)
downloadList = []

for file in downloadFiles:
    filePath = os.path.join(downloadFolderPath, file)
    tCreationDate = dt.datetime.fromtimestamp(os.path.getctime(filePath))
    
    shortendFile = fileNameLimiter(file)
    downloadList.append((shortendFile, tCreationDate.strftime("%a %b %d %Y")))

printDownloadList(downloadList)

