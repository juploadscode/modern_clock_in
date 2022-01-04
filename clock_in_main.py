from PyQt5.QtCore import QTimer
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from datetime import datetime
from facial_recognition_class import FaceRecognition
from database_window_class import DatabaseConnectWindow
from new_employee_class import NewEmployeeWindow

import mysql.connector
import cv2
import mediapipe as mp
import numpy as np

MOVE_CLOSER = "Move Closer"
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


class MainWindow:
    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    segment = mp_selfie_segmentation.SelfieSegmentation()

    def setupUi(self, main_window) -> None:
        main_window.resize(1280, 720)
        main_window.setFixedSize(1280, 720)
        main_window.setWindowIcon(QtGui.QIcon('clock_in.ico'))
        main_window.setWindowTitle("Clock In Software")

        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)

        self.centralwidget = QtWidgets.QWidget(main_window)

        self.path = 'images'
        self.face = FaceRecognition(self.path)

        self.camera_x = 1280
        self.camera_y = 720
        self.camera_screen = QtWidgets.QTextBrowser(self.centralwidget)
        self.camera_screen.setGeometry(QtCore.QRect(0, 0, self.camera_x, self.camera_y))

        self.vertical_layout = QtWidgets.QVBoxLayout(self.camera_screen)
        self.image_label = QtWidgets.QLabel(self.camera_screen)
        self.vertical_layout.addWidget(self.image_label)

        self.video_timer = QTimer()
        self.video_timer.start(20)
        self.video_timer.timeout.connect(self.open_vid_bg)
        self.background_video = 'clock_in_bg.mp4'
        self.vid = cv2.VideoCapture(self.background_video)
        self.frame_counter = 0

        self.cam_timer = QTimer()
        self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cam_timer.timeout.connect(self.start_clock_in)

        self.new_employee_timer = QTimer()
        self.employee_cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.new_employee_timer.timeout.connect(self.add_new_employee)

        self.register_employee_button = QtWidgets.QPushButton(self.centralwidget)
        self.register_employee_button.setGeometry(QtCore.QRect(520, 300, 180, 71))
        self.register_employee_button.setFont(font)
        self.register_employee_button.setText("Register New Employee")
        self.register_employee_button.clicked.connect(self.add_new_employee)

        self.start_clock_in_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_clock_in_button.setGeometry(QtCore.QRect(520, 400, 180, 71))
        self.start_clock_in_button.setText("Start Clock In Software")
        self.start_clock_in_button.clicked.connect(self.start_clock_in)

        self.clock_in_button = QtWidgets.QPushButton(self.centralwidget)
        self.clock_in_button.setGeometry(QtCore.QRect(530, 500, 180, 71))
        self.clock_in_button.hide()

        font.setPointSize(18)
        self.clock_in_button.setFont(font)
        self.clock_in_button.setText('Clock In')
        self.clock_in_button.clicked.connect(self.clock_in_clicked)

        font.setPointSize(11)
        self.clock_in_log = QtWidgets.QTextBrowser(self.centralwidget)
        self.clock_in_log.setGeometry(QtCore.QRect(450, 580, 331, 91))
        self.clock_in_log.setFont(font)
        self.clock_in_log.hide()

        self.snap_photo_button = QtWidgets.QPushButton(self.centralwidget)
        self.snap_photo_button.setGeometry(QtCore.QRect(515, 550, 180, 71))
        self.snap_photo_button.hide()

        font.setPointSize(18)
        self.snap_photo_button.setFont(font)
        self.snap_photo_button.setText('Take Photo')

        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)

        self.start_clock_in_button.setFont(font)

        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setTitle("File")

        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)

        main_window.setStatusBar(self.statusbar)
        self.actionConfigure_SQL = QtWidgets.QAction(main_window)
        self.actionConfigure_SQL.setText("Configure SQL")
        self.actionConfigure_SQL.triggered.connect(self.open_db_form)

        self.menuFile.addAction(self.actionConfigure_SQL)
        self.menubar.addAction(self.menuFile.menuAction())

        QtCore.QMetaObject.connectSlotsByName(main_window)

    @staticmethod
    def modify_background(screen, threshold) -> tuple:
        rgb_img = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
        result = MainWindow.segment.process(rgb_img)
        binary_mask = result.segmentation_mask > threshold
        binary_mask_3 = np.dstack((binary_mask, binary_mask, binary_mask))
        bg = cv2.imread('smile_bg.jpg')
        bg = cv2.resize(bg, (1080, 1920))
        background_img = cv2.resize(bg, (screen.shape[1], screen.shape[0]))
        background_img = cv2.cvtColor(background_img, cv2.COLOR_BGR2RGB)
        output_img = np.where(binary_mask_3, screen, background_img)
        return output_img

    def run_once(f):
        def wrapper(*args, **kwargs):
            if not wrapper.has_run:
                wrapper.has_run = True
                return f(*args, **kwargs)

        wrapper.has_run = False
        return wrapper

    @run_once
    def reload_images(self) -> None:
        self.face.load_encoding_images()

    def start_clock_in(self) -> None:
        self.register_employee_button.hide()
        self.start_clock_in_button.hide()
        self.menubar.hide()
        self.video_timer.stop()
        self.cam_timer.start(20)
        self.clock_in_button.show()
        self.clock_in_log.show()
        self.reload_images()

        success, frame = self.cam.read()
        frame = cv2.resize(frame, (self.camera_x, self.camera_y))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        faces_located = False
        face_locations, face_names = self.face.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            if name == MOVE_CLOSER:
                self.display_name = MOVE_CLOSER
            else:
                self.display_name = name[4:]
                self.name_key = int(name[0])
                faces_located = True
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            cv2.putText(frame, self.display_name, (x1 + 75, y1), cv2.FONT_HERSHEY_DUPLEX, 1, WHITE, 2)
        frame = self.modify_background(frame, 0.05)
        height, width, channel = frame.shape
        step = channel * width
        q_img = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(q_img))
        if faces_located is True:
            self.clock_in_button.setEnabled(True)
        else:
            self.clock_in_button.setEnabled(False)
            self.clock_in_log.clear()

    def clock_in_clicked(self) -> None:
        try:
            now = datetime.now()
            date = now.strftime("%Y-%m-%d")
            time_now = now.strftime("%H:%M:%S")
            post = f"Clock in successful\n Date: {date} \nTime: {time_now} \nHave a great day {self.display_name}"
            self.clock_in_log.setText(post)
            with open('db.dat', 'r', encoding='utf-8') as file:
                db_credentials = file.read().splitlines()
            my_db = mysql.connector.connect(
                host=db_credentials[0],
                user=db_credentials[1],
                password=db_credentials[2],
                port=db_credentials[3],
                database=db_credentials[4],
            )
            my_cursor = my_db.cursor()
            insert_statement = ("INSERT INTO clock_in"
                                "(clock_in_id, id, name, time, date)"
                                "VALUES (%s, %s, %s, %s, %s)")
            with open('clock_in_count.txt', 'r', encoding='utf-8') as file:
                clock_in_id_count = file.read()
                clock_in_id_count = int(clock_in_id_count)
            data = (clock_in_id_count, self.name_key, self.display_name, time_now, date)
            my_cursor.execute(insert_statement, data)
            my_db.commit()
            with open('clock_in_count.txt', 'w', encoding='utf-8') as file:
                file.write(str(clock_in_id_count + 1))
        except:
            error_box = QtWidgets.QMessageBox()
            error_box.setText('Error:\n Restart the program and enter database credentials.')
            error_box.setWindowTitle('Error')
            error_box.exec_()

    def add_new_employee(self) -> None:
        self.register_employee_button.hide()
        self.start_clock_in_button.hide()
        self.menubar.hide()
        self.snap_photo_button.show()
        self.video_timer.stop()
        self.cam_timer.stop()
        self.new_employee_timer.start(20)
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        success, frame = self.employee_cam.read()
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_cascade.detectMultiScale(grey, 1.1)
        frame = cv2.flip(frame, 1)
        face_flag = False
        for (x, y, w, h) in faces:
            face_x_pos = x + w
            face_y_pos = y + h
            if face_x_pos in range(300, 450) and face_y_pos in range(300, 450):
                face_flag = True
            else:
                cv2.putText(frame, 'Move Face Into Box', (155, 120), cv2.FONT_HERSHEY_DUPLEX, 0.9, BLACK, 1)
        frame = cv2.resize(frame, (self.camera_x, self.camera_y))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        cv2.rectangle(frame, (300, 100), (900, 600), WHITE, 2)
        height, width, channel = frame.shape
        step = channel * width
        q_img = QImage(frame.data, width, height, step, QImage.Format_RGB888)

        self.image_label.setPixmap(QPixmap.fromImage(q_img))

        if face_flag is True:
            self.snap_photo_button.setEnabled(True)
        else:
            self.snap_photo_button.setEnabled(False)

        if self.snap_photo_button.isDown():
            self.new_employee_timer.stop()

            new_employee_form = QtWidgets.QMainWindow()
            self.new_employee_ui = NewEmployeeWindow()
            self.new_employee_ui.set_up_ui(new_employee_form, frame)
            new_employee_form.show()

            self.register_employee_button.show()
            self.start_clock_in_button.show()
            self.snap_photo_button.hide()
            self.video_timer.start(20)
            self.cam_timer.stop()

    def open_db_form(self) -> None:
        self.database_form = QtWidgets.QMainWindow()
        self.ui = DatabaseConnectWindow()
        self.ui.set_up_ui(self.database_form)
        self.database_form.show()

    def open_vid_bg(self) -> None:
        self.clock_in_log.hide()
        if self.frame_counter == self.vid.get(cv2.CAP_PROP_FRAME_COUNT):
            self.frame_counter = 0
            self.vid = cv2.VideoCapture(self.background_video)
        success, frame = self.vid.read()
        self.frame_counter += 1
        frame = cv2.resize(frame, (self.camera_x, self.camera_y))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        step = channel * width
        q_img = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(q_img))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())
