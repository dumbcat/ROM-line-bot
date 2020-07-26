import configparser
import datetime as dt
import json
import os
import re
import time
from datetime import datetime
from threading import Thread

import schedule
from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (ImageSendMessage, MessageEvent, TextMessage,
                            TextSendMessage)

from bs_rom import rom_boss

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')
channel_access_token = config.get('BASE', 'channel_access_token')
channel_secret = config.get('BASE', 'channel_secret')

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# List of line group id for send the guild war alert.
group_list = config.get('BASE', 'group_list').split(',')

# Get first day of this week.
date1 = datetime.now()
this_week_start_dt = str(date1 - dt.timedelta(days=date1.weekday())).split()[0]


@app.route("/callback", methods=['POST'])
def callback():
    """Listen all POST request from /callback

    Returns:
        str: Request status.
    """
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
    """Return the corresponding message based on the keywords entered by the user.

    Args:
        event (MessageEvent): Webhook MessageEvent entered by the user.
    """
    devent = json.loads(str(event))
    # (FOR TEST)Print group id or user id in the console.
    if re.match('@guid', event.message.text):
        for key in devent['source']:
            print(key, ':', devent['source'][key])

    # Parser user input then return image message of ruins map.
    if re.match(r'^@\d\d\u907a\u8de1', event.message.text):
        # url example:
        # https://ro.fws.tw/uploads/raid/2018-04-09/EG_2018-04-09_80.jpg
        url = 'https://ro.fws.tw/uploads/raid/' + \
            this_week_start_dt + '/EG_' + this_week_start_dt

        if event.message.text == u"@40遺跡":
            url = url + '_40.jpg'
        if event.message.text == u"@60遺跡":
            url = url + '_60.jpg'
        if event.message.text == u"@80遺跡":
            url = url + '_80.jpg'

        # https://github.com/line/line-bot-sdk-python#imagesendmessage
        message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(event.reply_token, message)

    # Parser user input then return text message of endless tower boss imformation
    if re.match('^@B.+', event.message.text):
        name = event.message.text[2:]
        boss_list = rom_boss(name)
        message = '\n'.join(boss_list)
        # https://github.com/line/line-bot-sdk-python#textsendmessage
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=message))

    # (FOR TEST)Broadcast message to all groups in group list.
    if re.match('^@廣播.+', event.message.text):
        message = event.message.text[4:]

        for group_id in group_list:
            line_bot_api.push_message(
                group_id,
                TextSendMessage(text=message)
            )
    userid = devent['source']['userId']
    try:
        profile = line_bot_api.get_profile(userid)
        print(profile.display_name, 'says:', devent['message']['text'])
    except LineBotApiError as e:
        print('Status Code:', e.status_code)
        print('Error Message:', e.error.message)
        print('Error Details:', e.error.details)


def war_alarm(mins):
    """Alert push message before the guild war starts.

    Args:
        min (string): Alarm time before the guild war starts.
    """
    for group_id in group_list:
        line_bot_api.push_message(
            group_id,
            TextSendMessage(text=u'\U0001F4A5' +
                            '公會戰即將於「' + mins + '分鐘」後開始，請參戰人員上線準備' + u'\U00100035')
        )


def war_schedule():
    """Run the schedule of the guild war alert."""
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    # Guild war alert schedule.
    schedule.every().thursday.at("12:00").do(war_alarm('60'))
    schedule.every().thursday.at("12:30").do(war_alarm('30'))
    schedule.every().sunday.at("12:00").do(war_alarm('60'))
    schedule.every().sunday.at("12:30").do(war_alarm('30'))
    t = Thread(target=war_schedule)
    t.start()

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
