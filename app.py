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
from google_sheet import gsheet
from datetime import datetime
import re
import json
import schedule
import time
from threading import Thread
from bs_rom import rom_boss

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(
    'GJVhWFfLZiLXDpWJZDTNDzaN02icZ0SVldCAejfoe5a7SVVd5u6dkoFPcLQLx1QaDLRFeScN'
    'Ju+PSiVRVG+8GJNFQvbYyeATg8sWkpzGXGsuueNDC+zt1T6rT9sG7bgu9XdBuOSTY4uRXSXd'
    'eV0YSwdB04t89/1O/w1cDnyilFU='
)

# Channel Secret
handler = WebhookHandler('99f62b98d42e9be53921fa023b9bd754')

# group list
group_list = ['C22815b8fb3667c8c87886dec9e862810',
              'C4b622b292c25070df8ff03b11e35e3e9'
              ]


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
    # response group id或user id
    if re.match('@event', event.message.text):
        devent = json.loads(str(event))
        print(devent['source'])
    # response relic map
    if re.match('^@\d\d\u907a\u8de1', event.message.text):
        # get google sheet data
        values_list = gsheet()

        message_error = TextSendMessage(text="抱歉，尚未有本周遺跡路線")
        # determine map timestamp
        if datetime.now().isocalendar()[1] != int(values_list[3]):
            line_bot_api.reply_message(event.reply_token, message_error)
        else:
            if event.message.text == u"@40遺跡":
                map_no = 0
            if event.message.text == u"@60遺跡":
                map_no = 1
            if event.message.text == u"@80遺跡":
                map_no = 2
            # get image link of relic map
            message = ImageSendMessage(
                original_content_url=values_list[map_no],
                preview_image_url=values_list[map_no]
            )
            line_bot_api.reply_message(event.reply_token, message)
    if re.match('^@B.+', event.message.text):
        name = event.message.text[2:]
        boss_list = rom_boss(name)
        message = '%0D%0A'.join(boss_list)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=message))


# guild wars 60mins alarm
def war_alarm_60():
    for group_id in group_list:
        line_bot_api.push_message(
            group_id,
            TextSendMessage(text=u'\U0001F4A5' +
                            '公會戰即將於「60分鐘」後開始，請參戰人員上線準備' + u'\U00100035')
        )


# guild wars 30mins alarm
def war_alarm_30():
    for group_id in group_list:
        line_bot_api.push_message(
            group_id,
            TextSendMessage(text=u'\U0001F4A5' +
                            '公會戰即將於「60分鐘」後開始，請參戰人員上線準備' + u'\U00100035')
        )


# war alarm schedule runner
def war_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    # war alarm schedule
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
