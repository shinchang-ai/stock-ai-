import streamlit as st
import FinanceDataReader as fdr
import pandas as pd
from ta.volatility import BollingerBands
from ta.volume import OnBalanceVolumeIndicator
import datetime
import requests
import time
import urllib.parse 

# --- 1. 기본 설정 (무조건 맨 위에 있어야 에러 안 남!) ---
st.set_page_config(page_title="신창 세력 포착 AI", page_icon="🚀", layout="centered")

BOT_TOKEN = "8899908573:AAEOba8jFLi9h6S1Xhi5E-EqfTNoBf2r-xU"
CHAT_ID = "1076053813"
EXPIRATION_DATE = datetime.date(2026, 7, 11)
today = datetime.date.today()

# 시간 및 종가베팅 모드 설정
now_kst = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
current_time = now_kst.time()
is_jongbe = datetime.time(15, 15) <= current_time <= datetime.time(15, 35)
mode_text = "🌙 [종가베팅]" if is_jongbe else "☀️ [장중수급]"

# 로봇(크론잡) 감지
query_params = st.query_params
is_cron_job = (query_params.get("job") == "cron")

# --- 2. 등급 판독 함수 ---
def get_rank_info(score):
    if score >= 90: return "👑 [최상위 대장주]", "강력하게 풀매수!"
    elif score >= 70: return "🔥 [강력 추천]", "공격적인 분할매수!"
    else: return "🔔 [관심 추천]", "시세를 예의주시!"

# --- 3. 핵심 분석 엔진 ---
def run_stock_analysis():
    results = []
    try:
        # 무료 서버 다운 방지: 거래량 상위 50개 1차 필터링
        krx = fdr.StockListing('KRX')
        krx = krx[(krx['Close'] >= 1000) & (~krx['Name'].str.contains('우$|우B$|우C$|스팩|리츠'))]
        target_stocks = krx.sort_values('Volume', ascending=False).head(50) 
        
        for idx, row in target_stocks.iterrows():
            code, name = row['Code'], row['Name']
            df = fdr.DataReader(code, today - datetime.timedelta(days=120))
            if len(df) < 60: continue 
            
            close, volume = df['Close'].iloc[-1], df['Volume'].iloc[-1]
            if (close * volume) < 50000000000: continue # 500억 기준 유지!
            
            score = 0; details = []
            ma20_vol = df['Volume'].rolling(window=20).mean().iloc[-2]
            vol_ratio = volume / ma20_vol if ma20_vol > 0 else 0
            
            if vol_ratio >= 5: score += 30; details.append("거래량 폭발(+30)")
            elif vol_ratio >= 3: score += 20; details.append("거래량 급증(+20)")
            elif vol_ratio >= 2: score += 10; details.append("거래량 증가(+10)")
            
            bb = BollingerBands(close=df['Close'], window=20, window_dev=2)
            if close >= bb.bollinger_hband().iloc[-1]: score += 40; details.append("볼린저밴드 돌파(+40)")
            elif close >= bb.bollinger_mavg().iloc[-1]: score += 20; details.append("볼린저밴드 안착(+20)")
            
            obv = OnBalanceVolumeIndicator(close=df['Close'], volume=df['Volume']).on_balance_volume()
            if obv.iloc[-1] > obv.rolling(window=20).mean().iloc[-1]: score += 30; details.append("세력 매집(+30)")
            
            if score >= 60:
                rank_title, action = get_rank_info(score)
                results.append({'name': name, 'code': code, 'score': score, 'price': close, 'details': details, 'rank': rank_title, 'action': action})
        return sorted(results, key=lambda x: x['score'], reverse=True)
    except Exception as e:
        return []

# --- 4. 텔레그램 로봇 자동 발송 (목표가/손절가 완벽 복구) ---
if is_cron_job:
    if today > EXPIRATION_DATE: st.stop()
    stocks = run_stock_analysis()
    if stocks:
        for res in stocks:
            target_p = int(res['price'] * (1.05 if is_jongbe else 1.08))
            stop_p = int(res['price'] * (0.97 if is_jongbe else 0.95))
            msg = f"🚨 {mode_text} {res['name']}({res['code']})\n{res['rank']} {res['action']}\n⭐ 점수: {res['score']}점\n📝 근거: {' / '.join(res['details'])}\n📌 매수: {res['price']:,}원\n🎯 목표: {target_p:,}원\n🚨 손절: {stop_p:,}원"
            requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={urllib.parse.quote(msg)}")
    st.stop()

# --- 5. 일반 사용자 웹 화면 ---
st.title("🚀 신창 세력 포착 AI 시스템 (Pro)")
if is_jongbe: st.error("🌙 현재 모드: 찐 종가베팅 발굴")
else: st.success("🔥 현재 모드: 장중 실시간 수급 포착")

if st.button("🔄 실시간 세력 포착 무한 추적 시작!") or 'running' in st.session_state:
    st.session_state['running'] = True
    
    # 🎨 화면이 심심하지 않게 채워줄 분석 애니메이션 바!
    my_bar = st.progress(0, text="📡 KRX 전 종목 수급 스캔 중...")
    tasks = ["500억 이상 거래대금 필터링...", "볼린저밴드 파동 계산 중...", "OBV 세력 매집 패턴 감지...", "최종 주도주 랭킹 산정 중..."]
    for i, task in enumerate(tasks):
        time.sleep(0.6)
        my_bar.progress((i + 1) * 20, text=f"⏳ {task} ({(i+1)*20}%)")
    time.sleep(0.5)
    my_bar.empty() # 분석 끝나면 깔끔하게 삭제
    
    # 분석 실행
    stocks = run_stock_analysis()
    
    if stocks:
        st.success(f"🔥 총 {len(stocks)}개의 주도주를 포착했습니다!")
        for res in stocks:
            target_p = int(res['price'] * (1.05 if is_jongbe else 1.08))
            stop_p = int(res['price'] * (0.97 if is_jongbe else 0.95))
            
            with st.container():
                st.markdown(f"## {res['rank']} {res['name']} ({res['code']})")
                st.markdown(f"**🌟 AI 액션:** `{res['action']}` (세력점수: {res['score']}점)")
                st.caption(f"🔍 포착 근거: {' | '.join(res['details'])}")
                
                # 웹 화면에도 목표가,
