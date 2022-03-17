from __future__ import print_function
import datetime
import time
import os.path

from getScheduledStartTime import getScheduledStartTime
from profileManeger import loadProfile
from taskListManeger import updateTaskList

remainSec = 0
# スケジュール提案
def getTaskList(game_title):

    # 予定開始時刻取得 (UNIX)
    scheduledUNIX = int(getScheduledStartTime())

    # 現在時刻取得 (UNIX)
    nowUNIX = int(time.time())
    # print('now:', nowUNIX)
    # print('scheduled:', scheduledUNIX)

    # 残り時間計算(sec)
    remainSec = scheduledUNIX-nowUNIX
    
    # print(remainSec, 'seconds left')
    if remainSec > 0:
        print(datetime.timedelta(seconds=remainSec))
        remainTime = datetime.timedelta(seconds=remainSec)
    else:
        remainTime = "!!予定が進行中です!!"

    # # チェック入力
    # checkBoxListener = True
    # if checkBoxListener:
    #     # 必要時間最適化
    #     # 現在時刻取得 (UNIX)
    #     checkboxUNIX = int(time.time())
    #     # タスク名取得
    #     task_name = "3V3"
    #     required_time = 5
    #     optimizeProfile(game_title, task_name, required_time)
    # else:
    #     print('checkBoxListener == False')

    # # Update List
    # updatedTaskList = updateTaskList(remainSec, game_title)
    TaskList = updateTaskList(remainSec, game_title)

    # # Show List
    # if not updatedTaskList:
    #     print('リストはありません.\n')
    # else:
    #     for l in updatedTaskList:
    #         print('-', l.task_name, '[', l.required_time, 'm]')
    #     print('\n')

    return TaskList, remainTime