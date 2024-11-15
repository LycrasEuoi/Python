##! python3

import os
import datetime as dt

# Truncate the filename to a maximum of 60 characters
def truncateFileName(file):
    return file[:60] if len(file) > 60 else file

# Prints a formatted list of files and their creation dates from the specified folder
def printDownloadList(downloadList):
    # Check if the list is empty and provide feedback if no files are found
    if not downloadList:
        print("No files found in the specified folder.")
        return

    # Sort the list by creation date (second element in tuple)
    downloadList.sort(key=lambda x: x[1])

    # Print table header
    print(f'{"Naam":<60}{"Date":>30}')
    print('-' * 100)

    # Track the previous date to group files by the same creation day
    previous_date = None

    # Enumerate through the sorted download list for efficient index access
    for index, item in enumerate(downloadList):
        # Print a newline if the current file's date is different from the previous one
        if item[1] != previous_date:
            print('\n')
            previous_date = item[1]
        
        # Print each file's index, truncated name, and formatted creation date
        print(f'[{index}] {item[0]:<60}{item[1]:>30}')

# Define the path to the downloads folder
# `os.path.expanduser` ensures compatibility with different user environments
DOWNLOAD_FOLDER_PATH = os.path.expanduser(r'C:\Users\YClae\Downloads')

# List all files in the specified downloads folder
downloadFiles = os.listdir(DOWNLOAD_FOLDER_PATH)
downloadList = []

# Create a list of tuples containing truncated filenames and their formatted creation dates
for file in downloadFiles: 
    filePath = os.path.join(DOWNLOAD_FOLDER_PATH, file)  # Construct full file path
    shortendFile = truncateFileName(file)  # Truncate the filename if necessary

    # Get the file's creation date and format it as a readable string
    creation_date = dt.datetime.fromtimestamp(os.path.getctime(filePath))
    downloadList.append((shortendFile, creation_date.strftime("%a %b %d %Y")))

# Print the formatted list of downloads
printDownloadList(downloadList)

