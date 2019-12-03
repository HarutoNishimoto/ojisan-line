
import pandas as pd
import numpy as np
import makeReply as mr
import sys

if __name__ == '__main__':


	if sys.argv[1] == 'reply':
	    UN = "はると"

	    while True:
	        utterance = input('>>')
	        UUI = mr.getResponseCandidate(utterance, UN)
	        print(mr.parseResponse(UUI))


	if sys.argv[1] == 'df':


		df = pd.read_csv('QandA.csv')
		print(len(df))


