
import pandas as pd
import numpy as np
import makeReply as mr

if __name__ == '__main__':


    df = pd.read_csv("QandA.csv")

    print(df)

    aaa = mr.transWord(str(df.at[5, "reply"]), "はると")

    print(aaa)


    """






    utte = "こんにちは"
    reply_candidates = []
    for i, val in enumerate(df["keyword"].values):
        if val in utte:
            reply_candidates.append(str(df.at[i, "reply"]))



    reply = reply_candidates[0]
    Rlist = reply.split("|")

    for i, val in enumerate(Rlist):
        if val == "NAME":
            Rlist[i] = 0
        if "0x" in val:
            Rlist[i] = int(val, 16)







    """




