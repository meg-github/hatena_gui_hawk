# -*- coding: utf-8 -*-
import streamlit as st
import sys
import csv
import pandas as pd
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pickle
import collections

# # 外部pyファイル
sys.path.append('.functions/')
import scrape_user_comment 
import analyze_user
import analyze_text_janome


# --------functions---------

def func_aggrids_bookmarks(df):   # st_aggridを使ってデータの設定をする
	data_view = GridOptionsBuilder.from_dataframe(df)
	data_view.configure_pagination(enabled=True)
	data_view.configure_default_column(editable=False,groupable=True,autoHeight=True, wrapText=True)
	gridoptions = data_view.build()
	return(gridoptions)

# -----------------
st.header("タスク2")
"以下の記事を読んで，「質問回答」タブから質問に回答してください．"

kijilist = pd.read_csv('./data_kiji/kijilist.csv', header=0)
sentdata = pd.read_csv('./data_kiji/list_sentdata.csv', header=0,dtype=str)
target_kiji = kijilist[kijilist['task']==2]
target_sentdata = sentdata[sentdata['title'].isin(target_kiji['title'])]

for line in target_kiji.itertuples():
	with st.expander(line.title):
		sent = target_sentdata[target_sentdata["title"] == line.title]
		st.write(line.content)
		# sentidata_kiji = analyze_text_janome.analyze(line.content)
		st.text('感情語の割合: '+sent.sent_total.values+
			' ポジティブな語の割合: '+sent.sent_p.values+
			' ネガティブな語の割合: '+sent.sent_n.values)
		with open('./data_kiji/'+str(line.title), "rb") as comments:
			commentlist = pickle.load(comments)
			# for key,value in zip(commentlist.keys(),commentlist.values()):
				# st.write(key+":"+value)
			df_commentlist = pd.DataFrame({
				"User":commentlist.keys(),
				"Comment":commentlist.values()
			})
			# sentidata_comment = analyze_text_janome.analyze(list(df_commentlist["Comment"]))
			# st.write('感情語の割合: '+str(sentidata_comment[0])+' ポジティブな語の割合: '+str(sentidata_comment[1])+' ネガティブな語の割合: '+str(sentidata_comment[2]))

			gridoptions = func_aggrids_bookmarks(df_commentlist)
			table = AgGrid(df_commentlist,gridOptions=gridoptions,fit_columns_on_grid_load=True)
			

