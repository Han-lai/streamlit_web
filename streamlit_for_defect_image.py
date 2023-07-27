# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 08:31:16 2022

@author: AlbeeSHLai
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import concurrent.futures
import re
from re import search
# from streamlit.ReportThread import add_report_ctx
import threading
import time


# def scraper():
#     print("start")
#     time.sleep(5)
#     print("sleep done")


def St_Cfg():
    st.set_page_config(
        page_title="AIDI DEFECT App",
        page_icon="🧊",
        layout="wide"
    )
    st.sidebar.header("AIDI Image")
    st.sidebar.subheader("依序選擇")

# @st.cache(suppress_st_warning=True)
def AIDIdefect():
    data_colums = ['A2MORxxx', 'A2MORxxx', 'A2MORxxx', 'A2MORxxx', 'A2MORxxx', 'A2MORxxx']
    # -------GET TOOL ------------------
    url = 'http://10.88.xxx.x/AIDI/db_images/'
    # print(url)
    TOOLS_tag = st.sidebar.selectbox('Tool_info', data_colums)
    url = f"{url}{TOOLS_tag}/"
    # print(url)
    # try:


   # -------GET RECIPE ------------------

    r = requests.get(url=url)
    soup = BeautifulSoup(r.text, "html.parser")
    str = re.compile(".*/")
    recipe_colums = list(filter(str.match,[(i['href']) for i in soup.select('a')[1:]]))
    recipe_tag = st.sidebar.selectbox('recipe_info', recipe_colums)

    # -------GET LOT ------------------
    url = f"{url}{recipe_tag}/"
    # print(url)
    r = requests.get(url=url)
    soup = BeautifulSoup(r.text, "html.parser")
    lot_colums = [(i['href']) for i in soup.select('a')[1:]]
    lot_tag = st.sidebar.selectbox('lot_info', lot_colums)

    # -------GET SHEET ------------------
    url = f"{url}{lot_tag}"
    # print(url)
    r = requests.get(url=url)
    soup = BeautifulSoup(r.text, "html.parser")

    sheet_colums = [(i['href']) for i in soup.select('a')[1:]]
    sheet_tag = st.sidebar.selectbox('sheet_info', sheet_colums)

    # -------GET image ------------------
    url = f"{url}{sheet_tag}"
    print(url)
    r = requests.get(url=url)
    soup = BeautifulSoup(r.text, "html.parser")
    image_colums = [url + (i['href']) for i in soup.select('a')[1:]]
    return image_colums

    # except Exception as e:
    #     print(e)





def showImage(image_list):
    imageLotCount = 3
    count = 0
    cols = st.columns(imageLotCount)
    # print(cols)
    for i in range(len(image_colums)):
        option_5 = cols[count].text(image_colums[i].split('/')[-1])
        option_5 = cols[count].image(image_colums[i], use_column_width=True)
        count = count + 1
        count = count if count < imageLotCount else 0


if _name_ == '_main_':
    St_Cfg()

    start_time = time.time()  # 開始時間
    # print(start_time)

    url = 'http://10.88.xxx.5/AIDI/db_images/'
    image_colums = AIDIdefect()
    showImage(image_colums)

    t = threading.Thread(target=AIDIdefect)
    # add_report_ctx(t)
    # 開始執行緒
    t.start()
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(AIDIdefect, url)
    t.join()


    end_time = time.time()  # 開始時間
    # print(end_time)
    # print(f"{end_time - start_time} 爬取 {len(image_colums)} ")