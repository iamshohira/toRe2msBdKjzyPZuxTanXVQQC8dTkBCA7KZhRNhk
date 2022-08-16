import sys,os,pickle
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from ipython_widget import IPythonWidget
from figure_widget import MyFigureCanvas, DDHandler, randomname, MyToolbar
from log_widget import LogWidget
import numpy as np
import glob
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from edit_widget import EditWidget, TempWidget
from file_handler import savefile
from datetime import datetime
from matplotlib.lines import Line2D
import subprocess
import shutil
from addon_installer import AddonInstaller
import argparse
import graphlib
from axeslinestool import AxesTool, LinesTool
from update_checker import UpdateChecker

if os.name == "nt": #windows
    import PyQt6
    dirname = os.path.dirname(PyQt6.__file__)
    plugin_path = os.path.join(dirname, "Qt6", "plugins", "platforms")
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path

parser = argparse.ArgumentParser()
parser.add_argument("filename", nargs='?', default=None, help="input filename")
parser.add_argument("-l","--local", action="store_true")
args = parser.parse_args()
VSCODE = "/Applications/Visual Studio Code.app"
run_command = ["open",VSCODE]
jkndir = 'addon'
EXE_DIR = os.path.join(os.path.dirname(sys.argv[0]))
ADDON_TEMPRATE_DIR = os.path.join(os.path.dirname(sys.argv[0]),jkndir)
if args.local:
    JEMDIR = os.path.join(os.path.dirname(sys.argv[0]),"..","HOME")
else:
    JEMDIR = os.path.join(os.path.expanduser('~'),"JEMViewer")
ADDON_DIR = os.path.join(JEMDIR,jkndir)
RES_DIR = os.path.join(os.path.dirname(sys.argv[0]),'png')
pltprofile = 'default.mplstyle'
savefile.initialize(JEMDIR)
DEFAULT_NAMESPACE = {
    "np": np,
    "pickle": pickle,
    "os": os,
}

EXIT_CODE_REBOOT = -11231351

class MainWindow(QMainWindow):
    def __init__(self, filepath=os.path.join(os.path.expanduser('~'),'Desktop'), parent=None):
        super().__init__(parent)
        self.saved_command = ""
        window_id = "id: " + randomname(4)
        self.setWindowTitle(f"JEMViewer2 {window_id}")
        self.setGeometry(300, 300, 800, 500)
        self.filepath = filepath
        self.update_checker = UpdateChecker()
        # if filepath != None:
        #     matplotlib.rcParams['savefig.directory'] = (os.path.dirname(filepath))
        self.ipython_w = IPythonWidget(self.update_checker.header)
        self.ns = self.ipython_w.ns
        self.figure_widgets = []
        self.figs = []
        self.linestool = LinesTool(self.figs)
        self.axestool = AxesTool(self.figs)
        self.toolbar = MyToolbar(self)
        self.add_figure()
        self._set_initial_namespace()
        self.log_w = LogWidget(self,self.ns)
        self._create_main_window()
        self._set_slot()
        self._create_menubar()
        self.setAcceptDrops(True)
        self.initialize()
            
    def print_log(self,item):
        self.ipython_w.clearPrompt()
        self.ipython_w.printTextInBuffer(item.text())

    def print_log_str(self, text):
        self.ipython_w.clearPrompt()
        self.ipython_w.printTextInBuffer(text)

    def dragEnterEvent(self,event):
        event.accept()

    def dropEvent(self,event):
        event.accept()
        mime = event.mimeData()
        if os.name == 'posix':
            filenames = mime.text().replace('file://','').replace('file:','').split('\n')
        else:
            filenames = mime.text().replace('file:///','').replace('file:','').split('\n')
        if ".jem2" in filenames[0]:
            self.filepath = filenames[0]
            self._open()
        super().dropEvent(event)

    def _load_helper(self):
        with open(os.path.join(EXE_DIR,'helper_function.py'), 'r') as f:
            command = f.read()
            if command not in self.saved_command:
                self.ipython_w.executeCommand(command,hidden=True)
                savefile.save_command(command)

    def _load_user_py(self):
        files = glob.glob(os.path.join(ADDON_DIR,"*.py"))
        dependences = {}
        for fi in files:
            with open(fi, "r") as f:
                f.readline()
                line = f.readline()
                if "Dependence:" in line:
                    dep = [i.strip() for i in line.split(":")[1].split(",")]
                else:
                    dep = [""]
            dependences[os.path.basename(fi)] = dep
        ts = graphlib.TopologicalSorter(dependences)
        for fn in ts.static_order():
            if fn == "": continue
            fi = os.path.join(ADDON_DIR, fn)
            with open(fi,'r') as f:
                command = f.read()
                if command not in self.saved_command:
                    self.ipython_w.executeCommand(command,hidden=True)
                    savefile.save_command(command)
        self.ipython_w.executeCommand("",hidden=True)

    def _create_menubar(self):
        menubar = self.menuBar()
        filemenu = menubar.addMenu("&File")
        save = QAction("&Save",self)
        save.setShortcut(QKeySequence.Save)
        save.triggered.connect(self.save)
        filemenu.addAction(save)
        saveas = QAction("Save &As",self)
        saveas.setShortcut(QKeySequence.SaveAs)
        saveas.triggered.connect(self.saveas)
        filemenu.addAction(saveas)
        open_ = QAction("&Open",self)
        open_.setShortcut(QKeySequence.Open)
        open_.triggered.connect(self.open)
        filemenu.addAction(open_)

    def closeEvent(self, event):
        def exit():
            savefile.remove_tmpdir()
            for figure_w in self.figure_widgets:
                figure_w.close()
            self.linestool.close()
            self.axestool.close()
            event.accept()
            
        if '*' not in self.windowTitle():
            exit()
            return
        reply = QMessageBox.question(self,'Exit',
                                     "Do you want to save your changes?", QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                                     QMessageBox.Save)
        if reply == QMessageBox.Discard:
            exit()
        elif reply == QMessageBox.Save:
            self.save()
            exit()
        else:
            event.ignore()    

    def _create_main_window(self):
        layout = QVBoxLayout()
        layout3 = QHBoxLayout()
        layout3.addWidget(self.toolbar)
        layout.addLayout(layout3)
        layout2 = QSplitter()
        layout2.addWidget(self.log_w)
        layout2.addWidget(self.ipython_w)
        layout.addWidget(layout2)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def raise_figure_widgets(self):
        for figure_w in self.figure_widgets:
            figure_w.raise_()

    def draw_and_requiring_save(self):
        for figure_w in self.figure_widgets:
            figure_w.draw()
        title = self.windowTitle()
        if '*' not in title:
            self.setWindowTitle(title+'*')

    def _set_slot(self):
        self.linestool.line_moved.connect(self.update_alias)
        self.linestool.alias_clicked.connect(self.ipython_w.printTextInBuffer)
        self.ipython_w.command_finished.connect(self.log_w.store)
        self.ipython_w.command_finished.connect(lambda: self._save_command(fileparse=True))
        self.log_w.item_added.connect(self.draw_and_requiring_save)
        self.log_w.itemDoubleClicked.connect(self.print_log)
        self.log_w.inputText.connect(self.print_log_str)
        self.ipython_w.command_finished.connect(self.update_alias)

    def add_figure(self):
        figure_w = MyFigureCanvas(self, self.toolbar)
        figure_w.set_window_title(id=len(self.figure_widgets), prefix="Figure")
        figure_w.nd_pasted.connect(self.append_ndarray)
        figure_w.line_pasted.connect(self.append_line2D)
        figure_w.table_required.connect(self.open_tablewidget)
        figure_w.custom_loader.connect(self.run_custom_loader)
        figure_w.nd_pasted.connect(self.update_alias)
        figure_w.line_pasted.connect(self.update_alias)
        figure_w.table_required.connect(self.update_alias)
        figure_w.custom_loader.connect(self.update_alias)
        figure_w.show()
        self.toolbar.add_canvas(figure_w)
        self.figure_widgets.append(figure_w)
        self.figs.append(figure_w.fig)
        return figure_w.fig

    def remove_figure(self, id):
        figure_w = self.figure_widgets.pop(id)
        figs = self.figs.pop(id)
        self.toolbar.remove_canvas(figure_w)
        figure_w.nd_pasted.disconnect(self.append_ndarray)
        figure_w.line_pasted.disconnect(self.append_line2D)
        figure_w.table_required.disconnect(self.open_tablewidget)
        figure_w.custom_loader.disconnect(self.run_custom_loader)
        figure_w.nd_pasted.disconnect(self.update_alias)
        figure_w.line_pasted.disconnect(self.update_alias)
        figure_w.table_required.disconnect(self.update_alias)
        figure_w.custom_loader.disconnect(self.update_alias)
        figure_w.close()
        for i, figure_w in enumerate(self.figure_widgets):
            figure_w.set_window_title(id=i)
            
    def _remove_slot(self):
        self.linestool.line_moved.disconnect(self.update_alias)
        self.ipython_w.command_finished.disconnect(self.log_w.store)
        self.log_w.item_added.disconnect(self.draw_and_requiring_save)
        self.log_w.itemDoubleClicked.disconnect(self.print_log)
        self.ipython_w.command_finished.disconnect(self.update_alias)

    @pyqtSlot(str,np.ndarray)
    def append_ndarray(self,key,value):
        self.ns[key] = value
        self.ns["justnow"] = value
        text  = "# New ndarray was generated\n"
        text += "# Name: {}\n".format(key,)
        text += "# Size: {}".format(value.shape,)
        self.log_w.add_item(text)

    @pyqtSlot(str,list)
    def append_line2D(self,key,value):
        if len(value) == 1:
            self.ns[key] = value[0]
            self.ns["justnow"] = value[0]
            text  = "# New plot was generated\n"
            text += "# Name: {}".format(key,)
        else:
            self.ns[key] = value
            self.ns["justnow"] = value
            text  = "# New plot list was generated\n"
            text += "# Name: {}\n".format(key,)
            text += "# Size: {}".format(len(value))
        self.log_w.add_item(text)

    def save(self):
        if self.filepath is None:
            self.saveas()
            return
        self._save()

    def _save(self):
        self._set_windowname()
        log = self.log_w.get()
        savefile.save_log(log)
        savefile.save(self.filepath)
        
    def saveas(self):
        # path = self.filepath if self.filepath is not None else os.path.join(os.path.expanduser('~'),'Desktop')
        filepath = QFileDialog.getSaveFileName(self,"Project name",self.filepath,"JEM Viewer 2 file (*.jem2)")
        if filepath[0] == '':
            return
        self.filepath = filepath[0]
        matplotlib.rcParams['savefig.directory'] = (os.path.dirname(self.filepath))
        self._save()

    def open(self):
        # path = self.filepath if self.filepath is not None else os.path.join(os.path.expanduser('~'),'Desktop')
        filepath = QFileDialog.getOpenFileName(self,"Project name",self.filepath,"JEM Viewer 2 file (*.jem2)")
        if filepath[0] == '':
            return
        self.filepath = filepath[0]
        self._open()

    def _open(self):
        for figure_w in self.figure_widgets:
            figure_w.close()
        self.ipython_w.stop()
        self.close()
        get_app_qt6().exit(EXIT_CODE_REBOOT)

    def _set_windowname(self):
        self.setWindowTitle(os.path.basename(self.filepath))
        # self.figure_w.setWindowTitle(os.path.basename(self.filepath))
        # self.figure_w.get_default_filename = lambda: os.path.splitext(self.filepath)[0]

    def load(self):
        if self.filepath != None:
            savefile.open(self.filepath)
            command = savefile.load()
            self.ipython_w.executeCommand(command,hidden=True)
            log = savefile.load_log()
            self._set_windowname()
            self.log_w.set(log)
            # PyQt5 to PyQt6
            self.saved_command = command.replace("PyQt5","PyQt6")

    def show_datatable(self, data):
        if type(data) == Line2D:
            data = np.vstack(data.get_data())
        self.editwidget = EditWidget(data.T)
        self.editwidget.show()   
    
    @pyqtSlot(str,str)
    def open_tablewidget(self,filename,sep):
        self.tempwidget = TempWidget(filename,sep)
        self.tempwidget.setGeometry(self.geometry().left(),self.geometry().top(),self.geometry().width(),self.geometry().height())
        self.tempwidget.show()

    @pyqtSlot(list)
    def run_custom_loader(self,lis):
        functionname = lis[0]
        filename = lis[1]
        inaxes = lis[2]
        newname = lis[3]
        try:
            self.ns[newname] = self.ns[functionname](filename,inaxes)
            self.ns["justnow"] = self.ns[newname]
            text  = "# Output from \"{}\" was generated\n".format(functionname,)
            text += "# Name: {}\n".format(newname,)
            self.log_w.add_item(text)
            # self.figure_w.draw()
            savefile.save_customloader(lis)
        except:
            QMessageBox.critical(self, "Load error", "{} does not exist or there is something wrong with this function.")
        
    def _set_initial_namespace(self):
        namespace = {
            #"ax": self.figure_widgets[0].fig.axes[0],
            "fig_widget": self.figure_widgets[0],
            "fig_widgets": self.figure_widgets,
            "edit": self.direct_edit,
            "set_loader": DDHandler.set_loader,
            "savedir": savefile.dirname,
            "popup": self.raise_figure_widgets,
            "initialize": self.initialize,
            "update_command": self.update_command,
            "update_alias": self.update_alias,
            "show_data": self.show_datatable,
            "add_figure": self.add_figure,
            "remove_figure": self.remove_figure,
            "addon_store": AddonInstaller(ADDON_DIR),
            "set_lineproperties": self.linestool.set_properties,
            "move_line": self.linestool.move_line,
            "set_axesproperties": self.axestool.set_properties,
        }
        if self.update_checker.can_update:
            namespace["JEMViewer"] = self.update_checker
        self.ns.update(DEFAULT_NAMESPACE)
        self.ns.update(namespace)

    def _save_command(self,fileparse=False):
        if self.ipython_w.error:
            return
        id_ = len(self.ns['In'])-1
        lastcommand = self.ns['In'][-1].strip()
        if id_ in self.ns['Out']:
            lastcommand = "_ = " + lastcommand
        savefile.save_command(lastcommand,fileparse)

    def initialize(self):
        # self.figure_w.fig.clear()
        # self.figure_w.fig.subplots(1,1)
        # self.ns["ax"] = self.figure_w.fig.axes[0]
        self.update_alias() 
        try:
            savefile.make_commandfile()
        except:
            pass
        self._load_helper()
        self.load()
        savefile.save_command(datetime.now().strftime('\n# HEADER %Y-%m-%d %H:%M:%S\n'))
        self._load_user_py()
        savefile.save_command(datetime.now().strftime('\n# COMMAND LOG %Y-%m-%d %H:%M:%S\n'))
        self.update_alias()

    def update_command(self):
        pass
        # self.figure_w.fig.clear()
        # self.figure_w.fig.subplots(1,1)
        # self.ns["ax"] = self.figure_w.fig.axes[0]
        # command = savefile.load_command_py()
        # self.ipython_w.executeCommand(command,hidden=True)

    def direct_edit(self):
        subprocess.run(run_command+[savefile.logfilename])

    def update_alias(self):
        alias = {}
        alias["figs"] = self.figs
        for i, fig in enumerate(self.figs):
            alias[f"fig{i}"] = fig
            alias[f"fig{i}axs"] = fig.axes
            for j, ax in enumerate(fig.axes):
                alias[f"fig{i}ax{j}"] = ax
                alias[f"fig{i}ax{j}ls"] = ax.lines
                for k, line in enumerate(ax.lines):
                    alias[f"fig{i}ax{j}l{k}"] = line
                    alias[f"fig{i}ax{j}l{k}x"] = line.get_xdata()
                    alias[f"fig{i}ax{j}l{k}y"] = line.get_ydata()
        if len(self.figs) > 0:
            alias["fig"] = self.figs[0]
            alias["axs"] = self.figs[0].axes
            for ia, ax in enumerate(self.figs[0].axes):
                alias["ax{}".format(ia,)] = ax
                alias["ax{}ls".format(ia,)] = ax.lines
                for il, line in enumerate(ax.lines):
                    alias["ax{}l{}".format(ia,il)] = line
                    alias["ax{}l{}x".format(ia,il)] = line.get_xdata()
                    alias["ax{}l{}y".format(ia,il)] = line.get_ydata()
            if len(self.figs[0].axes) > 0:
                alias["ax"] = self.figs[0].axes[0]
                alias["ls"] = self.figs[0].axes[0].lines
                for il, line in enumerate(self.figs[0].axes[0].lines):
                    alias["l{}".format(il,)] = line
                    alias["l{}x".format(il,)] = line.get_xdata()
                    alias["l{}y".format(il,)] = line.get_ydata()
        self.ns.update(alias)
        self.linestool.load_lines()
        self.axestool.load_axes()

def get_app_qt6(*args, **kwargs):
    """Create a new qt6 app or return an existing one."""
    app = QApplication.instance()
    if app is None:
        if not args:
            args = ([''],)
        app = QApplication(*args, **kwargs)
    return app

def main():
    filename = args.filename
    if not os.path.exists(ADDON_DIR):
        os.makedirs(JEMDIR,exist_ok=True)
        shutil.copytree(ADDON_TEMPRATE_DIR, ADDON_DIR)
    pltpath = os.path.join(ADDON_DIR,pltprofile)
    plt.style.use(pltpath)

    while True:
        app = get_app_qt6()
        app.setWindowIcon(QIcon(os.path.join(RES_DIR,'logo.png')))
        form = MainWindow(filename)
        form.show()
        form.raise_()
        exit_code = app.exec_()
        filename = form.filepath
        del(form)
        del(app)
        if exit_code != EXIT_CODE_REBOOT:
            break

if __name__ == "__main__":
    main()
    