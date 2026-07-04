import streamlit as st
import FinanceDataReader as fdr
import pandas as pd
from ta.volatility import BollingerBands
from ta.volume import OnBalanceVolumeIndicator
import datetime
import requests
import time
import urllib.parse 
import random 

st.set_page_config(page_title="세력 포착 AI 시스템", page_icon="🚀", layout="centered")

st.markdown("""
    <style>
    div[data-testid="stStaleNode"] { opacity: 1 !important; filter: none !important; transition: none !important; }
    .naver-btn {
        background-color: #03c75a;
        color: white !important;
        padding: 2px 8px;
        border-radius: 5px;
        text-decoration: none;
        font-size: 0.5em;
        vertical-align: middle;
        margin-left: 10px;
    }
    /* 면책조항 스타일 */
    .disclaimer {
        text-align: center;
        color: #999999;
        font-size: 0.75em;
        padding: 20px 0;
        margin-top: 30px;
        border-top: 1px solid #eeeeee;
    }
    </style>
    """, unsafe_allow_html=True)

BOT_TOKEN = "8899908573:AAEOba8jFLi9h6S1Xhi5E-EqfTNoBf2r-xU"
CHAT_ID = "1076053813"
EXPIRATION_DATE = datetime.date(2026, 7, 11)
today = datetime.date.today()

now_kst = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
current_time = now_kst.time()
is_jongbe = datetime.time(15, 15) <= current_time <= datetime.time(15, 35)
mode_text = "🌙 [종가베팅]" if is_jongbe else "☀️ [장중수급]"

is_cron_job = (st.query_params.get("job") == "cron")

def get_rank_info(score):
    if score >= 90: return "👑 [최상위 대장주]", "강력하게 풀매수!"
    elif score >= 80: return "🔥 [강력 추천]", "공격적인 분할매수!"
    else: return "🔔 [관심 추천]", "시세를 예의주시!"

def format_marcap(marcap):
    uk = int(marcap // 100000000)
    if uk >= 10000:
        jo = uk // 10000
        remain_uk = uk % 10000
        if remain_uk > 0: return f"{jo}조 {remain_uk:,}억"
        else: return f"{jo}조"
    else:
        return f"{uk:,}억"

@st.cache_data(ttl=600)
def get_target_stocks():
    krx = fdr.StockListing('KRX')
    krx = krx[(krx['Close'] >= 1000) & (~krx['Name'].str.contains('우$|우B$|우C$|스팩|리츠'))]
    krx = krx[(krx['Marcap'] >= 100000000000) & (krx['Marcap'] <= 5000000000000)]
    return krx.sort_values('Amount', ascending=False).head(50)

def run_stock_analysis(ui_box=None):
    results = []
    try:
        if ui_box: ui_box.info("📡 시총 1천억~5조 알짜 주도주 압축 스캔 중...")
        target_stocks = get_target_stocks()
        total = len(target_stocks)
        
        for idx, (index, row) in enumerate(target_stocks.iterrows()):
            code, name, mar
