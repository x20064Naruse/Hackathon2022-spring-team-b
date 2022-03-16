from __future__ import print_function
from dataclasses import dataclass
import datetime
import time
import os.path

import profileManeger


def updateTaskList(remaining_time, game_title):

    newTaskList = []

    if remaining_time > 0:
        profile = profileManeger.loadProfile(game_title)

        # 優先度順にバブルソート
        for i in range(len(profile)-1):
            if profile[i].priority > profile[i+1].priority:
                swap = profile[i]
                profile[i] = profile[i+1]
                profile[i+1] = swap

        for pr in profile:
            loop = 0  # 繰り返し回数

            # タスクの最大数が0(無限)の場合はとりあえず上限10回だけ提案する
            if pr.quantity <= 0:
                loop = 10
            # タスクの最大数が1以上の場合はできるだけ最大数分提案する
            else:
                loop = pr.quantity

            for num in range(loop):
                # 現在のタスクが残り時間でできない場合
                if remaining_time < pr.required_time*60:
                    break
                # 現在のタスクが残り時間でできる場合
                else:
                    newTaskList.append(pr)  # 要素追加
                    remaining_time -= pr.required_time*60  # 残り時間減少
                    continue

    else:
        print('!!予定が進行中です!!')

    return newTaskList
