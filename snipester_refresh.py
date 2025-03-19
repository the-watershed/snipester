from http_engine import retrieve_information
from data_extraction import parse_bid_information
from snipester_utils import log_debug_info, display_info, start_countdown
import time
import re
from globals import refresh_in, retrieval_times, no_time_remaining_attempts
from link_mod import is_valid_link, strip_html_link  # Import functions from link_mod
from link_out import update_altered_link_pane  # Import the new function
from heartbeat import heartbeat  # Import the heartbeat function

# Removed the on_refresh function

def calculate_refresh_interval_from_seconds(seconds_remaining):
    """Calculate refresh interval based on seconds remaining"""
    if seconds_remaining > 3600:  # More than 1 hour
        return 600  # 10 minutes
    elif seconds_remaining > 600:  # More than 10 minutes
        return 60  # 1 minute
    elif seconds_remaining > 300:  # More than 5 minutes
        return 30  # 30 seconds
    elif seconds_remaining > 120:  # More than 2 minutes
        return 15  # 15 seconds
    elif seconds_remaining > 15:  # More than 15 seconds
        return 1  # 1 second
    else:
        return 0.333  # 3 times a second

def calculate_refresh_interval(self, time_remaining):
    total_seconds = 0
    days_match = re.search(r'(\d+)d', time_remaining)
    hours_match = re.search(r'(\d+)h', time_remaining)
    minutes_match = re.search(r'(\d+)m', time_remaining)
    seconds_match = re.search(r'(\d+)s', time_remaining)

    if days_match:
        total_seconds += int(days_match.group(1)) * 86400
    if hours_match:
        total_seconds += int(hours_match.group(1)) * 3600
    if minutes_match:
        total_seconds += int(minutes_match.group(1)) * 60
    if seconds_match:
        total_seconds += int(seconds_match.group(1))

    return calculate_refresh_interval_from_seconds(total_seconds)
