# -*- coding: utf-8 -*-
"""
Created on Sun Dec 08 22:29:44 2013

@author: stefaan.ghysels
"""
from PyQt4 import QtGui, QtCore
import qrcode
from PIL.ImageQt import ImageQt

class QRLabel(QtGui.QLabel):
    def __init__(self, text=""):
        super(QRLabel, self).__init__()        
        self.text = text

    def setCode(self, text=""):        
        self.text = text
        # create PIL QR code
        qrImg = qrcode.make(text)
        imgQt = ImageQt(qrImg.convert("RGB"))   # keep a reference!
        # convert to QImage, which is then loaded in QLabel as a QPixmap
        pixm = QtGui.QPixmap.fromImage(imgQt)
        self.setPixmap(pixm.scaled(self.size(),QtCore.Qt.KeepAspectRatio))
        # self.setPixmap(pixm)
