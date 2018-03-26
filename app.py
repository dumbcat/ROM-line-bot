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
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

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
    # 連接google sheet
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'python-455eb62bc054.json', scope)

    gc = gspread.authorize(credentials)

    # 連接試算表
    sh1 = gc.open_by_key('1QQOXE_WasDzkHnQ9aXvc--eXjRso7U77lCEM7Mug8Zc')
    # 連接試算表分頁
    worksheet = sh1.worksheet("imgur")
    # 取得第二列所有元素儲存為list
    values_list = worksheet.col_values(2)

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

    if datetime.now().isocalendar()[1] != values_list[3]:
        line_bot_api.reply_message(event.reply_token, message_error)
    elif datetime.now().isocalendar()[1] == values_list[3]:
        if event.message.text == u"@40遺跡":
            line_bot_api.reply_message(event.reply_token, message40)
        if event.message.text == u"@60遺跡":
            line_bot_api.reply_message(event.reply_token, message60)
        if event.message.text == u"@80遺跡":
            line_bot_api.reply_message(event.reply_token, message80)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
