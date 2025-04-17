from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import socket

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "Unavailable"

class WatermarkWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setContentsMargins(10, 5, 10, 5)

        content_widget = QtWidgets.QWidget()
        content_layout = QtWidgets.QVBoxLayout()
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Static text label
        label = QtWidgets.QLabel("STUDENT NAME : #########")
        label.setStyleSheet("color: white; font-size: 18pt; font-weight: bold;")
        content_layout.addWidget(label)

        # Dynamic IP label
        self.ip_label = QtWidgets.QLabel()
        self.ip_label.setStyleSheet("color: white; font-size: 10pt;")
        content_layout.addWidget(self.ip_label)

        content_widget.setLayout(content_layout)
        main_layout.addWidget(content_widget)

        self.close_btn = QtWidgets.QPushButton("✕")
        self.close_btn.setFixedSize(24, 24)
        self.close_btn.setVisible(False)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 0, 0, 180);
                color: white;
                border: none;
                font-weight: bold;
                font-size: 12pt;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 220);
            }
        """)
        self.close_btn.clicked.connect(self.close)
        main_layout.addWidget(self.close_btn)

        self.setLayout(main_layout)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 100);
                border: 1px solid white;
                border-radius: 5px;
            }
        """)

        self.move(100, 100)
        self.dragging = False
        self.drag_offset = QtCore.QPoint()

        self.update_ip()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_ip)
        self.timer.start(5000)  # 5 seconds

    def update_ip(self):
        ip = get_ip_address()
        formatted_ip = "IP address: {}".format(ip)
        if self.ip_label.text() != formatted_ip:
            self.ip_label.setText(formatted_ip)


    def enterEvent(self, event):
        self.close_btn.setVisible(True)

    def leaveEvent(self, event):
        self.close_btn.setVisible(False)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MiddleButton:
            self.dragging = True
            self.drag_offset = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() & QtCore.Qt.MiddleButton:
            self.move(event.globalPos() - self.drag_offset)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MiddleButton:
            self.dragging = False
            event.accept()

app = QtWidgets.QApplication(sys.argv)
window = WatermarkWindow()
window.show()
sys.exit(app.exec_())
