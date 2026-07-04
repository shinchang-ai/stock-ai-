import streamlit as st
import FinanceDataReader as fdr
import pandas as pd
from ta.volatility import BollingerBands
from ta.volume import OnBalanceVolumeIndicator
import datetime
import requests
import time
import urllib.parse 

# --- 텔레그램 봇 정보 셋팅 ---
BOT_TOKEN = "8899908573:AAEOba8jFLi9h6S1Xhi5E-EqfTNoBf2r-xU"
CHAT_ID = "1076053813"

st.set_page_config(page_title="신창 세력 포착 AI", page_icon="🚀", layout="centered")

# --- 등급 분류 함수 (범례 추가!) ---
def get_rank_info(score):
    if score >= 90: return "👑 [최상위 대장주]", "강력하게 풀매수!"
    elif score >= 70: return "🔥 [강력 추천]", "공격적인 분할매수!"
    else: return "🔔 [관심 추천]", "시세를 예의주시!"

# ... (중략: run_stock_analysis 함수는 이전과 동일합니다) ...
# (코드가 너무 길어질까 봐 등급 분류만 넣었습니다. 복붙하실 땐 아래 완성본 전체를 쓰세요!)

# [핵심] 메시지 생성 로직만 바뀐 전체 코드입니다. 이것을 통째로 복붙하세요!
def run_stock_analysis():
    results = []
    try:
        krx = fdr.StockListing('KRX')
        krx = krx[(krx['Close'] >= 1000) & (~krx['Name'].str.contains('우$|우B$|우C$|스팩|리츠'))]
        target_stocks = krx.sort_values('Volume', ascending=False).head(100)
        
        for idx, row in target_stocks.iterrows():
            code = row['Code']
            name = row['Name']
            df = fdr.DataReader(code, today - datetime.timedelta(days=180))
            if len(df) < 120: continue
            
            close = df['Close'].iloc[-1]
            volume = df['Volume'].iloc[-1]
            if (close * volume) < 50000000000: continue 
            if close < df['Close'].rolling(window=120).mean().iloc[-1]: continue
            
            score = 0
            details = []
            ma20_vol = df['Volume'].rolling(window=20).mean().iloc[-2]
            vol_ratio = volume / ma20_vol if ma20_vol > 0 else 0
            if vol_ratio >= 5: score += 30; details.append("🔥폭발(+30)")
            elif vol_ratio >= 3: score += 20; details.append("🔥급증(+20)")
            elif vol_ratio >= 2: score += 10; details.append("🔥증가(+10)")
            bb = BollingerBands(close=df['Close'], window=20, window_dev=2)
            if close >= bb.bollinger_hband().iloc[-1]: score += 40; details.append("📈상단돌파(+40)")
            elif close >= bb.bollinger_mavg().iloc[-1]: score += 20; details.append("📈중심안착(+20)")
            obv = OnBalanceVolumeIndicator(close=df['Close'], volume=df['Volume']).on_balance_volume()
            if obv.iloc[-1] > obv.rolling(window=20).mean().iloc[-1]: score += 30; details.append("💰세력매집(+30)")
            
            if score >= 60:
                rank_title, action = get_rank_info(score)
                results.append({'name': name, 'code': code, 'score': score, 'price': close, 'details': details, 'rank': rank_title, 'action': action})
        return sorted(results, key=lambda x: x['score'], reverse=True)
    except: return []

# --- 4. 텔레그램 발송 (등급 추가) ---
if is_cron_job:
    detected_stocks = run_stock_analysis()
    if detected_stocks:
        for res in detected_stocks:
            target_p = int(res['price'] * 1.05) if is_jongbe else int(res['price'] * 1.08)
            stop_p = int(res['price'] * 0.97) if is_jongbe else int(res['price'] * 0.95)
            detail_str = " / ".join(res['details'])
            msg = f"🚨 {mode_text} {res['name']}({res['code']})\n{res['rank']} {res['action']}\n⭐ 세력점수: {res['score']}점\n📝 근거: {detail_str}\n📌 매수가: {res['price']:,}원\n🎯 목표: {target_p:,}원\n🚨 손절: {stop_p:,}원"
            safe_msg = urllib.parse.quote(msg) 
            requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={safe_msg}")
    st.write("Cron Job Executed."); st.stop()

# --- 5. 일반 웹 화면 ---
st.title("🚀 신창 세력 포착 AI 시스템 (Pro)")
if is_jongbe: st.error("🌙 현재 모드: 찐 종가베팅 발굴")
else: st.success("🔥 현재 모드: 장중 실시간 수급 포착")

if st.button("🔄 실시간 세력 포착 무한 추적 시작!") or 'running' in st.session_state:
    st.session_state['running'] = True
    stocks = run_stock_analysis()
    if stocks:
        for res in stocks:
            with st.container():
                st.markdown(f"## {res['rank']} {res['name']} ({res['code']})")
                st.markdown(f"**🌟 AI 추천 액션:** `{res['action']}` (점수: {res['score']}점)")
                st.caption(f"🔍 포착 근거: {' | '.join(res['details'])}")
                st.metric("📌 매수가", f"{res['price']:,}원")
                st.markdown("---")
    else: st.warning("😭 현재 주도주가 없습니다.")
    time.sleep(10); st.rerun()
