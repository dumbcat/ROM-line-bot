import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    ImageSendMessage
)
# from google_sheet import gsheet
from datetime import datetime
import datetime as dt
import re
import json
import schedule
import time
from threading import Thread
from bs_rom import rom_boss

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(
    'Y20IOxeOFYFRsZiFbP432OINZhG+FYnLBzlts+QjnKJknzEk2isSAX+S0Ze0HojDDLRFeScN'
    'Ju+PSiVRVG+8GJNFQvbYyeATg8sWkpzGXGv97+AyumWmQtOqt9ZA+5aaPDkYn4ebmTJe9tjb'
    'gQNdpAdB04t89/1O/w1cDnyilFU='
)

# Channel Secret
handler = WebhookHandler('99f62b98d42e9be53921fa023b9bd754')

# 公會戰告警傳送group id
group_list = ['C22815b8fb3667c8c87886dec9e862810',
              'C4b622b292c25070df8ff03b11e35e3e9'
              ]

# 取得本周第一天的日期
date1 = datetime.now()
this_week_start_dt = str(date1 - dt.timedelta(days=date1.weekday())).split()[0]


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    devent = json.loads(str(event))
    # 測試用:回傳group id或user id於後台logs中
    if re.match('@guid', event.message.text):
        for key in devent['source']:
            print(key, ':', devent['source'][key])

    # 回傳遺跡地圖的圖片訊息
    if re.match('^@\d\d\u907a\u8de1', event.message.text):
        # 取得google試算表遺跡地圖連結
        # values_list = gsheet()
        # https://ro.fws.tw/uploads/raid/2018-04-09/EG_2018-04-09_80.jpg
        # message_error = TextSendMessage(text="抱歉，尚未有本周遺跡路線")
        url = 'https://ro.fws.tw/uploads/raid/' + \
            this_week_start_dt + '/EG_' + this_week_start_dt
        if event.message.text == u"@40遺跡":
            url = url + '_40.jpg'
        if event.message.text == u"@60遺跡":
            url = url + '_60.jpg'
        if event.message.text == u"@80遺跡":
            url = url + '_80.jpg'

        # 取得對應的遺跡地圖連結，儲存為回應訊息格式
        message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(event.reply_token, message)

    # 回傳恩德勒斯塔Boss文字訊息
    if re.match('^@B.+', event.message.text):
        name = event.message.text[2:]
        boss_list = rom_boss(name)
        message = '\n'.join(boss_list)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=message))

    # 廣播訊息至所有群組
    if re.match('^@廣播.+', event.message.text):
        message = event.message.text[4:]

        for group_id in group_list:
            line_bot_api.push_message(
                group_id,
                TextSendMessage(text=message)
            )
    print('message text:', devent['message']['text'])


# 公會戰開戰60分鐘前告警推送訊息
def war_alarm_60():
    for group_id in group_list:
        line_bot_api.push_message(
            group_id,
            TextSendMessage(text=u'\U0001F4A5' +
                            '公會戰即將於「60分鐘」後開始，請參戰人員上線準備' + u'\U00100035')
        )


# 公會戰開戰30分鐘前告警推送訊息
def war_alarm_30():
    for group_id in group_list:
        line_bot_api.push_message(
            group_id,
            TextSendMessage(text=u'\U0001F4A5' +
                            '公會戰即將於「30分鐘」後開始，請參戰人員上線準備' + u'\U00100035')
        )


# 公會戰告警排程執行器
def war_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    # 公會戰告警排程
    schedule.every().thursday.at("11:00").do(war_alarm_60)
    schedule.every().thursday.at("11:30").do(war_alarm_30)
    # schedule.every().friday.at("11:40").do(war_alarm_60)
    # schedule.every().friday.at("11:41").do(war_alarm_30)
    schedule.every().sunday.at("11:00").do(war_alarm_60)
    schedule.every().sunday.at("11:30").do(war_alarm_30)
    t = Thread(target=war_schedule)
    t.start()

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
