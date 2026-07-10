import streamlit as st
import requests
import datetime
import time

st.set_page_config(page_title="세력 포착 수동 리모컨", page_icon="🚀", layout="centered")

BOT_TOKEN = "8899908573:AAEOba8jFLi9h6S1Xhi5E-EqfTNoBf2r-xU"
CHAT_ID = "-1004426603017"

def get_kst_now():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))

st.title("🚀 VIP 텔레그램 수동 전송 리모컨")
st.error("⚠️ [주의] 이 화면은 자동 검색기가 아닙니다! 보스님이 직접 찐 주도주를 발굴했을 때 VIP 방으로 수동 전송하는 화면입니다.")

st.subheader("📝 VIP 방에 보낼 종목 직접 입력")
# 가짜 데이터 삭제! 보스님이 직접 입력하도록 입력칸 생성
input_stock_name = st.text_input("👑 종목명 입력", placeholder="예: 삼성전자")
input_stock_code = st.text_input("🔢 종목코드 입력", placeholder="예: 005930")
input_price = st.text_input("💵 현재가 입력", placeholder="예: 80,000원")

# 🚨 텔레그램 전송을 통제할 관리자 비밀번호
admin_password = st.text_input("🔑 관리자 암호 (텔레그램 전송용)", type="password")

if st.button("🔄 위 종목으로 VIP방 텔레그램 쏘기!", use_container_width=True, type="primary"):
    if not input_stock_name or not input_stock_code:
        st.warning("⚠️ 종목명과 종목코드를 반드시 입력해주세요!")
    else:
        with st.spinner("텔레그램 전송 중..."):
            now_time_full = get_kst_now().strftime("%Y-%m-%d %H:%M:%S")
            naver_investor_link = f"https://finance.naver.com/item/frgn.naver?code={input_stock_code}"
            
            # 수동 전송용 메시지
            perfect_msg = f"""🚨 <b>VIP 실시간 수급 포착 (수동발굴)</b> 🚨

⏰ 시간: {now_time_full}
👑 종목명: <b>{input_stock_name} ({input_stock_code})</b>
💵 현재가: <b>{input_price}</b>

<a href="{naver_investor_link}">📊 [누가 사고 있나? 세력 수급 바로가기 (클릭)]</a>

⚠️ 차트 및 수급 확인 후 진입하세요!"""
            
            if admin_password == "1234":
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                payload = {"chat_id": CHAT_ID, "text": perfect_msg, "parse_mode": "HTML", "disable_web_page_preview": True}
                res = requests.post(url, data=payload)
                if res.status_code == 200:
                    st.success(f"✨ '{input_stock_name}' VIP 방으로 텔레그램 전송 완료!")
                else:
                    st.error("❌ 전송 실패!")
            else:
                st.error("❌ 비밀번호가 틀렸습니다.")
