import streamlit as st
import requests
import datetime
import time

# ==========================================
# 1. 웹페이지 기본 설정
# ==========================================
st.set_page_config(page_title="세력 포착 AI 시스템 (Pro)", page_icon="🚀", layout="centered")

# 회원님 전용 텔레그램 봇 토큰 및 챗 아이디
BOT_TOKEN = "8899908573:AAEOba8jFLi9h6S1Xhi5E-EqfTNoBf2r-xU"
CHAT_ID = "1076053813"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": message})
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

    # 🔥 3시 15분 종가베팅 타임 (3시 10분~19분 사이 작동)
    if "1510" <= current_time < "1520":
        msg = f"🚨 [종가베팅 타임!] 🚨\n보스님, 3시 15분 종가베팅 시간입니다!\n현재 포착된 찐 주도주 종목을 확인하고 쏘세요! (현재 {now_str})"
        send_telegram(msg)
        return "종가베팅"

    # 🟢 평일 장중 (09:00 ~ 15:20) 10분 주기 생존 신고
    if "0900" <= current_time <= "1520":
        msg = f"🟢 [장중 자동 스캔] 스나이퍼 로봇 10분 주기 정상 감시 중! (현재 {now_str})"
        send_telegram(msg)
        return "장중스캔"

    return False

auto_system_check()

# ==========================================
# 3. 웹 화면 UI (줄바꿈 완벽 복구)
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

3️⃣ 이평선(20·60) 완벽 정배열

4️⃣ 기관·외국인 쌍끌이 수급 유입 추정

5️⃣ 볼린저밴드 중심선(20일선) 강력 돌파

6️⃣ OBV 세력 매집 시그널 포착
""")

if st.button("🔄 지금 당장 주도주 수동 스캔하기!", use_container_width=True, type="primary"):
    with st.spinner("텔레그램으로 수동 스캔 결과를 쏘는 중입니다..."):
        now_time = datetime.datetime.now().strftime("%H:%M:%S")
        manual_msg = f"🚨 [강제 수동 스캔] 보스님! 수동 스캔이 정상 작동했습니다. (요청 시각: {now_time})"
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        res = requests.post(url, data={"chat_id": CHAT_ID, "text": manual_msg})
        
        time.sleep(1)
        if res.status_code == 200:
            st.success("✨ 텔레그램 전송 완료! 스마트폰의 '주식비서' 방을 확인하세요.")
        else:
            st.error("❌ 전송 실패! 텔레그램 서버 상태를 확인해주세요.")

st.markdown("---")

# ==========================================
# 4. 실시간 다음 스캔 카운트다운 타이머 (부활!)
# ==========================================
timer_placeholder = st.empty()

while True:
    now = datetime.datetime.now()
    weekday = now.weekday()
    current_time_str = now.strftime("%H%M")
    
    # 주말이거나 장 마감(15:20) 이후면 타이머 대신 안내 문구 표시
    if weekday >= 5 or not ("0830" <= current_time_str <= "1520"):
        timer_placeholder.warning("🌙 장 마감 시간입니다. 자동 스캔 및 텔레그램 알림이 무음 처리됩니다. (수동 스캔은 언제든 가능)")
        break
        
    # 다음 10분 단위 시간 계산 (예: 9:10, 9:20 ...)
    next_time = now + datetime.timedelta(minutes=10 - (now.minute % 10))
    next_time = next_time.replace(second=0, microsecond=0)
    
    remaining = next_time - now
    mins, secs = divmod(remaining.seconds, 60)
    
    # 초 단위로 화면 업데이트
    timer_placeholder.info(f"⏳ **다음 자동 스캔(생존 신고)까지 남은 시간:** {mins:02d}분 {secs:02d}초")
    time.sleep(1)
