#ticker.py
import sys
import json

from PyQt4 import QtGui, QtCore
from PyQt4 import QtNetwork
#from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest, QUrl


class Ticker(QtCore.QObject):

    changed = QtCore.pyqtSignal(object)

    def __init__(self):
        super(Ticker, self).__init__()
        self.manager = QtNetwork.QNetworkAccessManager(self)
        self.manager.finished.connect(self.replyFinished)

    def request(self):
        print "Ticker request"
        self.changed.emit('Updating...')
        self.manager.get(QtNetwork.QNetworkRequest(QtCore.QUrl("http://blockchain.info/ticker")))

    def replyFinished(self, reply="None"):
        try:            
            answer = json.loads(unicode(QtCore.QString(reply.readAll())))['EUR']['15m']
        except:
            print "Ticker reply error"
            answer = "error"
        self.changed.emit(answer)
            
            
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
