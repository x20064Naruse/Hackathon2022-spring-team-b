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


# ゲームタイトルを指定してプロファイル保存
def saveProfile(updateRequestProfile,game_title):
    # loadedProfiles = loadProfile(game_title)  # プロファイル読込

    # # プロファイル書換
    # for uP in updateRequestProfiles:
    #     for lP in loadedProfiles:
    #         if uP.game_title == lP.game_title and uP.task_name == lP.task_name:
    #             # 既存のプロファイルは更新
    #             lP.required_time = uP.required_time
    #             lP.priority = uP.priority
    #             lP.quantity = uP.quantity
    #         else:
    #             # 新規のプロファイルは追加
    #             lP.append(uP)

    newProfile = updateRequestProfile
    filename = game_title + '.pkl'
    pandas.to_pickle(newProfile, filename)  # プロファイル保存
    print('[ProfileManeger] Saved to',filename)

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


# # プロファイル最適化&保存（保留）
# def optimizeProfile(game_title, task_name, required_time):
#     obj = loadProfile(game_title)  # プロファイル読込

#     pandas.to_pickle(obj, "profiles.pkl")  # オブジェクト保存
#     print('[ProfileManeger] Optimized.')

#     # # プロファイルが存在しない場合はそのまま保存
#     # if not obj:
#     #     init = []
#     #     init[0] = ProfileList(game_title, task_name,required_time, priority, quantity)
#     #     pandas.to_pickle(obj, "profiles.pkl")  # オブジェクト保存
#     #     print('[ProfileManeger] Initialized.')
#     # # プロファイルが存在する場合は中身を更新
#     # else:
#     #     pandas.to_pickle(obj, "profiles.pkl")  # オブジェクト保存
#     #     print('[ProfileManeger] Saved.')


# ゲームタイトルを指定してプロファイル読込
def loadProfile(game_title):
    filename='./' + game_title+'.pkl'
    if not os.path.exists(filename):
        print('[ProfileManeger]',filename,'is not found.')

    loadedProfiles = pandas.read_pickle(filename)  # オブジェクト読出
    print('[ProfileManeger] Loaded from',filename)

    return loadedProfiles
