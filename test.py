
import pandas as pd
import numpy as np
import makeReply as mr

if __name__ == '__main__':


	df = pd.read_csv("QandA.csv")

	print(df)


	candi = mr.selectKey("好きなスポーツはなに？")
	print(candi)



