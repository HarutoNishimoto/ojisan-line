
import pandas as pd
import numpy as np

if __name__ == '__main__':


	df = pd.read_csv("QandA.csv")


	if "こんばんは" in df["keyword"].values:
		print("sssss")

		reply_candidates = df[df["keyword"] == "こんばんは"]["reply"].values
		idx = np.random.randint(len(reply_candidates))
		print(reply_candidates[idx])







