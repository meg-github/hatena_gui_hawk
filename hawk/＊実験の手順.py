# -*- coding: utf-8 -*-
import streamlit as st
import sys
import csv
import pandas as pd
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pickle
# # 外部pyファイル
from PIL import Image

#-----------関数----------------
markdown = '''
## はじめに
実験に参加していただき、ありがとうございます。\n
以下に実験の手順が記されておりますので、よくお読みいただいた上で参加してください。

## 実験手順
今から、あるニュース記事とその記事につけられたコメントについての質問を行います。
以下の手順に従って提示される内容を把握し、質問への回答を行ってください。

1. ページ左側の「タスク1」タブを押して開いてください。タブを開くと、実験対象のニュース記事のタイトルが3件表示されます。
2. タイトル部分をクリックしてください。ニュース記事の内容と，その記事につけられたコメント，コメント群に含まれる感情的な語の割合が表示されます。
3. 3件のニュース記事を全て読み，各記事につけられたコメントの中から，あなたがもっとも賛同できるコメントを1件決めてください。
4. ページの下部に表示される質問に回答してください。回答の入力が完了しましたら，必ず「送信」ボタンを押して回答を確定させてください。
5. 「タスク2」も同様に行ってください。


'''
st.markdown(markdown)

st.subheader("タスク画面の説明")
st.write("タブ「タスク1」「タスク2」を開くと、いくつかの機能を備えたwebページが表示されます。各機能の使い方を以下の動画で確認してください。")
st.video("https://raw.githubusercontent.com/meg-github/hatena_gui_hawk/main/hawk/movie_hawk.mp4", format="video/mp4", start_time=0)

# st.write("タブ：「タスク1」「タスク2」を開くと、以下のような画面が表示されます。"
# "画面の構成は以下のようになっています。")
# st.image("https://raw.githubusercontent.com/meg-github/hatena_gui_hawk/main/hawk/fig_exp.png", caption='画面構成',use_column_width="auto")
# "①：ニュース記事のタイトルです。クリックすることで記事内容を確認することができます。"
# "②：ニュース記事の本文です。記事内容をお読みいただいた上でアンケートに回答してください。"
# "③：ニュース記事につけられたコメントの感情分析結果です。この記事につけられたコメントの全体的な感情の傾向を知ることができます。つけられたコメントの量が多い場合や、質問回答の際に参考にしてください。"
# "④：ニュース記事につけられたコメントの一覧です。コメントは10件ずつ表示されています。左下の「＜」「＞」ボタンで11件目以降のコメントを見ることができます。"

st.header("注意事項")

"1. 実験中にページを閉じないでください。ページから離れると入力されたデータがリセットされます。"
"2. 実験は2つのタスクから構成されています。必ず2つとも回答してください。"
"3. ニュース記事は1つのタスクにつき3件表示されます。3件の記事内容を全てお読みいただいた上で回答するようにしてください。"
"4. 質問の回答にはgoogleアカウントへのログインが必要です。googleアカウントを作成し，ログインした状態で回答してください。このログインは重複回答を避けるためのものです。メールアドレスなどの個人情報の収集は行っていません。"
"5. 質問の入力後は必ず「送信」ボタンを押してください。送信後に回答の編集はできません。"
"6. 「送信」を押した後に表示される確認番号は，報酬の獲得に必要です（下の画像のように表示されます）。必ずメモなどで記録しておいてください。"
st.image("https://raw.githubusercontent.com/meg-github/hatena_gui_hawk/main/hawk/fig_num.png", caption='確認番号はこのように表示されます',use_column_width="auto")


st.header(" ")
contact = '''
#### 連絡先
本実験に関するお問い合わせは，以下の連絡先までご連絡ください。

**所在地**
>569-1045
>大阪府高槻市霊仙寺町2-1-1
>関西大学高槻キャンパス

**実験者**
>関西大学大学院　総合情報学研究科　総合情報学専攻  松下光範研究室\n
>m_mat(at)kansai-u.ac.jp

>博士後期課程 3年　安尾　萌\n
>k290993(at)kansai-u.ac.jp
'''

st.markdown(contact)
st.write('<span style="color:red;background:pink">ここはページの最下部です。最初にここが表示されてしまう場合は，ページを上までスクロールして実験手続きを確認してください。</span>',unsafe_allow_html=True)


