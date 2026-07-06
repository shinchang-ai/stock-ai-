import streamlit as st
import requests
import datetime
import time
import FinanceDataReader as fdr

# --- 1. 시간 제어 엔진 ---
def is_market_hours():
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    market_open = now.replace(hour=9, minute=0, second=0, microsecond=0)
    market_close = now.replace(hour=15, minute=20, second=0, microsecond=0)
    return market_open <= now <= market_close

def is_closing_time():
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    return now.hour == 15 and now.minute >= 15

# [ ... 이전 UI/함수 코드 동일 ... ]
# (텔레그램 함수 등은 그대로 유지하시고 버튼 누른 후 로직만 교체하십시오!)

if st.session_state.is_tracking:
    # 1. 장중 시간 체크
    if not is_market_hours():
        st.info("🌙 현재는 장중 시간이 아닙니다. 내일 오전 9시부터 다시 가동됩니다!")
        time.sleep(60)
        st.rerun()

    # 2. 종가 베팅 시간 알람 (15:15 이후)
    if is_closing_time():
        st.error("🚨 팝업! 지금은 종가 베팅 시간입니다! 종가 종목 분석을 시작합니다!")
        # 종가 베팅용 종목 스캔 로직 추가... (이후 로직은 아래에서 수행)

    # ... [종목 스캔 로직] ...
