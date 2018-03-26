from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

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
    # message = TextSendMessage(text=event.message.text)
    # line_bot_api.reply_message(event.reply_token, message)
    message40 = ImageSendMessage(
        original_content_url='https://imgur.com/zbrbCfT.jpg',
        preview_image_url='https://imgur.com/zbrbCfT.jpg'
    )
    message60 = ImageSendMessage(
        original_content_url='https://imgur.com/HoJ6Izx.jpg',
        preview_image_url='https://imgur.com/HoJ6Izx.jpg'
    )
    message80 = ImageSendMessage(
        original_content_url='https://imgur.com/5liVr1z.jpg',
        preview_image_url='https://imgur.com/5liVr1z.jpg'
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
