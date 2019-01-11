
import pandas as pd
import random
from googletrans import Translator

# 日本語を翻訳してreturn
def translation(utterance, lang="en"):
	# 翻訳ミスの防止
	if "おじさん" in utterance:
		utterance = utterance.replace("おじさん", "私")
	translator = Translator()
	return translator.translate(utterance, src='ja' ,dest=lang).text

def addName(user_name, thres=0.3):
	rand = random.random()
	if rand > thres:
		return user_name + "チャン" + chr(0x10008D) 
	else:
		return user_name

def transReply(utterance, user_name):

	Ulist = utterance.split("|")
	for i, val in enumerate(Ulist):
		if val == "NAME":
			Ulist[i] = user_name
		if "0x" in val:
			Ulist[i] = chr(int(val, 16))

	Ulist = ''.join(Ulist)

	return Ulist

# NAMEや絵文字の特殊文字を取り除いてreturn
def transReplyForForeign(utterance, user_name):

	Ulist = utterance.split("|")
	for i, val in enumerate(Ulist):
		if val == "NAME":
			Ulist[i] = ""
		if "0x" in val:
			Ulist[i] = ""

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

