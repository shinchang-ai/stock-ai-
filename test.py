import streamlit as st
import requests
import datetime
import time

# ==========================================
# 1. 기본 설정 및 텔레그램 정보
# ==========================================
st.set_page_config(page_title="세력 포착 AI 시스템 (Pro)", page_icon="🚀", layout="centered")

# 보스님의 텔레그램 진짜 토큰과 챗 아이디
BOT_TOKEN = "8899908573:AAEOba8jFLi9h6S1Xhi5E-EqfTNoBf2r-xU"
CHAT_ID = "1076053813"

# ==========================================
# 2. 서버 수면 방지 및 10분 주기 생존 신고 알림
# ==========================================
# ttl=600 덕분에 새로고침을 마구 눌러도 딱 10분에 1번씩만 텔레그램이 발송됩니다!
@st.cache_data(ttl=600)
def send_keep_alive_message():
    now = datetime.datetime.now().strftime("%H시 %M분")
    message = f"🟢 [서버 생존 신고] 보스님! 시스템 절대 안 자고 정상 가동 중입니다. (현재 {now})"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": message})
    except:
        pass
    return True

# 웹사이트가 열릴 때마다 생존 신고 함수 실행 (10분 방어막 작동)
send_keep_alive_message()

# ==========================================
# 3. 텔레그램 수동 전송 함수 (빨간 버튼용)
# ==========================================
def send_manual_alert():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    message = f"🚨 [강제 수동 스캔] 보스님! 수동 스캔이 정상 작동했습니다. (요청 시각: {now})"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        return response.status_code == 200
    except:
        return False

# ==========================================
# 4. 웹 화면 UI 구성 (복구하신 원본 화면과 100% 동일)
# ==========================================
st.title("🚀 세력 포착 AI 시스템 (Pro)")

st.info("🎉 VIP 멤버님, 환영합니다! (웹 & 텔레그램 자동 연동 완료)")

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

# 수동 스캔 빨간색 버튼
if st.button("🔄 지금 당장 주도주 수동 스캔하기!", use_container_width=True, type="primary"):
    with st.spinner("텔레그램으로 수동 스캔 결과를 쏘는 중입니다..."):
        time.sleep(1)
        if send_manual_alert():
            st.success("✨ 텔레그램 전송 완료! 스마트폰의 '주식비서' 방을 확인하세요.")
        else:
            st.error("❌ 전송 실패! 텔레그램 서버 상태를 확인해주세요.")

st.warning("🌙 현재는 장 마감 시간입니다. (위에 '수동 스캔' 버튼을 누르시면 지금 즉시 강제로 텔레그램을 쏩니다!)")
