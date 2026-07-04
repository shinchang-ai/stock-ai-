import streamlit as st
import FinanceDataReader as fdr
import pandas as pd
from ta.volatility import BollingerBands
from ta.volume import OnBalanceVolumeIndicator
import datetime

# --- 1. 페이지 및 어플 설정 ---
st.set_page_config(page_title="신창 세력 포착 AI", page_icon="🚀", layout="centered")

# --- 2. 유료화 (7일 무료 체험 락 기능) ---
EXPIRATION_DATE = datetime.date(2026, 7, 11)
today = datetime.date.today()

st.title("🚀 신창 세력 포착 AI 시스템 (Pro)")

if today > EXPIRATION_DATE:
    st.error("🔒 무료 체험 기간이 만료되었습니다.")
    st.write("계속 사용하시려면 VIP 인증 암호를 입력하세요.")
    vip_password = st.text_input("VIP 암호", type="password")
    if vip_password != "신창대박":  
        st.stop() 
    else:
        st.success("✅ VIP 인증 완료! 시스템을 정상 가동합니다.")
else:
    st.info(f"💡 무료 체험 기간: {EXPIRATION_DATE} 까지 (이후 유료 전환됩니다)")

# --- 3. 사용자 UI (직장인 맞춤형 모드 선택) ---
st.markdown("### 🎯 탐색 모드 선택")
mode = st.radio("어떤 매매를 준비하시겠습니까?", 
                ("🔥 실시간 수급 포착 (장중 단타/스윙)", 
                 "🚨 찐 종가베팅 발굴 (오후 3시 10분 권장)"))

if st.button("🔍 세력 주도주 검색 시작!"):
    with st.spinner("AI가 전 종목의 세력 매집(OBV)과 볼린저밴드를 분석 중입니다... (약 10~20초 소요)"):
        try:
            krx = fdr.StockListing('KRX')
            krx = krx[(krx['Close'] >= 1000) & (~krx['Name'].str.contains('우$|우B$|우C$|스팩|리츠'))]
            
            target_stocks = krx.sort_values('Volume', ascending=False).head(100)
            
            results = []
            progress_bar = st.progress(0)
            total = len(target_stocks)
            
            # 여기서 에러 났던 카운터를 수정했습니다! (current_step 추가)
            current_step = 0 
            
            for idx, row in target_stocks.iterrows():
                current_step += 1 # 1, 2, 3... 정상적으로 숫자가 올라가게 수정
                
                code = row['Code']
                name = row['Name']
                
                df = fdr.DataReader(code, datetime.date.today() - datetime.timedelta(days=180))
                if len(df) < 120:
                    progress_bar.progress(current_step / total)
                    continue
                
                close = df['Close'].iloc[-1]
                volume = df['Volume'].iloc[-1]
                
                trading_val = close * volume
                if trading_val < 50000000000: 
                    progress_bar.progress(current_step / total)
                    continue
                    
                ma120 = df['Close'].rolling(window=120).mean().iloc[-1]
                if close < ma120:
                    progress_bar.progress(current_step / total)
                    continue
                
                score = 0
                
                ma20_vol = df['Volume'].rolling(window=20).mean().iloc[-2]
                vol_ratio = volume / ma20_vol if ma20_vol > 0 else 0
                if vol_ratio >= 5: score += 30
                elif vol_ratio >= 3: score += 20
                elif vol_ratio >= 2: score += 10
                
                bb = BollingerBands(close=df['Close'], window=20, window_dev=2)
                bb_upper = bb.bollinger_hband().iloc[-1]
                if close >= bb_upper: score += 40
                elif close >= bb.bollinger_mavg().iloc[-1]: score += 20
                
                obv = OnBalanceVolumeIndicator(close=df['Close'], volume=df['Volume']).on_balance_volume()
                obv_ma20 = obv.rolling(window=20).mean().iloc[-1]
                if obv.iloc[-1] > obv_ma20: score += 30
                
                if score >= 60:
                    results.append({
                        '종목명': name,
                        '코드': code,
                        '점수': score,
                        '현재가': close,
                    })
                
                # 수정한 정상적인 로딩률 업데이트 적용!
                progress_bar.progress(current_step / total)
            
            progress_bar.empty()
            
            if len(results) > 0:
                results = sorted(results, key=lambda x: x['점수'], reverse=True)
                st.success(f"🔥 분석 완료! 총 {len(results)}개의 초강력 세력주가 포착되었습니다.")
                
                for res in results:
                    score = res['점수']
                    price = res['현재가']
                    
                    if "종가베팅" in mode:
                        target_price = int(price * 1.05) 
                        stop_price = int(price * 0.97)   
                        mode_text = "🌙 [종가베팅]"
                    else:
                        target_price = int(price * 1.08) 
                        stop_price = int(price * 0.95)   
                        mode_text = "☀️ [장중수급]"
                    
                    with st.container():
                        st.markdown(f"## {mode_text} {res['종목명']} ({res['코드']})")
                        st.markdown(f"**🌟 세력 랭킹 점수:** `{score}점 / 100점`")
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric("📌 권장 매수가", f"{price:,}원")
                        col2.metric("🎯 목표가", f"{target_price:,}원")
                        col3.metric("🚨 손절가", f"{stop_price:,}원")
                        
                        st.markdown(f"👉 [네이버 금융에서 관련 뉴스 & 호가창 바로보기](https://finance.naver.com/item/main.naver?code={res['코드']})")
                        st.markdown("---") 
            else:
                st.warning("😭 현재 세력 조건(대금 500억, 매집 흔적)을 만족하는 찐 주도주가 없습니다. 억지로 매매하지 마세요!")

        except Exception as e:
            st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
