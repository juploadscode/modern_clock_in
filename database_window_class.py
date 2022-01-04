from PyQt5 import QtCore, QtGui, QtWidgets

import mysql.connector


class DatabaseConnectWindow:
    def set_up_ui(self, db_form) -> None:
        db_form.setObjectName("db_form")
        db_form.resize(246, 240)
        db_form.setFixedSize(246, 240)
        db_form.setWindowIcon(QtGui.QIcon('clock_in.ico'))
        db_form.setWindowTitle("MySQL Login")

        font = QtGui.QFont()
        font.setPointSize(12)
        db_form.setFont(font)

        self.central_widget = QtWidgets.QWidget(db_form)

        self.host_label = QtWidgets.QLabel(self.central_widget)
        self.host_label.setGeometry(QtCore.QRect(20, 20, 47, 13))
        self.host_label.setFont(font)
        self.host_label.setText("Host:")

        self.user_label = QtWidgets.QLabel(self.central_widget)
        self.user_label.setGeometry(QtCore.QRect(20, 50, 47, 13))
        self.user_label.setFont(font)
        self.user_label.setText("User:")

        self.pw_label = QtWidgets.QLabel(self.central_widget)
        self.pw_label.setGeometry(QtCore.QRect(20, 80, 81, 16))
        self.pw_label.setFont(font)
        self.pw_label.setText("Password:")

        self.port_label = QtWidgets.QLabel(self.central_widget)
        self.port_label.setGeometry(QtCore.QRect(20, 110, 47, 13))
        self.port_label.setFont(font)
        self.port_label.setText("Port#:")

        self.db_label = QtWidgets.QLabel(self.central_widget)
        self.db_label.setGeometry(QtCore.QRect(20, 140, 81, 16))
        self.db_label.setFont(font)
        self.db_label.setText("Database:")

        self.host_line_edit = QtWidgets.QLineEdit(self.central_widget)
        self.host_line_edit.setGeometry(QtCore.QRect(110, 20, 113, 20))

        self.user_line_edit = QtWidgets.QLineEdit(self.central_widget)
        self.user_line_edit.setGeometry(QtCore.QRect(110, 50, 113, 20))

        self.pw_line_edit = QtWidgets.QLineEdit(self.central_widget)
        self.pw_line_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pw_line_edit.setGeometry(QtCore.QRect(110, 80, 113, 20))

        self.port_line_edit = QtWidgets.QLineEdit(self.central_widget)
        self.port_line_edit.setGeometry(QtCore.QRect(110, 110, 113, 20))

        self.db_line_edit = QtWidgets.QLineEdit(self.central_widget)
        self.db_line_edit.setGeometry(QtCore.QRect(110, 140, 113, 20))

        self.enter_button = QtWidgets.QPushButton(self.central_widget)
        self.enter_button.setGeometry(QtCore.QRect(70, 170, 91, 41))
        self.enter_button.setText("Enter")
        self.enter_button.clicked.connect(lambda: self.press_enter_button(db_form))

        db_form.setCentralWidget(self.central_widget)
        self.menu_bar = QtWidgets.QMenuBar(db_form)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 246, 21))
        db_form.setMenuBar(self.menu_bar)
        self.status_bar = QtWidgets.QStatusBar(db_form)
        db_form.setStatusBar(self.status_bar)

        QtCore.QMetaObject.connectSlotsByName(db_form)

    def press_enter_button(self, db_form) -> None:
        self.host_text = self.host_line_edit.text()
        self.user_text = self.user_line_edit.text()
        self.pw_text = self.pw_line_edit.text()
        self.port_text = self.port_line_edit.text()
        self.db_text = self.db_line_edit.text()
        self.set_db_input()
        db_form.close()

    def set_db_input(self) -> None:
        try:
            my_db = mysql.connector.connect(
                host=self.host_text,
                user=self.user_text,
                password=self.pw_text,
                port=self.port_text,
                database=self.db_text,
            )
            with open('db.dat', 'w', encoding='utf-8') as file:
                file.write('{}\n{}\n{}\n{}\n{}\n'.format(self.host_text, self.user_text, self.pw_text,
                                                         self.port_text, self.db_text))
            my_db.cursor()
            success_box = QtWidgets.QMessageBox()
            success_box.setText('Success')
            success_box.setWindowTitle('Success')
            success_box.exec_()
        except Exception as e:
            error_box = QtWidgets.QMessageBox()
            error_box.setText('Error:\n' + str(e))
            error_box.setWindowTitle('Error')
            error_box.exec_()
