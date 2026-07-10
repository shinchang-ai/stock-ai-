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

def get_kst_now():
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID, 
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        requests.post(url, data=payload)
    except:
        pass

# ==========================================
# 2. 웹 화면 UI (뽀대 유지 + 가짜 종목 강력 경고)
# ==========================================
st.title("🚀 세력 포착 AI 시스템 (Pro)")
st.info("🎉 VIP 멤버님, 환영합니다! (웹 & 텔레그램 자동 연동 완료)")

# 🚨 강력 경고문 추가
st.error("⚠️ **[주의] 현재 화면에 표시된 종목은 시스템 테스트를 위한 가짜(마네킹) 데이터입니다. 절대 매수하지 마십시오! 실시간 찐 주도주는 텔레그램 알림으로만 전송됩니다.**")

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
# 3. 수동 스캔 테스트 버튼
# ==========================================
admin_password = st.text_input("🔑 관리자 암호 (텔레그램 전송용)", type="password")

if st.button("🔄 시스템 정상 작동 테스트 스캔!", use_container_width=True, type="primary"):
    with st.spinner("시스템 점검을 진행 중입니다..."):
        
        now_kst = get_kst_now()
        now_time_full = now_kst.strftime("%Y-%m-%d %H:%M:%S")
        
        # 🔥 [핵심] 더 이상 금호건설이 아닙니다. 매수할 수 없는 가짜 종목으로 고정!
        stock_name = "테스트용 가짜종목 (절대 매수금지)"
        stock_code = "000000"
        raw_price = 10500 
        formatted_price = f"{raw_price:,}원"
        market_cap_korean = "4천 6백 1억"
        formatted_volume = "15,234,560주" 
        formatted_trading_value = "2,540억 원" 
        ai_score = 98
        
        naver_investor_link = f"https://finance.naver.com/"
        naver_link = f"https://m.stock.naver.com/"

        header = "🚨 <b>[시스템 테스트] 텔레그램 전송 확인용</b> 🚨"
        alert_msg = "이 알림은 시스템이 정상 작동하는지 확인하기 위한 테스트 발송입니다. (매수 금지)"

        perfect_msg = f"""{header}

⏰ 포착시간: {now_time_full}

👑 종목명: <b>{stock_name}</b>
💵 현재가: <b>{formatted_price}</b>
📊 시가총액: {market_cap_korean}
📈 당일 거래량: {formatted_volume}
💰 당일 거래대금: {formatted_trading_value}
⭐ AI 세력 점수: {ai_score}점

⚠️ {alert_msg}"""
        
        time.sleep(1) 
        
        st.subheader("📊 시스템 테스트 결과 (가짜 데이터)")
        st.warning(f"""
**{header.replace('<b>','').replace('</b>','')}**

**⏰ 포착시간:** {now_time_full}

**👑 종목명:** ❌ **{stock_name}** ❌
**💵 현재가:** {formatted_price}
**📊 시가총액:** {market_cap_korean}
**📈 당일 거래량:** {formatted_volume}
**💰 당일 거래대금:** {formatted_trading_value}
**⭐ AI 세력 점수:** {ai_score}점

**🔎 찐 주도주 포착 근거 (샘플)**
* 🏢 외인/기관 추정 대량 매수세 유입 (+35점)
* 📈 20·60·120일선 완벽 정배열 돌파 (+35점)
* 👑 OBV 세력 매집 시그널 폭발 (+20점)
* 💰 당일 거래대금 압도적 상위 (+10점)
        """)
        
        if admin_password == "1234":
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": CHAT_ID, 
                "text": perfect_msg, 
                "parse_mode": "HTML",
                "disable_web_page_preview": True
            }
            res = requests.post(url, data=payload)
            if res.status_code == 200:
                st.success("✨ 테스트 완료! VIP 방으로 텔레그램 전송 성공!")
            else:
                st.error(f"❌ 전송 실패! (에러: {res.status_code})")
        else:
            if admin_password != "":
                st.error("❌ 비밀번호가 틀렸습니다.")

st.markdown("---")
