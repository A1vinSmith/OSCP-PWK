# !/bin/python3

import os
import sys
import zipfile

# Verbose checking
if len(sys.argv) == 2:
    try:
        filename = os.path.isfile(sys.argv[1]) and sys.argv[1]
    except ValueError:
        print("File could not be resolved. e.g. /home/user/xxx.zip")
        sys.exit()
else:
    print("Invalid amount of arguments.")
    print("Syntax: python3 extractAll.py <FilePath>")
    sys.exit()

initExtractPath = filename + "_extracted"
os.makedirs(initExtractPath)
with zipfile.ZipFile(filename, 'r') as main_zip:
    main_zip.extractall(initExtractPath)

currentpath = os.getcwd()
pathtoextract = currentpath + "/extracted"
os.makedirs(pathtoextract)


def getAll():
    Files = os.listdir(initExtractPath)
    mainpath = initExtractPath
    for file in Files:
        filepath = (mainpath + '/' + file)
        if filepath.endswith('.zip'):
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(pathtoextract)

    files_getAll = os.listdir(pathtoextract)
    counter = 0
    for files in files_getAll:
        counter += 1
    return counter


def question2():
    Files = os.listdir(pathtoextract)
    mainpath = pathtoextract
    for files in Files:
        filepath = (mainpath + '/' + files)
        cmd = 'exiftool ' + filepath + ' >> exiftool.txt'
        os.system(cmd)

    with open(currentpath + '/exiftool.txt', 'r') as f:
        metadata = f.readlines()
        counter = 0
        for line in metadata:
            if "Version" in line and "1.1" in line:
                counter += 1
        return counter


def question3():
    Files = os.listdir(pathtoextract)
    mainpath = pathtoextract
    for files in Files:
        filepath = (mainpath + '/' + files)
        try:
            with open(filepath, 'r') as f:
                data = f.read()
                if "password" in data:
                    password_found = filepath
                    return password_found
        except:
            continue


print("Files Extracted: ", getAll())
print("Files containing Version: 1.1 in their metadata: ", question2())
print("Password Found in :", question3())
