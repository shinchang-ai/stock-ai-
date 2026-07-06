import streamlit as st
import requests
import datetime
import time
import FinanceDataReader as fdr

st.set_page_config(page_title="세력 포착 AI 시스템 (Pro)", page_icon="🚀", layout="centered")

def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    try: requests.post(url, data=payload)
    except: pass

if "is_tracking" not in st.session_state: st.session_state.is_tracking = False

st.markdown("## 🚀 세력 포착 AI 시스템 (Pro)")

if st.button("🔄 실시간 세력 포착 무한 추적 시작!", type="primary", use_container_width=True):
    st.session_state.is_tracking = True

if st.session_state.is_tracking:
    # 1. 시간 제어 엔진 (09:00~15:20)
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    if not ((now.hour == 9 and now.minute >= 0) or (now.hour < 15) or (now.hour == 15 and now.minute <= 20)):
        st.info("🌙 장 마감 시간이 지났습니다. 내일 오전 9시에 뵙겠습니다.")
        time.sleep(60); st.rerun()
    
    # 2. 종가 베팅 알람 (15:15~)
    if now.hour == 15 and now.minute >= 15:
        st.warning("🚨 [종가 베팅 시간] 지금은 종가 종목을 집중 분석합니다!")

    try:
        TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
        CHAT_ID = st.secrets["CHAT_ID"]
    except: st.error("🚨 텔레그램 세팅 오류!"); st.stop()

    detected_stocks = []
    df_krx = fdr.StockListing('KRX')
    # 3. 실전 필터링: 시총 3천억~1조 & 거래대금 500억 이상
    df_krx = df_krx[(df_krx['Marcap'] >= 300000000000) & (df_krx['Marcap'] <= 1000000000000)]
    df_krx = df_krx[df_krx['Amount'] >= 50000000000]
    top_active = df_krx.sort_values('Amount', ascending=False).head(30)
    
    for idx, row in top_active.iterrows():
        code, name = row['Code'], row['Name']
        df_chart = fdr.DataReader(code, (datetime.datetime.now() - datetime.timedelta(days=200)).strftime('%Y-%m-%d'))
        if len(df_chart) < 120: continue
        
        df_chart['MA20'] = df_chart['Close'].rolling(20).mean()
        df_chart['MA60'] = df_chart['Close'].rolling(60).mean()
        df_chart['MA120'] = df_chart['Close'].rolling(120).mean()
        last = df_chart.iloc[-1]
        
        if (last['Close'] > last['MA20'] > last['MA60'] > last['MA120']):
            detected_stocks.append({
                "name": name, "code": code, "amount": f"{int(row['Amount']/100000000):,}억", 
                "volume": f"{int(row['Volume']/10000):,}만주", "marcap": f"{int(row['Marcap']/100000000):,}억"
            })
        if len(detected_stocks) >= 3: break
    
    for stock in detected_stocks:
        msg = f"🚨 [주도주 포착]\n종목: {stock['name']}\n거래대금: {stock['amount']}\n거래량: {stock['volume']}\n시총: {stock['marcap']}"
        send_telegram_message(TELEGRAM_TOKEN, CHAT_ID, msg)
        st.write(f"### 👑 {stock['name']} | 💰 {stock['amount']} | 📊 {stock['volume']}")
        st.markdown("---")

    countdown_placeholder = st.empty()
    for i in range(600, 0, -1):
        countdown_placeholder.info(f"⏳ 다음 검색까지 {i//60}분 {i%60}초 남았습니다.")
        time.sleep(1)
    st.rerun()
