import streamlit as st
import FinanceDataReader as fdr
from ta.volume import money_flow_index
import pandas as pd
import time
import requests

# 🔑 내 텔레그램 정보
TOKEN = '8899908573:AAEOba8jFLi9h6S1Xhi5E-EqfTNoBf2r-xU'
CHAT_ID = '1076053813'

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'HTML'}
    requests.get(url, params=params)

# ==========================================
# 🎨 스마트폰/웹 화면 꾸미기 (Streamlit 뷰어)
# ==========================================
st.set_page_config(page_title="세력 포착 AI 시스템", page_icon="📈")

st.title("🚀 신창 세력 포착 AI 시스템 v1.0")
st.write("이 어플은 24시간 클라우드 서버에서 작동하며, 세력 진입 종목을 감지해 내 폰으로 즉시 발송합니다.")

# 암호 걸기 기능
password = st.text_input("🔑 VIP 인증 암호를 입력하세요", type="password")

if password == "대박가자":
    st.success("인증 성공! VIP 전용 기능을 사용할 수 있습니다.")
    
    # 🔍 검색 시작 버튼 만들기
    if st.button("🔥 지금 주식 시장 세력 검색 시작"):
        status_text = st.empty()
        status_text.write("🚀 실시간 코스닥 100개 종목 스캔을 시작합니다...")
        send_message("🤖 [서버 알림] VIP 사용자가 세력 조건 검색을 시작했습니다.")
        
        krx_list = fdr.StockListing('KOSDAQ')
        stocks_to_scan = krx_list[:100]
        
        pockets = []
        
        for index, row in stocks_to_scan.iterrows():
            code = row['Code']
            name = row['Name']
            
            status_text.write(f"🔎 현재 검색 중인 종목: **{name}** ({code})")
            
            try:
                df = fdr.DataReader(code, '2024-01-01')
                if len(df) < 15: continue

                df['MFI'] = money_flow_index(df['High'], df['Low'], df['Close'], df['Volume'], window=14)
                df['거래대금'] = df['Close'] * df['Volume']

                today = df.iloc[-1]
                yesterday = df.iloc[-2]

                cond_volume = today['Volume'] > yesterday['Volume'] 
                cond_money = today['거래대금'] >= 10000000000       
                cond_mfi = today['MFI'] >= 50                         

                if cond_volume and cond_money and cond_mfi:
                    naver_link = f"https://m.stock.naver.com/domestic/stock/{code}/total"
                    
                    msg = f"🚨 <b>[세력 포착!!] <a href='{naver_link}'>{name} ({code})</a></b>\n"
                    msg += f"▶ MFI: {today['MFI']:.1f}\n"
                    msg += f"▶ 거래대금: {today['거래대금']/100000000:.0f}억원"
                    
                    send_message(msg)
                    pockets.append(f"✨ <b>{name}</b> (MFI: {today['MFI']:.1f})")
                    
                time.sleep(0.05)
            except:
                pass
                
        status_text.write("✅ 모든 종목 검색이 완료되었습니다!")
        send_message("✅ [검색 완료] 모든 VIP 조건 검색이 끝났습니다. 성투하세요! 💰")
        
        if pockets:
            st.balloons()
            st.write("### 🎯 오늘 포착된 세력 주식 명단")
            for p in pockets:
                st.write(p, unsafe_allow_html=True)
        else:
            st.write("오늘 포착된 종목이 없습니다.")

elif password != "":
    st.error("❌ 암호가 틀렸습니다. 올바른 VIP 암호를 입력해 주세요.")