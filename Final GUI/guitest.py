import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QMessageBox, QAction, QLineEdit, QTableWidget, QTableWidgetItem, QLabel, QGroupBox, QVBoxLayout, QGridLayout, QFileDialog, QRadioButton, QHeaderView
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import pyqtSlot, Qt
from vqa_change import run_func

class App(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.title = "VQA"
        self.left = 100
        self.top = 200
        self.width = 640
        self.height = 690
        self.question=""
        self.fileName=""
        self.resultset=[('a',1),('b',2),('c',3),('d',4),('e',5)]
        self.initUI()

        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)
        cwidget = QWidget()
        self.setCentralWidget(cwidget)
        
        self.createquestion()
        self.createimage()
        self.createresult()
        
        self.subutton = QPushButton("submit",self)
        self.subutton.clicked.connect(self.on_submit)
        self.subutton.hide()
        
        wLayout = QVBoxLayout()
        wLayout.addWidget(self.questiongroup)
        wLayout.addWidget(self.imagegroup)
        wLayout.addWidget(self.subutton)
        wLayout.addWidget(self.resultgroup)
        wLayout.setAlignment(Qt.AlignTop)
        
        cwidget.setLayout(wLayout)
        
        #Menu bar
        mainmenu = self.menuBar()
        option = mainmenu.addMenu("Options")
        hhelp = mainmenu.addMenu("Help")
        
        resetButton = QAction(QIcon("restart.png"),"Reset",self)
        resetButton.setShortcut("Ctrl+R")
        resetButton.setStatusTip("Reset image and question")
        resetButton.triggered.connect(self.reset)
        option.addAction(resetButton)
        
        exitButton = QAction(QIcon('exit.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        option.addAction(exitButton)
        
        helpButton = QAction(QIcon('help.png'), 'Help', self)
        helpButton.setShortcut('Ctrl+H')
        helpButton.setStatusTip('Help to run application')
        helpButton.triggered.connect(self.on_clickhelp)
        hhelp.addAction(helpButton)
        
        aboutButton = QAction(QIcon('about.png'), 'About', self)
        aboutButton.setShortcut('Ctrl+I')
        aboutButton.setStatusTip('About the application')
        aboutButton.triggered.connect(self.on_clickabout)
        hhelp.addAction(aboutButton)
        
        # Status bar
        self.statusBar().showMessage("Hello and Welcome to this Application")
        
        self.show()
        
    # get Question
    def createquestion(self):
        self.questiongroup = QGroupBox("Select Image and Enter Question")
        layout = QGridLayout()
        layout.setSpacing(10)
        
        qlabel = QLabel("Question",self)
        layout.addWidget(qlabel,0,0)
        
        self.textbox = QLineEdit(self)
        layout.addWidget(self.textbox,0,1)

        self.ibutton = QPushButton("Select Image",self)
        self.ibutton.clicked.connect(self.on_click)
        layout.addWidget(self.ibutton,1,1,Qt.AlignHCenter)
        
        self.questiongroup.setLayout(layout)
        
    def createimage(self):
        self.imagegroup = QGroupBox()
        ilayout = QGridLayout()
        
        self.ibutt = QPushButton("Reselect new image",self)
        self.ibutt.clicked.connect(self.on_reselect)
        ilayout.addWidget(self.ibutt,0,1,Qt.AlignHCenter)
        
        self.ilabel = QLabel(self)
        ilayout.addWidget(self.ilabel,1,1,Qt.AlignHCenter)
       
        self.imagegroup.setLayout(ilayout)
        self.imagegroup.hide()
        
    def createresult(self):
        self.resultgroup = QGroupBox("The result is")
        rlayout = QGridLayout()
        
        self.r1 = QRadioButton("Top 5")
        self.r1.setChecked(True)
        self.r1.toggled.connect(lambda:self.btnstate(self.r1))
        rlayout.addWidget(self.r1,0,0)
        
        self.r2 = QRadioButton("highest")
        self.r2.toggled.connect(lambda:self.btnstate(self.r2))
        rlayout.addWidget(self.r2,0,2,1,2)
        
        self.tab1 = QTableWidget()
        self.tab1.setRowCount(5)
        self.tab1.setColumnCount(1)
        self.tab1.setHorizontalHeaderLabels(['Results'])
        self.tab1.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        i = 0
        for x in self.resultset:
            item = QTableWidgetItem(x[0])
            item.setFlags((Qt.ItemIsSelectable |  Qt.ItemIsEnabled))
            self.tab1.setItem(0, i, item)
            i=i+1
        self.tab1.doubleClicked.connect(self.on_tab1)
        rlayout.addWidget(self.tab1,1,0,1,2)
        
        self.tab2 = QTableWidget()
        self.tab2.setRowCount(1)
        self.tab2.setColumnCount(1)
        self.tab2.setHorizontalHeaderLabels(['Results'])
        self.tab2.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        item = QTableWidgetItem(self.resultset[0][0])
        item.setFlags((Qt.ItemIsSelectable |  Qt.ItemIsEnabled))
        self.tab2.setItem(0, 0, item)
        self.tab2.doubleClicked.connect(self.on_tab2)
        rlayout.addWidget(self.tab2,1,2,1,2)
        self.tab2.hide()
        
        self.resultgroup.setLayout(rlayout)
        self.resultgroup.hide()
        
    @pyqtSlot()
    def on_tab1(self):
        for currentQTableWidgetItem in self.tab1.selectedItems():
            s = currentQTableWidgetItem.text()
            for x in self.resultset:
                if s == x[0]:
                    q = "Prob of "+s+" is "+str(x[1])
        print(s)
        QMessageBox.about(self,s,q)
            
    @pyqtSlot()
    def on_tab2(self):
        for currentQTableWidgetItem in self.tab2.selectedItems():
            s = currentQTableWidgetItem.text()
            for x in self.resultset:
                if s == x[0]:
                    q = "Prob of "+s+" is "+str(x[1])
        print(s)
        QMessageBox.about(self,s,q)
            
    def btnstate(self,r):
        if r.text()=="Top 5":
            if r.isChecked() == True:
                print("1 is selected")
                self.tab1.show()
                self.tab2.hide()
            else:
                print("1 is deselected")
        else:
            if r.isChecked() == True:
                print("2 is selected")
                self.tab1.hide()
                self.tab2.show()
            else:
                print("2 is deselected")
        
    def showimage(self):
        ipixmap = QPixmap(self.fileName)
        ipixmap = ipixmap.scaled(256,256)
        self.ilabel.setPixmap(ipixmap)
        
        self.imagegroup.show()
    
    @pyqtSlot()
    def on_click(self):
        self.question = self.textbox.text()
        print(self.question)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.xpm *.jpg *.jpeg)",options=options)
        if self.fileName:
            print(self.fileName)
            self.ibutton.hide()
            self.showimage()
            self.subutton.show()
            
    @pyqtSlot()
    def on_reselect(self):
        print("clicked on reselect")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.xpm *.jpg *.jpeg)",options=options)
        if self.fileName:
            print(self.fileName)
            ipixmap = QPixmap(self.fileName)
            ipixmap = ipixmap.scaled(256,256)
            self.ilabel.setPixmap(ipixmap)
        
    @pyqtSlot()
    def on_submit(self):
        print("clicked submit")
        self.question = self.textbox.text()
        if self.question and self.fileName:
            print(self.question)
            print(self.fileName)
            self.resultset = run_func(self.question,self.fileName)
            i =0
            for x in self.resultset:
                item = QTableWidgetItem(x[0])
                item.setFlags((Qt.ItemIsSelectable |  Qt.ItemIsEnabled))
                self.tab1.setItem(0, i, item)
                i=i+1
            item = QTableWidgetItem(self.resultset[0][0])
            item.setFlags((Qt.ItemIsSelectable |  Qt.ItemIsEnabled))
            self.tab2.setItem(0, 0, item)
            #self.imagegroup.hide()
            #self.questiongroup.hide()
            #self.subutton.hide()
            self.resultgroup.show()
        else:
            if self.question:
                print("enter image")
            else:
                print("enter question")
    
    @pyqtSlot()
    def reset(self):
        self.textbox.setText("")
        self.question=""
        self.fileName=""
        self.questiongroup.show()
        self.ibutton.show()
        self.imagegroup.hide()
        self.subutton.hide()
        self.resultgroup.hide()
        
    @pyqtSlot()
    def on_clickhelp(self):
        print("code for dialog to run")
        
    @pyqtSlot()
    def on_clickabout(self):
        print("code for about the application")
        
if __name__=='__main__':
        app = QApplication(sys.argv)
        ex = App()
        sys.exit(app.exec_())
