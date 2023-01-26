from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi("51Qgh3mubaQd0zkxg+C/CVdhsQiRccoEsakdQk6U5hU7imK7DSRv8X6ZSZIXHD32I5r3RGcySdCR7scJr/BvgfE9QYBgNtbxLi5yggwMeAb3Oj2HpYJ+LIzKkB5eF0Xrtd7NSCK8nVOMfG0I7nMjcwdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("88261bd6e27022f23ab85d68341e6c01")


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()