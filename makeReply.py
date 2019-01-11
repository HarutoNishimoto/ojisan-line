
import pandas as pd
import random


def addName(user_name, thres=0.3):
	rand = random.random()
	if rand > thres:
		return user_name + "チャン" + chr(0x10008D) 
	else:
		return ""

def transReply(utterance, user_name):

	Ulist = utterance.split("|")
	for i, val in enumerate(Ulist):
		if val == "NAME":
			Ulist[i] = user_name
		if "0x" in val:
			Ulist[i] = chr(int(val, 16))

	Ulist = ''.join(Ulist)

	return Ulist

def selectKey(utterance):
	# read
	df = pd.read_csv("QandA.csv")

	reply_candidates = []
	for i, val in enumerate(df["keyword"].values):
		key_alias = val.split("|")
		for key in key_alias:
			if key in utterance:
				reply_candidates.append(str(df.at[i, "reply"]))

		key_alias = val.split("&")
		for key in key_alias:
			chk_all_in = True
			if key not in utterance:
				chk_all_in = False
				break
		if chk_all_in:
			reply_candidates.append(str(df.at[i, "reply"]))




	return reply_candidates

if __name__ == '__main__':

	pass

