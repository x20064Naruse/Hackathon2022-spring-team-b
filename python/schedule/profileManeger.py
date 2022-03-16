from __future__ import print_function
from dataclasses import dataclass
import datetime
import time
import os.path


@dataclass
class ProfileList:
    game_title: str
    task_name: str
    required_time: int
    priority: int
    quantity: int

# プロファイル作成


def makeProfile(game_title, task_name, required_time, priority, quantity):
    m = ProfileList(game_title, task_name, required_time, priority, quantity)


# プロファイル保存
def saveProfile():
    print('Saved.')


# プロファイル読込
def loadProfile(game_title):
    p = []
    p.append(ProfileList("Apex", "1Round", 30, 1, 0))
    p.append(ProfileList("Apex", "DailyChallenge", 2, 3, 5))
    p.append(ProfileList("Apex", "3V3", 10, 2, 0))
    p.append(ProfileList("Apex", "WeeklyChallenge", 10, 4, 11))
    profile = p
    return profile
