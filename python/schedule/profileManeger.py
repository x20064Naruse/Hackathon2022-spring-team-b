from __future__ import print_function
from dataclasses import dataclass
import pandas
import datetime
import time
import os.path

# プロファイル構造体


@dataclass
class ProfileList:
    game_title: str  # ゲームタイトル
    task_name: str  # タスク名
    required_time: int  # 必要時間
    priority: int  # 優先度
    quantity: int  # 最大値

# プロファイル作成


def initProfile(game_title, task_name, required_time, priority, quantity):
    m = ProfileList(game_title, task_name, required_time, priority, quantity)


# プロファイル最適化&保存
def optimizeProfile(game_title, task_name, required_time):
    obj = loadProfile(game_title)  # プロファイル読込

    pandas.to_pickle(obj, "profiles.pkl")  # オブジェクト保存
    print('[ProfileManeger] Optimized.')

    # # プロファイルが存在しない場合はそのまま保存
    # if not obj:
    #     init = []
    #     init[0] = ProfileList(game_title, task_name,required_time, priority, quantity)
    #     pandas.to_pickle(obj, "profiles.pkl")  # オブジェクト保存
    #     print('[ProfileManeger] Initialized.')
    # # プロファイルが存在する場合は中身を更新
    # else:
    #     pandas.to_pickle(obj, "profiles.pkl")  # オブジェクト保存
    #     print('[ProfileManeger] Saved.')


# プロファイル読込
def loadProfile(game_title):
    # プロファイル読込
    # obj = pandas.read_pickle("profiles.pkl")  # オブジェクト読出
    print('[ProfileManeger] Loaded.')

    # ダミーデータ
    p = []
    p.append(ProfileList("Apex", "1Round", 30, 1, 0))
    p.append(ProfileList("Apex", "DailyChallenge", 2, 3, 5))
    p.append(ProfileList("Apex", "3V3", 10, 2, 0))
    p.append(ProfileList("Apex", "WeeklyChallenge", 10, 4, 11))
    profile = p

    return profile
