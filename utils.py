import pygame
import pygame_gui
import re
from utils import log_debug_info, is_valid_link, display_info, start_countdown, update_timer, update_info_pane, paste_clipboard, set_refresh_interval
from PyQt5.QtCore import QDateTime, QTimer
from PyQt5.QtWidgets import QApplication

# Function to ensure text gets displayed correctly on the screen
def display_text_correctly(text, container, manager):
    for element in container.get_container().elements:
        element.kill()
    pygame_gui.elements.UITextBox(
        html_text=text, 
        relative_rect=pygame.Rect((0, 0), (container.get_relative_rect().width, container.get_relative_rect().height)), 
        manager=manager, 
        container=container
    )

def log_debug_info(message, color='white'):
    # ...existing code...
    pass

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

def display_info(self, bid_info):
    self.bid_info = bid_info
    self.update_info_pane()

def start_countdown(self, time_remaining):
    total_seconds = 0
    days_match = re.search(r'(\d+)d', time_remaining)
    hours_match = re.search(r'(\d+)h', time_remaining)
    minutes_match = re.search(r'(\d+)m', time_remaining)
    seconds_match = re.search(r'(\d+)s', time_remaining)

    if days_match:
        total_seconds += int(days_match.group(1)) * 86400  # 24 hours * 3600 seconds
    if hours_match:
        total_seconds += int(hours_match.group(1)) * 3600
    if minutes_match:
        total_seconds += int(minutes_match.group(1)) * 60
    if seconds_match:
        total_seconds += int(seconds_match.group(1))

    self.total_seconds = total_seconds
    self.end_datetime = QDateTime.currentDateTime().addSecs(total_seconds)
    self.set_refresh_interval()
    self.timer = QTimer(self)
    self.timer.timeout.connect(self.update_timer)
    self.timer.start(10)  # Update every 10 milliseconds for hundredths of a second

def update_timer(self):
    if self.total_seconds > 0:
        self.total_seconds -= 0.01
        days, remainder = divmod(self.total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        hundredths = int((seconds - int(seconds)) * 100)
        self.bid_info['Time Remaining'] = f"{int(days)}d {int(hours):02}h {int(minutes):02}m {int(seconds):02}s {hundredths:02}"
        self.bid_info['Time Remaining (English)'] = f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds"
    else:
        self.timer.stop()
        self.bid_info['Time Remaining'] = "0d 00h 00m 00s 00"
        self.bid_info['Time Remaining (English)'] = "0 days, 0 hours, 0 minutes, and 0 seconds"

    self.bid_info['End Date'] = self.end_datetime.toString('dddd, MMMM d, yyyy hh:mm:ss AP')
    self.update_info_pane()
    self.update_refresh_in_label()

def update_info_pane(self):
    self.info_pane.clear()
    for key, value in self.bid_info.items():
        self.info_pane.append(f"<b>{key}:</b> {value}")
    self.info_pane.append(f"<b>Refresh In:</b> {self.time_til_refresh:.2f} seconds")

def paste_clipboard(self):
    clipboard = QApplication.clipboard()
    self.link_input.setPlainText(clipboard.text())
