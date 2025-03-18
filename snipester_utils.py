import re
from PyQt5.QtCore import QDateTime, QTimer
from PyQt5.QtWidgets import QApplication
from http_engine import retrieve_information
from data_extraction import parse_bid_information
from globals import refresh_in, timer, total_seconds, end_datetime, bid_info

def log_debug_info(self, message, color='white'):
    self.debug_pane.append(f'<font color="{color}">{message}</font>')

def is_valid_link(link):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, link) is not None

def display_info(self, info):
    global bid_info
    bid_info = info
    update_info_pane(self)

def start_countdown(self, time_remain):
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
    update_refresh_in_label(self)

def update_info_pane(self):
    global refresh_in, bid_info
    self.info_pane.clear()
    for key, value in bid_info.items():
        if key == 'Title':
            self.info_pane.append(f"<b>{key}:</b> <font color='#ADFF2F'><b>{value}</b></font>")
        else:
            self.info_pane.append(f"<b>{key}:</b> <font color='#66FF66'>{value}</font>")
    self.info_pane.append(f"<b>Refresh In:</b> <font color='#66CCFF'>{refresh_in:.2f} seconds</font>")

def update_refresh_in_label(self):
    global refresh_in
    self.refresh_in_label.setText(f"Refresh In: {refresh_in:.2f} seconds")

def auction_ended(self):
    global timer, total_seconds, refresh_in
    self.refresh_timer.stop()
    if timer:
        timer.stop()
    refresh_in = 0
    total_seconds = 0
    self.refresh_in_label.setText("Refresh In: 0.00 seconds")
    self.info_pane.append("<font color='red'><b>Auction ended.</b></font>")
    log_debug_info(self, "Auction ended.", 'red')

def paste_clipboard(self):
    clipboard = QApplication.clipboard()
    self.link_input.setPlainText(clipboard.text())

def set_refresh_interval(self):
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
