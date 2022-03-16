from __future__ import print_function
import datetime
import time
import os.path

from getScheduledStartTime import getScheduledStartTime
from profileManeger import loadProfile
from taskListManeger import updateTaskList


def main():

    # 予定開始時刻取得 (UNIX)
    scheduledUNIX = int(getScheduledStartTime())

    # アプリ終了まで無限ループ
    while True:

        # 表示切替ON
        toggleButton = True
        if (toggleButton):

            # 現在時刻取得 (UNIX)
            nowUNIX = int(time.time())
            # print('now:', nowUNIX)
            # print('scheduled', scheduledUNIX)

            # 残り時間計算(sec)
            remainSec = scheduledUNIX-nowUNIX
            print(remainSec)

            # チェック入力
            checkBoxListener = True
            if (checkBoxListener):
                # get pctime
                checkboxUNIX = int(time.time())
            else:
                print('checkBoxListener == False')

            # Update List
            game_title = "Apex"
            updatedTaskList = updateTaskList(remainSec, game_title)

            # Show List
            print(updatedTaskList)

        # 表示切替OFF
        else:
            print('toggleButton == False')

        # 1sec待つ
        time.sleep(1)


if __name__ == '__main__':
    main()
