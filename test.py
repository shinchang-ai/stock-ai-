import streamlit as st
import FinanceDataReader as fdr
import pandas as pd
from ta.volatility import BollingerBands
from ta.volume import OnBalanceVolumeIndicator
import datetime
import requests
import time
import urllib.parse 

# 설정
BOT_TOKEN = "8899908573:AAEOba8jFLi9h6S1Xhi5E-EqfTNoBf2r-xU"
CHAT_ID = "1076053813"
st.set_page_config(page_title="신창 세력 포착 AI", page_icon="🚀", layout="centered")

# 로봇 확인
query_params = st.query_params
is_cron_job = (query_params.get("job") == "cron")

# 분석 함수
def run_stock_analysis():
    results = []
    try:
        krx = fdr.StockListing('KRX')
        krx = krx[(krx['Close'] >= 1000) & (~krx['Name'].str.contains('우$|우B$|우C$|스팩|리츠'))]
        target_stocks = krx.sort_values('Volume', ascending=False).head(100)
        for idx, row in target_stocks.iterrows():
            df = fdr.DataReader(row['Code'], datetime.date.today() - datetime.timedelta(days=180))
            if len(df) < 120: continue
            close, vol = df['Close'].iloc[-1], df['Volume'].iloc[-1]
            if (close * vol) < 50000000000: continue
            
            score = 0; details = []
            ma20 = vol / df['Volume'].rolling(20).mean().iloc[-2]
            if ma20 >= 5: score += 30; details.append("거래량 폭발(+30)")
            elif ma20 >= 2: score += 10; details.append("거래량 증가(+10)")
            
            bb = BollingerBands(close=df['Close'], window=20, window_dev=2)
            if close >= bb.bollinger_hband().iloc[-1]: score += 40; details.append("볼밴 돌파(+40)")
            
            obv = OnBalanceVolumeIndicator(close=df['Close'], volume=df['Volume']).on_balance_volume()
            if obv.iloc[-1] > obv.rolling(20).mean().iloc[-1]: score += 30; details.append("세력 매집(+30)")
            
            if score >= 60:
                results.append({'name': row['Name'], 'code': row['Code'], 'score': score, 'price': close, 'details': details})
        return sorted(results, key=lambda x: x['score'], reverse=True)
    except: return []

# 자동화 처리
if is_cron_job:
    stocks = run_stock_analysis()
    if stocks:
        for res in stocks:
            msg = f"🚨 {res['name']}\n⭐ 점수: {res['score']}점\n📝 근거: {'/'.join(res['details'])}\n📌 매수: {res['price']:,}원"
            requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={urllib.parse.quote(msg)}")
    st.stop()

# 일반 화면
st.title("🚀 신창 세력 포착 AI")
if st.button("🔄 실시간 세력 포착 시작!") or 'running' in st.session_state:
    st.session_state['running'] = True
    with st.spinner("AI 분석 중..."):
        stocks = run_stock_analysis()
        if stocks:
            for res in stocks:
                st.subheader(f"{res['name']} ({res['score']}점)")
                st.caption(f"근거: {' | '.join(res['details'])}")
                st.metric("매수가", f"{res['price']:,}원")
        else: st.write("포착된 주도주가 없습니다.")
    time.sleep(10)
    st.rerun()
