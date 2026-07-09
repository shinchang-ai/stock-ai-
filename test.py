import streamlit as st
import requests
import datetime
import time
import FinanceDataReader as fdr

# ==========================================
# 1. 페이지 기본 설정
# ==========================================
st.set_page_config(page_title="세력 포착 AI 시스템 (Pro)", page_icon="🚀", layout="centered")

# ==========================================
# 2. 핵심 함수 모음
# ==========================================
def format_korean_money(value):
    """숫자를 한국어 금액 단위(천, 백, 억)로 변환하는 함수"""
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
    """텔레그램 봇으로 메시지를 쏘는 함수"""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    try: 
        response = requests.post(url, data=payload)
        return response.status_code == 200 # 성공하면 True 반환
    except Exception as e: 
        return False

# ==========================================
# 3. 웹 화면 UI 및 동작 로직
# ==========================================
st.title("🚀 세력 포착 AI 시스템 (Pro)")
st.markdown("---")

st.subheader("🚨 텔레그램 강제 전송 테스트 구역")
st.info("아래에 봇 토큰과 챗 아이디를 입력하고 버튼을 누르면 스마트폰으로 강제 알림이 전송됩니다.")

# 봇 토큰과 챗 아이디 입력받기 (비밀번호 처리)
bot_token = st.text_input("텔레그램 봇 토큰 (Bot Token)", type="password", placeholder="예: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz")
chat_id = st.text_input("챗 아이디 (Chat ID)", type="password", placeholder="예: 12345678")

# 버튼 생성
if st.button("🚀 텔레그램 억지로 쏴보기 (강제 검출)", use_container_width=True):
    if bot_token and chat_id:
        with st.spinner("텔레그램으로 강제 전송 중입니다..."):
            # 텔레그램으로 보낼 테스트 메시지 내용
            test_message = f"""
🚨 **[VWAP 극강의 눌림목 포착] (강제 테스트)** 🚨

🎯 **종목:** [피에스케이] (031980)
⏱ **검출 시각:** {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
💸 **수급 조건:** 50억 이상 뭉텅이 수급 유입 완료
📉 **타점:** VWAP 검정색 하단선 정확히 터치!

➡️ 지금 당장 8282 호가창을 확인하세요!
"""
            # 메시지 전송 실행
            success = send_telegram_message(bot_token, chat_id, test_message)
            time.sleep(1) # 부드러운 화면 처리를 위한 1초 대기
            
            if success:
                st.success("✨ 전송 완벽하게 성공! 지금 텔레그램 앱이 울렸는지 확인해보세요!")
                st.balloons() # 축하 애니메이션
            else:
                st.error("전송 실패! 봇 토큰이나 챗 아이디가 정확한지 다시 한번 확인해주세요.")
    else:
        st.warning("봇 토큰과 챗 아이디를 모두 입력하셔야 쏠 수 있습니다!")
