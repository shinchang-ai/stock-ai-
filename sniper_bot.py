import sys
import datetime
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit
from PyQt5.QAxContainer import QAxWidget

# 🔥 텔레그램 봇 토큰과 회원님의 '개인 고유 아이디' 완벽 적용!
TELEGRAM_BOT_TOKEN = "8899908573:AAEOba8jFLi9h6S1Xhi5E-EqfTNoBf2r-xU" 
TELEGRAM_CHAT_ID = "1076053813"

class SniperBot(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 1. 윈도우 창 설정
        self.setWindowTitle("🚀 보스 전용 세력 포착 스나이퍼 봇 v1.0")
        self.setGeometry(300, 300, 500, 600) # x, y, 너비, 높이
        
        # 2. 메인 화면 레이아웃 잡기
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)
        
        # 3. 로그(글씨)가 찍힐 까만 창 만들기
        self.log_window = QTextEdit()
        self.log_window.setReadOnly(True)
        self.log_window.setStyleSheet("background-color: black; color: #00FF00; font-size: 10pt;")
        self.layout.addWidget(self.log_window)
        
        # 4. 로그인 버튼 만들기
        self.btn_login = QPushButton("🔑 키움증권 OpenAPI 자동 로그인")
        self.btn_login.setStyleSheet("background-color: #ff4b4b; color: white; font-weight: bold; font-size: 12pt; height: 40px;")
        self.btn_login.clicked.connect(self.login)
        self.layout.addWidget(self.btn_login)

        # 🔥 4-1. 텔레그램 강제 테스트 버튼 만들기
        self.btn_test = QPushButton("🚀 [강제 테스트] VWAP 방으로 텔레그램 쏘기!")
        self.btn_test.setStyleSheet("background-color: #008CBA; color: white; font-weight: bold; font-size: 12pt; height: 40px;")
        self.btn_test.clicked.connect(self.force_test_telegram)
        self.layout.addWidget(self.btn_test)
        
        # 5. 키움 OpenAPI 모듈 연결 (가장 중요!)
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        
        # 로그인 결과가 나오면 'login_slot' 함수로 연결
        self.kiwoom.OnEventConnect.connect(self.login_slot)
        
        self.log("시스템 부팅 완료! [강제 테스트] 버튼을 눌러 텔레그램을 확인해보세요.")

    def log(self, message):
        """로그 창에 시간과 함께 메시지를 찍어주는 마법의 함수"""
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_window.append(f"[{now}] {message}")

    def login(self):
        """키움 로그인 창을 띄우는 명령"""
        self.log("키움증권 서버에 연결을 시도합니다...")
        self.kiwoom.dynamicCall("CommConnect()")

    def login_slot(self, err_code):
        """로그인이 성공했는지 실패했는지 알려주는 곳"""
        if err_code == 0:
            self.log("✅ 키움증권 서버에 성공적으로 접속되었습니다!! (VIP 로그인 완료)")
            # 성공하면 버튼 글씨를 바꿔버립니다!
            self.btn_login.setText("✅ 로그인 완료 (대기 중...)")
            self.btn_login.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; font-size: 12pt; height: 40px;")
        else:
            self.log(f"🚨 로그인 실패 (에러코드: {err_code})")

    # 🔥 텔레그램 강제 전송용 함수
    def force_test_telegram(self):
        self.log("텔레그램 강제 전송 테스트를 시작합니다...")
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 영웅문 4가지 조건식 중 하나에 걸렸다고 가정하고 가짜 메시지 세팅
        test_msg = f"""🚨 [VWAP 지지선 돌파 포착] 🚨

🎯 포착 조건식: 노란색 강세패턴 우량주 (테스트)
⏰ 포착시간: {now_time}

👑 종목명: 삼성전자 (005930)
💸 현재가: 85,000원
📈 등락률: +3.5%

⚠️ 본 알림은 봇 작동 확인을 위한 강제 테스트입니다!"""
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": test_msg}
        
        try:
            res = requests.post(url, data=payload)
            if res.status_code == 200:
                self.log("✅ '실시간 vwap라인 매수 bot' 방으로 텔레그램 전송 대성공!!")
            else:
                self.log(f"❌ 전송 실패! 토큰을 확인하세요. (에러코드: {res.status_code})")
        except Exception as e:
            self.log(f"❌ 전송 중 컴퓨터 에러 발생: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    bot = SniperBot()
    bot.show()
    sys.exit(app.exec_())
