import os
import time

downloadFolderPath = r'C:\Users\YClae\Downloads'

downloadFiles = os.listdir(downloadFolderPath)
downloadList = []

for file in downloadFiles:
    
    filePath = os.path.join(downloadFolderPath, file)
    timeStampCreationDate = time.ctime(os.path.getctime(filePath))
    downloadList.append((file, timeStampCreationDate))

downloadList.sort(key=lambda x: x[1])

print(f'{"Naam":<60}{"Date":>60}')
print('-' * 120)

for item in downloadList:
    print(f'{item[0]:<60}{item[1]:>60}')

#print(downloadListTotal)