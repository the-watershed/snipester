from snipester_utils import log_debug_info
from globals import refresh_timer, timer

def on_stop(self):
    if refresh_timer:
        refresh_timer.stop()
    if timer:
        timer.stop()
    log_debug_info(self, "Data retrieval stopped.", 'red')
