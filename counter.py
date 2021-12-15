from sys import argv
import datetime
from os import listdir
from os.path import isfile, join
from typing import Iterable

#    TODO
# * save files
# * load files

fmt = "%H:%M:%S"
statsPath     = "dataFiles/stats.txt"
namePath      = "dataFiles/name.txt"
runsPath      = "dataFiles/runs.txt"
timePath      = "dataFiles/startTime.txt"
profilesPath  = "dataFiles/profiles/"

def exportStats():
    with open(statsPath, "r+") as statsFile:
        statsFile.write(stats())

def getStartTime():
    with open(timePath, "r+") as startFile:
        start = startFile.readlines()[0]
        return start.replace("\n", "")
def getTime():
    return datetime.datetime.now().strftime(fmt)

def getName():
    with open(namePath, "r+") as nameFile:
        name = nameFile.read()
        return name
def getRuns():
    with open(runsPath, "r+") as runFile:
        runs = runFile.read()
        return runs
def getStart():
    with open(timePath, "r+") as startFile:
        start = startFile.readlines()[0]
        return start.replace("\n", "")
def getStop():
    with open(timePath, "r+") as startFile:
        stop = startFile.readlines()[1]
        return stop.replace("\n", "")
def getProfiles():
    profiles = [f for f in listdir(profilesPath)
                if isfile(join(profilesPath,f))]
    return profiles

def add():
    with open(runsPath, "r+") as runFile:
        runs = runFile.read()
        runFile.seek(0)
        if runs == "0":
            startTime()
        newRun = int(runs) + 1
        runFile.write(str(newRun))
        print(f"{getTime()} {getName()} Run: {newRun}")

def startTime():
    with open(timePath, "r+") as startFile:
        startFile.seek(0)
        startFile.truncate()
        startFile.write(f"{getTime()}")

def endTime():
    with open(timePath, "a") as startFile:
        startFile.write(f"\n{getTime()}")

def timeDiff():
    td = datetime.datetime.strptime(getStop(), fmt) - datetime.datetime.strptime(getStart(), fmt)
    return td

def stats():
    #print(timeDiff().total_seconds())
    timePerRun = int(timeDiff().total_seconds())/int(getRuns())
    text = f"Run Start: {getStart()}\nRun  Stop: {getStop()}\n"
    if getName() != "":
        text += f"Time Spent Farming {getName().capitalize()}: {timeDiff()}"
    else:
        text += f"Time Used: {timeDiff()}"
    text += f"\nRuns: {getRuns()}"
    text += f"\nTime Spent per Run: {timePerRun:.2f} seconds"
    #print(text)
    return text

def reset():
    with open(runsPath, "r+") as runFile:
        print(stats())
        exportStats()
        runFile.seek(0)
        runFile.truncate()

        runFile.write('0')
        endTime()
        return '\nReset'

def naming(Name):
    with open(namePath, "r+") as nameFile:
        nameFile.truncate()
        nameFile.write(Name)
        reset()
        return Name

def resetName():
    with open(namePath, "r+") as nameFile:
        nameFile.seek(0)
        nameFile.truncate()
        nameFile.write("")

def readFile(fileName):
    with open(fileName, "r") as f:
        lines = f.readlines()
    for l in lines:
        print(l.replace("\n",""))
        #return f.readlines()
        

def dataSave(saveFileName, runStart, runs, name):
    runStart = getStartTime()
    runs     = getRuns()
    name     = getName()
    with open(f"{profilesPath}{saveFileName}.txt", "a+") as statsFile:
        statsFile.seek(0)
        statsFile.write("")
        statsFile.write(f"{runStart}\n{runs}\n{name}")

def loadSave():
    profiles = getProfiles()
    i = 0
    saves = {}
    for p in iter(profiles):
        i += 1
        fileName,_,_ = p.partition(".")
        saves[i] = fileName 
    #print(sorted(saves.items(), reverse=True))
    for index, name in sorted(saves.items(),reverse=True):
        print(f"{index}: {name}")
    try:
        choice = int(input("enter index of saveFile: "))
        print() # Line Seperator for input and output of file

    except ValueError:
        print("lol ValueError!\n")
        loadSave()
    if choice in saves.keys():
        print(saves[choice])
        readFile(f"{profilesPath}{saves[choice]}.txt")

    else:
        print("Save File not found or corrupt!")
        print(f"Default saveFile Path: {profilesPath}")

try:
    if argv[1] == '-r': # stops the session
        print(reset())
    elif argv[1] == "name": # sets the name
        naming(argv[2])
    elif argv[1] == "rn": # resets the name
        resetName()
    elif argv[1] == "stats": # prints stats
        stats()
    elif argv[1] == "-w": # setup Wizard
        print("Welcome to the setup Wizard")
        name    = input("Please enter name of your farm: ")
        saveName = name.lower().replace(" ", "")#input("Save File Name: ").lower().replace(" ", "")
        naming(name)
        exit()
    elif argv[1] == "save":
        dataSave(input("save file name: "), getStartTime(), getRuns(), getName())
    elif argv[1] == "-h": # prints help
        print("""python counter.py 
            -r:    reset 
            name:  set name ('Chonk Stomp')
            rn:    reset name
            stats: shows run stats from lastest session
            \n""",end="")
        
except IndexError:
    #add()
    loadSave()
    #dataSave(saveName, getStartTime(), getRuns(), getName())