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
import random
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

    def addName(user_name, thres=0.3):
        rand = random.random()
        if rand > thres:
            return user_name + "チャン" + chr(0x10008D) 
        else:
            return ""

    # read
    df = pd.read_csv("QandA.csv")

    if event.type == "message":
        utte = event.message.text
        if utte in df["keyword"].values:
            reply_candidates = df[df["keyword"] == utte]["reply"].values
            idx = np.random.randint(len(reply_candidates))
            
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text=reply_candidates[idx]),
                ]
            )
        else:
            line_bot_api.reply_message(

                event.reply_token,
                [
                    #TextSendMessage(text="{}「{}」って言ったの{}".format(addName(UN), event.message.text, chr(0x100036))),
                    TextSendMessage(text="その言葉は知らないナァ" + chr(0x10002F)),
                ]
            )

    """

    if event.type == "message":
        if "おはよう" in event.message.text:
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text='オハヨウ'+ chr(0x10002D) + addName(UN) + '今日も1日頑張ろうネ'+ chr(0x1000A4)),
                ]
            )
        if "おやすみ" in event.message.text:
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text='おやすみ'+ chr(0x10002D) + 'いい夢がみれるといいね' + addName(UN) + chr(0x10008D)),
                ]
            )
        if "ありがとう" in event.message.text:
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text="おじさん役に立ててうれしいよ" + addName(UN) + chr(0x100033)),
                ]
            )
        if ("名前" in event.message.text) and ("変" in event.message.text):
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text= addName(UN) +'，なんて呼んでほしいの'+ chr(0x100036))
                ]
            )
            global chgNameFlag
            chgNameFlag = True
        else:
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(mr.chg2Kana(addName(UN) + "「" + event.message.text + "」って言ったの" + chr(0x100036))),
                    TextSendMessage(text="おはよう，おやすみ，ありがとう，に反応するよ" + chr(0x10002F)),
                ]
            )

    """



if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
