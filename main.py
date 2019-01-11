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
import os
import makeReply as mr
import numpy as np
import pandas as pd

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


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

"""
# オウム返し
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
"""

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    profile = line_bot_api.get_profile(event.source.user_id)
    UN = profile.display_name

    if event.type == "message":
        utterance = event.message.text
        reply_candidates = mr.selectKey(utterance)

        if len(reply_candidates) > 0:
            idx = np.random.randint(len(reply_candidates))
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text=mr.transReply(reply_candidates[idx], mr.addName(UN))),
                ]
            )
        else:
            line_bot_api.reply_message(

                event.reply_token,
                [
                    TextSendMessage(text="{}「{}」って言ったの{}".format(mr.addName(UN), event.message.text, chr(0x100036))),
                    TextSendMessage(text="その言葉は知らないナァ" + chr(0x10002F)),
                ]
            )


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
