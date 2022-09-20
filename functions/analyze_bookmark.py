# -*- coding: utf-8 -*-
# 参考：https://note.nkmk.me/python-scrapy-hatena-bookmark-api/
import pprint
import requests
import sys
import MeCab
import csv

# はてブのAPI使って対象のブコメを取得

# url = sys.argv[1]
def analyze_b(url,opt):
	hb_entry = 'http://b.hatena.ne.jp/entry/jsonlite/'

	r = requests.get(hb_entry, params={'url': url})
	print(r.url)
	j = r.json()
	print(str(j['title'])+' '+str(j['count'])+'bookmarks')

	# -----辞書の準備-------
	dict_orgn = open('../dict/dict_inui',mode="r")
	dict_orgn2 = open('../dict/dict_inui2',mode="r")
	dic = csv.reader(dict_orgn, delimiter = '\t')
	dic2 = csv.reader(dict_orgn2, delimiter = '\t')

	mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

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
	for b in j['bookmarks']:
		parsed = mecab.parse(b['comment'])
		for x in parsed.splitlines()[:-1]:
			if x.split('\t')[1].split(',')[0] in [ '名詞','形容詞','動詞','副詞']:
				words = x.split('\t')[0]
				wordcount.append(words)
				if words in dict_data.keys():
					emotion_data.append(words + ":" +dict_data[words]+"//" )
					score_p += dict_data[words].count('p')
					score_n += dict_data[words].count('n')
	# ーーーーーーーーーーーーーーーーーー				
	# スコア（パーセント）の算出
	# 感情語比率：分析対象となる語（'名詞','形容詞','動詞','副詞'）全体数のうち，感情語の辞書に載っている語の数＊100
	# ポジティブ：分析対象となる語（'名詞','形容詞','動詞','副詞'）全体数のうち，「ポジティブ」と判定された語の数＊100
	# ネガティブ：分析対象となる語（'名詞','形容詞','動詞','副詞'）全体数のうち，「ネガティブ」と判定された語の数＊100
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
	# print("---------")
	# 	# print(emotion_data,len(wordcount),score_p,score_n)
	# print("感情語比率："+str(per_emo)+"%,ポジティブ："+str(per_p)+"%,ネガティブ："+str(per_n)+"%")
	# ーーーーーーコメントが見たい時は引数を追加してくださいーーーーーーー
	com_list = {}
	if opt:
		for b in j['bookmarks']:
			if b['comment'] ==	"":
				continue
			com_list[b['user']] = b['comment']
		return(per_emo, per_p, per_n, com_list)
	else:
		return(per_emo, per_p, per_n)


# val = analyze_b('https://www.itmedia.co.jp/news/articles/2207/07/news050.html',"opt!")
# print(str(val))
