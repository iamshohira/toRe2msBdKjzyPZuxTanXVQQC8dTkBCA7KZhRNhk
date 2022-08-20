import os
os.environ['QT_API'] = 'PyQt6'

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

# Import the console machinery from ipython
from qtconsole.rich_ipython_widget import RichIPythonWidget
from qtconsole.inprocess import QtInProcessKernelManager
import qtconsole.styles as styles

class IPythonWidget(RichIPythonWidget):
    command_finished = pyqtSignal()
    """ Convenience class for a live IPython console widget. We can replace the standard banner using the customBanner argument"""
    def __init__(self,customBanner=None,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if customBanner!=None: self.banner=customBanner
        self.kernel_manager = kernel_manager = QtInProcessKernelManager()
        self.set_default_style(colors='linux')
        self.syntax_style = 'monokai'
        self.style_sheet = styles.default_dark_style_template%dict(bgcolor='#222222', fgcolor='#dddddd', select="#555")
        kernel_manager.start_kernel()
        kernel_manager.kernel.gui = 'qt'
        self.kernel_client = kernel_client = self._kernel_manager.client()
        self.ns = self.kernel_manager.kernel.shell.user_ns
        self.ns_hidden = self.kernel_manager.kernel.shell.user_ns_hidden
        kernel_client.start_channels()       
        self.exit_requested.connect(self.stop)
        self.error = False

    def stop(self):
        self.kernel_client.stop_channels()
        self.kernel_manager.shutdown_kernel()

    def pushVariables(self,variableDict):
        """ Given a dictionary containing name / value pairs, push those variables to the IPython console widget """
        self.kernel_manager.kernel.shell.push(variableDict)

    def clearTerminal(self):
        """ Clears the terminal """
        self._control.clear()    

    def printText(self,text,beforeprompt=True):
        """ Prints some plain text to the console """
        self._append_plain_text(text,beforeprompt)        
        
    def clearPrompt(self):
        self.input_buffer = ""

    def printTextInBuffer(self,text):
        """ Prints some plain text to the console """
        self._insert_plain_text_into_buffer(self._get_prompt_cursor(), text)

    def printTextAtCurrentPos(self,text):
        """ Prints some plain text to the console """
        self._insert_plain_text_into_buffer(self._get_cursor(), text)

    def executeCommand(self,command,hidden=False):
        """ Execute a command in the frame of the console widget """
        self._execute(command,hidden)

    def _execute(self, source, hidden):
        return super()._execute(source, hidden)

    def _handle_error(self, msg):
        self.error = True
        return super()._handle_error(msg)

    def _on_flush_pending_stream_timer(self):
        self.command_finished.emit()
        self.error = False
        return super()._on_flush_pending_stream_timer()

    def key_find(self,valiable):
        for key, value in self.ns.items():
            if valiable is value:
                return key
        return
    
