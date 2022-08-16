import sys, os
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class EditWidget(QTableWidget):
    def __init__(self,data):
        super().__init__()
        self.clipboard = QApplication.clipboard()
        self.nrow = len(data)
        self.ncol = len(data[0])
        self.setRowCount(self.nrow)
        self.setColumnCount(self.ncol)
        self.datum = data
        self._set_data()
        self.resizeColumnsToContents()
    
    def _set_data(self):
        for i in range(self.nrow):
            for j in range(self.ncol):
                item = QTableWidgetItem(str(self.datum[i,j]))
                self.setItem(i,j,item)
                
    def _parse_data(self,minrow,maxrow,cols):
        datum = []
        for i in range(minrow,maxrow+1):
            data = []
            for j in cols:
                data.append(str(self.datum[i][j]))
            datum.append("\t".join(data))
        return "\n".join(datum)

    def data_to_clipboard(self):
        cols = []
        minrow = len(self.datum)
        maxrow = 0
        for ran in self.selectedRanges():
            cols.extend(list(range(ran.leftColumn(), ran.rightColumn()+1)))
            if minrow > ran.topRow():
                minrow = ran.topRow()
            if maxrow < ran.bottomRow():
                maxrow = ran.bottomRow()
        cols = list(set(cols))
        self.clipboard.setText(self._parse_data(minrow,maxrow,cols))

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Copy):
            self.data_to_clipboard()
        else:
            super().keyPressEvent(event)
            
    @staticmethod
    def showwidget(data):
        widget = EditWidget(data)
        widget.show()

class TempWidget(QTableWidget):
    def __init__(self,filename,sep):
        super().__init__()
        self.clipboard = QApplication.clipboard()
        #text = clipboard_get()
        datum = []
        maxcol = 0
        if sep == '':
            sep = None #sepのスロットがstrなのでNoneが''になってしまう
        try:
            try:
                with open(filename,'r',encoding='utf-8') as f:
                    texts = f.readlines()
            except:
                with open(filename,'r',encoding='shift-jis') as f:
                    texts = f.readlines()
        except:
            texts = filename.splitlines()
        for line in texts:
            data = line.strip().split(sep)
            datum.append(data)
            if maxcol < len(data):
                maxcol = len(data)
        self.nrow = len(datum)
        self.setRowCount(self.nrow)
        self.setColumnCount(maxcol)
        self.datum = datum
        self._set_data()
        self.resizeColumnsToContents()
    
    def _set_data(self):
        for i in range(self.nrow):
            for j in range(len(self.datum[i])):
                item = QTableWidgetItem(self.datum[i][j])
                self.setItem(i,j,item)

    def _parse_data(self,minrow,maxrow,cols):
        datum = []
        for i in range(minrow,maxrow+1):
            data = []
            for j in cols:
                data.append(self.datum[i][j])
            datum.append("\t".join(data))
        return "\n".join(datum)

    def data_to_clipboard(self):
        cols = []
        minrow = len(self.datum)
        maxrow = 0
        for ran in self.selectedRanges():
            cols.extend(list(range(ran.leftColumn(), ran.rightColumn()+1)))
            if minrow > ran.topRow():
                minrow = ran.topRow()
            if maxrow < ran.bottomRow():
                maxrow = ran.bottomRow()
        cols = list(set(cols))
        self.clipboard.setText(self._parse_data(minrow,maxrow,cols))

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Copy):
            self.data_to_clipboard()
        else:
            super().keyPressEvent(event)