from cx_Freeze import setup, Executable
from PyQt5.QtCore import QTimer, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from datetime import datetime
import mysql.connector
import cv2
import mediapipe as mp
import numpy as np
import face_recognition
import os
import glob
import sys


build_exe_options = {"packages": ["PyQt5", "datetime", "mysql.connector", "cv2", "mediapipe", "numpy",
                                  "facial_recognition_class", "database_window_class", "new_employee_class",
                                  "os", "glob", "sys"],

                     "include_files": ["images", "clock_in.ico", "clock_in_bg.mp4", "clock_in_count.txt", "db.dat",
                                       'haarcascade_frontalface_default.xml', 'smile_bg.jpg']}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Time Clock Software",
    version="1.0",
    description="MySQL Clock in Application",
    options={"build_exe": build_exe_options},
    executables=[Executable("clock_in_main.py", base=base, icon='clock_in.ico')]
)
