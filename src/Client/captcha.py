import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton
import cv2
# from keras.models import load_model
import numpy as np

class Captcha(QtWidgets.QMainWindow):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        top = 400
        left = 400
        width = 200
        height = 500
        self.setGeometry(top, left, width, height)
        self.label = QtWidgets.QLabel("", self)
        background = QtWidgets.QLabel("", self)
        background.setGeometry(0, 0, 200, 225)
        background.setStyleSheet("Background-color:pink")
        p = QtWidgets.QLabel("Narysuj obrazek(captcha)", self)
        p.setGeometry(40, 200, 200, 25)
        canvas = QtGui.QPixmap(200, 200)
        canvas.fill(QtGui.QColor("white"))
        self.label.setPixmap(canvas)
        self.label.setGeometry(0, 225, 200, 200)
        self.obraz = QtWidgets.QLabel("", self)
        pixmap = QPixmap('show.png')
        self.obraz.setPixmap(pixmap)
        self.obraz.setGeometry(0, 0, 200, 200)
        self.obraz.setStyleSheet("")
        self.last_x, self.last_y = None, None
        self.button = QPushButton("Potwierdz", self)
        self.button.clicked.connect(self.save)
        self.button.setGeometry(0, 425, 200, 75)
        self.show()

    def mouseMoveEvent(self, e):
        if self.last_x is None:  # First event.
            self.last_x = e.x()
            self.last_y = e.y()
            return

        painter = QtGui.QPainter(self.label.pixmap())
        painter.setPen(QtGui.QPen(QtGui.QColor("black"), 5))
        painter.drawLine(self.last_x, self.last_y - 225, e.x(), e.y() - 225)
        painter.end()
        self.update()
        self.last_x = e.x()
        self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None

    def save(self):
        self.label.pixmap().save("siema.png", "PNG")
        cv2.imread("siema.png")

        #self.save_tests_to_model()

        if self.rmsdiff(cv2.imread("siema.png"), cv2.imread("show.png")) and self.model(cv2.imread("siema.png", cv2.IMREAD_GRAYSCALE)) :
            self.label.pixmap().fill(QtGui.QColor("white"))
            self.label.hide()
            self.label.show()
            self.parent.Register()
            self.close()
            self.destroy()
        else:
            self.label.pixmap().fill(QtGui.QColor("white"))
            self.label.hide()
            self.label.show()
            print("Musisz jeszcze poprobwac")
    def rmsdiff(self, image1, image2):
        good = 0
        all = 0
        good2 = 0
        allw = 0
        for i in range(200):
            for j in range(200):
                if image1[i][j][0] == image2[i][j][0] and image1[i][j][1] == image2[i][j][1] and image1[i][j][2] == \
                        image2[i][j][2] and image1[i][j][0] == 0:
                    good += 1
                if image2[i][j][1] == 0:
                    all += 1
                if image1[i][j][0] == image2[i][j][0] and image1[i][j][1] == image2[i][j][1] and image1[i][j][2] == \
                        image2[i][j][2] and image1[i][j][0] == 255:
                    good2 += 1
                allw += 1
        if good / all > 0.4 and good2 / allw > 0.6:
            print(good / all)
            return True
        else:
            print(good / all)
            return False
    def model(self,image1):
        model = load_model("model_good.h5")
        xtest = np.array(image1/255)
        xtest = xtest.reshape((1,) + xtest.shape + (1,))
        preds = model.predict(xtest)[0][1]
        if preds > 0.6:
            return True
        else:
            return False

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Captcha(123)
    window.show()
    app.exec_()
