import sys
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox, QCheckBox
)
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='Ashraf',
            password='miniproject', 
            database='respirex_db',
            auth_plugin='mysql_native_password'
        )
        return conn
    except Error as e:
        QMessageBox.critical(None, "Database Error", f"Error connecting to MySQL:\n{e}")
        return None
    
def setup_clock(self, layout):
    self.time_label = QLabel()
    self.time_label.setStyleSheet("font-size: 18px; color: white;")
    layout.addWidget(self.time_label)

    timer = QTimer(self)
    timer.timeout.connect(self.update_time)
    timer.start(1000)  # update every second

    self.update_time()

def update_time(self):
    current_time = QTime.currentTime().toString("hh:mm:ss AP")
    self.time_label.setText(f"🕒 {current_time}")

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(600, 300, 300, 200)
        self.showFullScreen()

        layout = QVBoxLayout()

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.show_pass_checkbox = QCheckBox("Show Password")
        

        self.show_pass_checkbox.toggled.connect(self.toggle_password_visibility)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.login)

        layout.addWidget(QLabel("Login to RespireX"))
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.show_pass_checkbox)
        layout.addWidget(login_btn)

        self.setLayout(layout)

        def toggle_password_visibility(self):
            self.password_input.setEchoMode(
            QLineEdit.Normal if self.show_pass_checkbox.isChecked() else QLineEdit.Password
        )

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                QMessageBox.information(self, "Success", "Login Successful!")
            else:
                QMessageBox.warning(self, "Error", "Invalid Credentials!")
        else:
            QMessageBox.critical(self, "Error", "Database connection failed!")

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
        self.setGeometry(600, 300, 300, 200)
        self.showFullScreen()

        layout = QVBoxLayout()

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.show_pass_checkbox = QCheckBox("Show Password")

        register_btn = QPushButton("Register")
        register_btn.clicked.connect(self.register)

        layout.addWidget(QLabel("Register on RespireX"))
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.show_pass_checkbox)
        layout.addWidget(register_btn)

        self.setLayout(layout)

    def register(self):
        email = self.email_input.text()
        password = self.password_input.text()

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users (email, password) VALUES (%s, %s)', (email, password))
                conn.commit()
                cursor.close()
                conn.close()
                QMessageBox.information(self, "Success", "Registration Successful! Please Login.")
            except mysql.connector.IntegrityError:
                QMessageBox.warning(self, "Error", "Email already exists!")
        else:
            QMessageBox.critical(self, "Error", "Database connection failed!")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RespireX")
        self.setGeometry(500, 250, 300, 200)
        self.showFullScreen()

        layout = QVBoxLayout()

        welcome_label = QLabel("Welcome to RespireX")
        welcome_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        login_button = QPushButton("Login")
        login_button.setStyleSheet(button_style)
        register_button = QPushButton("Register")
        register_button.setStyleSheet(button_style)
        login_button.setCursor(Qt.PointingHandCursor)
        register_button.setCursor(Qt.PointingHandCursor)


        login_button.clicked.connect(self.open_login)
        register_button.clicked.connect(self.open_register)

        layout.addWidget(welcome_label)
        layout.addWidget(login_button)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def open_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()

    def open_register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()

button_style = """
    QPushButton {
        background-color: #0277bd;
        color: white;
        font-size: 16px;
        padding: 12px;
        border-radius: 10px;
    }
    QPushButton:hover {
        background-color: #039be5;
    }
    QPushButton:pressed {
        background-color: #01579b;
    }
"""



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
