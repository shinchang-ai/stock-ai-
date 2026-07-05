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

# 창고에서 빼서 바로 실행하도록 수정!
cookie_manager = stx.CookieManager()

# 프론트엔드 쿠키 로딩 대기 딜레이 제거
if cookie_manager.get_all() is None:
    st.stop() 

# 대표님이 바쁘셔도 승인번호가 1시간 동안 지워지지 않는 서버 공유 보관소!
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
    /* 모바일 폰 화면 크기에 맞춰 글자 및 픽셀 자동 축소 디자인 */
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
            if obv.iloc[-1] > obv.rolling(window=20).mean().iloc[-1]: score += 30; details.append("
