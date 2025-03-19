from snipester_utils import log_debug_info  # Import utility for logging debug information

from globals import refresh_timer, timer

def on_stop(self): 
    """
    Stop the ongoing data retrieval operations and log the action.
    """

    if refresh_timer:
        refresh_timer.stop()
    if timer:
        timer.stop()
    log_debug_info(self, "Data retrieval stopped.", 'red')  # Log the stopping action
