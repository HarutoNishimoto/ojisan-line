
import pandas as pd
import numpy as np
import makeReply as mr

if __name__ == '__main__':
    UN = "はると"

    while True:
        utterance = input('>>')

        reply_candidates = mr.getResponseCandidate(utterance)
        print(reply_candidates)

        utte = np.random.choice(reply_candidates)
        print(mr.transReply(utte, UN))



