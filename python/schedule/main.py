from __future__ import print_function
import datetime
import time
import os.path

from getScheduledStartTime import getScheduledStartTime
from profileManeger import loadProfile
from profileManeger import optimizeProfile
from getTaskList import getTaskList
from taskListManeger import updateTaskList


def main():

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
