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
    """텔레그램 봇으로 메시지를 쏘는 핵심 함수"""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, data=payload)
        return response.status_code == 200
    except:
        return False

def check_vwap_and_alert(token, chat_id, code, name, current_price, vwap_bottom):
    """현재가가 VWAP 하단 지지선에 도달했는지 확인하고 텔레그램 발송"""
    # 핵심 로직: 현재가가 VWAP 하단선(검정선) 이하로 떨어졌을 때만 작동
    if current_price <= vwap_bottom:
        message = f"""
🚨 **[VWAP 극강 눌림목 포착]** 🚨
🎯 **종목:** {name} ({code})
💸 **현재가:** {current_price:,}원
📉 **상태:** 분봉 VWAP 하단 지지선(검정선) 도달!
➡️ 신속히 8282 호가창을 확인하세요!
"""
        return send_telegram_message(token, chat_id, message)
    return False

# ==========================================
# 3. 웹 화면 UI 및 동작 로직
# ==========================================
st.title("🚀 세력 포착 AI 시스템 (Pro)")
st.markdown("---")

st.subheader("🚨 분봉 VWAP 지지선 텔레그램 테스트")
st.info("실제 '보스 전용 스나이퍼 봇 v8.17'에 이식하기 전, 웹에서 로직을 테스트하는 완전체 코드입니다.")

# 입력 폼 구성 (두 줄로 깔끔하게 배치)
col1, col2 = st.columns(2)
with col1:
    bot_token = st.text_input("텔레그램 봇 토큰", type="password")
    stock_name = st.text_input("테스트 종목명", value="피에스케이")
    current_p = st.number_input("실시간 현재가", value=25000, step=100)
with col2:
    chat_id = st.text_input("챗 아이디", type="password")
    stock_code = st.text_input("종목코드", value="031980")
    vwap_b = st.number_input("VWAP 하단선 (검정선)", value=25500, step=100)

st.markdown("---")

# 실행 버튼
if st.button("🚀 VWAP 지지선 도달 시뮬레이션 쏘기", use_container_width=True):
    if bot_token and chat_id:
        with st.spinner("VWAP 로직 판별 및 전송 중..."):
            time.sleep(0.5) # 부드러운 UI 처리
            
            # 현재가가 VWAP 하단선보다 같거나 작으면 전송
            if current_p <= vwap_b:
                success = check_vwap_and_alert(bot_token, chat_id, stock_code, stock_name, current_p, vwap_b)
                if success:
                    st.success(f"✨ [조건 만족] 현재가({current_p:,}원)가 VWAP하단({vwap_b:,}원)에 닿았습니다. 텔레그램 전송 완료!")
                    st.balloons()
                else:
                    st.error("전송 실패! 텔레그램 토큰이나 챗 아이디가 정확한지 확인하세요.")
            else:
                # 현재가가 아직 지지선 위에 있으면 쏘지 않음
                st.warning(f"⚠️ [조건 미달] 현재가({current_p:,}원)가 아직 VWAP하단({vwap_b:,}원) 위에 있습니다. 텔레그램을 쏘지 않습니다.")
    else:
        st.error("봇 토큰과 챗 아이디를 모두 입력하셔야 테스트가 가능합니다.")
