# --- (전체 코드 중 이 부분만 교체해서 덮어쓰기 하세요!) ---

if st.button("🔄 실시간 세력 포착 무한 추적 시작!") or 'running' in st.session_state:
    st.session_state['running'] = True
    
    # 1. 멋진 진행률 바와 분석 근거 노출
    progress_text = "AI 분석 가동 중... 잠시만 기다려주세요."
    my_bar = st.progress(0, text=progress_text)
    
    tasks = ["전 종목 수급 스캔", "거래대금 필터링", "볼린저밴드 계산", "세력 매집 감지", "랭킹 산정"]
    for i, task in enumerate(tasks):
        time.sleep(0.5)
        my_bar.progress((i + 1) * 20, text=f"분석 중: {task}...")
    my_bar.empty() # 분석 끝나면 바 사라짐
    
    # 2. 분석 실행
    stocks = run_stock_analysis()
    
    # 3. 결과 표시
    if stocks:
        st.success(f"🔥 총 {len(stocks)}개의 주도주를 포착했습니다!")
        for res in stocks:
            with st.container():
                st.markdown(f"## {res['rank']} {res['name']} ({res['code']})")
                st.markdown(f"**🌟 추천:** `{res['action']}` (점수: {res['score']}점)")
                st.caption(f"🔍 근거: {' | '.join(res['details'])}")
                st.metric("📌 매수가", f"{res['price']:,}원")
                st.markdown("---")
        time.sleep(10) # 종목이 있을 땐 10초 대기 후 새로고침
    else:
        st.warning("😭 현재 조건에 맞는 주도주가 없습니다. 30초 뒤 재분석합니다.")
        time.sleep(30) # 종목이 없을 땐 30초 동안 우아하게 쉬기
        
    st.rerun()
