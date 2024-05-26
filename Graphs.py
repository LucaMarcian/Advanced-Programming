#Importing pyqt5 and the necessary widgets to display the GUI 
from PyQt5 import QtCore, QtGui, QtWidgets

#importing matplotlib to create graphs 
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')

#importing pandas and numpy to prepare variables and compute statistics 
import pandas as pd
import numpy as np 


class Ui_Graphs(object):

    #FUNCTION TO PLOT BASED ON USER INPUT
    def Plot(self):
        """
        Function used for plotting the graphs on a new window
        based on user provided information

        From the combo boxes available in the user interface it's derived
        the x and y, graph type, graph theme and period to restrict the
        plotting to     
        """
        # Retrieve the Data
        df = pd.read_csv('book_data.csv')

        # Convert 'End' to datetime
        df['End'] = pd.to_datetime(df['End'])

        # Get the initial and final date from the user interface
        from_date = self.plotFromDateTimeEdit.dateTime().toPyDateTime()
        to_date = self.plottoDateEdit.dateTime().toPyDateTime()

        # Filter rows where 'End' is between selected dates
        df = df[df['End'].between(from_date, to_date) | df['End'].isna()]

        # Retrieve variables 
        X = self.xAxisComboBox.currentText()
        X_counts = df[X].value_counts()
        Y = self.yAxisComboBox.currentText()
        df['Y_tot'] = df.groupby(X)[Y].transform('sum')  
        # total of var Y by groups of var X, 
        # is used in 2d graphs as they show cumulative measures

        #Setting theme
        theme = self.comboBox.currentText()
        plt.style.use(theme)
        
        # Create an array of colors for the plots
        colors = plt.cm.viridis(np.linspace(0, 1, len(X_counts.index)))

        #generate basic fig
        fig, ax = plt.subplots(figsize = (8, 6))
        
        #Gen the various plots
        if self.graphTypeComboBox.currentText() == "Pie (x)":
            ax.pie(X_counts, autopct='%1.1f%%', startangle=140, pctdistance=0.65, labels=X_counts.index)
            centre_circle = plt.Circle((0,0),0.35,fc='white')
            fig.gca().add_artist(centre_circle)
            ax.axis('equal')

            # Add varname in the centre of the pie
            plt.text(0, 0, X, horizontalalignment='center', verticalalignment='center', fontsize=12, color='black')

            plt.tight_layout()
            
        elif self.graphTypeComboBox.currentText() == "Hist (x)":
            ax.bar(X_counts.index, X_counts, color=colors)

            ax.set_xlabel(X)
            ax.set_ylabel('Number of Books')
            title = 'Number of books by ' + self.xAxisComboBox.currentText()
            ax.set_title(title)

            # Apply tight layout
            plt.xticks(rotation=30, ha='right')

            plt.tight_layout()
        elif self.graphTypeComboBox.currentText() == "Scatter (x,y)":
            # Create the scatter plot
            df = df.sort_values(X)
            ax.scatter(df[X], df['Y_tot'])

            # Set the labels
            ax.set_xlabel(X)
            ax.set_ylabel(Y)
            title = 'Scatter plot of Book ' + X + ' vs book ' + Y
            ax.set_title(title)
            plt.xticks(rotation=30, ha='right')
            plt.tight_layout()

        elif self.graphTypeComboBox.currentText() == "Line (x,y)":
            # Create the line plot
            df = df.sort_values(X)
            ax.plot(df[X], df['Y_tot'])

            # Set the labels
            ax.set_xlabel(X)
            ax.set_ylabel('total ' + Y)
            title = 'Plot of Book ' + X + ' vs book ' + Y
            ax.set_title(title)
            plt.xticks(rotation=30, ha='right')
            plt.tight_layout()
        elif self.graphTypeComboBox.currentText() == "Bar (x,y)":
            # Create the bar plot
            df = df.sort_values(X)
            ax.bar(df[X], df['Y_tot'])

            # Set the labels
            ax.set_xlabel(X)
            ax.set_ylabel('total ' + Y)
            title = 'Bar graph of Book ' + X + ' and book ' + Y
            ax.set_title(title)
            plt.xticks(rotation=30, ha='right')
            plt.tight_layout()
        elif self.graphTypeComboBox.currentText() == "Stem (x,y)":
            # Create the stem plot
            df = df.sort_values(X)
            df['Y_tot'] = df.groupby(X)[Y].sum()
            ax.stem(df[X], df['Y_tot'])

            # Set the labels
            ax.set_xlabel(X)
            ax.set_ylabel('total ' + Y)
            title = 'Stem plot of Book ' + X + ' and book ' + Y
            ax.set_title(title)
            plt.xticks(rotation=30, ha='right')
            plt.tight_layout()

        plt.show()
        
    ###BEGINNING OF IMPORTED GUI###
    def setupUi(self, Graphs):
        Graphs.setObjectName("Graphs")
        Graphs.resize(290, 274)
        self.centralwidget = QtWidgets.QWidget(Graphs)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.xAxisLabel = QtWidgets.QLabel(self.centralwidget)
        self.xAxisLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.xAxisLabel.setObjectName("xAxisLabel")
        self.gridLayout_2.addWidget(self.xAxisLabel, 0, 0, 1, 1)
        self.xAxisComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.xAxisComboBox.setObjectName("xAxisComboBox")
        self.gridLayout_2.addWidget(self.xAxisComboBox, 0, 1, 1, 1)
        self.plotFromLabel = QtWidgets.QLabel(self.centralwidget)
        self.plotFromLabel.setObjectName("plotFromLabel")
        self.gridLayout_2.addWidget(self.plotFromLabel, 0, 2, 1, 1)
        self.plotFromDateTimeEdit = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.plotFromDateTimeEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(1754, 1, 1), QtCore.QTime(0, 0, 0)))
        self.plotFromDateTimeEdit.setObjectName("plotFromDateTimeEdit")
        self.gridLayout_2.addWidget(self.plotFromDateTimeEdit, 0, 3, 1, 1)
        self.yAxisLabel = QtWidgets.QLabel(self.centralwidget)
        self.yAxisLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.yAxisLabel.setObjectName("yAxisLabel")
        self.gridLayout_2.addWidget(self.yAxisLabel, 1, 0, 1, 1)
        self.yAxisComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.yAxisComboBox.setObjectName("yAxisComboBox")
        self.gridLayout_2.addWidget(self.yAxisComboBox, 1, 1, 1, 1)
        self.plottoLabel = QtWidgets.QLabel(self.centralwidget)
        self.plottoLabel.setObjectName("plottoLabel")
        self.gridLayout_2.addWidget(self.plottoLabel, 1, 2, 1, 1)
        self.plottoDateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.plottoDateEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(9999, 1, 1), QtCore.QTime(0, 0, 0)))
        self.plottoDateEdit.setObjectName("plottoDateEdit")
        self.gridLayout_2.addWidget(self.plottoDateEdit, 1, 3, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 2, 1, 1, 4)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.graphTypeLabel = QtWidgets.QLabel(self.centralwidget)
        self.graphTypeLabel.setMaximumSize(QtCore.QSize(100, 20))
        self.graphTypeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.graphTypeLabel.setObjectName("graphTypeLabel")
        self.gridLayout.addWidget(self.graphTypeLabel, 0, 0, 1, 1)
        self.selectThemeLabel = QtWidgets.QLabel(self.centralwidget)
        self.selectThemeLabel.setMinimumSize(QtCore.QSize(80, 20))
        self.selectThemeLabel.setMaximumSize(QtCore.QSize(100, 20))
        self.selectThemeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.selectThemeLabel.setObjectName("selectThemeLabel")
        self.gridLayout.addWidget(self.selectThemeLabel, 0, 1, 1, 1)
        self.graphTypeComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.graphTypeComboBox.setMinimumSize(QtCore.QSize(78, 0))
        self.graphTypeComboBox.setMaximumSize(QtCore.QSize(100, 16777215))
        self.graphTypeComboBox.setObjectName("graphTypeComboBox")
        self.gridLayout.addWidget(self.graphTypeComboBox, 1, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setMinimumSize(QtCore.QSize(78, 0))
        self.comboBox.setMaximumSize(QtCore.QSize(100, 16777215))
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 1, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 1, 1, 4)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 3, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 28, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 1, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 4, 0, 1, 2)
        self.ButtonPlot = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonPlot.setEnabled(True)
        self.ButtonPlot.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.ButtonPlot.setFont(font)
        self.ButtonPlot.setObjectName("ButtonPlot")
        self.gridLayout_3.addWidget(self.ButtonPlot, 4, 2, 1, 2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem3, 4, 4, 1, 2)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem4, 2, 5, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem5, 0, 5, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem6, 2, 0, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem7, 0, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        Graphs.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Graphs)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 290, 21))
        self.menubar.setObjectName("menubar")
        Graphs.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Graphs)
        self.statusbar.setObjectName("statusbar")
        Graphs.setStatusBar(self.statusbar)

        self.retranslateUi(Graphs)
        QtCore.QMetaObject.connectSlotsByName(Graphs)

    def retranslateUi(self, Graphs):
        _translate = QtCore.QCoreApplication.translate
        Graphs.setWindowTitle(_translate("Graphs", "Graph Maker"))
        self.xAxisLabel.setText(_translate("Graphs", "X-Axis"))
        self.plotFromLabel.setText(_translate("Graphs", "From:"))
        self.plotFromDateTimeEdit.setDisplayFormat(_translate("Graphs", "MM/yyyy"))
        self.yAxisLabel.setText(_translate("Graphs", "Y-Axis"))
        self.plottoLabel.setText(_translate("Graphs", " To:"))
        self.plottoDateEdit.setDisplayFormat(_translate("Graphs", "MM/yyyy"))
        self.graphTypeLabel.setText(_translate("Graphs", "Graph type"))
        self.selectThemeLabel.setText(_translate("Graphs", "Theme"))
        self.ButtonPlot.setText(_translate("Graphs", "PLOT!"))
        
        ###END OF IMPORTED GUI###       
        
        #Connnect the "Plot" function to the button
        self.ButtonPlot.clicked.connect(self.Plot)

        #Add elements to the dropdown menu
        self.GraphTypes = ["Pie (x)", "Hist (x)", "Scatter (x,y)", "Line (x,y)", "Bar (x,y)", "Stem (x,y)" ]
        self.graphTypeComboBox.addItems(self.GraphTypes)

        self.themes = ['bmh', 'classic', 'dark_background', 'fast', 
        'fivethirtyeight', 'ggplot', 'grayscale', 'Solarize_Light2', 'tableau-colorblind10']  
        self.comboBox.addItems(self.themes)

        self.variables_x = ['Authors', 'Rating', 'N° pages', 'Genre', 
        'Reading Status', 'Reading Place', 'Storing Place', 'Publication']
        self.variables_y = ['Rating', 'N° pages']
        self.xAxisComboBox.addItems(self.variables_x)
        self.yAxisComboBox.addItems(self.variables_y)

#Allow all the above to be displayed when program is run
# or called from the open window function of MainPage
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Graphs = QtWidgets.QMainWindow()
    ui = Ui_Graphs()
    ui.setupUi(Graphs)
    Graphs.show()
    sys.exit(app.exec_())
