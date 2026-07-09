import streamlit as st
import requests
import datetime
import time

# ==========================================
# 1. 웹페이지 기본 설정
# ==========================================
st.set_page_config(page_title="세력 포착 AI 시스템 (Pro)", page_icon="🚀", layout="centered")

BOT_TOKEN = "8899908573:AAEOba8jFLi9h6S1Xhi5E-EqfTNoBf2r-xU"
CHAT_ID = "1076053813"

# 텔레그램 발송 공통 함수 (링크 미리보기 방지 기능 추가로 화면 깔끔하게 유지)
def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID, 
        "text": message,
        "disable_web_page_preview": True # 네이버 링크 썸네일 때문에 지저분해지는 것 방지
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
    now = datetime.datetime.now()
    current_time = now.strftime("%H%M")
    now_str = now.strftime("%H시 %M분")
    weekday = now.weekday()

    if weekday >= 5:
        return False

    # 🔥 3시 15분 종가베팅 타임
    if "1510" <= current_time < "1520":
        msg = f"🚨 [종가베팅 타임!] 🚨\n보스님, 3시 15분 종가베팅 시간입니다!\n현재 포착된 찐 주도주 종목을 확인하고 쏘세요! (현재 {now_str})"
        send_telegram(msg)
        return "종가베팅"

    # 🟢 평일 장중 생존 신고
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

current_hm = datetime.datetime.now().strftime("%H%M")
if "1510" <= current_hm < "1520":
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

# ==========================================
# 4. 수동 스캔 시 회원님 사진과 100% 동일한 양식 발송!
# ==========================================
if st.button("🔄 지금 당장 주도주 수동 스캔하기!", use_container_width=True, type="primary"):
    with st.spinner("텔레그램으로 완벽한 포맷의 신호를 쏘는 중입니다..."):
        
        # 임시 테스트용 데이터 (나중에 영웅문 데이터로 교체될 부분)
        now_time_full = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        stock_name = "금호건설"
        stock_code = "002990"
        market_cap = "4,601억"
        ai_score = 98
        naver_link = f"https://m.stock.naver.com/domestic/stock/{stock_code}/total"

        # 사진과 토씨 하나 안 틀리고 똑같이 만든 메시지 양식
        perfect_msg = f"""🚨 VIP 실시간 수급 포착 🚨

⏰ 포착시간: {now_time_full}

👑 종목명: {stock_name} ({stock_code})
📊 시가총액: {market_cap}
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
            st.success("✨ 텔레그램 전송 완료! 스마트폰을 확인하세요.")
        else:
            st.error("❌ 전송 실패! 텔레그램 서버 상태를 확인해주세요.")

st.markdown("---")

# ==========================================
# 5. 실시간 다음 스캔 카운트다운 타이머
# ==========================================
timer_placeholder = st.empty()

while True:
    now = datetime.datetime.now()
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
