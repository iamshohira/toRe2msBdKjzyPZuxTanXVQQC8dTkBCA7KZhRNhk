from asyncore import read
from readline import read_init_file
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import os, json
import matplotlib.backends.qt_editor.figureoptions as figopt
from matplotlib import colors as mcolors
import re
from file_handler import savefile

class IntEdit(QLineEdit):
    def __init__(self, parent=None, initial=None):
        super().__init__(parent)
        self.setFrame(False)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedWidth(40)
        self.setValidator(QIntValidator())
        self.changed = self.textChanged
        if initial != None:
            self.setText(str(initial))
    
    def value(self):
        try:
            return int(self.text())
        except:
            return 0

    def set(self, value):
        self.setText(str(value))


class FloatEdit(QLineEdit):
    def __init__(self, parent=None, initial=None):
        super().__init__(parent)
        self.setFrame(False)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedWidth(40)
        self.setValidator(QDoubleValidator())
        self.changed = self.textChanged
        if initial != None:
            self.setText(str(initial))
    
    def value(self):
        try:
            return float(self.text())
        except:
            return 0.0

    def set(self, value):
        self.setText(str(value))

    
class StrEdit(QLineEdit):
    def __init__(self, parent=None, initial=None):
        super().__init__(parent)
        self.setFrame(False)
        self.changed = self.textChanged
        if initial != None:
            self.setText(initial)

    def value(self):
        return self.text()

    def set(self, value):
        self.setText(str(value))


class BoolEdit(QWidget): # centerにalignmentするためにwidgetでラップ
    changed = pyqtSignal()
    def __init__(self, parent=None, initial=None):
        super().__init__(parent)
        self.checkbox = QCheckBox()
        layout = QHBoxLayout()
        layout.addWidget(self.checkbox)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)
        self.checkbox.stateChanged.connect(self.changed.emit)
        if initial != None:
            self.checkbox.setChecked(initial)

    def value(self):
        return self.checkbox.isChecked()

    def set(self, value):
        self.checkbox.setChecked(value)

class ColorButton(QPushButton):
    colorPicked = pyqtSignal(str)
    def __init__(self, inicolor):
        super().__init__()
        self.clicked.connect(self._call)
        self.set_color(inicolor)
        
    def _call(self):
        color = QColorDialog().getColor(QColor(self.color))
        color = color.name()
        self.set_color(color)
        self.colorPicked.emit(self.color)

    def set_color(self, color):
        if bool(re.fullmatch(r"^#([\da-fA-F]{6})$",color)):
            self.color = color
            stylesheet = "background-color: %s;border: 1px solid; border-color: gray" % color
            self.setStyleSheet(stylesheet)
        
class ColorEdit(QWidget):
    changed = pyqtSignal()
    def __init__(self, parent=None, initial=None):
        super().__init__(parent)
        self.edit = StrEdit(initial=initial)
        self.edit.setFixedWidth(50)
        self.btn = ColorButton(inicolor=initial)
        self.btn.colorPicked.connect(lambda color: self.edit.setText(color))
        self.edit.textChanged.connect(self.btn.set_color)
        self.btn.setFixedWidth(20)
        layout = QHBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.btn)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)
        self.edit.textChanged.connect(self.changed.emit)

    def value(self):
        return self.btn.color
    
class ComboEdit(QComboBox):
    def __init__(self, parent=None, dict=None, initial=None):
        super().__init__(parent)
        self.dict = dict
        self.invdict = {v:k for k,v in dict.items()}
        if dict != None:
            self.addItems(self.invdict.keys())
        if initial != None:
            self.setCurrentText(self.dict[initial])
        self.changed = self.currentIndexChanged
    
    def value(self):
        return self.invdict[self.currentText()]

    def set(self, value):
        self.setCurrentText(value)

class IntComboEdit(QComboBox):
    def __init__(self, parent=None, max=None, initial=None):
        super().__init__(parent)
        if max != None:
            self.addItems([str(i) for i in range(max)])
        if initial != None:
            self.setCurrentIndex(initial)
        self.changed = self.currentIndexChanged
    
    def value(self):
        return self.currentIndex()

class AliasButton(QPushButton):
    changed = pyqtSignal()
    def __init__(self, parent=None, initial=None):
        super().__init__(parent)
        if initial != None:
            self.setText(initial)
    
    def value(self):
        return ""

class LinesTool(QTableWidget):
    line_moved = pyqtSignal()
    alias_clicked = pyqtSignal(str)
    def __init__(self, figs):
        super().__init__()
        self.header = ["show","figs","axes","lines","alias","zorder","label","memo","line style","width","line color","marker","size","marker color","edge","edge color"]
        self.setColumnCount(len(self.header))
        self.setHorizontalHeaderLabels(self.header)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.figs = figs
        self.load_lines()
        self.setWindowTitle("LinesTool")

    def fit_size(self):
        self.setMinimumWidth(self.horizontalHeader().length()+40)
        self.setMaximumWidth(self.horizontalHeader().length()+40)
        self.setMinimumWidth(100)
        height = self.verticalHeader().length()+40
        height = height if height < 400 else 400
        self.setMinimumHeight(height)
        self.setMaximumHeight(self.verticalHeader().length()+40)
        self.setMinimumWidth(100)
        
    def appendCellWidgetToColumn(self,type,initial=None,dict=None,max=None,readonly=False):
        self.column_id += 1
        if type == "int":
            obj = IntEdit(initial=initial)
            obj.setReadOnly(readonly)
        elif type == "float":
            obj = FloatEdit(initial=initial)
        elif type == "str":
            obj = StrEdit(initial=initial)
        elif type == "bool":
            obj = BoolEdit(initial=initial)
        elif type == "combo":
            obj = ComboEdit(initial=initial,dict=dict)
        elif type == "intcombo":
            obj = IntComboEdit(initial=initial,max=max)
        elif type == "alias":
            obj = AliasButton(initial=initial)
            obj.clicked.connect(lambda: self.alias_clicked.emit(obj.text()))
        elif type == "color":
            obj = ColorEdit(initial=initial)
        obj.row = self.row_id
        obj.changed.connect(self.update)
        self.setCellWidget(self.row_id, self.column_id, obj)
        
    def appendRow(self):
        self.row_id += 1
        self.insertRow(self.row_id)
        self.column_id = -1
        
    def initialize(self):
        self.setRowCount(0)
        self.row_id = -1
        self.column_id = -1
        self.lines = []
        
    def load_lines(self):
        self.initialize()
        for h, fig in enumerate(self.figs):
            for i, ax in enumerate(fig.axes):
                for j, line in enumerate(ax.lines):
                    self.appendRow()
                    # visible
                    self.appendCellWidgetToColumn("bool", initial=line.get_visible())
                    # axes
                    self.appendCellWidgetToColumn("intcombo", max=len(self.figs), initial=h)
                    # axes
                    self.appendCellWidgetToColumn("intcombo", max=len(fig.axes), initial=i)
                    # lines
                    self.appendCellWidgetToColumn("int", initial=j, readonly=True)
                    # lines
                    self.appendCellWidgetToColumn("alias", initial=f"fig{h}ax{i}l{j}")
                    # zorder
                    self.appendCellWidgetToColumn("int", initial=line.get_zorder())
                    # label
                    self.appendCellWidgetToColumn("str", initial=line.get_label())
                    # memo
                    self.appendCellWidgetToColumn("str", initial=line.get_gid())
                    # ls
                    self.appendCellWidgetToColumn("combo", initial=line.get_ls(), dict=figopt.LINESTYLES)
                    # lw
                    self.appendCellWidgetToColumn("float", initial=line.get_lw())
                    # lc
                    color = mcolors.to_hex(mcolors.to_rgb(line.get_color()))
                    self.appendCellWidgetToColumn("color", initial=color)
                    # marker
                    self.appendCellWidgetToColumn("combo", initial=line.get_marker(), dict=figopt.MARKERS)
                    # markersize
                    self.appendCellWidgetToColumn("float", initial=line.get_markersize())
                    # markerfacecolor
                    facecolor = mcolors.to_hex(mcolors.to_rgb(line.get_markerfacecolor()))
                    self.appendCellWidgetToColumn("color", initial=facecolor)
                    # markeredgewidth
                    self.appendCellWidgetToColumn("float", initial=line.get_markeredgewidth())
                    # markeredgecolor
                    edgecolor = mcolors.to_hex(mcolors.to_rgb(line.get_markeredgecolor()))
                    self.appendCellWidgetToColumn("color", initial=edgecolor)
                    self.lines.append(line)
        self.resizeColumnsToContents()
        self.fit_size()
                
    def update(self):
        irow = self.sender().row
        values = {h:self.cellWidget(irow,icol).value() for icol, h in enumerate(self.header)}
        line = self.lines[irow]
        old_id = self.get_id(line)
        if old_id["figs"] == values["figs"] and old_id["axes"] == values["axes"]:
            self.set_properties(old_id, values)
            savefile.save_lineproperties(old_id, values)
            self.figs[values["figs"]].canvas.draw()
        else:
            new_id = {k:values[k] for k in ["figs","axes"]}
            if old_id["figs"] != values["figs"]: new_id["axes"] = 0
            self.move_line(old_id, new_id)
            savefile.save_linemove(old_id, new_id)
            self.figs[old_id["figs"]].canvas.draw()
            self.figs[new_id["figs"]].canvas.draw()
            self.load_lines()

    def get_id(self, line):
        id = {}
        id["figs"] = self.figs.index(line.axes.figure)
        id["axes"] = self.figs[id["figs"]].axes.index(line.axes)
        id["lines"] = self.figs[id["figs"]].axes[id["axes"]].lines.index(line)
        return id        

    def set_properties(self, line_id, values):
        line = self.figs[line_id["figs"]].axes[line_id["axes"]].lines[line_id["lines"]]
        line.set_visible(values["show"])
        line.set_zorder(values["zorder"])
        line.set_label(values["label"])
        line.set_gid(values["memo"])
        line.set_ls(values["line style"])
        line.set_lw(values["width"])
        line.set_color(values["line color"])
        line.set_marker(values["marker"])
        line.set_markersize(values["size"])
        line.set_markerfacecolor(values["marker color"])
        line.set_markeredgewidth(values["edge"])
        line.set_markeredgecolor(values["edge color"])

    def move_line(self, old_id, new_id):
        line = self.figs[old_id["figs"]].axes[old_id["axes"]].lines[old_id["lines"]]
        new_line, = self.figs[new_id["figs"]].axes[new_id["axes"]].plot(*line.get_data())
        new_line.set_visible(line.get_visible())
        new_line.set_zorder(line.get_zorder())
        new_line.set_label(line.get_label())
        new_line.set_gid(line.get_gid())
        new_line.set_ls(line.get_ls())
        new_line.set_lw(line.get_lw())
        new_line.set_color(line.get_color())
        new_line.set_marker(line.get_marker())
        new_line.set_markersize(line.get_markersize())
        new_line.set_markerfacecolor(line.get_markerfacecolor())
        new_line.set_markeredgewidth(line.get_markeredgewidth())
        new_line.set_markeredgecolor(line.get_markeredgecolor())
        line.remove()
        self.line_moved.emit()


class AxesTool(QTableWidget):
    def __init__(self, figs):
        super().__init__()
        self.header = ["figs","axes","title","xlabel","ylabel","xmin","xmax","xscale","ymin","ymax","yscale"]
        self.setColumnCount(len(self.header))
        self.setHorizontalHeaderLabels(self.header)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.figs = figs
        self.load_axes()
        self.setWindowTitle("AxesTool")

    def fit_size(self):
        self.setMinimumWidth(self.horizontalHeader().length()+40)
        self.setMaximumWidth(self.horizontalHeader().length()+40)
        self.setMinimumWidth(100)
        height = self.verticalHeader().length()+40
        height = height if height < 400 else 400
        self.setMinimumHeight(height)
        self.setMaximumHeight(self.verticalHeader().length()+40)
        self.setMinimumWidth(100)
        
    def appendCellWidgetToColumn(self,type,initial=None,dict=None,max=None,readonly=False):
        self.column_id += 1
        if type == "int":
            obj = IntEdit(initial=initial)
            obj.setReadOnly(readonly)
            obj.editingFinished.connect(self.quick_set)
        elif type == "float":
            obj = FloatEdit(initial=initial)
            obj.setFixedWidth(60)
            obj.editingFinished.connect(self.quick_set)
        elif type == "str":
            obj = StrEdit(initial=initial)
            obj.setFixedWidth(150)
            obj.editingFinished.connect(self.quick_set)
        elif type == "bool":
            obj = BoolEdit(initial=initial)
        elif type == "combo":
            obj = ComboEdit(initial=initial,dict=dict)
        elif type == "intcombo":
            obj = IntComboEdit(initial=initial,max=max)
        elif type == "alias":
            obj = AliasButton(initial=initial)
        elif type == "color":
            obj = ColorEdit(initial=initial)
        obj.row = self.row_id
        obj.changed.connect(self.update)
        if type == "combo": obj.changed.connect(self.quick_set)
        self.setCellWidget(self.row_id, self.column_id, obj)
        
    def appendRow(self):
        self.row_id += 1
        self.insertRow(self.row_id)
        self.column_id = -1
        
    def initialize(self):
        self.setRowCount(0)
        self.row_id = -1
        self.column_id = -1
        self.lines = []

    def load_axes(self):
        self.initialize()
        for h, fig in enumerate(self.figs):
            for i, ax in enumerate(fig.axes):
                self.appendRow()
                # figs
                self.appendCellWidgetToColumn("int", initial=h, readonly=True)
                # axes
                self.appendCellWidgetToColumn("int", initial=i, readonly=True)
                # title
                self.appendCellWidgetToColumn("str", initial=ax.get_title())
                # xlabel
                self.appendCellWidgetToColumn("str", initial=ax.get_xlabel())
                # ylabel
                self.appendCellWidgetToColumn("str", initial=ax.get_ylabel())
                # xmin
                self.appendCellWidgetToColumn("float", initial=ax.get_xlim()[0])
                # xmax
                self.appendCellWidgetToColumn("float", initial=ax.get_xlim()[1])
                # xscale
                self.appendCellWidgetToColumn("combo", initial=ax.get_xscale(), dict={"linear":"linear","log":"log"})
                # ymin
                self.appendCellWidgetToColumn("float", initial=ax.get_ylim()[0])
                # ymax
                self.appendCellWidgetToColumn("float", initial=ax.get_ylim()[1])
                # yscale
                self.appendCellWidgetToColumn("combo", initial=ax.get_yscale(), dict={"linear":"linear","log":"log"})
        self.resizeColumnsToContents()
        self.fit_size()

    def quick_set(self):
        for irow in range(self.rowCount()):
            figid = self.cellWidget(irow,0).value()
            axid = self.cellWidget(irow,1).value()
            ax = self.figs[figid].axes[axid]
            self.cellWidget(irow,2).set(ax.get_title())
            self.cellWidget(irow,3).set(ax.get_xlabel())
            self.cellWidget(irow,4).set(ax.get_ylabel())
            self.cellWidget(irow,5).set(ax.get_xlim()[0])
            self.cellWidget(irow,6).set(ax.get_xlim()[1])
            self.cellWidget(irow,7).set(ax.get_xscale())
            self.cellWidget(irow,8).set(ax.get_ylim()[0])
            self.cellWidget(irow,9).set(ax.get_ylim()[1])
            self.cellWidget(irow,10).set(ax.get_yscale())
                
    def update(self):
        irow = self.sender().row
        values = {h:self.cellWidget(irow,icol).value() for icol, h in enumerate(self.header)}
        if values["xmin"] <= 0 and values["xscale"] == "log":
            values["xmin"] = 1e-6
        if values["ymin"] <= 0 and values["yscale"] == "log":
            values["ymin"] = 1e-6
        if values["xmax"] <= 0 and values["xscale"] == "log":
            values["xmax"] = 1.0
        if values["ymax"] <= 0 and values["yscale"] == "log":
            values["ymax"] = 1.0            
        self.set_properties(values)
        try:
            self.figs[values["figs"]].canvas.draw()
            savefile.save_axesproperties(values)
        except:
            pass

    def show(self):
        self.load_axes()
        super().show()

    # def get_id(self, line):
    #     id = {}
    #     id["figs"] = self.figs.index(line.axes.figure)
    #     id["axes"] = self.figs[id["figs"]].axes.index(line.axes)
    #     id["lines"] = self.figs[id["figs"]].axes[id["axes"]].lines.index(line)
    #     return id        

    def set_properties(self, values):
        ax = self.figs[values["figs"]].axes[values["axes"]]
        ax.set_title(values["title"])
        ax.set_xlabel(values["xlabel"])
        ax.set_xlim((values["xmin"],values["xmax"]))
        ax.set_xscale(values["xscale"])
        ax.set_ylabel(values["ylabel"])
        ax.set_ylim((values["ymin"],values["ymax"]))
        ax.set_yscale(values["yscale"])

    # @classmethod
    # def move_line(cls, figs, old_id, new_id):
    #     line = figs[old_id["figs"]].axes[old_id["axes"]].lines[old_id["lines"]]
    #     new_line, = figs[new_id["figs"]].axes[new_id["axes"]].plot(*line.get_data())
    #     new_line.set_visible(line.get_visible())
    #     new_line.set_zorder(line.get_zorder())
    #     new_line.set_label(line.get_label())
    #     new_line.set_gid(line.get_gid())
    #     new_line.set_ls(line.get_ls())
    #     new_line.set_lw(line.get_lw())
    #     new_line.set_color(line.get_color())
    #     new_line.set_marker(line.get_marker())
    #     new_line.set_markersize(line.get_markersize())
    #     new_line.set_markerfacecolor(line.get_markerfacecolor())
    #     new_line.set_markeredgewidth(line.get_markeredgewidth())
    #     new_line.set_markeredgecolor(line.get_markeredgecolor())
    #     line.remove()