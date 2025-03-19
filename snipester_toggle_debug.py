from snipester_utils import log_debug_info
from PyQt5.QtCore import Qt

def toggle_debug(self, state): 
    """
    Show or hide the debug pane based on the checkbox state and log the action.
    """

    if state == Qt.Checked:
        self.debug_pane.show()  # Show the debug pane

        log_debug_info(self, "Debug mode enabled.", 'yellow')
    else:
        self.debug_pane.hide()  # Hide the debug pane

        log_debug_info(self, "Debug mode disabled.", 'yellow')  # Log disabling of debug mode
