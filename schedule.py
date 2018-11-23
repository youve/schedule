#!/usr/bin/python3

import readline
import getopt
import sys
import os
import datetime
import calendar
import parsedatetime as pdt

cal = pdt.Calendar()

# @TODO: speed up. import profile, cProfile, timeit, logging

verbose = False


if __name__ == '__main__':
    """ Parse flags.
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
        for o, a in opts:
            if o in ("-v", "--verbose"):
                verbose = True
            if o in ("-h", "--help"):
                print("The files are text files that can be edited in your",
                      "favourite text editor.")
    except:
        pass


def again():
    """Reload the files, add a task, or quit.
    """
    whatDo = input("\nDo you want to [R]eload the files, [A]dd a program to " +
                   "the schedule, or [Q]uit? R/a/q ") or 'R'
    if whatDo[0].upper() == "R":
        mainThread()
    elif whatDo[0].upper() == "A":
        addEvent()
    else:
        print("Bye!")
        exit()


def loadFiles():
    """Load all the files in the files directory.  Return a dict of files and
    their contents.  Return the length of the longest file name, for alignment.
    """
    abspath = os.path.abspath(__file__)
    fileDirectory = os.path.dirname(abspath) + '/files/'
    scheduleFiles = os.listdir(fileDirectory)
    scheduleFiles.sort()
    allFiles = {}
    colWidth = 5
    for file in scheduleFiles:
        if len(file) > colWidth:
            colWidth = len(file) 
        with open(fileDirectory + file, "r") as f:
            allFiles[file] = list(f)
    return allFiles, colWidth


# def timeFormat(when):
#     try:
#         time.strptime(when, '%j')
#         return '%j'
#     try:
#         time.strptime(when, '%F')
#         return '%F'
#     except ValueError:
#         return False

#             useFormat = ''
#             task = task.split(' ')
#             if task[0].isdigit(): # day of the year
#                 useFormat += '%j'

#     time.strptime('250 18:00','%j %H:%M')
#     time.struct_time(tm_year=1900, tm_mon=9, tm_mday=7, tm_hour=18, tm_min=0, 
#                      tm_sec=0, tm_wday=4, tm_yday=250, tm_isdst=-1)


def addEvent():
    """Add a line to an existing or new file.
    """
    allFiles = loadFiles()
    thisFile = ''
    while thisFile not in allFiles:
        thisFile = input("Which file? (Default=main) ") or 'main'
        if thisFile not in allFiles:
            createNew = input("Create new file? y/N") or "n"
            if createNew[0].upper() == "Y":
                allFiles[thisFile] = []
    thisTask = ''
    if thisFile == 'main': 
        what, when = '', ''
        while not when: 
        # @TODO bug in parsedatetime renders %j as today
            when = time.strftime('%Y %j %H:%M',cal.parse(input("When? "))[0])
        while not what:
            what = input(f"Add to main on {when}: ")
        thisTask = when + ' ' + what
        for task in allFiles['main'][:]:
            if task[0].isdigit() and thisTask < task:
                allFiles['main'].insert(allFiles['main'].index(task),thisTask)
                break
        if thisTask not in allFiles['main']:
            allFiles['main'].append(thisTask)
    else:  # thisFile != 'main'
        while not thisTask:
            thisTask = input(f"Add to {thisFile}: ")
        allFiles[thisFile].append(thisTask)
    # @TODO then save it


def orientInTime():
    """Returns today's and tomorrow's day of the year and dates, and what 
    hour it is right now.
    """
    now = datetime.datetime.now()
    thisHour = int(now.strftime('%H'))
    today = int(now.strftime('%j')) # day of the year
    todayAlt = str(datetime.date.today()) # %Y-%M-%D
    tomorrow = (today + 1)%365
    tomorrowAlt = str(datetime.date.today() + (datetime.timedelta(days=1)))
    if calendar.isleap(datetime.datetime.now().timetuple().tm_year):
        tomorrow = (today + 1)%366
    return today, todayAlt, tomorrow, tomorrowAlt, thisHour


def prepareText(allFiles, today, todayAlt, tomorrow, tomorrowAlt, thisHour, 
                colWidth):
    """Print today's and tomorrow's tasks.  'main' has tasks based on day of  
    the year.  'hour' has tasks for this hour. all lines in 'sticky' are 
    displayed.  For each other file, the line corresponding to today's date 
    modulus the number of lines in the file is displayed (e.g. an 8 line file 
    will display each line once every 8 days and start out over on line 0 on 
    1st January.)
    """
    print('\n')
    todayTasks = []
    tomorrowTasks = []
    stickyTasks = []
    hourTasks = ''
    regularTasks = []
    for file in allFiles:
        if file == 'main': 
            # Lines in 'main' start with the date, in day of the year or 
            # YYYY-MM-DD format.
            # Today's and tomorrow's events will be displayed.
            # Lines that don't begin with a number are ignored.
            for line in allFiles['main']:
                if (line.startswith(str(today) + ' ') 
                        or line.startswith(str(todayAlt) + ' ')):
                    todayTasks.append(line)
                elif (line.startswith(str(tomorrow) + ' ') 
                        or line.startswith(str(tomorrowAlt) + ' ')):
                    tomorrowTasks.append(line)
        elif file == 'hour': 
            # Lines in 'hour' represent hours, not days.  Use this for stuff  
            # that you do at the same time every day.
            if allFiles[file][thisHour%len(allFiles[file])].strip():
                hourTasks = allFiles[file][thisHour%len(allFiles[file])]
                hourTasks = hourTasks.strip().capitalize()
        elif file == 'sticky':
            for line in allFiles['sticky']:
                stickyTasks.append(line)
        else:
            if allFiles[file][today%len(allFiles[file])].strip():
                regularTasks.append("%-*s %-*s" % (colWidth, file.title(), 
                                    colWidth, allFiles[file][today%len(
                                    allFiles[file])].strip().capitalize()))
    if stickyTasks:
        print("Sticky:")
        for line in stickyTasks:
            print(line.strip())
    if hourTasks:
        print(f"\nThis hour: {thisHour}:00: {hourTasks.strip()}")
    if regularTasks:
        print("\nRegular Tasks:")
        for line in regularTasks:
            print(line.strip())
    if todayTasks:
        print("\nToday's tasks:")
        for line in todayTasks:
            print(line.strip())
    if tomorrowTasks:
        print("\nTomorrow's tasks:")
        for line in tomorrowTasks:
            print(line.strip())


def mainThread():
    """Clear the screen.  Load the files.  Print today's and tomorrow's tasks.
    Then keep going or quit.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    allFiles, colWidth = loadFiles()
    today, todayAlt, tomorrow, tomorrowAlt, thisHour = orientInTime()
    prepareText(allFiles, today, todayAlt, tomorrow, tomorrowAlt, thisHour, 
                colWidth)
    again()


mainThread()