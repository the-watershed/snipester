import re
from PyQt5.QtCore import QDateTime, QTimer
from PyQt5.QtWidgets import QApplication
from http_engine import retrieve_information
from data_extraction import parse_bid_information
from globals import refresh_in, timer, total_seconds, end_datetime, bid_info

def log_debug_info(self, message, color='white', variables=None): 
    """
    Log a debug message to the debug pane with the specified color.
    If variables are provided, log their names and values as well.
    """
    if hasattr(self, 'debug_checkbox') and self.debug_checkbox.isChecked():
        self.debug_pane.append(f'<font color="{color}">{message}</font>')
        if variables:
            for var_name, var_value in variables.items():
                self.debug_pane.append(f'<font color="cyan">{var_name}:</font> <font color="yellow">{var_value}</font>')

def display_info(self, info): 
    """
    Display bid information in the info pane and log the action.
    """

    """
    Display bid information in the info pane.
    """
    global bid_info
    bid_info = info
    log_debug_info(self, f"Displaying info: {info}", 'blue')  # Debug log for info
    update_info_pane(self)

def start_countdown(self, time_remain): 
    """
    Start a countdown timer based on the time remaining.
    Updates the timer and refresh interval accordingly.
    """

    """
    Start a countdown timer based on the time remaining.
    """
    global total_seconds, end_datetime, timer
    total_seconds = 0
    days_match = re.search(r'(\d+)d', time_remain)
    hours_match = re.search(r'(\d+)h', time_remain)
    minutes_match = re.search(r'(\d+)m', time_remain)
    seconds_match = re.search(r'(\d+)s', time_remain)

    if days_match:
        total_seconds += int(days_match.group(1)) * 86400  # 24 hours * 3600 seconds
    if hours_match:
        total_seconds += int(hours_match.group(1)) * 3600
    if minutes_match:
        total_seconds += int(minutes_match.group(1)) * 60
    if seconds_match:
        total_seconds += int(seconds_match.group(1))

    end_datetime = QDateTime.currentDateTime().addSecs(total_seconds)
    set_refresh_interval(self)
    timer = QTimer(self)
    timer.timeout.connect(lambda: update_timer(self))
    timer.start(10)  # Update every 10 milliseconds for hundredths of a second

def update_timer(self): 
    """
    Update the countdown timer and refresh the info pane.
    Stops the timer when the countdown reaches zero.
    """

    """
    Update the countdown timer and refresh the info pane.
    """
    global total_seconds, end_datetime, bid_info
    if total_seconds > 0:
        total_seconds -= 0.01
        days, remainder = divmod(total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        hundredths = int((seconds - int(seconds)) * 100)
        bid_info['Time Remaining'] = f"{int(days)}d {int(hours):02}h {int(minutes):02}m {int(seconds):02}s {hundredths:02}"
        bid_info['Time Remaining (English)'] = f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds"
    else:
        if timer:
            timer.stop()
        bid_info['Time Remaining'] = "0d 00h 00m 00s 00"
        bid_info['Time Remaining (English)'] = "0 days, 0 hours, 0 minutes, and 0 seconds"
        auction_ended(self)

    if end_datetime:
        bid_info['End Date'] = end_datetime.toString('dddd, MMMM d, yyyy hh:mm:ss AP')
    update_info_pane(self)

def update_info_pane(self): 
    """
    Update the info pane with the current bid information.
    Clears the pane if no bid information is available.
    """

    """
    Update the info pane with the current bid information.
    """
    global refresh_in, bid_info
    self.info_pane.clear()
    log_debug_info(self, f"Updating info pane with: {bid_info}", 'blue')  # Debug log for bid_info
    if not bid_info:
        self.info_pane.setText("<font color='red'>No bid information available.</font>")
        return

    for key, value in bid_info.items():
        if key == 'Title':
            self.info_pane.append(f"<b>{key}:</b> <font color='#ADFF2F'><b>{value}</b></font>")
        else:
            self.info_pane.append(f"<b>{key}:</b> <font color='#66FF66'>{value}</font>")
    self.info_pane.append(f"<b>Refresh In:</b> <font color='#66CCFF'>{refresh_in:.2f} seconds</font>")

def paste_clipboard(self): 
    """
    Paste the clipboard content into the link input field.
    """

    """
    Paste the clipboard content into the link input field.
    """
    clipboard = QApplication.clipboard()
    self.link_input.setPlainText(clipboard.text())

def set_refresh_interval(self): 
    """
    Set the refresh interval based on the total seconds remaining.
    Adjusts the refresh rate dynamically as time decreases.
    """

    """
    Set the refresh interval based on the total seconds remaining.
    """
    global total_seconds, refresh_in
    if total_seconds > 3600:
        self.refresh_interval = 600000  # 10 minutes
    elif total_seconds > 600:
        self.refresh_interval = 60000  # 1 minute
    elif total_seconds > 300:
        self.refresh_interval = 30000  # 30 seconds
    elif total_seconds > 120:
        self.refresh_interval = 15000  # 15 seconds
    elif total_seconds > 15:
        self.refresh_interval = 1000  # 1 second
    else:
        self.refresh_interval = 333  # 3 times a second
    refresh_in = self.refresh_interval / 1000.0
