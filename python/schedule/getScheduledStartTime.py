from __future__ import print_function
from asyncio.windows_events import NULL
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# これらのスコープを変更する場合は、token.jsonを削除
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def getScheduledStartTime():
    """
    ユーザーのカレンダーにある次の1件のイベントの開始と名前を表示
    """
    creds = None
    # token.jsonというファイルには、ユーザーのアクセストークンやリフレッシュトークンが保存され、
    # 認可フローが初めて完了したときに自動的に作成
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # 利用可能な（有効な）認証情報がない場合、ユーザーにログインを許可
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # 次の実行のために認証情報を保存
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # カレンダーAPIを呼出
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    # print('Getting the upcoming 1 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=1, singleEvents=True,
                                          orderBy='startTime').execute()  # maxResults:直近イベント件数
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('dateTime'))
        # print('StartTime:', start, '\n','EventName:', event['summary'])

        scheduledUNIX=0
        if start == None:
            #日にち取得
            uptoSecond = event['start'].get('dateTime', event['start'].get('date'))
            d = datetime.datetime.strptime(
                uptoSecond, '%Y-%m-%d')  # string -> datetime
            scheduledUNIX = d.timestamp()  # datetime -> UNIXTIME
        else:
            # UNIXTIMEへ変換
            uptoSecond = start[:start.find('+')]  # '+'よりも前を抽出
            d = datetime.datetime.strptime(
                uptoSecond, '%Y-%m-%dT%H:%M:%S')  # string -> datetime
            scheduledUNIX = d.timestamp()  # datetime -> UNIXTIME

    return scheduledUNIX
