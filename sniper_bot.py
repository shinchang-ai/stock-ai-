import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit
from PyQt5.QAxContainer import QAxWidget
import datetime

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
        
        # 5. 키움 OpenAPI 모듈 연결 (가장 중요!)
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        
        # 로그인 결과가 나오면 'login_slot' 함수로 연결
        self.kiwoom.OnEventConnect.connect(self.login_slot)
        
        self.log("시스템 부팅 완료! [로그인] 버튼을 눌러주십시오.")

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    bot = SniperBot()
    bot.show()
    sys.exit(app.exec_())
