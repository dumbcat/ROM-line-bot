from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(
    'N0TaKleRhxpl5PihcX3X/KdT4LkqC94ac/yRbqkw9hWbIlo7Vb4Ov1nk2PHCDE4GPZrW34mnnO37H56XHIHF9q9MK7bcYzykEeRDZm5XxeLAWLya5kYPYUdG4TniM7/nAB5ar/vzyZnMsSsE7TpZkwdB04t89/1O/w1cDnyilFU=')

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
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('python-455eb62bc054.json', scope)

    gc = gspread.authorize(credentials)

    sh1 = gc.open_by_key('1QQOXE_WasDzkHnQ9aXvc--eXjRso7U77lCEM7Mug8Zc')
    worksheet = sh1.worksheet("imgur")
    values_list = worksheet.col_values(2)
    print(values_list)
    # message = TextSendMessage(text=event.message.text)
    # line_bot_api.reply_message(event.reply_token, message)
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

    if event.message.text == u"@40遺跡":
        line_bot_api.reply_message(event.reply_token, message40)
    if event.message.text == u"@60遺跡":
        line_bot_api.reply_message(event.reply_token, message60)
    if event.message.text == u"@80遺跡":
        line_bot_api.reply_message(event.reply_token, message80)
        # line_bot_api.reply_message(event.reply_token, TextSendMessage(u"2017年底終於有人知道==不要加空格"))
    # else:
        # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))

    # line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
