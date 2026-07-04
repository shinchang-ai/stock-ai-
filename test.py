import streamlit as st
import FinanceDataReader as fdr
import pandas as pd
from ta.volatility import BollingerBands
from ta.volume import OnBalanceVolumeIndicator
import datetime
import requests
import time
import urllib.parse 

# --- 1. 기본 설정 ---
st.set_page_config(page_title="신창 세력 포착 AI", page_icon="🚀", layout="centered")

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
    elif score >= 70: return "🔥 [강력 추천]", "공격적인 분할매수!"
    else: return "🔔 [관심 추천]", "시세를 예의주시!"

@st.cache_data(ttl=300)
def get_target_stocks():
    krx = fdr.StockListing('KRX')
    krx = krx[(krx['Close'] >= 1000) & (~krx['Name'].str.contains('우$|우B$|우C$|스팩|리츠'))]
    return krx.sort_values('Amount', ascending=False).head(50)

# --- 2. 핵심 분석 엔진 ---
def run_stock_analysis(ui_box=None):
    results = []
    try:
        if ui_box: ui_box.info("📡 500억 이상 주도주 수급 스캔 중...")
        
        target_stocks = get_target_stocks()
        total = len(target_stocks)
        
        for idx, (index, row) in enumerate(target_stocks.iterrows()):
            code, name = row['Code'], row['Name']
            
            if ui_box: ui_box.warning(f"⏳ AI 정밀 분석 중 [{idx+1}/{total}] : 🔍 **{name}**")
            
            df = fdr.DataReader(code, today - datetime.timedelta(days=120))
            if len(df) < 60: continue 
            
            close, volume = df['Close'].iloc[-1], df['Volume'].iloc[-1]
            tr_val = close * volume 
            
            if tr_val < 50000000000: continue 
            
            score = 0; details = []
            
            # ⭐ 1. 거래대금 풀네임 변경
            if tr_val >= 100000000000: 
                score += 30; details.append("💰거래대금 1천억 돌파(+30)")
            elif tr_val >= 50000000000: 
                score += 20; details.append("💰거래대금 5백억 돌파(+20)")
                
            # ⭐ 2. 거래량 풀네임 변경
            ma20_vol = df['Volume'].rolling(window=20).mean().iloc[-2]
            vol_ratio = volume / ma20_vol if ma20_vol > 0 else 0
            
            if vol_ratio >= 5: score += 30; details.append("🔥거래량 5배 폭발(+30)")
            elif vol_ratio >= 3: score += 20; details.append("🔥거래량 3배 급증(+20)")
            elif vol_ratio >= 2: score += 10; details.append("🔥거래량 2배 증가(+10)")
            
            # ⭐ 3. 볼린저밴드 풀네임 변경
            bb = BollingerBands(close=df['Close'], window=20, window_dev=2)
            if close >= bb.bollinger_hband().iloc[-1]: score += 40; details.append("📈볼린저밴드 상단돌파(+40)")
            elif close >= bb.bollinger_mavg().iloc[-1]: score += 20; details.append("📈볼린저밴드 중심선 안착(+20)")
            
            # ⭐ 4. OBV 풀네임 변경
            obv = OnBalanceVolumeIndicator(close=df['Close'], volume=df['Volume']).on_balance_volume()
            if obv.iloc[-1] > obv.rolling(window=20).mean().iloc[-1]: score += 30; details.append("👑OBV 세력매집 포착(+30)")
            
            if score >= 60:
                rank_title, action = get_rank_info(score)
                results.append({'name': name, 'code': code, 'score': score, 'price': close, 'details': details, 'rank': rank_title, 'action': action})
        
        if ui_box: ui_box.success("✅ 500억 이상 주도주 스캔 완료!")
        time.sleep(0.5)
        if ui_box: ui_box.empty()
        
        return sorted(results, key=lambda x: x['score'], reverse=True)
    except Exception as e:
        if ui_box: ui_box.error("네트워크 지연! 잠시 후 재시도합니다.")
        return []

# --- 3. 텔레그램 발송 ---
if is_cron_job:
    if today > EXPIRATION_DATE: st.stop()
    stocks = run_stock_analysis()
    if stocks:
        for res in stocks:
            target_p = int(res['price'] * (1.05 if is_jongbe else 1.08))
            stop_p = int(res['price'] * (0.97 if is_jongbe else 0.95))
            msg = f"🚨 {mode_text} {res['name']}({res['code']})\n{res['rank']} {res['action']}\n⭐ 총점: {res['score']}점\n📝 근거: {' / '.join(res['details'])}\n📌 매수: {res['price']:,}원\n🎯 목표: {target_p:,}원\n🚨 손절: {stop_p:,}원"
            requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={urllib.parse.quote(msg)}")
    st.stop()

# --- 4. 사용자 웹 화면 ---
st.title("🚀 신창 세력 포착 AI 시스템 (Pro)")
if is_jongbe: st.error("🌙 현재 모드: 찐 종가베팅 발굴")
else: st.success("🔥 현재 모드: 장중 500억 이상 수급 포착")

if st.button("🔄 실시간 세력 포착 무한 추적 시작!") or 'running' in st.session_state:
    st.session_state['running'] = True
    
    status_box = st.empty() 
    stocks = run_stock_analysis(status_box)
    
    if stocks:
        st.success(f"🔥 조건 만족 주도주 총 {len(stocks)}개 포착!")
        for res in stocks:
            target_p = int(res['price'] * (1.05 if is_jongbe else 1.08))
            stop_p = int(res['price'] * (0.97 if is_jongbe else 0.95))
            
            with st.container():
                st.markdown(f"## {res['rank']} {res['name']} ({res['code']})")
                st.markdown(f"**🌟 AI 액션:** `{res['action']}` (세력점수: {res['score']}점)")
                st.caption(f"🔍 포착 근거: {' | '.join(res['details'])}")
                col1, col2, col3 = st.columns(3)
                col1.metric("📌 매수가", f"{res['price']:,}원")
                col2.metric("🎯 목표가", f"{target_p:,}원")
                col3.metric("🚨 손절가", f"{stop_p:,}원")
                st.markdown("---")
        time.sleep(10)
    else:
        st.warning("😭 현재 500억 이상 터진 주도주가 없습니다. 30초 뒤 재탐색합니다.")
        time.sleep(30)
        
    st.rerun()
