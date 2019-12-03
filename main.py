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


class userName():
    """docstring for ClassName"""
    def __init__(self):
        self.name = None
        self.chg_flag = False

    def chgName(self, newname):
        self.name = newname

    def chgNameFlag(self):
        if self.chg_flag == False:
            self.chg_flag = True
        if self.chg_flag == True:
            self.chg_flag = False




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

    UN = userName()
    profile = line_bot_api.get_profile(event.source.user_id)
    if UN.name == None:
        UN.chgName(profile.display_name)

    if event.type == "message":            
        utterance = event.message.text
        response_candidates = mr.getResponseCandidate(utterance)

        # 応答生成
        response = np.random.choice(response_candidates)
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text=mr.transReply(response, UN.name))
            ]
        )



if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
