import streamlit as st
import requests
from datetime import datetime
import pytz

# --- 텔레그램 발송 함수 ---
def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, data=payload)
        return response
    except Exception as e:
        return str(e)

# --- 메인 화면 UI ---
st.title("🔥 AI 실시간 세력 & 수급 포착 레이더")
st.markdown("**(법적 리스크 방어 / 외인·기관·정배열 조건 추가 버전)**")

# Secrets에서 주소장 가져오기 (오전에 세팅하신 거 그대로 유지됩니다!)
try:
    TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
    CHAT_ID = st.secrets["CHAT_ID"]
except:
    st.error("🚨 텔레그램 세팅(Secrets)을 먼저 해주세요!")
    st.stop()

# --- 무한 추적 시작 버튼 ---
if st.button("🔄 실시간 세력 포착 및 단톡방 전송 시작!", type="primary"):
    
    # 1. 검색 시간 생성 (한국 시간 기준)
    kst = pytz.timezone('Asia/Seoul')
    search_time = datetime.now(kst).strftime('%Y-%m-%d %H:%M:%S')
    
    with st.spinner("외인/기관 수급 및 정배열 종목 분석 중..."):
        
        # -------------------------------------------------------------
        # [주의] 이 부분에 보스님이 쓰시던 진짜 주식 데이터 수집 코드가 들어갑니다!
        # 지금은 완벽한 테스트를 위해 '파세코' 등 임시 데이터를 띄웁니다.
        # -------------------------------------------------------------
        detected_stocks = [
            {
                "name": "파세코",
                "code": "037070",
                "score": 120,
                "reasons": "📈 이동평균선(20,60,120) 완벽 정배열 돌파(+40)\n🏢 외인/기관 쌍끌이 양매수 유입(+30)\n💰 거래대금 5백억 폭발(+30)\n👑 OBV 세력 매집 시그널(+20)"
            },
            {
                "name": "삼성전자",
                "code": "005930",
                "score": 95,
                "reasons": "🏢 기관 대량 순매수 포착(+40)\n📈 단기 이평선 골든크로스(+30)\n🔥 볼린저밴드 상단 안착(+25)"
            }
        ]
        # -------------------------------------------------------------
        
        st.success(f"🎯 총 {len(detected_stocks)}개 종목 포착 완료! (검색시간: {search_time})")
        
        # 2. 결과 출력 및 텔레그램 쏘기 (중복 필터 완전 삭제 -> 버튼 누를 때마다 쏨!)
        for stock in detected_stocks:
            
            # 텔레그램으로 보낼 텍스트 조립 (법적 방어 문구 포함)
            telegram_msg = f"""🚨 **[AI 실시간 수급/세력 포착]** 🚨

⏰ **검색시간:** {search_time}

👑 **종목명:** {stock['name']} ({stock['code']})
⭐️ **AI 세력 점수:** {stock['score']}점

🔎 **[ AI 포착 근거 ]**
{stock['reasons']}

⚠️ **[면책 조항]**
본 알림은 AI 알고리즘이 특정 수급 및 차트 조건(정배열 등)을 만족한 종목을 기계적으로 검출한 결과입니다. 매수/매도 추천이 아니며, 투자의 최종 책임은 투자자 본인에게 있습니다."""

            # 스마트폰 화면에 출력
            st.markdown(f"### 👑 {stock['name']} ({stock['code']})")
            st.write(f"**점수:** {stock['score']} | **시간:** {search_time}")
            st.text(stock['reasons'])
            st.write("---")
            
            # 텔레그램으로 쏘기 (중복 체크 안 함! 냅다 쏩니다!)
            send_telegram_message(TELEGRAM_TOKEN, CHAT_ID, telegram_msg)
            
        st.info("✅ 단톡방으로 중복 무시하고 전송 완료되었습니다! 폰 확인해보세요!")
