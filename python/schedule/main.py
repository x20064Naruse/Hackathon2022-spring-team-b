from __future__ import print_function
import datetime
import time
import os.path

from getScheduledStartTime import getScheduledStartTime
from profileManeger import loadProfile
from getTaskList import getTaskList
from profileManeger import ProfileList
from profileManeger import saveProfile
from profileManeger import getGameTitleList
from taskListManeger import updateTaskList


def main():

    titleList=getGameTitleList()
    for t in titleList:
        print(t)

    game_title = "Apex"
    l=[]
    l.append(ProfileList(game_title, "1Round", 30, 1, 0))
    l.append(ProfileList(game_title, "DailyChallenge", 2, 3, 5))
    l.append(ProfileList(game_title, "3V3", 10, 2, 0))
    l.append(ProfileList(game_title, "WeeklyChallenge", 10, 4, 11))
    saveProfile(l,game_title)

    game_title = "MineCraft"
    l=[]
    l.append(ProfileList(game_title, "1", 30, 1, 0))
    l.append(ProfileList(game_title, "2", 2, 3, 5))
    l.append(ProfileList(game_title, "3", 10, 2, 0))
    l.append(ProfileList(game_title, "4", 10, 4, 11))
    saveProfile(l,game_title)

    loadProfiles=loadProfile(game_title="Apex")
    for l in loadProfiles:
        print(l)

    loadProfiles=loadProfile(game_title="MineCraft")
    for l in loadProfiles:
        print(l)

    game_title = "Apex"

    # Update List
    updatedTaskList = getTaskList(game_title)

    # Show List
    if not updatedTaskList:
        print('リストはありません.\n')
    else:
        for l in updatedTaskList:
            print('-', l.task_name, '[', l.required_time, 'm]')
        print('\n')


if __name__ == '__main__':
    main()
