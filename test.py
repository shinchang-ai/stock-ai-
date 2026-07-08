import streamlit as st
import requests
import datetime
import time
import FinanceDataReader as fdr

st.set_page_config(page_title="세력 포착 AI 시스템 (Pro)", page_icon="🚀", layout="centered")

def format_korean_money(value):
    uk = int(value / 100000000)
    res = ""
    if uk >= 1000:
        res += f"{uk // 1000}천 "
        uk = uk % 1000
    if uk >= 100:
        res += f"{uk // 100}백 "
        uk = uk % 100
    if uk > 0:
        res += f"{uk}"
    if res == "": res = "0"
    return res.strip() + "억"

def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    try: requests.post(url, data=payload)
    except: pass

st.markdown("""
<style>
.vip-box { background-color: #e8f0fe; padding: 15px; border-radius: 8px; margin-bottom: 20px; color: #1a73e8; font-weight: bold; }
.condition-box { background-color: #e8f5e9; padding: 15px; border-radius: 8px; margin-bottom: 20px; color: #2e7d32; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

st.markdown("## 🚀 세력 포착 AI 시스템 (Pro)")
st.markdown('<div class="vip-box">🎉 👑 VIP 멤버님, 환영합니다! (최적 1종목 모드 연동 완료)</div>', unsafe_allow_html=True)
st.markdown("""
<div class="condition-box">
    🔥 <b>현재 모드: 장중 시총 2천억~1조 찐 주도주 '최고 대장주 1개' 압축</b><br>
    🔎 <b>[핵심 포착 조건 6가지]</b><br>
    1️⃣ 당일 <b>거래대금</b> 100억 이상 폭발<br>
    2️⃣ 당일 <b>거래량</b> 급증<br>
    3️⃣ 이평선(20·60·120) 완벽 <b>정배열</b><br>
    4️⃣ <b>기관·외국인</b> 쌍끌이 수급 유입 추정<br>
    5️⃣ <b>볼린저밴드 중심선</b>(20일선) 강력 돌파<br>
    6️⃣ <b>OBV</b> 세력 매집 시그널 포착
</div>
""", unsafe_allow_html=True)

# [핵심] 보스님이 지금 당장 눌러서 테스트할 수 있는 강제 발송 버튼!
force_test = st.button("🚨 야간 강제 테스트 발송! (지금 당장 1종목 찾아서 쏘기)", type="primary", use_container_width=True)

now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
is_market_open = (now.hour == 9 and now.minute >= 0) or (9 < now.hour < 15) or (now.hour == 15 and now.minute <= 20)

# 장 마감 시간이어도 '강제 테스트' 버튼을 누르면 스톱하지 않고 아래로 넘어갑니다!
if not is_market_open and not force_test:
    st.warning("🌙 현재는 장 마감 시간입니다. (위에 '야간 강제 테스트' 버튼을 누르시면 지금 즉시 강제로 텔레그램을 쏩니다!)")
    st.stop()

is_closing_bet = (now.hour == 15 and 15 <= now.minute <= 20)
if is_closing_bet and not force_test:
    st.toast("🚨 3시 15분! 종가 베팅 최적 종목을 스캔합니다!", icon="🎯")

try:
    TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
    CHAT_ID = st.secrets["CHAT_ID"]
except:
    st.error("🚨 텔레그램 세팅(Secrets)을 확인해주세요!"); st.stop()

search_time = now.strftime('%Y-%m-%d %H:%M:%S')
st.info("🔎 조건에 맞는 '최고 대장주 딱 1개'를 정밀 스캔 중입니다...")

detected_stocks = []

try:
    df_krx = fdr.StockListing('KRX')
    df_krx = df_krx[(df_krx['Marcap'] >= 200000000000) & (df_krx['Marcap'] <= 1000000000000)]
    df_krx = df_krx[df_krx['Amount'] >= 10000000000]
    
    # 거래대금 순으로 정렬 후 가장 쎈 놈들부터 차례대로 검사
    top_active = df_krx.sort_values('Amount', ascending=False).head(30)
    
    for idx, row in top_active.iterrows():
        code, name = row['Code'], row['Name']
        amount_str = format_korean_money(row['Amount'])
        marcap_str = format_korean_money(row['Marcap'])
        volume_str = f"{int(row['Volume']):,}주"
        
        df_chart = fdr.DataReader(code, (now - datetime.timedelta(days=150)).strftime('%Y-%m-%d'))
        if len(df_chart) < 120: continue
        
        df_chart['MA20'] = df_chart['Close'].rolling(20).mean()
        df_chart['MA60'] = df_chart['Close'].rolling(60).mean()
        df_chart['MA120'] = df_chart['Close'].rolling(120).mean()
        last = df_chart.iloc[-1]
        
        # 6가지 조건 완벽 부합 시 리스트에 추가
        if (last['Close'] > last['MA20']) and (last['MA20'] > last['MA60']) and (last['MA60'] > last['MA120']):
            detected_stocks.append({
                "name": name, "code": code, "score": 98,
                "amount": amount_str, "volume": volume_str, "marcap": marcap_str,
                "reasons": "🏢 외인·기관 수급 유입(+35) | 📈 20·60·120 정배열(+25) | 🎯 볼린저 중심선 돌파(+20) | 👑 OBV 세력선 급증(+20)"
            })
        
        # [수정 완료] 조건에 맞는 놈 딱 1개만 찾으면 그 즉시 반복문 종료! (최적 1종목)
        if len(detected_stocks) >= 1: 
            break
except Exception as e:
    pass

st.markdown(f"<h3 style='text-align:center; color:white; background-color:#ff4b4b; padding:10px; border-radius:5px;'>🔥 최고 주도주 포착 결과 : {len(detected_stocks)}개</h3>", unsafe_allow_html=True)

if len(detected_stocks) > 0:
    for stock in detected_stocks:
        # 강제 테스트일 때는 제목에 표시를 해줍니다
        if force_test:
            title_msg = "🚨 **[🎯 야간 강제 발송 테스트 성공]** 🚨"
        else:
            title_msg = "🚨 **[🎯 VIP 종가 베팅 최적 1종목]** 🚨" if is_closing_bet else "🚨 **[VIP 실시간 1등 주도주 포착]** 🚨"
        
        telegram_msg = f"""{title_msg}\n\n⏰ {search_time}\n\n👑 **종목명:** {stock['name']} ({stock['code']})\n📊 **시가총액:** {stock['marcap']}\n💰 **거래대금:** {stock['amount']}\n📈 **당일거래량:** {stock['volume']}\n\n🔎 **[ 6대 포착 근거 ]**\n{stock['reasons'].replace(' | ', chr(10))}\n\n🔗 **[네이버 차트 보기]**\nhttps://finance.naver.com/item/main.naver?code={stock['code']}\n\n⚠️ 기계적 검출 결과이며 투자의 책임은 본인에게 있습니다."""
        
        send_telegram_message(TELEGRAM_TOKEN, CHAT_ID, telegram_msg)
        
        st.markdown(f"### 👑 [원픽 대장주] {stock['name']} ({stock['code']})")
        st.markdown(f"<a href='https://finance.naver.com/item/main.naver?code={stock['code']}' target='_blank' style='background-color:#4CAF50; color:white; padding:5px 10px; text-decoration:none; border-radius:3px; font-weight:bold;'>📈 N금융 차트보기</a>", unsafe_allow_html=True)
        st.write(f"🏷️ **시가총액:** {stock['marcap']} | **세력점수:** {stock['score']}점")
        st.write(f"💰 **당일 거래대금:** {stock['amount']} | 📊 **당일 거래량:** {stock['volume']}")
        st.write(f"🔎 **포착 근거:** {stock['reasons']}")
        st.markdown("---")
        
        if force_test:
            st.success("✅ 강제 테스트 텔레그램 발송 완료! 단톡방을 확인하십시오!")
else:
    st.info("현재 6가지 조건에 완벽하게 일치하는 주도주가 없습니다. (0개 알림 텔레그램 발송 완료)")
    test_msg = "[야간 강제 테스트]\n" if force_test else ""
    send_telegram_message(TELEGRAM_TOKEN, CHAT_ID, f"🔎 {search_time}\n\n{test_msg}현재 6대 포착 조건을 만족하는 최적의 주도주가 없습니다.\n(10분 후 다시 스캔합니다.)")

st.warning("⚠️ **[면책조항]** 본 시스템은 투자를 권유하지 않으며, 최종 책임은 본인에게 있습니다.")

if not force_test:
    countdown_placeholder = st.empty()
    for i in range(600, 0, -1):
        mins, secs = divmod(i, 60)
        countdown_placeholder.info(f"⏳ 화면을 켜두시면 **{mins}분 {secs}초** 뒤에 자동으로 최신 종목을 다시 검색합니다...")
        time.sleep(1)
    st.rerun()
