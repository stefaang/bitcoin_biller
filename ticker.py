#ticker.py
import sys
import json

from PyQt4 import QtGui, QtCore
from PyQt4 import QtNetwork
#from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest, QUrl

class TickerButton(QtGui.QPushButton):
    
    def __init__(self):
        super(TickerButton, self).__init__()        

        manager = QtNetwork.QNetworkAccessManager(self)
        manager.finished.connect(self.replyFinished)
        self.clicked.connect(self.updateRate)
        self.manager = manager
        
        # initialize the rate
        self.rate = 0.77
        self.setText("Wisselkoers: %.3f EUR/mBTC" % self.rate)        
        #self.updateRate()

    def updateRate(self):
        self.manager.get(QtNetwork.QNetworkRequest(QtCore.QUrl("http://blockchain.info/ticker")))
        self.setText("Updating...")

    def replyFinished(self, reply="None"):        
        try:            
            answer = json.loads(unicode(QtCore.QString(reply.readAll())))['EUR']['15m']
        except:
            print "error with reply"
            answer = "xxx"
        self.setText("Wisselkoers: %.3f EUR/mBTC" % (answer/1000))
        self.rate = answer/1000
            
            
class TestApp(QtGui.QWidget):   
    """Only used for testing.."""
    def __init__(self):
        super(TestApp, self).__init__()        
        self.initUI()
        
    def initUI(self):
        ticker = TickerButton()
        grid = QtGui.QGridLayout()
        grid.addWidget(ticker)
        self.setLayout(grid)
        self.setWindowTitle('Bitcoin Biller')
        self.show()
        
def main():    
    app = QtGui.QApplication(sys.argv)
    mw = TestApp()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
