# -*- coding: utf-8 -*-
# 参考：https://note.nkmk.me/python-scrapy-hatena-bookmark-api/
import pprint
import requests
import sys
import csv
from janome.tokenizer import Tokenizer
import time
import pickle
import collections

# ものすごくシンプルに，テキスト群を投げたらポジネガ率と感情語率,使用語ランキングが帰ってくる関数
# 辞書はdictディレクトリにある
# 辞書中の？判定はスルー
# 対象は名詞、形容詞、動詞、副詞

def analyze(text):

	# -----辞書の準備-------
	dict_orgn = open('../dict/dict_inui',mode="r")
	dict_orgn2 = open('../dict/dict_inui2',mode="r")
	dic = csv.reader(dict_orgn, delimiter = '\t')
	dic2 = csv.reader(dict_orgn2, delimiter = '\t')

	# mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

	dict_data = {}
	for low in dic:
		lists = {low[0]:low[1]}
		if "?" in low[1]:
			continue
		dict_data.update(lists)
	for low in dic2:
		lists2 = {low[1]:low[0]}
		if "?" in low[1]:
			continue
		dict_data.update(lists2)
	# ----------
	# ーーーーーーブコメの感情語解析ーーーーー
	wordcount = []
	score_p = 0
	score_n = 0
	emotion_data = []

	wordlist = []
	w_rank = []

	# parsed = mecab.parse(b['comment'])
	for low in text:
		parsed = Tokenizer(mmap=False).tokenize(low)
		for x in parsed:
			if x.part_of_speech.split(',')[0] in [ '名詞','形容詞','動詞','副詞']:
				words = x.base_form
				wordcount.append(words)
				if words in dict_data.keys():
					wordlist.append(words)
					emotion_data.append(words + ":" +dict_data[words]+"//" )
					score_p += dict_data[words].count('p')
					score_n += dict_data[words].count('n')
		# ーーーーーーーーーーーーーーーーーー				
		# スコア（パーセント）の算出
		# 感情語比率：分析対象となる語（'名詞','形容詞','動詞','副詞'）全体数のうち，感情語の辞書に載っている語の数＊100
		# ポジティブ：分析対象となる語（'名詞','形容詞','動詞','副詞'）全体数のうち，「ポジティブ」と判定された語の数＊100
		# ネガティブ：分析対象となる語（'名詞','形容詞','動詞','副詞'）全体数のうち，「ネガティブ」と判定された語の数＊100

	c = collections.Counter(wordlist)
	w_rank.append(c.most_common(10))

	try:
		per_emo = round(((score_p+score_n)/len(wordcount))*100,3)
	except ZeroDivisionError:
		per_emo = 0
	try:
		per_p = round((score_p/len(wordcount))*100,3)
	except ZeroDivisionError:
		per_p = 0
	try:
		per_n = round((score_n/len(wordcount))*100,3)
	except ZeroDivisionError:
		per_n = 0
	return(per_emo, per_p, per_n, w_rank)