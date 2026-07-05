import streamlit as st
import FinanceDataReader as fdr
import pandas as pd
from ta.volatility import BollingerBands
from ta.volume import OnBalanceVolumeIndicator
import datetime
import requests
import time
import urllib.parse
import random

# 영구 쿠키 매니저 부품
import extra_streamlit_components as stx

st.set_page_config(page_title="세력 포착 AI 시스템", page_icon="🚀", layout="centered")

# 영구 쿠키 매니저 실행
@st.cache_resource
def get_cookie_manager():
    return stx.CookieManager()

cookie_manager = get_cookie_manager()

# 프론트엔드 쿠키 로딩 대기 딜레이 제거
if cookie_manager.get_all() is None:
    st.stop() 

# ⭐ 대표님 요청 반영: 대표님이 바쁘셔도 승인번호가 1시간 동안 지워지지 않는 서버 공유 보관소!
@st.cache_resource
def get_approval_db():
    return {}

st.markdown("""
    <style>
    div[data-testid="stStaleNode"] { opacity: 1 !important; filter: none !important; transition: none !important; }
    .naver-btn {
        background-color: #03c75a;
        color: white !important;
        padding: 2px 8px;
        border-radius: 5px;
        text-decoration: none;
        font-size: 0.5em;
        vertical-align: middle;
        margin-left: 10px;
    }
    .disclaimer {
        text-align: center;
        color: #999999;
        font-size: 0.75em;
        padding: 20px 0;
        margin-top: 30px;
        border-top: 1px solid #eeeeee;
    }
    .kakao-warning {
        background-color: #ffe0e0;
        color: #d32f2f;
        padding: 15px;
        border-radius: 10px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        border: 2px solid #ff4b4b;
    }
    /* ⭐ 대표님 요청 반영: 모바일 폰 화면 크기에 맞춰 글자 및 픽셀 자동 축소 디자인 */
    @media (max-width: 640px) {
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.25rem !important; }
        h3 { font-size: 1.05rem !important; display: inline-block !important; }
        div[data-testid="stMetricValue"] { font-size: 1.3rem !important; }
        div[data-testid="stMetricLabel"] { font-size: 0.75rem !important; }
        .stButton>button { width: 100% !important; font-size: 0.9rem !important; padding: 8px !important; }
        .naver-btn { display: inline-block !important; margin-top: 5px !important; margin-left: 0px !important; padding: 4px 8px !important; font-size: 0.65em !important; }
    }
    </style>
    """, unsafe_allow_html=True)

BOT_TOKEN = "8899908573:AAEOba8jFLi9h6S1Xhi5E-EqfTNoBf2r-xU"
ADMIN_ID = "1076053813"         
CHANNEL_ID = "-1004426603017"   

EXPIRATION_DATE = datetime.date(2026, 7, 11)
today = datetime.date.today()

now_kst = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
current_time = now_kst.time()

is_jongbe = datetime.time(15, 15) <= current_time <= datetime.time(15, 20)
mode_text = "🌙 [종가베팅]" if is_jongbe else "☀️ [장중수급]"

is_cron_job = (st.query_params.get("job") == "cron")

def get_rank_info(score):
    if score >= 90: return "👑 [최상위 대장주]", "강력하게 풀매수!"
    elif score >= 80: return "🔥 [강력 추천]", "공격적인 분할매수!"
    else: return "🔔 [관심 추천]", "시세를 예의주시!"

def format_marcap(marcap):
    uk = int(marcap // 100000000)
    if uk >= 10000:
        jo = uk // 10000
        remain_uk = uk % 10000
        if remain_uk > 0: return f"{jo}조 {remain_uk:,}억"
        else: return f"{jo}조"
    else:
        return f"{uk:,}억"

@st.cache_data(ttl=600)
def get_target_stocks():
    krx = fdr.StockListing('KRX')
    krx = krx[(krx['Close'] >= 1000) & (~krx['Name'].str.contains('우$|우B$|우C$|스팩|리츠'))]
    krx = krx[(krx['Marcap'] >= 100000000000) & (krx['Marcap'] <= 5000000000000)]
    return krx.sort_values('Amount', ascending=False).head(50)

def run_stock_analysis(ui_box=None):
    results = []
    try:
        if ui_box: ui_box.info("📡 시총 1천억~5조 알짜 주도주 압축 스캔 중...")
        target_stocks = get_target_stocks()
        total = len(target_stocks)
        
        for idx, (index, row) in enumerate(target_stocks.iterrows()):
            code, name, marcap = row['Code'], row['Name'], row['Marcap']
            
            industry = row.get('Industry', '')
            sector = row.get('Sector', '')
            final_sector = industry if pd.notna(industry) and str(industry).strip() != '' else (sector if pd.notna(sector) and str(sector).strip() != '' else "분류없음")
                
            if ui_box: ui_box.warning(f"⏳ AI 정밀 분석 중 [{idx+1}/{total}] : 🔍 **{name}**")
            
            df = fdr.DataReader(code, today - datetime.timedelta(days=120))
            if len(df) < 60: continue 
            
            close, volume = df['Close'].iloc[-1], df['Volume'].iloc[-1]
            tr_val = close * volume 
            if tr_val < 50000000000: continue 
            
            ma20_vol = df['Volume'].rolling(window=20).mean().iloc[-2]
            vol_ratio = volume / ma20_vol if ma20_vol > 0 else 0
            bb = BollingerBands(close=df['Close'], window=20, window_dev=2)
            bb_upper = bb.bollinger_hband().iloc[-1]
            
            if vol_ratio < 1.5 and close < bb_upper: continue 
            
            score = 0; details = []
            if tr_val >= 100000000000: score += 30; details.append("💰거래대금 1천억 돌파(+30)")
            elif tr_val >= 50000000000: score += 20; details.append("💰거래대금 5백억 돌파(+20)")
                
            if vol_ratio >= 5: score += 30; details.append("🔥거래량 5배 폭발(+30)")
            elif vol_ratio >= 3: score += 20; details.append("🔥거래량 3배 급증(+20)")
            elif vol_ratio >= 2: score += 10; details.append("🔥거래량 2배 증가(+10)")
            
            if close >= bb_upper: score += 40; details.append("📈볼린저밴드 상단돌파(+40)")
            elif close >= bb.bollinger_mavg().iloc[-1]: score += 20; details.append("📈볼린저밴드 중심선 안착(+20)")
            
            obv = OnBalanceVolumeIndicator(close=df['Close'], volume=df['Volume']).on_balance_volume()
            if obv.iloc[-1] > obv.rolling(window=20).mean().iloc[-1]: score += 30; details.append("👑OBV 세력매집 포착(+30)")
            
            if score >= 70:
                rank_title, action = get_rank_info(score)
                marcap_str = format_marcap(marcap)
                results.append({'name': name, 'code': code, 'score': score, 'price': close, 'details': details, 'rank': rank_title, 'action': action, 'marcap_str': marcap_str, 'sector': final_sector})
        
        if ui_box: ui_box.success("✅ 스캔 완료!")
        time.sleep(0.5)
        if ui_box: ui_box.empty()
        return sorted(results, key=lambda x: x['score'], reverse=True)
    except Exception as e:
        if ui_box: ui_box.error("네트워크 지연! 잠시 후 재시도합니다.")
        return []

if is_cron_job:
    if today > EXPIRATION_DATE: st.stop()
    
    if not (datetime.time(9, 0) <= current_time <= datetime.time(15, 20)):
        st.stop()
        
    stocks = run_stock_analysis()
    if stocks:
        for res in stocks:
            target_p = int(res['price'] * (1.05 if is_jongbe else 1.08))
            stop_p = int(res['price'] * (0.97 if is_jongbe else 0.95))
            
            msg = f"🚨 {mode_text} <a href='https://finance.naver.com/item/main.naver?code={res['code']}'>{res['name']}({res['code']})</a>\n🏢 시총: {res['marcap_str']} | 🏷️ {res['sector']}\n{res['rank']} {res['action']}\n⭐ 총점: {res['score']}점\n📝 근거: {' / '.join(res['details'])}\n📌 매수: {res['price']:,}원\n🎯 목표: {target_p:,}원\n🚨 손절: {stop_p:,}원"
            
            requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHANNEL_ID}&text={urllib.parse.quote(msg)}&parse_mode=HTML")
    st.stop()


# --- ⭐ 완벽 통제 로그인 (10년 영구 자동 로그인 및 타임아웃 1시간 연장!) ---
saved_vip_name = cookie_manager.get(cookie="vip_name")

if saved_vip_name:
    st.session_state.auth = True
    st.session_state.req_name = saved_vip_name
else:
    if "auth" not in st.session_state:
        st.session_state.auth = False
        st.session_state.req_name = ""

if not st.session_state.auth:
    st.title("🔒 세력 포착 AI (VIP 전용)")
    
    st.markdown("""
    <div class="kakao-warning">
        🚨 잠깐! 현재 <b>카카오톡 내부 창</b>으로 열고 계신가요?<br><br>
        카톡 내부 창은 닫는 순간 자동로그인 기록이 <b>모든 삭제</b>됩니다!<br>
        화면 우측 하단의 점 3개(…)를 누르고 반드시<br>
        <b>👉 [다른 브라우저로 열기] (크롬, 사파리, 삼성인터넷) 👈</b><br>
        로 접속하셔야 평생 자동 로그인이 유지됩니다!
    </div>
    """, unsafe_allow_html=True)
    
    st.error("⚠️ 외부인 접속 통제 구역입니다. 관리자의 승인이 있어야만 접속 가능합니다.")
    
    approval_db = get_approval_db()
    default_name = st.session_state.get("input_name", "")
    req_name = st.text_input("접속자 이름 (예: 김영해)", value=default_name).strip()
    
    active_otp = None
    if req_name:
        if req_name in approval_db:
            otp_info = approval_db[req_name]
            # ⭐ 1시간(3600초) 이내면 대표님이 다른 일 하셔도 번호가 살아있음!
            if (datetime.datetime.now() - otp_info["time"]).total_seconds() < 3600:
                active_otp = otp_info["otp"]
            else:
                del approval_db[req_name]
                
    if active_otp is None:
        st.info("✋ [신규 접속] 본인의 이름을 적고 승인을 요청하세요. (최초 1회만 인증)")
        if st.button("승인 요청 보내기"):
            if req_name == "":
                st.warning("이름을 꼭 입력해주세요!")
            else:
                otp_code = str(random.randint(1000, 9999))
                approval_db[req_name] = {"otp": otp_code, "time": datetime.datetime.now()}
                st.session_state["input_name"] = req_name
                
                msg = f"🚨 [VIP 앱 접속 요청]\n👤 누군가 접속을 시도합니다: {req_name}\n🔑 이 사람을 허락하시려면 다음 4자리 코드를 알려주세요: {otp_code}\n⏰ (코드는 1시간 동안 무조건 안전하게 유지됩니다.)"
                requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={ADMIN_ID}&text={urllib.parse.quote(msg)}")
                
                st.success("✅ 승인 요청이 전송되었습니다! 아래에 전달받은 코드를 입력하세요.")
                st.rerun()
    else:
        # ⭐ 대표님이 늦게 봐도 지인이 다시 들어와서 이름만 치면 이 화면으로 바로 복구됨!
        st.success(f"📌 [{req_name}]님에 대한 승인 요청이 활성화되어 있습니다. (1시간 동안 유효)")
        entered_otp = st.text_input("승인 코드 4자리", type="password")
        
        if st.button("승인 확인 및 자동 로그인 등록"):
            if entered_otp == active_otp:
                expire_date = datetime.datetime.now() + datetime.timedelta(days=3650)
                cookie_manager.set("vip_name", req_name, expires_at=expire_date)
                
                if req_name in approval_db:
                    del approval_db[req_name]
                    
                st.session_state.auth = True
                st.session_state.req_name = req_name
                st.rerun()
            else:
                st.error("❌ 코드가 틀렸습니다.")
                
        if st.button("이름 바꾸거나 다시 요청하기"):
            if req_name in approval_db:
                del approval_db[req_name]
            st.session_state["input_name"] = ""
            st.rerun()

    st.markdown("---")
    
    st.warning("👑 [친한 지인/관리자 전용] 마스터 키를 입력하면 즉시 접속되며, 이후 자동 로그인됩니다.")
    master_pwd = st.text_input("마스터 비밀번호", type="password")
    if st.button("프리패스 접속"):
        if master_pwd == "7777": 
            expire_date = datetime.datetime.now() + datetime.timedelta(days=3650)
            cookie_manager.set("vip_name", "👑 VIP 멤버", expires_at=expire_date)
            
            st.session_state.auth = True
            st.session_state.req_name = "👑 VIP 멤버"
            st.rerun()
        else:
            st.error("❌ 마스터 코드가 일치하지 않습니다.")
            
    st.stop()
# ------------------------------------------------

# 메인 화면
st.title("🚀 신창 세력 포착 AI 시스템 (Pro)")
st.info(f"🎉 **{st.session_state.req_name}**님, 환영합니다! (자동 로그인 완료)")

if is_jongbe: st.error("🌙 현재 모드: 찐 종가베팅 발굴")
else: st.success("🔥 현재 모드: 장중 500억 이상 찐 주도주 압축")

if st.button("🔄 실시간 세력 포착 무한 추적 시작!") or 'running' in st.session_state:
    st.session_state['running'] = True
    
    status_box = st.empty() 
    stocks = run_stock_analysis(status_box)
    
    if stocks:
        st.markdown(f"<div style='text-align: center; background-color: #ff4b4b; color: white; padding: 15px; border-radius: 10px; margin-bottom: 20px;'><h2>🔥 현재 포착된 찐 주도주 : 총 {len(stocks)}개</h2></div>", unsafe_allow_html=True)
        
        for res in stocks:
            target_p = int(res['price'] * (1.05 if is_jongbe else 1.08))
            stop_p = int(res['price'] * (0.97 if is_jongbe else 0.95))
            
            st.markdown(f"<h3 style='margin-bottom:0px;'>{res['rank']} {res['name']} ({res['code']}) "
                        f"<a href='https://finance.naver.com/item/main.naver?code={res['code']}' target='_blank' class='naver-btn'>📈 N금융 차트보기</a></h3>"
                        f"<span style='font-size: 0.8em; color: #888888;'>시총: {res['marcap_str']} | 🏷️ {res['sector']}</span>", unsafe_allow_html=True)
            
            st.markdown(f"**🌟 AI 액션:** `{res['action']}` (세력점수: {res['score']}점)")
            st.caption(f"🔍 포착 근거: {' | '.join(res['details'])}")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("📌 매수가", f"{res['price']:,}원")
            col2.metric("🎯 목표가", f"{target_p:,}원")
            col3.metric("🚨 손절가", f"{stop_p:,}원")
            st.markdown("---")
    else:
        st.warning("😭 현재 AI 기준을 통과한 강력한 주도주가 없습니다.")
        
    st.markdown("""
        <div class="disclaimer">
            ⚠️ <b>투자 유의사항 (면책 조항)</b><br>
            본 시스템이 제공하는 모든 정보는 AI 알고리즘에 기반한 단순 참고용 데이터이며, 절대적인 수익을 보장하지 않습니다.<br>
            종목 매수/매도에 대한 최종 판단과 모든 법적/재무적 책임은 전적으로 투자자 본인에게 귀속됩니다.
        </div>
    """, unsafe_allow_html=True)
        
    countdown_box = st.empty()
    for i in range(600, 0, -1):
        mins, secs = divmod(i, 60)
        countdown_box.info(f"⏰ 다음 AI 스캔까지 대기 중... ({mins}분 {secs:02d}초 남음)")
        time.sleep(1)
        
    st.rerun()
