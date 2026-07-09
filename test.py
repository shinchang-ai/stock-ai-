import streamlit as st
import requests
import datetime
import time

# ==========================================
# 1. 페이지 기본 설정 및 텔레그램 정보
# ==========================================
st.set_page_config(page_title="세력 포착 AI 시스템 (Pro)", page_icon="🚀", layout="centered")

# 회원님 토큰과 챗 아이디가 박혀있는 완전체 정보
BOT_TOKEN = "8899908573:AAEOba8jFLi9h6S1Xhi5E-EqfTNoBf2r-xU"
CHAT_ID = "1076053813"

# ==========================================
# 2. 텔레그램 강제 전송 함수
# ==========================================
def send_force_alert():
    message = "🚨 [강제 테스트] 보스님! VWAP 하단 지지선 포착 시스템이 정상 가동 중입니다!"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        return response.status_code == 200
    except:
        return False

# ==========================================
# 3. 웹 화면 UI (깃허브 에디터 붙여넣기용)
# ==========================================
st.title("🚀 세력 포착 AI 시스템 (Pro)")
st.markdown("---")

st.subheader("🚨 텔레그램 강제 알림 테스트")

if st.button("🚀 텔레그램으로 강제 알림 쏘기", use_container_width=True):
    with st.spinner("텔레그램 서버로 신호를 쏘는 중입니다..."):
        if send_force_alert():
            st.success("✨ 전송 성공! 지금 텔레그램 앱 '주식비서' 방을 확인해보세요!")
            st.balloons()
        else:
            st.error("전송 실패! 깃허브에서 다시 확인해보겠습니다.")
