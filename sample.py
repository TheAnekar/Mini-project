import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('Hello Nigga')
window.setGeometry(100, 100, 300, 200)

label = QLabel('RespireX', window)
label.move(100, 80)

window.show()
sys.exit(app.exec_())
