from PyQt4 import QtGui, QtCore

pricelist = {
    "favorite" : {
        "cola" :    2.00,
        "jupiler":  2.00,
        "koffie":   2.50,
    },
    "frisdrank" : {
        "cola" :    2.00,
        "cola-lt":  2.00,
        "fanta":    2.00,
        "sprite":   2.00,
        "ice-tea":  2.00,
        "fruitsap": 2.00,
        "water-plat":   2.00,
        "water-spuit":  2.00,
    },
    "bieren" : {
        "jupiler":      2.00,
        "leffe blond":  3.10,
        "duvel":        3.50,
        "keizer karel": 3.50,       
    },    
    "wijnen": {
        "rode wijn":    3.50,
        "witte wijn":   3.50,
        "cava":         3.50,
        "champagne":   12.00,
    },
    "warme\ndranken": {
        "koffie":       2.50,
        "decaf":        2.50,
        "+slagroom":    0.30,
        "thee":         2.10,
    }
}

class CatButton(QtGui.QPushButton):
    def __init__(self, name):
        super(CatButton, self).__init__(name.title())        
        self.name = name
        
class ProductButton(QtGui.QPushButton):
    def __init__(self, name, price):
        super(ProductButton, self).__init__(name.title())
        self.name = name
        self.price = price
        

class Browser(QtGui.QWidget):
    addProduct = QtCore.pyqtSignal()
    openCat = QtCore.pyqtSignal()
    
    def __init__(self):
        super(Browser, self).__init__()
        
        self.initUI()
        

    def initUI(self):        
        # FUNCTION
        self.cats = {}
        self.btns = {}
        for cat, d in pricelist.viewitems():
            catbtn = CatButton(cat)
            catbtn.clicked.connect(self.changeCat)
            self.cats[cat] = catbtn
            if cat == "favorite":   # don't make extra ProductButtons for favs
                continue
            for drink,price in d.viewitems():
                btn = ProductButton(drink,price)
                self.btns[drink] = btn
    
        # LAYOUT
        grid = QtGui.QGridLayout()
        i = 0
        # backup solution
#        drinks = [drink for cat in pricelist for drink in sorted(pricelist[cat])]
#        print drinks
#        for drink in drinks:
#            
#            btn = self.btns[drink]
#            grid.addWidget(btn, i/4, i%4)
#            i+=1
        i = 0
        for drink in sorted(pricelist["favorite"]):            
            btn = self.btns[drink]
            grid.addWidget(btn, i/4, i%4)
            i+=1
        
        j = 0
        for cat in sorted(pricelist):
            if cat == "favorite":
                continue
            catbtn = self.cats[cat]
            grid.addWidget(catbtn, (i+3)/4+j/4, j%4)
            j+=1
        
        grid.setMargin(0)
        self.setLayout(grid)

    def changeCat(self):
        catactive = self.sender().name
        
        print catactive
        drinks = pricelist[catactive]
        print drinks.keys()
        
        grid = self.layout()
        for btn in self.btns.viewvalues():
            grid.removeWidget(btn)
            btn.setParent(None)
        for btn in self.cats.viewvalues():
            grid.removeWidget(btn)
            btn.setParent(None)
        
        i = 0
        for drink in sorted(drinks):
            btn = self.btns[drink]
            grid.addWidget(btn, i/4, i%4)
            i+=1
        j = 0
        for cat in sorted(pricelist):
            if cat == "favorite":
                continue
            catbtn = self.cats[cat]
            if cat == catactive:
                catbtn.setStyleSheet("background:#eee;")
            else:
                catbtn.setStyleSheet("background:#ccc;")
            grid.addWidget(catbtn, (i+3)/4+j/4, j%4)
            j+=1
        
        

    def getButtons(self):
        return self.btns.viewvalues()

    def getCategories(self):
        return self.cats

    # signal that sends the button upstairs