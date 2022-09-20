import streamlit as st
import sys
import csv
import pandas as pd
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pickle
# # 外部pyファイル
sys.path.append('../functions/')
import scrape_user_comment
import analyze_user
import analyze_text_janome
import collections



kijilist = pd.read_csv('kijilist.csv', header=0)
result = open("list_sentdata.csv", mode='w')

for line in kijilist.itertuples():

	with open('../data_kiji/'+str(line.title), "rb") as comments:
		commentlist = pickle.load(comments)
		df_commentlist = pd.DataFrame({
			"User":commentlist.keys(),
			"Comment":commentlist.values()
		})
		sentidata_comment = analyze_text_janome.analyze(list(df_commentlist["Comment"]))
		result.write(line.title+","+str(sentidata_comment[0])+","+str(sentidata_comment[1])+","+str(sentidata_comment[2])+",")
		result.writelines(sentidata_comment[3])
		result.write("\n")
result.close()