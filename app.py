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

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(
    'N0TaKleRhxpl5PihcX3X/KdT4LkqC94ac/yRbqkw9hWbIlo7Vb4Ov1nk2PHCDE4GPZrW34mnn'
    'O37H56XHIHF9q9MK7bcYzykEeRDZm5XxeLAWLya5kYPYUdG4TniM7/nAB5ar/vzyZnMsSsE7T'
    'pZkwdB04t89/1O/w1cDnyilFU='
)

# Channel Secret
handler = WebhookHandler('0113bf91055e79d3f25ea9639a1b656f')

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
        # get image link of relic map
        message40 = ImageSendMessage(
            original_content_url=values_list[0],
            preview_image_url=values_list[0]
        )
        message60 = ImageSendMessage(
            original_content_url=values_list[1],
            preview_image_url=values_list[1]
        )
        message80 = ImageSendMessage(
            original_content_url=values_list[2],
            preview_image_url=values_list[2]
        )
        message_error = TextSendMessage(text="抱歉，尚未有本周遺跡路線")
        # determine map timestamp
        if datetime.now().isocalendar()[1] != int(values_list[3]):
            line_bot_api.reply_message(event.reply_token, message_error)
        else:
            if event.message.text == u"@40遺跡":
                line_bot_api.reply_message(event.reply_token, message40)
            if event.message.text == u"@60遺跡":
                line_bot_api.reply_message(event.reply_token, message60)
            if event.message.text == u"@80遺跡":
                line_bot_api.reply_message(event.reply_token, message80)


def war_alarm():
    line_bot_api.push_message(
        'Cb8e8e11642b667670f2bd401499cc2b6',
        TextSendMessage(text='Hello World!')
    )


schedule.every(1).minutes.do(war_alarm)

while True:
    schedule.run_pending()
    time.sleep(1)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
