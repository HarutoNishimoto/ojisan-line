
import pandas as pd
import numpy as np
import makeReply as mr

if __name__ == '__main__':


    df = pd.read_csv("QandA.csv")


    utterance = "ああああ"

    UN = "はると"

    if True:
        reply_candidates = mr.selectKey(utterance)
        print(reply_candidates)

        if len(reply_candidates) > 0:
            idx = np.random.randint(len(reply_candidates))

            print(mr.transReply(reply_candidates[idx], mr.addName(UN)))

        else:

            print("該当なし")



