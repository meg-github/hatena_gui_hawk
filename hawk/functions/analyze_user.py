# -*- coding: utf-8 -*-
import csv
import sys
import collections
from janome.tokenizer import Tokenizer


# username = sys.argv[1]
def analyze_usr(name):
	comment_orgn = open('./result/'+name,mode='r')
	dict_orgn = open('./dict/dict_inui',mode="r")
	dict_orgn2 = open('./dict/dict_inui2',mode="r")

	comments = csv.reader(comment_orgn, delimiter='\t')
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

	wordcount_total = 0
	score_p_total = 0
	score_n_total = 0

	comments_usr = []
	wordlist = []
	w_rank = []

	for low in comments:
		comments_usr.append(low[3])
		wordcount = []
		score_p = 0
		score_n = 0
		emotion_data = []
		parsed = Tokenizer(mmap=False).tokenize(low[3])
		for x in parsed:
			if x.part_of_speech.split(',')[0] in [ '名詞','形容詞','動詞','副詞']:
				words = x.base_form
				wordcount.append(words)
				wordcount_total +=len(wordcount)
				if words in dict_data.keys():
					wordlist.append(words)
					emotion_data.append(words + ":" +dict_data[words] )
					score_p += dict_data[words].count('p')
					score_p_total += score_p
					score_n += dict_data[words].count('n')
					score_n_total += score_n

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
		if len(sys.argv) == 3:
		 	print("---------")
		 	print(low[3])
		 	# print(emotion_data,len(wordcount),score_p,score_n)
		 	# print("感情語比率："+str(per_emo)+"%,ポジティブ："+str(per_p)+"%,ネガティブ："+str(per_n)+"%")


	c = collections.Counter(wordlist)
	w_rank.append(c.most_common(10))

	try:
		per_emo_total = round(((score_p_total+score_n_total)/wordcount_total)*100,3)#感情語比率
		per_p_total = round((score_p_total/wordcount_total)*100,3)#ポジティブ率
		per_n_total = round((score_n_total/wordcount_total)*100,3)#ネガティブ率
	except ZeroDivisionError:
		print("error!")

	return(per_emo_total, per_p_total, per_n_total, w_rank)

	# splitted = ' '.join([x.split('\t')[0] for x in parsed.splitlines()[:-1] if x.split('\t')[1].split(',')[0] in [ '名詞','形容詞']])
	# comments.append(splitted)

