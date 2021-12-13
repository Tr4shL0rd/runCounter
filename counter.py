from sys import argv
import datetime

#fmt = "%H:%M:%S"

def exportStats():
    with open("stats.txt", "r+") as statsFile:
        statsFile.write(stats())

def getTime():
    return datetime.datetime.now().strftime("%H:%M:%S")

def getName():
    with open("name.txt", "r+") as nameFile:
        name = nameFile.read()
        return name
def getRuns():
    with open("runs.txt", "r+") as runFile:
        runs = runFile.read()
        return runs
def getStart():
    with open("startTime.txt", "r+") as startFile:
        start = startFile.readlines()[0]
        return start.replace("\n", "")
def getStop():
    with open("startTime.txt", "r+") as startFile:
        stop = startFile.readlines()[1]
        return stop.replace("\n", "")

def add():
    with open("runs.txt", "r+") as runFile:
        runs = runFile.read()
        runFile.seek(0)
        if runs == "0":
            startTime()
        newRun = int(runs) + 1
        runFile.write(str(newRun))
        print(f"{getTime()} {getName()} Run: {newRun}")

def startTime():
    with open("startTime.txt", "r+") as startFile:
        startFile.seek(0)
        startFile.truncate()
        startFile.write(f"{getTime()}")

def endTime():
    with open("startTime.txt", "a") as startFile:
        startFile.write(f"\n{getTime()}")

def timeDiff():
    td = datetime.datetime.strptime(getStop(), "%H:%M:%S") - datetime.datetime.strptime(getStart(), "%H:%M:%S")
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
    with open("runs.txt", "r+") as runFile:
        print(stats())
        exportStats()
        runFile.seek(0)
        runFile.truncate()

        runFile.write('0')
        endTime()
        return '\nReset'

def naming(Name):
    with open("name.txt", "r+") as nameFile:
        nameFile.truncate()
        nameFile.write(Name)
        reset()
        return Name

def resetName():
    with open("name.txt", "r+") as nameFile:
        nameFile.seek(0)
        nameFile.truncate()
        nameFile.write("")

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
        name = input("Please enter name of your farm: ")
        naming(name)
        exit()
    elif argv[1] == "-h": # prints help
        print("""python counter.py 
            -r:    reset 
            name:  set name ('Chonk Stomp')
            rn:    reset name
            stats: shows run stats from lastest session
            \n""",end="")
        
except IndexError:
    add()