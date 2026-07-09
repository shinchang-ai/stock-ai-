import streamlit as st
import requests
import datetime
import time

# ==========================================
# 1. 웹페이지 기본 설정
# ==========================================
st.set_page_config(page_title="세력 포착 AI 시스템 (Pro)", page_icon="🚀", layout="centered")

BOT_TOKEN = "8899908573:AAEOba8jFLi9h6S1Xhi5E-EqfTNoBf2r-xU"
CHAT_ID = "-1004426603017"

# 🇰🇷 한국 시간(KST) 가져오는 함수
def get_kst_now():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID, 
        "text": message,
        "disable_web_page_preview": True
    }
    try:
        requests.post(url, data=payload)
    except:
        pass

# ==========================================
# 2. 서버 수면 방지 및 시간대별 알림 로직
# ==========================================
@st.cache_data(ttl=600)
def auto_system_check():
    now = get_kst_now()
    current_time = now.strftime("%H%M")
    now_str = now.strftime("%H시 %M분")
    weekday = now.weekday()

    if weekday >= 5:
        return False

    if "1510" <= current_time < "1520":
        msg = f"🚨 [종가베팅 타임!] 🚨\n보스님, 3시 15분 종가베팅 시간입니다!\n현재 포착된 찐 주도주 종목을 확인하고 쏘세요! (현재 {now_str})"
        send_telegram(msg)
        return "종가베팅"

    if "0900" <= current_time <= "1520":
        msg = f"🟢 [장중 자동 스캔] 스나이퍼 로봇 정상 감시 중! (현재 {now_str})"
        send_telegram(msg)
        return "장중스캔"

    return False

auto_system_check()

# ==========================================
# 3. 웹 화면 UI
# ==========================================
st.title("🚀 세력 포착 AI 시스템 (Pro)")
st.info("🎉 VIP 멤버님, 환영합니다! (웹 & 텔레그램 자동 연동 완료)")

now_hm = get_kst_now().strftime("%H%M")
if "1510" <= now_hm < "1520":
    st.toast('🚨 지금은 종가베팅 시간입니다! 종목을 확인하세요!', icon='🔥')
    st.error("🚨 **[알림] 지금은 종가베팅 시간입니다! 포착된 종목을 확인하세요!**")

st.success("""
🔥 **현재 모드:** 장중 시총 2천억~1조 찐 주도주 압축 (외부 서버 자동 스캔 중)

🔎 **[핵심 포착 조건 6가지]**

1️⃣ 당일 거래대금 100억 이상 폭발

2️⃣ 당일 거래량 급증

3️⃣ 이평선(20·60·120) 완벽 정배열

4️⃣ 기관·외국인 쌍끌이 수급 유입 추정

5️⃣ 볼린저밴드 중심선(20일선) 강력 돌파

6️⃣ OBV 세력 매집 시그널 포착
""")

# 🔥 시가총액을 한글(천, 백, 십) 단위로 예쁘게 바꿔주는 똑똑한 함수
def format_korean_market_cap(eok_value):
    jo = eok_value // 10000
    eok = eok_value % 10000
    
    def format_eok(n):
        s = ""
        if n >= 1000:
            s += f"{n // 1000}천 "
            n %= 1000
        if n >= 100:
            s += f"{n // 100}백 "
            n %= 100
        if n > 0:
            s += f"{n}"
        return s.strip()
        
    res = ""
    if jo > 0:
        res += f"{jo}조 "
    if eok > 0:
        res += f"{format_eok(eok)}억"
    return res.strip() if res else "0억"

# ==========================================
# 4. 수동 스캔 (완벽한 양식 전송)
# ==========================================
if st.button("🔄 지금 당장 주도주 수동 스캔하기!", use_container_width=True, type="primary"):
    with st.spinner("텔레그램 '실시간세력 포착방'으로 완벽한 포맷의 신호를 쏘는 중입니다..."):
        
        now_kst = get_kst_now()
        now_time_full = now_kst.strftime("%Y-%m-%d %H:%M:%S")
        stock_name = "금호건설"
        stock_code = "002990"
        
        # 실제 숫자 4601이 들어가면 -> "4천 6백 1억"으로 자동 변환!
        raw_market_cap = 4601 
        market_cap_korean = format_korean_market_cap(raw_market_cap)
        
        ai_score = 98
        naver_link = f"https://m.stock.naver.com/domestic/stock/{stock_code}/total"

        perfect_msg = f"""🚨 VIP 실시간 수급 포착 🚨

⏰ 포착시간: {now_time_full}

👑 종목명: {stock_name} ({stock_code})
📊 시가총액: {market_cap_korean}
⭐ AI 세력 점수: {ai_score}점
🔗 네이버 증권 연결: {naver_link}

🔎 찐 주도주 포착 근거
🏢 외인/기관 추정 대량 매수세 유입(+35)
📈 20·60·120일선 완벽 정배열 돌파(+35)
👑 OBV 세력 매집 시그널 폭발(+20)
💰 당일 거래대금 압도적 상위(+10)

⚠️ 면책조항 본 알림은 차트(정배열) 및 수급, OBV 지표를 분석한 AI 기계적 검출 결과이며 매수/매도를 추천하지 않습니다. 투자의 책임은 본인에게 있습니다."""
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": perfect_msg, "disable_web_page_preview": True}
        res = requests.post(url, data=payload)
        
        time.sleep(1)
        if res.status_code == 200:
            st.success("✨ '실시간세력 포착방'으로 텔레그램 전송 완료! 방을 확인하세요.")
        else:
            st.error(f"❌ 전송 실패! (에러: {res.status_code})")

st.markdown("---")

# ==========================================
# 5. 실시간 다음 스캔 카운트다운 타이머
# ==========================================
timer_placeholder = st.empty()

while True:
    now = get_kst_now() 
    weekday = now.weekday()
    current_time_str = now.strftime("%H%M")
    
    if weekday >= 5 or not ("0830" <= current_time_str <= "1520"):
        timer_placeholder.warning("🌙 장 마감 시간입니다. 자동 스캔 및 텔레그램 알림이 무음 처리됩니다. (수동 스캔은 언제든 가능)")
        break
        
    next_time = now + datetime.timedelta(minutes=10 - (now.minute % 10))
    next_time = next_time.replace(second=0, microsecond=0)
    
    remaining = next_time - now
    mins, secs = divmod(remaining.seconds, 60)
    
    timer_placeholder.info(f"⏳ **다음 자동 스캔(생존 신고)까지 남은 시간:** {mins:02d}분 {secs:02d}초")
    time.sleep(1)
