# standard imports
import sys
from datetime import datetime
import json

# proprietary imports
from PyQt4 import QtGui, QtCore

# local imports
from browser import Browser
from ticker import Ticker
from qrlabel import QRLabel



class MainWidget(QtGui.QWidget):
    
    def __init__(self):
        super(MainWidget, self).__init__()
        
        self.initUI()
        
    def initUI(self):        
        
        #######################
        # FUNCTIONS

        # init payment setup
        self.amount = "0.00"
        self.address = "13BjVxFnZrFCZAR3e1144cWMWwT3WJBJXw"
        self.rate  = 0.56
        
        # set current language
        with open("languages.json") as f:
            languages = json.loads(f.read())
            print languages
            
            cl = languages["NL"]


        # get products & prices
        browser = Browser()        
        # TODO: keep browsing internal to browser
        # TODO: create addProduct signal to browser browser.getButtons()

        for btn in browser.getButtons():
            btn.clicked.connect(self.incrClick)

        # TODO: custom widget/label, styling via stylesheet        
        overviewEdit = QtGui.QTextEdit()
        overviewEdit.setText(datetime.now().strftime("%Y/%m/%d %H:%M"))
        overviewEdit.setReadOnly(1)
        self.overview = overviewEdit

        # TODO: custom widget/label, styling via stylesheet
        # TODO: add sum in EUR (USD)
        sumEdit = QtGui.QLineEdit(self.amount)
        self.sumEdit = sumEdit # keep reference for later updates
        sumLabel = QtGui.QLabel(cl["sum"])
        sumLabel.setFrameStyle(0x0006)  

        # TODO: custom widget/label, styling via stylesheet
        resetBtn = QtGui.QPushButton(cl["reset"])
        resetBtn.clicked.connect(self.resetClick)
        
        # TODO: custom widget/label, styling via stylesheet
        addressLine = QtGui.QLineEdit(self.address)        
        addressLine.setReadOnly(1)
        addressLine.adjustSize()
        addressLine.setMinimumWidth(230)
        self.addressLine = addressLine
        addressLabel = QtGui.QLabel(cl["payTo"])
        addressLabel.setBuddy(addressLine)
        addressLabel.setFrameStyle(0x0006)
        # TODO: get addresses from public address seed
        newAddrButton = QtGui.QPushButton(cl["newAddr"])
        
        qrLabel = QRLabel()                
        self.qrLabel = qrLabel  # keep reference for later updates       
        self.updateQR()
        
        # Update ticker
        ticker = Ticker()
        ticker.changed.connect(self.showRate)
        QtCore.QTimer.singleShot(100, ticker.request);

        # Rate
        rateLabel = QtGui.QLabel(cl["rate"])
        rateText = QtGui.QLabel()
        rateBtn = QtGui.QPushButton(cl["refresh"])
        rateBtn.clicked.connect(ticker.request)

        self.ticker = ticker
        self.rateText = rateText
        self.showRate('Updating...')

        #######################
        # LAYOUT
        grid = QtGui.QGridLayout()
        grid.addWidget(browser, 0, 0, 1, 3)
        
        grid.addWidget(overviewEdit, 1, 0, 1, 3)

        grid.addWidget(rateLabel, 2, 0)
        grid.addWidget(rateText, 2, 1)
        grid.addWidget(rateBtn, 2, 2)
        
        grid.addWidget(sumLabel, 3, 0)
        grid.addWidget(sumEdit, 3, 1)
        grid.addWidget(resetBtn, 3, 2)

        grid.addWidget(addressLabel, 4, 0)        
        grid.addWidget(addressLine, 4, 1, 1, 2)

        grid.addWidget(qrLabel, 0, 3, 5, 1)
        

        self.setLayout(grid)       
        #self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Bitcoin Biller')
        
        #######################
        # STYLESHEET
        with open("styles.css") as f:
            ss = f.read()
            self.setStyleSheet(ss)
            

        self.show()

    def incrClick(self):
        # check if we are ready to process
        if self.rateText.text().contains("..."):
            return
        # get productButton that is clicked
        sender = self.sender()
        # update overview
        text = self.overview.toPlainText()
        price_EUR = sender.price
        price_mBTC = price_EUR / self.rate * 1000
        text += "\n%14s \t EUR %5.2f \t mBTC %5.2f" % (sender.text(), price_EUR, price_mBTC)
        self.overview.setText(text)
        # update sum --> TODO: move to custom widget
        text = "%6.2f" % ( float(self.sumEdit.text()) + price_mBTC)
        self.sumEdit.setText(text)
        # update QR code
        self.updateQR()

    def resetClick(self):
        self.ticker.request()
        self.sumEdit.setText("0.00") 
        self.overview.setText(datetime.now().strftime("%Y/%m/%d %H:%M"))
        self.updateQR()        

    def updateQR(self):
        # bitcoin:<address>[?amount=<amount>][?label=<label>][?message=<message>]        
        amount = 0.001 * float(self.sumEdit.text())
        address = self.addressLine.text()
        text = "bitcoin:"+address+"?amount="+str(amount)
        self.qrLabel.setCode(text)

    def showRate(self, rate = "1"):
        # print "Main showRate"
        try:
            self.rate = float(rate)
            self.rateText.setText("%.3f EUR/mBTC" % (self.rate/1000))
        except ValueError:
            self.rateText.setText(rate)
        
        
def main():    
    app = QtGui.QApplication(sys.argv)
    mw = MainWidget()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()