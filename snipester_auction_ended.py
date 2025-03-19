from globals import timer, total_seconds, refresh_in  # Import global variables for timer and refresh

from snipester_utils import log_debug_info

def auction_ended(self): 
    """
    Stop the refresh timer and update the UI to indicate that the auction has ended.
    """

    global timer, total_seconds, refresh_in
    self.refresh_timer.stop()  # Stop the refresh timer

    if timer:
        timer.stop()
    refresh_in = 0
    total_seconds = 0
    self.refresh_in_label.setText("Refresh In: 0.00 seconds")
    self.info_pane.append("<font color='red'><b>Auction ended.</b></font>")  # Update UI to show auction ended message

    log_debug_info(self, "Auction ended.", 'red')  # Log the auction end event
