# -*- coding: utf-8 -*-
"""
Created on Sun Dec 08 22:29:44 2013

@author: stefaan.ghysels

help by ekhumoro
"""
from PyQt4 import QtGui, QtCore
import qrcode

class QRLabel(QtGui.QLabel):
    def __init__(self, text=""):
        super(QRLabel, self).__init__()        
        self.text = text

    def setCode(self, text=""):        
        self.text = text
        # create QR code and convert to QPixmap
        pixm = qrcode.make(text, image_factory=QRImage).pixmap()
        # scale to label size
        self.setPixmap(pixm.scaled(self.size(),QtCore.Qt.KeepAspectRatio))


class QRImage(qrcode.image.base.BaseImage):
    def __init__(self, border, width, box_size):
        self.border = border
        self.width = width
        self.box_size = box_size
        size = (width + border * 2) * box_size
        self._image = QtGui.QImage(
            size, size, QtGui.QImage.Format_RGB16)
        self._image.fill(QtCore.Qt.white)

    def pixmap(self):
        return QtGui.QPixmap.fromImage(self._image)

    def drawrect(self, row, col):
        painter = QtGui.QPainter(self._image)
        painter.fillRect(
            (col + self.border) * self.box_size,
            (row + self.border) * self.box_size,
            self.box_size, self.box_size,
            QtCore.Qt.black)

    def save(self, stream, kind=None):
        pass
