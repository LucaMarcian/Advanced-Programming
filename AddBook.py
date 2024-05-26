#Import the PyQt5 and the needed modules 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QListWidget, QWidget, QMessageBox

import pandas as pd #needed to create the csv I'll use to make graphs
import os           #used to determine if the csv file is present or if it has to be created
import requests     #nedded to connect with  google API 


class Ui_AddBook(QWidget):

    # generate a dictionary to be populated with the info retrieved
    data = {} 

    #BOOK SEARCH AND SELECTION
    def SearchBooks(self, title):
        '''
        Function to send a get request to google API and store search results
        '''

        #Define details of search 
        url = "https://www.googleapis.com/books/v1/volumes"
        params = {
            "q": title,
            "printType": "books",
            "maxResults": 10
        }

        #send get request & store result in the data object (dictionary)
        response = requests.get(url, params=params)
        data = response.json()

        #generate the list to store book info turples
        self.books = []

        #estract wanted infos from data dictionary and append them to 
        #the library self.books created above 
        if "items" in data:
            for item in data["items"]:
                book = item["volumeInfo"]
                title = book.get("title")
                authors = ", ".join(book.get("authors", []))
                publication_year = book.get("publishedDate")
                if publication_year is not None:
                    publication_year = publication_year[:4] 
                    #this is done as sometimes publication date is not available 
                    #thus the slicer operator (used to grab just publication year and not the whole date)
                    #encounters a TypeError leading the program to crash
                pages = book.get("pageCount")
                categories = ", ".join(book.get("categories", []))
                self.books.append((title, authors, publication_year, pages, categories))
            return self.books 
        else:
            return self.books

    def display_results(self):
        '''
        Method to run the search and update search results 
        '''

        # Clear the list widget at the beginning of each search
        self.listView.clear()  
        #Runs the above functions with the keyword given by user
        #(onlinetext is the name of the line where the user types)
        title = self.onlinetitle.text()
        books = self.SearchBooks(title)

        #adds to the listView object the retrieved items      
        for book in books:
            self.listView.addItem(f"{book[0]} by {book[1]} ({book[2]})")

        #triggers the select method if one item is clicked
        self.listView.itemClicked.connect(self.Select)
        
        #changes the label under button save "as not saved"
        self.label_saved.setText('''Saving Status:
Not Saved''')

    def Select(self, item):
        """
        Method to retireve selected book info
        """
        #makes sure the user selected the desired boook by asking it 
        #with a message boc widges
        reply = QMessageBox.question(self, 'Book Selected', "Do you want to select this book?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        #if yes store the book data in the "data" dictionary
        #if no does nothing 
        if reply == QMessageBox.Yes:
            book_info = item.text().split(' by ')
            title = book_info[0]
            authors = book_info[1].split(' (')[0]
            publication_year = book_info[1].split(' (')[1][:-1]

            for book in self.books:
                if book[0] == title and book[1] == authors and book[2] == publication_year:
                    self.data['Title'] = book[0]
                    self.data['Authors'] = book[1]
                    self.data['Publication'] = book[2]
                    self.data['N° pages'] = book[3]
                    self.data['Genre'] = book[4].split(',')[0] if book[4] else None
                    break

    def Save(self):
        """
        This method translates the dictionary containing the book information to a one-line pandas dataframe wich is then appended to the csv 'dataset' file.
        k represent the dictionary keys (which will become the headers of the csv file) 
        and v the values, which will become the data point
        """
        #1 Make sure a book title has been entered
        if ((self.titleLineEdit.text() == '') or (self.authorSurnameLineEdit.text()=='')) and self.listView.count() == 0:
            ##Fix by adding if search display list empty instead of the bool seaRch occurred
            QMessageBox.warning(self, 'Error', 'Please enter a book information manually or search online before saving.')
            return
        
        #2 if manual search
        if self.listView.count() == 0:
            self.data['Title'] = self.titleLineEdit.text()
            self.data['Authors'] = self.authorSurnameLineEdit.text() 
            self.data['Publication'] = self.year_dateEdit.date().toString('yyyy')
            self.data['N° pages'] = self.Npages_spinBox.value()
            self.data['Genre'] = self.GenreComboBox.currentText()

        #3 understand if the book had been Read or not
        self.data['Reading Status'] = self.StatusComboBox.currentText()
        if self.data['Reading Status'] == 'Read':    
            self.data['Start'] = self.ReadingInitDateEdit.date().toString('yyyy-MM')
            self.data['End'] = self.ReadingEndDateEdit.date().toString('yyyy-MM')
            self.data['Reading Place'] = self.ReadingComboBox.currentText()
            self.data['Storing Place'] = self.StoringComboBox.currentText()
            self.data['Rating'] = self.RatingLabel.text()
        else:
            self.data['Start'] = None
            self.data['End'] = None
            self.data['Reading Place'] = None
            self.data['Storing Place'] = None
            self.data['Rating'] = None

        #Transform the dictionary into a Pandas dataframe
        book_list = pd.DataFrame({k: [v] for k, v in self.data.items()})

        #This dataframe is then added to a csv file which consitute this project's storage method  
        if not os.path.isfile('book_data.csv'):
            book_list.to_csv('book_data.csv', header=True, index=False)
                    #if not existent yet the csv is created with headers

        else:   
            book_list.to_csv('book_data.csv', mode='a', header=False, index=False)
                    #if csv exists already data are simply appended withoutwriting the headers
                    #mode='a' opens the file in append mode, which means that data will be added to the end of the file instead of overwriting the existing content
                    #header=False prevents pandas from writing column headers when appending data.
    
        self.label_saved.setText('''Saving Status:
Saved''')
        self.listView.clear()
        self.onlinetitle.setText(' ')
        self.titleLineEdit.setText(' ')
        self.authorSurnameLineEdit.setText(' ')
 
    
    ####BEGINNING OF IMPORTED GUI####    
        
    def setupUi(self, AddBook):
        AddBook.setObjectName("AddBook")
        AddBook.resize(530, 530)
        AddBook.setIconSize(QtCore.QSize(0, 0))
        self.centralwidget = QtWidgets.QWidget(AddBook)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.textBrowser_7 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_7.setMaximumSize(QtCore.QSize(16777215, 37))
        self.textBrowser_7.setObjectName("textBrowser_7")
        self.gridLayout_4.addWidget(self.textBrowser_7, 0, 1, 1, 1)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(0, -1, -1, -1)
        self.formLayout.setObjectName("formLayout")
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setObjectName("titleLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.titleLabel)
        self.titleLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.titleLineEdit.setObjectName("titleLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.titleLineEdit)
        self.authorSSurnameLabel = QtWidgets.QLabel(self.centralwidget)
        self.authorSSurnameLabel.setObjectName("authorSSurnameLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.authorSSurnameLabel)
        self.authorSurnameLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.authorSurnameLineEdit.setObjectName("authorSurnameLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.authorSurnameLineEdit)
        self.nPagesLabel = QtWidgets.QLabel(self.centralwidget)
        self.nPagesLabel.setObjectName("nPagesLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.nPagesLabel)
        self.Npages_spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.Npages_spinBox.setMaximum(10000000)
        self.Npages_spinBox.setObjectName("Npages_spinBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.Npages_spinBox)
        self.publicationYearLabel = QtWidgets.QLabel(self.centralwidget)
        self.publicationYearLabel.setObjectName("publicationYearLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.publicationYearLabel)
        self.year_dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.year_dateEdit.setObjectName("year_dateEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.year_dateEdit)
        self.genreLabel = QtWidgets.QLabel(self.centralwidget)
        self.genreLabel.setObjectName("genreLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.genreLabel)
        self.GenreComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.GenreComboBox.setEnabled(True)
        self.GenreComboBox.setObjectName("GenreComboBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.GenreComboBox)
        self.formLayout_2.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.formLayout)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_27 = QtWidgets.QLabel(self.centralwidget)
        self.label_27.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_27.setAlignment(QtCore.Qt.AlignCenter)
        self.label_27.setWordWrap(True)
        self.label_27.setObjectName("label_27")
        self.verticalLayout_6.addWidget(self.label_27)
        self.onlinetitle = QtWidgets.QLineEdit(self.centralwidget)
        self.onlinetitle.setText("")
        self.onlinetitle.setObjectName("onlinetitle")
        self.verticalLayout_6.addWidget(self.onlinetitle)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ButtonOnlineSearch = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonOnlineSearch.setObjectName("ButtonOnlineSearch")
        self.horizontalLayout.addWidget(self.ButtonOnlineSearch)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.listView = QListWidget(self.centralwidget)
        self.listView.setMaximumSize(QtCore.QSize(16777215, 80))
        self.listView.setObjectName("listView")
        self.verticalLayout_6.addWidget(self.listView)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setText("")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_6.addWidget(self.label_2)
        self.formLayout_2.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.verticalLayout_6)
        self.gridLayout_4.addLayout(self.formLayout_2, 1, 0, 1, 2)
        self.textBrowser_6 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_6.setMaximumSize(QtCore.QSize(16777215, 37))
        self.textBrowser_6.setObjectName("textBrowser_6")
        self.gridLayout_4.addWidget(self.textBrowser_6, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_4)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 11)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 3)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.ReadingInitDateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.ReadingInitDateEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(0, 0, 0)))
        self.ReadingInitDateEdit.setMinimumDateTime(QtCore.QDateTime(QtCore.QDate(2001, 1, 1), QtCore.QTime(0, 0, 0)))
        self.ReadingInitDateEdit.setCalendarPopup(False)
        self.ReadingInitDateEdit.setCurrentSectionIndex(0)
        self.ReadingInitDateEdit.setObjectName("ReadingInitDateEdit")
        self.gridLayout_3.addWidget(self.ReadingInitDateEdit, 1, 0, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setObjectName("label_16")
        self.gridLayout_3.addWidget(self.label_16, 2, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setObjectName("label_15")
        self.gridLayout_3.addWidget(self.label_15, 2, 0, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setObjectName("label_13")
        self.gridLayout_3.addWidget(self.label_13, 0, 0, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setObjectName("label_14")
        self.gridLayout_3.addWidget(self.label_14, 0, 1, 1, 1)
        self.ReadingComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.ReadingComboBox.setEditable(True)
        self.ReadingComboBox.setObjectName("ReadingComboBox")
        self.gridLayout_3.addWidget(self.ReadingComboBox, 3, 0, 1, 1)
        self.StoringComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.StoringComboBox.setEditable(True)
        self.StoringComboBox.setObjectName("StoringComboBox")
        self.gridLayout_3.addWidget(self.StoringComboBox, 3, 1, 1, 1)
        self.ReadingEndDateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.ReadingEndDateEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2001, 1, 1), QtCore.QTime(0, 0, 0)))
        self.ReadingEndDateEdit.setCalendarPopup(False)
        self.ReadingEndDateEdit.setObjectName("ReadingEndDateEdit")
        self.gridLayout_3.addWidget(self.ReadingEndDateEdit, 1, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 2, 3, 1, 5)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 3, 7, 1, 4)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 2, 8, 1, 3)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 6, 2, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 1, 6, 1, 5)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem6, 6, 0, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem7, 1, 0, 1, 5)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem8, 3, 0, 1, 4)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 0, 2, 1, 7)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.label_17.setFont(font)
        self.label_17.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_17.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_17.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_17.setMidLineWidth(0)
        self.label_17.setTextFormat(QtCore.Qt.AutoText)
        self.label_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_17.setWordWrap(False)
        self.label_17.setObjectName("label_17")
        self.gridLayout_2.addWidget(self.label_17, 1, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setText("")
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 1, 0, 1, 1)
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.horizontalSlider.setAutoFillBackground(True)
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(5)
        self.horizontalSlider.setPageStep(1)
        self.horizontalSlider.setProperty("value", 1)
        self.horizontalSlider.setTracking(True)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setInvertedAppearance(False)
        self.horizontalSlider.setInvertedControls(False)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider.setTickInterval(0)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.gridLayout_2.addWidget(self.horizontalSlider, 0, 0, 1, 4)
        self.RatingLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.RatingLabel.setFont(font)
        self.RatingLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.RatingLabel.setObjectName("RatingLabel")
        self.gridLayout_2.addWidget(self.RatingLabel, 1, 2, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 3, 4, 1, 3)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem9, 6, 10, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem10, 6, 8, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem11, 6, 4, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem12, 6, 6, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_22 = QtWidgets.QLabel(self.centralwidget)
        self.label_22.setObjectName("label_22")
        self.label_22.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout_4.addWidget(self.label_22)
        self.StatusComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.StatusComboBox.setEditable(False)
        self.StatusComboBox.setObjectName("StatusComboBox")
        self.StatusComboBox.addItems(["Read", "Not Read"])
        self.verticalLayout_4.addWidget(self.StatusComboBox)
        self.gridLayout.addLayout(self.verticalLayout_4, 1, 5, 1, 1)
        self.ButtonSave = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.ButtonSave.setFont(font)
        self.ButtonSave.setObjectName("ButtonSave")
        self.gridLayout.addWidget(self.ButtonSave, 6, 5, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem13)
        self.label_saved = QtWidgets.QLabel(self.centralwidget)
        self.label_saved.setObjectName("label_saved")
        self.label_saved.setAlignment(QtCore.Qt.AlignCenter)
        self.horizontalLayout_2.addWidget(self.label_saved)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem14)
        self.gridLayout.addLayout(self.horizontalLayout_2, 7, 5, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.gridLayout_5.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        AddBook.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(AddBook)
        self.statusbar.setObjectName("statusbar")
        AddBook.setStatusBar(self.statusbar)

        self.retranslateUi(AddBook)
        self.horizontalSlider.valueChanged['int'].connect(self.RatingLabel.setNum)
        QtCore.QMetaObject.connectSlotsByName(AddBook)

        ###Combo box values setting
        self.ReadingComboBox.addItems(["Home ", "Train ", "Vacations ", "Commuting "])
        self.StoringComboBox.addItems(["Home ", "Digital ", "Library"])
        self.Generes= ["Antique & Collectibles", "Architecture","Art", "Bibles", "Biography & Autobiography",
                                     "Body, Mind & Spirit", "Business & Economics", "Comics & Graphic Novels", "Computers",
                                     "Cooking", "Crafts & Hobbies", "Design", "Drama", "Education", "Family & Relationships",
                                     "Fiction", "Foreign Language Study", "Games & Activities", "Gardening", "Health & Fitness",
                                     "History", "House & Home", "Humor", "Juvenile Fiction", "Juvenile Nonfiction",
                                     "Language Arts & Disciplines", "Law", "Literary Collections", "Literary Criticism",
                                     "Mathematics", "Medical", "Music", "Nature", "Performing Arts", "Pets","Philosophy",
                                     "Photography", "Poetry", "Political Science", "Psychology", "Reference", "Religion",
                                     "Science", "Self-Help", "Social Science", "Sports & Recreation", "Study Aids",
                                     "Technology & Engineering", "Transportation", "Travel", "True Crime",
                                     "Young Adult Fiction", "Young Adult Nonfiction"]
        self.GenreComboBox.addItems(self.Generes)
        

    def retranslateUi(self, AddBook):
        _translate = QtCore.QCoreApplication.translate
        AddBook.setWindowTitle(_translate("AddBook", "Add a Book"))
        self.textBrowser_7.setHtml(_translate("AddBook", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">SEARCH TITLE ONLINE<br>(be sure to have internet access) </p></body></html>"))
        self.titleLabel.setText(_translate("AddBook", "Title:"))
        self.authorSSurnameLabel.setText(_translate("AddBook", "Author\'s Surname:"))
        self.nPagesLabel.setText(_translate("AddBook", "N° pages:"))
        self.publicationYearLabel.setText(_translate("AddBook", "Publication year:"))
        self.year_dateEdit.setStatusTip(_translate("AddBook", "0"))
        self.year_dateEdit.setDisplayFormat(_translate("AddBook", "yyyy"))
        self.genreLabel.setText(_translate("AddBook", "Genre:"))
        self.GenreComboBox.setCurrentText(_translate("AddBook", "Antique & Collectibles"))
        self.label_27.setText(_translate("AddBook", "Type book title below:"))
        self.ButtonOnlineSearch.setText(_translate("AddBook", "Search"))
        self.textBrowser_6.setHtml(_translate("AddBook", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">INSERT BOOK INFORMATION MANUALLY</p></body></html>"))
        self.ReadingInitDateEdit.setDisplayFormat(_translate("AddBook", "MM/yyyy"))
        self.label_16.setText(_translate("AddBook", "Storing Place"))
        self.label_15.setText(_translate("AddBook", "Reading Place"))
        self.label_13.setText(_translate("AddBook", "Reading started"))
        self.label_14.setText(_translate("AddBook", "Reading ended"))
        self.ReadingEndDateEdit.setDisplayFormat(_translate("AddBook", "MM/yyyy"))
        self.label_17.setText(_translate("AddBook", "Rating:"))
        self.RatingLabel.setText(_translate("AddBook", "1"))
        self.label_22.setText(_translate("AddBook", "Reading Status"))
        self.label_saved.setText(_translate("AddBook", '''Saving Status: 
Not Saved'''))
        self.ButtonSave.setText(_translate("AddBook", "SAVE"))


        ####END OF IMPORTED GUI####    
        #Storing Data 
        self.ButtonOnlineSearch.clicked.connect(lambda: self.display_results ())
        self.ButtonSave.clicked.connect(lambda: self.Save())


#Allow all the above to be displayed when program is run
# or called from the open window function of MainPage
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AddBook = QtWidgets.QMainWindow()
    ui = Ui_AddBook()
    ui.setupUi(AddBook)
    AddBook.show()
    sys.exit(app.exec_())
