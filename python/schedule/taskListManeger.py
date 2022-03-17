from __future__ import print_function
import collections
from dataclasses import dataclass
import datetime
import time
import os.path

import profileManeger

#チェック済みリスト
CHECKED_TASK_LIST_=[]

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

#チェックしたタスクをチェック済みリストへ入れる
def addToCheckedTaskList(profile):
    CHECKED_TASK_LIST_.append(profile)

#チェックを外したタスクをチェック済みリストから消す
def removeFromCheckedTaskList(profile):
    CHECKED_TASK_LIST_.remove(profile)

#タスクリストからチェック済みリスト中の同名タスクのチェック数だけ減らし再提案
def reduceCheckedTask(taskList):
    countList=countCheckNum()
    reducedTaskList=taskList
    for t in taskList:
        if not t.quantity<=0:
            for k in countList.keys():
                if t.task_name==k:
                    for n in countList[k]:
                        if t in reducedTaskList:
                            reducedTaskList.remove(t)
                
    return reducedTaskList

# チェック済みリスト中のタスク数計算
def countCheckNum():
    task_nameList=[]
    for c in CHECKED_TASK_LIST_:
        task_nameList.append(c.task_name)
    countList=collections.Counter(task_nameList)
    # countList=collections.Counter(CHECKED_TASK_LIST_)
    # countList=[]
    # for c in CHECKED_TASK_LIST_:
    #     if not countList:
    #         countList.append([c.task_name,])
    #     if countList[][]!=c.task_name:
    return countList
