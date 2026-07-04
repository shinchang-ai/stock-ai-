import streamlit as st
import FinanceDataReader as fdr
import pandas as pd
from ta.volatility import BollingerBands
from ta.volume import OnBalanceVolumeIndicator
import datetime
import requests
import time
import urllib.parse 

# --- 텔레그램 봇 정보 셋팅 (완벽 세팅됨) ---
BOT_TOKEN = "8899908573:AAEOba8jFLi9h6S1Xhi5E-EqfTNoBf2r-xU"
CHAT_ID = "1076053813"

st.set_page_config(page_title="신창 세력 포착 AI", page_icon="🚀", layout="centered")

EXPIRATION_DATE = datetime.date(2026, 7, 11)
today = datetime.date.today()

now_kst = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
current_time = now_kst.time()

if datetime.time(15, 15) <= current_time <= datetime.time(15, 35):
    is_jongbe = True
    mode_text = "🌙 [종가베팅]"
else:
    is_jongbe = False
    mode_text = "☀️ [장중수급]"

query_params = st.query_params
is_cron_job = (query_params.get("job") == "cron")

if today > EXPIRATION_DATE:
    if is_cron_job: st.stop()
    st.error("🔒 무료 체험 기간이 만료되었습니다. 계속 사용하시려면 VIP 인증이 필요합니다.")
    st.stop()

# --- 3. 핵심 알고리즘 함수 (항목별 점수 상세 기록 추가!) ---
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
            details = [] # ⭐ 점수 획득 이유를 담을 주머니 생성!
            
            # 1. 거래량 분석
            ma20_vol = df['Volume'].rolling(window=20).mean().iloc[-2]
            vol_ratio = volume / ma20_vol if ma20_vol > 0 else 0
            if vol_ratio >= 5: 
                score += 30
                details.append("🔥거래량 폭발(+30점)")
            elif vol_ratio >= 3: 
                score += 20
                details.append("🔥거래량 급증(+20점)")
            elif vol_ratio >= 2: 
                score += 10
                details.append("🔥거래량 증가(+10점)")
            
            # 2. 볼린저밴드 분석
            bb = BollingerBands(close=df['Close'], window=20, window_dev=2)
            if close >= bb.bollinger_hband().iloc[-1]: 
                score += 40
                details.append("📈볼밴 상단 돌파(+40점)")
            elif close >= bb.bollinger_mavg().iloc[-1]: 
                score += 20
                details.append("📈볼밴 중심선 안착(+20점)")
            
            # 3. OBV 매집 분석
            obv = OnBalanceVolumeIndicator(close=df['Close'], volume=df['Volume']).on_balance_volume()
            if obv.iloc[-1] > obv.rolling(window=20).mean().iloc[-1]: 
                score += 30
                details.append("💰OBV 세력 매집(+30점)")
            
            if score >= 60:
                results.append({
                    'name': name, 
                    'code': code, 
                    'score': score, 
                    'price': close,
                    'details': details # ⭐ 이유를 결과에 저장!
                })
                
        return sorted(results, key=lambda x: x['score'], reverse=True)
    except Exception as e:
        return []

# --- 4. 로봇(Cron) 전용 텔레그램 발송 ---
if is_cron_job:
    detected_stocks = run_stock_analysis()
    
    if detected_stocks:
        for res in detected_stocks:
            target_p = int(res['price'] * 1.05) if is_jongbe else int(res['price'] * 1.08)
            stop_p = int(res['price'] * 0.97) if is_jongbe else int(res['price'] * 0.95)
            
            # ⭐ 텔레그램 메시지에도 점수 이유를 쏙!
            detail_str = " / ".join(res['details'])
            msg = f"🚨 {mode_text} {res['name']}({res['code']})\n⭐ 세력점수: {res['score']}점 / 100점\n📝 포착이유: {detail_str}\n📌 매수가: {res['price']:,}원\n🎯 목표가: {target_p:,}원\n🚨 손절가: {stop_p:,}원"
            
            safe_msg = urllib.parse.quote(msg) 
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={safe_msg}"
            requests.get(url)
    else:
        msg = f"🔔 [신창 AI 생존신고] 보스! 현재 시장에 거래대금 500억 이상 터진 찐 주도주가 0개입니다. (텔레그램 연결 상태: 정상 🟢)"
        safe_msg = urllib.parse.quote(msg)
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={safe_msg}"
        requests.get(url)
        
    st.write("Cron Job Executed.")
    st.stop() 

# --- 5. 일반 사용자(지인용) 웹 화면 ---
st.title("🚀 신창 세력 포착 AI 시스템 (Pro)")
st.info(f"💡 무료 체험 기간: {EXPIRATION_DATE} 까지")

if is_jongbe:
    st.toast("🚨 [종가베팅 모드 발동] 장 막판 찐 세력주 마감 타임입니다!", icon="🌙")
    st.error("🌙 현재 모드: 찐 종가베팅 발굴 (오후 3시 15분 타임)")
else:
    st.toast("🔔 [실시간 수급 모드] 최신 주도주 리스트가 갱신되었습니다.", icon="🔥")
    st.success("🔥 현재 모드: 장중 실시간 수급 포착 추적")

st.markdown("### 🎯 실시간 포착 가동")
start_btn = st.button("🔄 실시간 세력 포착 무한 추적 시작!")

if start_btn or 'running' in st.session_state:
    st.session_state['running'] = True
    
    with st.spinner("AI가 최신 거래 데이터를 스캔하고 있습니다..."):
        stocks = run_stock_analysis()
        
        if stocks:
            st.write(f"⏰ 마지막 갱신 시각: {now_kst.strftime('%H시 %M분 %S초')}")
            for res in stocks:
                target_p = int(res['price'] * 1.05) if is_jongbe else int(res['price'] * 1.08)
                stop_p = int(res['price'] * 0.97) if is_jongbe else int(res['price'] * 0.95)
                
                with st.container():
                    # ⭐ 제목 깔끔하게 유지하고, 100점 만점 표시 추가!
                    st.markdown(f"## {mode_text} {res['name']} ({res['code']})")
                    st.markdown(f"**🌟 세력 랭킹 점수:** `{res['score']}점 / 100점`")
                    
                    # ⭐ 캡션(작고 흐린 글씨)으로 지저분하지 않게 세부 이유 노출!
                    detail_str = " | ".join(res['details'])
                    st.caption(f"**[🔍 AI 포착 근거]** {detail_str}")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("📌 권장 매수가", f"{res['price']:,}원")
                    col2.metric("🎯 목표가", f"{target_p:,}원")
                    col3.metric("🚨 손절가", f"{stop_p:,}원")
                    st.markdown(f"👉 [네이버 금융 바로가기](https://finance.naver.com/item/main.naver?code={res['code']})")
                    st.markdown("---")
        else:
            st.warning("😭 현재 조건에 맞는 세력 주도주가 없습니다. 잠시 후 재충전됩니다.")
            
    countdown_placeholder = st.empty()
    for remaining in range(600, 0, -60):
        countdown_placeholder.write(f"🔄 {remaining // 60}분 뒤 자동으로 차트를 재분석하여 화면을 갱신합니다...")
        time.sleep(60)
        
    st.rerun()
