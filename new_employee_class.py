from PyQt5 import QtCore, QtGui, QtWidgets

import cv2


class NewEmployeeWindow:
    def set_up_ui(self, new_employee_form, frame) -> None:
        new_employee_form.setObjectName("new_employee_form")
        new_employee_form.resize(250, 160)
        new_employee_form.setFixedSize(250, 160)
        new_employee_form.setWindowIcon(QtGui.QIcon('clock_in.ico'))
        new_employee_form.setWindowTitle("New Employee Window")

        font = QtGui.QFont()
        font.setPointSize(12)

        self.frame = frame

        self.employee_form = QtWidgets.QWidget(new_employee_form)

        self.first_name = QtWidgets.QLabel(self.employee_form)
        self.first_name.setGeometry(QtCore.QRect(10, 10, 91, 21))
        self.first_name.setFont(font)
        self.first_name.setText("First Name:")

        self.last_name = QtWidgets.QLabel(self.employee_form)
        self.last_name.setGeometry(QtCore.QRect(10, 50, 91, 21))
        self.last_name.setFont(font)
        self.last_name.setText("Last Name:")

        self.enter_fname = QtWidgets.QLineEdit(self.employee_form)
        self.enter_fname.setGeometry(QtCore.QRect(120, 10, 113, 20))

        self.enter_lname = QtWidgets.QLineEdit(self.employee_form)
        self.enter_lname.setGeometry(QtCore.QRect(120, 50, 113, 20))

        self.submit_name_button = QtWidgets.QPushButton(self.employee_form)
        self.submit_name_button.setGeometry(QtCore.QRect(70, 90, 101, 41))
        self.submit_name_button.setText("Submit")
        self.submit_name_button.clicked.connect(lambda: self.press_enter(new_employee_form))

        new_employee_form.setCentralWidget(self.employee_form)
        self.menu_bar = QtWidgets.QMenuBar(new_employee_form)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 250, 21))

        new_employee_form.setMenuBar(self.menu_bar)
        self.status_bar = QtWidgets.QStatusBar(new_employee_form)
        new_employee_form.setStatusBar(self.status_bar)

        QtCore.QMetaObject.connectSlotsByName(new_employee_form)

    def press_enter(self, new_employee_form) -> None:
        self.f_name = self.enter_fname.text()
        self.l_name = self.enter_lname.text()
        new_employee_form.close()
        with open('clock_in_count.txt', 'r', encoding='utf-8') as file:
            employee_id = int(file.read())
        file = f"{employee_id} - {self.f_name} {self.l_name}.png"
        cropped_img = self.frame[100:600, 300:900]
        cv2.imwrite('images/' + file, cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))
        with open('clock_in_count.txt', 'w', encoding='utf-8') as file:
            file.write(str(employee_id + 1))
