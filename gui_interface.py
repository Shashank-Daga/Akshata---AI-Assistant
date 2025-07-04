import sys
import threading
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QTextEdit, QLineEdit, QLabel, QHBoxLayout, QCheckBox)
from PyQt5.QtCore import Qt, QTimer

from core.cmds import exe_cmd
from core.logger import read_log
from core.speech import listen_to_user


class SmartAssistantGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Smart Assistant")
        self.setGeometry(100, 100, 700, 600)

        layout = QVBoxLayout()

        # Header and toggle
        header_layout = QHBoxLayout()
        self.voice_toggle = QCheckBox("Voice Input")
        self.voice_toggle.setChecked(False)
        header_layout.addWidget(QLabel("Smart Assistant"))
        header_layout.addStretch()
        header_layout.addWidget(self.voice_toggle)
        layout.addLayout(header_layout)

        # Chat area
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        layout.addWidget(self.chat_area)

        # Text input
        input_layout = QHBoxLayout()
        self.text_input = QLineEdit()
        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.handle_input)
        input_layout.addWidget(self.text_input)
        input_layout.addWidget(self.send_btn)
        layout.addLayout(input_layout)

        # Log viewer
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setFixedHeight(150)
        layout.addWidget(QLabel("Live Log Viewer"))
        layout.addWidget(self.log_area)

        # Timer for log updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_log)
        self.timer.start(3000)  # every 3 seconds

        self.setLayout(layout)

    def update_log(self):
        logs = read_log()
        self.log_area.setPlainText(logs)

    def handle_input(self):
        if self.voice_toggle.isChecked():
            self.chat_area.append("[User - Voice]: ...")
            threading.Thread(target=self.process_voice_command).start()
        else:
            query = self.text_input.text()
            if query:
                self.chat_area.append(f"[User]: {query}")
                response = exe_cmd(query)
                self.chat_area.append(f"[Assistant]: {response if response else 'I did not understand that.'}")
                self.text_input.clear()

    def process_voice_command(self):
        try:
            query = listen_to_user()
            self.chat_area.append(f"[User - Voice]: {query}")
            response = exe_cmd(query)
            self.chat_area.append(f"[Assistant]: {response if response else 'I did not understand that.'}")
        except Exception as e:
            self.chat_area.append(f"[Error]: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    assistant_gui = SmartAssistantGUI()
    assistant_gui.show()
    sys.exit(app.exec_())
