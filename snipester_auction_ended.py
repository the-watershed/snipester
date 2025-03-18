from snipester_utils import log_debug_info
from globals import refresh_in, refresh_timer, timer, total_seconds

def auction_ended(self):
    global refresh_in, total_seconds
    if refresh_timer:
        refresh_timer.stop()
    if timer:
        timer.stop()
    refresh_in = 0
    total_seconds = 0
    self.refresh_in_label.setText("Refresh In: 0.00 seconds")
    self.info_pane.append("<font color='red'><b>Auction ended.</b></font>")
    log_debug_info(self, "Auction ended.", 'red')
