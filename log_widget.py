import sys,os,pickle

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class LogWidget(QListWidget):
    item_added = pyqtSignal()
    inputText = pyqtSignal(str)
    def __init__(self,parent,ns):
        super().__init__(parent)
        self.ns = ns
        self.setAlternatingRowColors(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextmenu)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def add_item(self,text,row=-1):
        if row < 0: #default add
            item = QListWidgetItem(text,self)
        else: #insert
            self.insertItem(row,text)
            item = self.item(row)
        if text[0] == "#":
            item.setForeground(QColor("red"))
        self.item_added.emit()
        return item

    def store(self):
        lastcommand = self.ns['In'][-1].strip()
        if lastcommand == "": return
        # try:
        #     previous = self.item(self.count()-1).text().strip()
        # except:
        #     previous = ""
        # if previous != lastcommand:
        self.add_item(lastcommand)
            
    def set(self,log):
        for i in log:
            self.add_item(i)

    def get(self):
        logs = []
        for i in range(self.count()):
            logs.append(self.item(i).text())
        return logs

    def delete(self):
        item = self.currentItem()
        row = self.row(item)
        self.takeItem(row)
    
    def copy(self):
        item = self.currentItem()
        cpb = QApplication.clipboard()
        cpb.setText(item.text())

    def insert(self):
        selected_item = self.currentItem()
        row = self.row(selected_item)
        inserted_item = self.add_item("# ",row)
        inserted_item.setFlags(inserted_item.flags() | Qt.ItemIsEditable)
        self.editItem(inserted_item)
        
    def copy_all(self):
        indexes = self.selectedIndexes()
        texts = []
        for id_ in indexes:
            item = self.itemFromIndex(id_)
            texts.append(item.text())
        cpb = QApplication.clipboard()
        cpb.setText("\n".join(texts))

    def delete_all(self):
        indexes = self.selectedIndexes()
        rows = []
        for id_ in indexes:
            item = self.itemFromIndex(id_)
            rows.append(self.row(item))
        for row in sorted(rows, reverse=True):
            self.takeItem(row)

    def input(self):
        item = self.currentItem()
        self.inputText.emit(item.text())
        
    def input_all(self):
        indexes = self.selectedIndexes()
        texts = []
        for id_ in indexes:
            item = self.itemFromIndex(id_)
            texts.append(item.text())
        self.inputText.emit("\n".join(texts))

    def contextmenu(self,point):
        menu = QMenu(self)
        indexes = self.selectedIndexes()
        num = len(indexes)
        if num == 1:
            input_action = menu.addAction('Input')
            input_action.triggered.connect(self.input)
            copy_action = menu.addAction('Copy')
            copy_action.triggered.connect(self.copy)
            delete_action = menu.addAction('Delete')
            delete_action.triggered.connect(self.delete)
        elif num > 1:
            input_action = menu.addAction('Input all')
            input_action.triggered.connect(self.input_all)
            copy_action = menu.addAction('Copy all')
            copy_action.triggered.connect(self.copy_all)
            delete_action = menu.addAction('Delete all')
            delete_action.triggered.connect(self.delete_all)            
        if num <= 1:
            insert_action = menu.addAction('Insert comment')
            insert_action.triggered.connect(self.insert)
        menu.exec_(self.mapToGlobal(point))