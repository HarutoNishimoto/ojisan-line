
import pandas as pd
from googletrans import Translator

def transReply(utterance, user_name):

	utte_split = utterance.split("|")
	for i, val in enumerate(utte_split):
		# 名前の変換
		if val == "NAME":
			utte_split[i] = user_name + "チャン" + chr(0x10008D)
		# 絵文字の付与
		if "0x" in val:
			utte_split[i] = chr(int(val, 16))
	return ''.join(utte_split)

def getResponseCandidate(utterance):
	# 読み込み
	df = pd.read_csv("QandA.csv")

	# 候補を検索
	reply_candidates = []
	for i, val in enumerate(df["keyword"].values):

		# 条件にマッチしたの発話選択
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

	if len(reply_candidates) > 0:
		return reply_candidates
	else:
		# 候補がない場合，default(*のついているもの)から選択
		return df[df["keyword"] == '*']['reply'].values

# parse前の日本語を翻訳してreturn
# ドイツ語は'de'，英語は’en’
def translateUtterance(utterance, user_name, lang="de"):
	# 条件に応じてパルス
	utte_split = utterance.split("|")
	for i, val in enumerate(utte_split):
		if "おじさん" in val:
			utte_split[i] = val.replace("おじさん", "私")
	catstetetet = ''.join(utte_split)
	# 翻訳
	translator = Translator()
	return translator.translate(catstetetet, src='ja' ,dest=lang).text




if __name__ == '__main__':

	pass

