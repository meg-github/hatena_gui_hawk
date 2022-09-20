# -*- coding: utf-8 -*-
import sys
import time
import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os 

# user = sys.argv[1]
# pages = sys.argv[2]

def scrape(user,pages):
	home = "https://b.hatena.ne.jp/"
# ユーザのブコメを取得するメソッド
	filepath = "../result/"+user
	if not os.path.isfile(filepath):
		result = open(filepath, mode='w')
		dynamic_url = home + user + "/bookmark?page="
		st.write(dynamic_url)
		flag = 1

		for i in range(int(pages)):
			time.sleep(2)
			r = requests.get(dynamic_url + str(i+1))
			soup = BeautifulSoup(r.content, 'html.parser')	 

			title = soup.find_all('a', class_='js-clickable-link js-keyboard-openable')
			url = []
			for link in title:
				url.append(link.get('href'))
			comment = soup.find_all('span', class_='js-comment')
			print(len(title))

			for i in range(len(title)):
				kakikomi = str(flag) + "\t" + url[i] + "\t" + title[i].text + "\t" + comment[i].text + '\n'
				result.write(kakikomi)
				flag += 1	
		result.close()
	else:
		pass



# result.write(soup)
