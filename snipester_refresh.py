from http_engine import retrieve_information
from data_extraction import parse_bid_information
from snipester_utils import log_debug_info, is_valid_link, display_info, start_countdown
import time
import re
from globals import refresh_in, retrieval_times, no_time_remaining_attempts

def on_refresh(self):
    global refresh_in, retrieval_times, no_time_remaining_attempts
    
    link = self.link_input.toPlainText()
    modified_link = self.strip_html_link(link)
    self.modified_link_pane.setText(modified_link)
    log_debug_info(self, f"Refresh button pressed. Link: {modified_link}", 'yellow')
    if is_valid_link(modified_link):
        log_debug_info(self, "Link is valid.", 'green')
        start_time = time.time()
        info = retrieve_information(modified_link)
        retrieval_time = time.time() - start_time
        retrieval_times.append(retrieval_time)
        if len(retrieval_times) > 3:
            retrieval_times.pop(0)
        average_retrieval_time = sum(retrieval_times) / len(retrieval_times)
        refresh_in -= average_retrieval_time
        if "Bidding ended on" in info:
            self.auction_ended()
            return
        log_debug_info(self, f"Information retrieved: {info[:100]}...", 'blue')
        bid_info = parse_bid_information(info)
        log_debug_info(self, f"Parsed bid information: {bid_info}", 'blue')
        display_info(self, bid_info)
        if bid_info['Time Remaining'] == 'N/A':
            no_time_remaining_attempts += 1
            if no_time_remaining_attempts >= 3:
                self.auction_ended()
                return
        else:
            no_time_remaining_attempts = 0
            start_countdown(self, bid_info['Time Remaining'])
            refresh_in = self.calculate_refresh_interval(bid_info['Time Remaining']) - average_retrieval_time
    else:
        log_debug_info(self, "Invalid link.", 'red')
        self.info_pane.setText("<font color='red'>Invalid link. Please enter a valid URL.</font>")

def calculate_refresh_interval(self, time_remaining):
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
    return total_seconds