
import pandas as pd
import numpy as np
from googletrans import Translator


class userUtteranceInfo():
	"""docstring for userUtteranceInfo"""
	def __init__(self, keyword, response_before_parse):
		self.key = keyword
		self.res_b_p = response_before_parse
		self.name = None
		self.food = None
		self.place = None
		self.sport = None

		self.slot_name_list = ['FOOD','PLACE','SPORT']
		for s in self.slot_name_list:
			if s in self.res_b_p:
				self.addInfo(self.key, s)

	def addInfo(self, keyword, word_type):
		if word_type == 'NAME':
			self.name = keyword
		elif word_type == 'FOOD':
			self.food = keyword
		elif word_type == 'PLACE':
			self.place = keyword
		elif word_type == 'SPORT':
			self.sport = keyword
		else:
			pass

	def getSlotValue(self, word_type):
		if word_type == 'NAME':
			slotval = self.name
		elif word_type == 'FOOD':
			slotval = self.food
		elif word_type == 'PLACE':
			slotval = self.place
		elif word_type == 'SPORT':
			slotval = self.sport
		else:
			pass

		if slotval == None:
			return ''
		else:
			return slotval


def parseResponse(user_utte_info):

	utte_split = user_utte_info.res_b_p.split('|')
	for i, val in enumerate(utte_split):
		# 名前の変換
		if val == 'NAME':
			utte_split[i] = user_utte_info.name + 'チャン' + chr(0x10008D)
		# 絵文字の付与
		if '0x' in val:
			utte_split[i] = chr(int(val, 16))
		# SLOTの変換
		if val in user_utte_info.slot_name_list:
			utte_split[i] = user_utte_info.getSlotValue(val)
	return ''.join(utte_split)

def getResponseCandidate(utterance, user_name):
	# 読み込み
	df = pd.read_csv('QandA.csv')

	# 候補を検索
	response_candidates = []
	key = None
	for i, val in enumerate(df['keyword'].values):

		# 条件にマッチしたの発話選択
		key_alias = val.split('|')
		for key_or in key_alias:
			if key_or in utterance:
				response_candidates.append(str(df.at[i, 'reply']))
				key = key_or
				break
		key_alias = val.split('&')
		for key_and in key_alias:
			chk_all = True
			if key_and not in utterance:
				chk_all = False
				break
		if chk_all:
			response_candidates.append(str(df.at[i, 'reply']))

	# 候補がない場合，default(*のついているもの)から選択
	if len(response_candidates) == 0:
		response_candidates = df[df['keyword'] == '*']['reply'].values
	response_before_parse = np.random.choice(response_candidates)

	# 独自のクラス使用している
	UUI = userUtteranceInfo(key, response_before_parse)
	UUI.addInfo(user_name, 'NAME')
	return UUI

# parse前の日本語を翻訳してreturn
# ドイツ語は'de'，英語は’en’
def translateUtterance(utterance, user_name, lang='de'):
	# 条件に応じてパルス
	utte_split = utterance.split('|')
	for i, val in enumerate(utte_split):
		if 'おじさん' in val:
			utte_split[i] = val.replace('おじさん', '私')
	catstetetet = ''.join(utte_split)
	# 翻訳
	translator = Translator()
	return translator.translate(catstetetet, src='ja' ,dest=lang).text




if __name__ == '__main__':

	pass

