from snipester_utils import log_debug_info
from PyQt5.QtCore import Qt

def toggle_debug(self, state):
    if state == Qt.Checked:
        self.debug_pane.show()
        log_debug_info(self, "Debug mode enabled.", 'yellow')
    else:
        self.debug_pane.hide()
        log_debug_info(self, "Debug mode disabled.", 'yellow')
