#! python3

import os
import datetime as dt


# A function that limits the charsize of a file, foldername is < 60 char's
def fileNameLimiter(file):
    if len(file) > 60:
        return file[:60]
    return file

# A function that print a formated list of the conents of the specified folder
def printDownloadList(downloadList):

    downloadList.sort(key=lambda x: x[1]) # Sort list by Date, the second value in the tuple

    print(f'{"Naam":<60}{"Date":>60}') # Print the header of the list     
    print('-' * 120)                             

    for item in downloadList: # A for-loop that print every item of a folder, is separatedby a newline between every section with the same date(rounded by day)
        if item[1] != downloadList[downloadList.index(item)-1][1]:
            print('\n') # Prints a newline for every bundel that's created on the same date
        
        print(f'[{downloadList.index(item)}] {item[0]:<60}{item[1]:>60}')
            

downloadFolderPath = r'C:\Users\YClae\Downloads' # Folder of which contents are printed

downloadFiles = os.listdir(downloadFolderPath)
downloadList = []

# A for loop that creates a list-variable of all the items in a folder
for file in downloadFiles: 
    filePath = os.path.join(downloadFolderPath, file) # Gets folder name
    shortendFile = fileNameLimiter(file) 

    tCreationDate = dt.datetime.fromtimestamp(os.path.getctime(filePath)) # gets creation date
    downloadList.append((shortendFile, tCreationDate.strftime("%a %b %d %Y"))) # Formats creation date

printDownloadList(downloadList)

