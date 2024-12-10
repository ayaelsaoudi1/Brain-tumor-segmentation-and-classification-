import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QMessageBox, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui
from tkinter import filedialog
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Spacer
from reportlab.lib.units import inch
import numpy as np
import cv2
import tensorflow as tf
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QApplication, QLineEdit, QWidget, QLabel, QComboBox, QSpinBox, QDateEdit
from PyQt5.QtGui import QIntValidator
import os
from PyQt5.QtGui import qRgb



headers = [ "Meningioma Tumor", "Glioma Tumor", "Pituitary Tumor", "Number of tumors", "Types of Tumors (if any)"]
results = []

class ImageSelectorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.img_path = ""
        self.setWindowTitle("Brain Tumour Segmentaton & Classification")
        
        #put icon for the window
        self.setWindowIcon(QtGui.QIcon("C:/Users/ADMIN/Desktop/new fyp/brain.png"))

        self.patientname_label = QLabel("Name:", self)
        self.patientname_label.setGeometry(170, 140, 50, 30)
        self.patientname_edit = QLineEdit(self)
        font = QFont()
        font.setPointSize(10)
        self.patientname_edit.setFont(font)
        self.patientname_edit.setFixedSize(150, 30)
        self.patientname_edit.move(10, 10)
        self.patientname_edit.setGeometry(210, 140, 150, 30)

        self.patientgender_label = QLabel("Gender:", self)
        self.patientgender_label.setGeometry(410, 140, 150, 30)

        self.patientgender_dropdown = QComboBox(self)
        self.patientgender_dropdown.addItem('')
        self.patientgender_dropdown.addItem('Female')
        self.patientgender_dropdown.addItem('Male')
        font = QFont()
        font.setPointSize(10)
        self.patientgender_dropdown.setFont(font)
        self.patientgender_dropdown.model().item(0).setEnabled(False)  # disable the first item
        self.patientgender_dropdown.model().item(0).setTextAlignment(Qt.AlignCenter)  # center-align the first item
        self.patientgender_dropdown.setGeometry(460, 140, 150, 30)

        self.patientage_label = QLabel("Age:", self)
        self.patientage_label.setGeometry(665, 140, 150, 30)

        self.age_spinbox = QSpinBox(self)
        self.age_spinbox.setMinimum(0)
        self.age_spinbox.setMaximum(150)
        self.age_spinbox.setGeometry(695, 140, 100, 30)

        self.todaydate_label = QLabel("Date:", self)
        self.todaydate_label.setGeometry(845, 140, 150, 30)

        today_date = QDate.currentDate()
        self.date_edit = QDateEdit(today_date, self)
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setGeometry(880, 140, 150, 30)

        self.image_label1 = QLabel(self)
        self.image_label1.setObjectName("label1")
        self.image_label1.setGeometry(20, 250, 270, 300)
        self.image_label1.setAlignment(Qt.AlignCenter)
        self.image_label1.setStyleSheet("background-color: white; border: 1px solid black;")

        self.select_button = QPushButton("Select Image", self)
        self.select_button.setGeometry(330, 350, 100, 30)
        self.select_button.clicked.connect(self.select_image)

        self.select_button = QPushButton("Detect", self)
        self.select_button.setGeometry(330, 400, 100, 30)
        self.select_button.clicked.connect(self.detect_tumor)

        self.image_label2 = QLabel(self)
        self.image_label2.setObjectName("label2")
        self.image_label2.setGeometry(460, 250, 270, 300)
        self.image_label2.setAlignment(Qt.AlignCenter)
        self.image_label2.setStyleSheet("background-color: white; border: 1px solid black;")
        


        self.image_label3 = QLabel(self)
        self.image_label3.setObjectName("label3")
        self.image_label3.setGeometry(760, 250, 270, 300)
        self.image_label3.setAlignment(Qt.AlignCenter)
        self.image_label3.setStyleSheet("background-color: white; border: 1px solid black;")
        # pixmap = QPixmap("E:\dataset\Brain_Tumor_Detection\pred\pred13.jpg")
        # self.image_label3.setPixmap(pixmap)


        self.select_button = QPushButton("Download as PDF", self)
        self.select_button.setGeometry(1080, 140, 100, 30)
        self.select_button.clicked.connect(self.create_pdf)

        self.table = QTableWidget(self)
        self.table.setStyleSheet("background-color: white; border: 1px solid black;")
        self.table.setGeometry(1060, 250, 270, 300)
        self.table.setRowCount(5)
        self.table.setColumnCount(2)
        self.table.horizontalHeader().setStretchLastSection(True) 
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False) 
        self.table.resizeColumnToContents(0) 
        self.table.setColumnWidth(0, self.table.width() // 2) 
        self.table.setColumnWidth(1, self.table.width() // 2)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


        for i, header in enumerate(headers):
            item = QTableWidgetItem(header)
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable) 
            self.table.setItem(i, 0, item)
            font = QtGui.QFont()
            font.setBold(True)
            item.setFont(font)

        for i, result in enumerate(results):
            item = QTableWidgetItem(result)
            self.table.setItem(i, 1, item)

        self.resize(1260, 600)
        self.showMaximized()
        self.show()

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg )")
        if file_path:
            self.img_path = file_path
            image = QImage(file_path)
            image = image.scaled(270, 270, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            pixmap = QPixmap.fromImage(image)
            self.image_label1.setPixmap(pixmap)

    def detect_tumor(self):
        img=cv2.imread(self.img_path)
        if img is None:
            QMessageBox.warning(self, "Warning", "You haven't selected an image.")
            return
        new_model = tf.keras.models.load_model('C:/Users/python/Desktop/fyp/braintumor.h5')
        img=cv2.imread(self.img_path)
        img=cv2.resize(img,(150,150))
        img_array=np.array(img)
        img_array=img_array.reshape(1,150,150,3)
        a=new_model.predict(img_array)
        a, b, c, d  = a[0]
        arr=[b,a,d]
        t=[b*100,a*100,d*100]
        count=0
        indexes=[]
        res=[]
        results=[]
        numbers_formatted = ['{:.10f} %'.format(num*100) for num in arr]
        for i, tumor in enumerate(t):
            if tumor > 10:
                count += 1
                indexes.append(i)
        numbers_formatted.append(str(count))
        if count == 0:
            res.append("No tumor")
            QMessageBox.warning(self, "Warning", "This brain doesn't have a tumor.")
            res=", ".join(res)
            numbers_formatted.append(res)
            results=numbers_formatted
            for i, item in enumerate(results):
                table_item = QTableWidgetItem(item)
                self.table.setItem(i, 1, table_item)
            return results
        else:
            for index in indexes:
                if index == 0:
                    res.append("Meningioma tumor")
                elif index == 1:
                    res.append("Glioma tumor")
                elif index == 2:
                    res.append("Pituitary tumor")
            res=", ".join(res)
            numbers_formatted.append(res)
            results=numbers_formatted
            for i, item in enumerate(results):
                table_item = QTableWidgetItem(item)
                self.table.setItem(i, 1, table_item)
            model = tf.keras.models.load_model(os.path.join(os.getcwd(), "model.h5"), compile=False)
            input_image_path =self.img_path
            input_image = cv2.imread(input_image_path, cv2.IMREAD_COLOR)
            input_image_copy = input_image.copy() 
            input_image = cv2.resize(input_image, (256, 256))
            input_image = input_image / 255.0
            input_image = np.expand_dims(input_image, axis=0)
            prediction = model.predict(input_image)[0]
            prediction = np.squeeze(prediction, axis=-1)
            prediction = (prediction >= 0.5).astype(np.uint8) * 255
            prediction2 = cv2.resize(prediction, (input_image_copy.shape[1], input_image_copy.shape[0]))
            contours, hierarchy = cv2.findContours(prediction2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(prediction2, contours, -1, (0, 0, 255), 3)
            cv2.drawContours(input_image_copy, contours, -1, (0, 0, 255), 3)
            input_image_copy = cv2.cvtColor(input_image_copy, cv2.COLOR_BGR2RGB)
            qimage2 = QImage(prediction.data, prediction.shape[1], prediction.shape[0], QImage.Format_Indexed8)
            pixmap2 = QPixmap.fromImage(qimage2)
            self.image_label2.setPixmap(pixmap2)
            qimage3 = QImage(input_image_copy.data, input_image_copy.shape[1], input_image_copy.shape[0], QImage.Format_RGB888)
            pixmap3 = QPixmap.fromImage(qimage3)
            scaled_pixmap3 = pixmap3.scaled(self.image_label3.width(), self.image_label3.height(), aspectRatioMode=Qt.KeepAspectRatio)
            self.image_label3.setPixmap(scaled_pixmap3)
            return results


    def create_pdf(self):
        r = self.detect_tumor()
        if not r:
            QMessageBox.warning(self, "Warning", "Can't download an empty table.")
            return
        name = self.patientname_edit.text()
        gender = self.patientgender_dropdown.currentText()
        age = self.age_spinbox.value()
        date = self.date_edit.date().toString(Qt.ISODate)
        if not name:
            QMessageBox.warning(self, "Missing Information", "Please enter a name.")
            return
        elif not gender:
            QMessageBox.warning(self, "Missing Information", "Please select a gender.")
            return
        elif age == 0:
            QMessageBox.warning(self, "Missing Information", "Please enter a valid age.")
            return
        
        output_folder = filedialog.askdirectory()
        if output_folder:
            doc = SimpleDocTemplate(output_folder + "/table.pdf", pagesize=letter)
            elements = []

        header_style = ParagraphStyle(
            'header',
            fontName='Helvetica-Bold',
            fontSize=12,
            textColor='black',
            leading=16,
            leftIndent=0,
            rightIndent=0,
            alignment=TA_LEFT,
            spaceAfter=0.2*inch  # add some extra space after the header
        )

        date_style = ParagraphStyle(
            'date',
            parent=header_style,  # inherit from header style
            alignment=TA_RIGHT  # right-align the text
        )

        name_text = f"Name: {name.title()}"
        gender_text = f"Gender: {gender}"
        age_text = f"Age: {age}"
        date_text = f"Date: {date}"
        name = Paragraph(name_text, header_style)
        gender = Paragraph(gender_text, header_style)
        age = Paragraph(age_text, header_style)
        date = Paragraph(date_text, date_style)

        elements.append(date)
        elements.append(name)
        elements.append(gender)
        elements.append(age)
        elements.append(Spacer(1, 16))


        table_data = list(zip(headers, r))
        table = Table(table_data)
       
        table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (0, -1), 12),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
        elements.append(table)

        elements.append(Spacer(1, 16))

        doc.build(elements)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = ImageSelectorGUI()
    sys.exit(app.exec_())