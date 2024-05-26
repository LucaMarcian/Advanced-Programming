#Importing UI of the windows connected to the main one
from AddBook import Ui_AddBook
from Graphs import Ui_Graphs

#import matplotlib and pandas to create graphs
import pandas as pd
import matplotlib
matplotlib.use('Qt5Agg') #needed to render plots into pyqt5 widgets
from matplotlib.backends.backend_qt5agg import FigureCanvas #needed to render plots into pyqt5 widgets
from matplotlib.figure import Figure

#Import the PyQt5 and the needed modules 
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QAbstractItemView, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import sys

import os #used to check for the presence of files in directory

#At the beginning I generate the csv file for the book if not present
if not os.path.isfile('book_data.csv'):
    headers = ["Title", "Authors", "Publication", "N° pages", "Genre", "Reading Status", "Start", "End", "Reading Place", "Storing Place", "Rating"]
    df = pd.DataFrame(columns=headers)
    df.to_csv('book_data.csv', index=False)


class Ui_Menu(object):

    def setupUi(self, Menu):
        Menu.setObjectName("Menu")
        Menu.resize(1400, 800)
        Menu.setMinimumSize(QtCore.QSize(0, 3))
        self.centralwidget = QtWidgets.QWidget(Menu)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.add_books = QtWidgets.QPushButton(self.splitter)
        self.add_books.setMinimumSize(QtCore.QSize(100, 100))
        self.add_books.setObjectName("add_books")
        self.access_graphs = QtWidgets.QPushButton(self.splitter)
        self.access_graphs.setMinimumSize(QtCore.QSize(40, 100))
        self.access_graphs.setObjectName("access_graphs")
        self.horizontalLayout_13.addWidget(self.splitter)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_13.addWidget(self.frame)
        self.horizontalLayout_13.setStretch(0, 2)
        self.horizontalLayout_13.setStretch(1, 10)
        self.verticalLayout.addLayout(self.horizontalLayout_13)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.horizontalLayout_14.addWidget(self.tableView)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem2)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem3)
        self.ButtonAdd_2 = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonAdd_2.setObjectName("ButtonAdd_2")
        self.horizontalLayout_8.addWidget(self.ButtonAdd_2)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_8)
        self.splitter_3 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.ButtoDelete_2 = QtWidgets.QPushButton(self.splitter_3)
        self.ButtoDelete_2.setObjectName("ButtoDelete_2")
        self.ButtonRestore_2 = QtWidgets.QPushButton(self.splitter_3)
        self.ButtonRestore_2.setObjectName("ButtonRestore_2")
        self.verticalLayout_5.addWidget(self.splitter_3)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem5)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem6)
        self.verticalLayout_5.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_refresh = QtWidgets.QHBoxLayout()
        self.horizontalLayout_refresh.setObjectName("horizontalLayout_refresh")
        spacerItem_refresh1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_refresh.addItem(spacerItem_refresh1)
        self.ButtonRefresh = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonRefresh.setObjectName("ButtonRefresh")
        self.horizontalLayout_refresh.addWidget(self.ButtonRefresh)
        spacerItem_refresh2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_refresh.addItem(spacerItem_refresh2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_refresh)

        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem7)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setMinimumSize(QtCore.QSize(118, 0))
        self.line_2.setMaximumSize(QtCore.QSize(118, 16777215))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_10.addWidget(self.line_2)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem8)
        self.verticalLayout_5.addLayout(self.horizontalLayout_10)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem9)
        self.ButtonSave_2 = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonSave_2.setMinimumSize(QtCore.QSize(0, 30))
        self.ButtonSave_2.setMaximumSize(QtCore.QSize(75, 30))
        self.ButtonSave_2.setObjectName("ButtonSave_2")
        self.horizontalLayout_11.addWidget(self.ButtonSave_2)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem10)
        self.verticalLayout_6.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.verticalLayout_6.addLayout(self.horizontalLayout_12)
        self.verticalLayout_5.addLayout(self.verticalLayout_6)
        self.horizontalLayout_7.addLayout(self.verticalLayout_5)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem11)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        spacerItem12 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem12)
        self.horizontalLayout_14.addLayout(self.verticalLayout_4)
        self.horizontalLayout_14.setStretch(0, 10)
        self.horizontalLayout_14.setStretch(1, 2)
        self.verticalLayout.addLayout(self.horizontalLayout_14)
        self.verticalLayout.setStretch(0, 10)
        self.verticalLayout.setStretch(2, 10)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        Menu.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Menu)
        self.statusbar.setObjectName("statusbar")
        Menu.setStatusBar(self.statusbar)

        self.retranslateUi(Menu)
        QtCore.QMetaObject.connectSlotsByName(Menu)

    def retranslateUi(self, Menu):
        _translate = QtCore.QCoreApplication.translate
        Menu.setWindowTitle(_translate("Menu", "Main Page"))
        self.add_books.setText(_translate("Menu", "ADD A BOOK"))
        self.access_graphs.setText(_translate("Menu", "CUSTOM GRAPHS "))
        self.label.setText(_translate("Menu", "Your Current Library:"))
        self.ButtonAdd_2.setText(_translate("Menu", "Add a Row"))
        self.ButtoDelete_2.setText(_translate("Menu", "Delete Row"))
        self.ButtonRestore_2.setText(_translate("Menu", "Restore Row"))
        self.ButtonRefresh.setText(_translate("Menu", "Refresh Library"))
        self.ButtonSave_2.setText(_translate("Menu", "Save"))

        #CONNECTING BUTTONS TO FUNCTIONALITIES
        self.add_books.clicked.connect(lambda: self.open_window(Ui_AddBook()))
        self.access_graphs.clicked.connect(lambda: self.open_window(Ui_Graphs()))


        #ADDING GRAPH AND STATISTICS TO FRAME        
    
        # Create the layout for the frame
        self.layout = QtWidgets.QHBoxLayout(self.frame)
        
        # Create the left plot canvas
        self.figure_left = Figure(figsize=(4, 4), dpi=100)
        self.canvas_left = FigureCanvas(self.figure_left)
        self.layout.addWidget(self.canvas_left)
        self.figure_left.patch.set_facecolor((0.941, 0.941, 0.941))
        
        # Create the center labels

        # Load the data from the CSV file
        df = pd.read_csv('book_data.csv')

        # Filter the dataframe to include only the books that have been read
        df = df[df['Reading Status'] == 'Read']
        df['Start'] = pd.to_datetime(df['Start'], format='%Y-%m')
        df['End'] = pd.to_datetime(df['End'], format='%Y-%m')
        days= (df['End'].max() -df['Start'].min()).days
        
        # Calculate the statistics
        average_pages_per_day = round((df['N° pages'].sum())/days, 3)
        #Set up the labels
        if df['Reading Place'].empty:
            favourite_reading_place = None
        else:
            favourite_reading_place = df['Reading Place'].mode()[0]

        if df['Authors'].empty:
            favourite_author = None
        else:
            favourite_author = df['Authors'].mode()[0]

        if df['Genre'].empty:
            favourite_genre = None
        else:
            favourite_genre = df['Genre'].mode()[0]

        # Create the labels     
        self.label_layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.label_layout)

        font = QtGui.QFont()

        label = QtWidgets.QLabel(f"Average Pages per Day: {average_pages_per_day}")
        font.setPointSize(12)  # change the font size
        font.setBold(False)        
        label.setFont(font)  # set the font to the QLabel
        self.label_layout.addWidget(label)

        label = QtWidgets.QLabel(f"Favourite Reading Place: {favourite_reading_place}")
        font.setPointSize(12)  
        font.setBold(False)        
        label.setFont(font)  
        self.label_layout.addWidget(label)

        label = QtWidgets.QLabel(f"Favourite Author: {favourite_author}")
        font.setPointSize(12)  
        label.setFont(font)
        font.setBold(False)
        self.label_layout.addWidget(label)

        label = QtWidgets.QLabel(f"Favourite Genre: {favourite_genre}")
        font.setPointSize(12)
        font.setBold(False)
        label.setFont(font)
        self.label_layout.addWidget(label)
        
        # Create the right plot canvas
        self.figure_right = Figure(figsize=(4, 2), dpi=100)
        self.canvas_right = FigureCanvas(self.figure_right)
        self.layout.addWidget(self.canvas_right)
        self.figure_right.patch.set_facecolor((0.941, 0.941, 0.941))

        # Plot the data
        self.left_plot()
        self.right_plot()

    #DEFINE THE FUNCTIONS TO PLOT
    def left_plot(self):
        self.figure_right.clf()
        ax = self.figure_left.add_subplot(111)
        ax.cla()
        df = pd.read_csv('book_data.csv')
        df['pg_tot'] = df.groupby('End')['N° pages'].transform('sum')
        df['End'] = pd.to_datetime(df['End'], format='%Y-%m')
        df = df.sort_values(by='End')

        ax.plot(df['End'], df['pg_tot'])
        ax.set_xlabel('Time')
        ax.set_ylabel('Total Read pages')
        title = 'Number of pages read over time'
        ax.set_title(title)
        
        self.figure_left.autofmt_xdate() 
        self.figure_left.tight_layout()

        self.canvas_left.draw()

    def right_plot(self):
        self.figure_right.clf()
        ax = self.figure_right.add_subplot(111)
        ax.cla()
        df = pd.read_csv('book_data.csv')
        X = df['Reading Status'].value_counts()
        ax.pie(X, autopct='%1.1f%%', startangle=140, pctdistance=0.65, labels=X.index)
        title = 'Read vs Not Read Books'
        ax.set_title(title)
        # Draw 
        self.canvas_right.draw()

    
    #DEFINE THE FUNCTION TO OPEN OTHER WINDOWS
    def open_window(self, Ui):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui
        self.ui.setupUi(self.window)
        self.window.show()


        
#DISPLAYING THE LIBRARY

class CsvReader(QMainWindow, Ui_Menu):
    def __init__(self, csv_file):
        super().__init__()

        self.deletedRows = [] #Needed to restore rows

        self.setupUi(self) #Needed to display GUI defined above and inherited

        # Create QStandardItemModel object and link it to the table viewer        
        self.model = QStandardItemModel(self)
        self.tableView.setModel(self.model)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows) 
        #this allows to selecct the whole row by simply clicking on any part 
        #of it (and not only by cliching the row index)
        
        self.tableView.setSortingEnabled(True)
        #this allows for lexicographic sorting to take place, problem with numbers
        
        #This signals changes to the model to the method ManualUpdate
        self.model.itemChanged.connect(self.ManualUpdate)


        #select csv and read it through the apposit method
        self.csv_file = csv_file 
        self.loadCsv()

        # Connect the buttons to functions
        self.ButtonSave_2.clicked.connect(self.saveCsv)
        self.ButtoDelete_2.clicked.connect(self.deleteRow)
        self.ButtonRestore_2.clicked.connect(self.restoreRow)
        self.ButtonAdd_2.clicked.connect(self.addRow)
        self.ButtonRefresh.clicked.connect(self.refreshCsv)

    ####DEFINE FUNCTIONS###
    def loadCsv(self):
        #read csv
        self.df = pd.read_csv(self.csv_file)

        # Load headers
        self.model.setHorizontalHeaderLabels(self.df.columns)
        # Load data
        for row in self.df.values:
            items = [QStandardItem(str(i)) for i in row]
            self.model.appendRow(items)

    def ManualUpdate(self):
        # Update pandas df when StandardItemModel elements are changed
        self.df = pd.DataFrame([[self.model.item(row, col).text() for col in range(self.model.columnCount())]
                                for row in range(self.model.rowCount())],
                               columns=self.df.columns)

    def saveCsv(self):
        self.ManualUpdate()
        with open(self.csv_file, 'w', encoding='utf-8') as file:
            file.write(self.df.to_csv(index=False))


    def deleteRow(self):
        indexes = self.tableView.selectionModel().selectedRows()
        if not indexes:
            QMessageBox.warning(self, 'Warning', 'No row selected.')
            return

        for index in sorted(indexes, reverse=True):
            deletedRow = self.df.iloc[index.row()].copy()
            self.deletedRows.append((index.row(), deletedRow))
            self.df = self.df.drop(self.df.index[index.row()])
            self.model.removeRow(index.row())

    def restoreRow(self):
        if not self.deletedRows:
            QMessageBox.warning(self, 'Warning', 'No row to restore.')
            return

        row, rowData = self.deletedRows.pop()
        self.df = pd.concat([self.df.iloc[:row], pd.DataFrame(rowData).T, self.df.iloc[row:]]).reset_index(drop=True)
        self.model.insertRow(row, [QStandardItem(str(i)) for i in rowData])
    
    def addRow(self):
        # Create a new row with default values
        new_row = pd.DataFrame([[""]*len(self.df.columns)], columns=self.df.columns)
        
        # Append the new row to the dataframe
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        
        # Create a QStandardItem for each value in the new row
        items = [QStandardItem(str(i)) for i in new_row.iloc[0]]
        
        # Append the new row to the model
        self.model.appendRow(items)
    
    def refreshCsv(self):
        # Clear the model
        self.model.clear()

        # Reload the CSV into the model
        self.loadCsv()
        self.left_plot()
        self.right_plot() 

###Runs what defined above upon program execution 
#(here the QApp is launced as the full GUI is inherited by 
# Csvreader window) 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    CsvReader = CsvReader('book_data.csv')
    CsvReader.show()
    sys.exit(app.exec_())
