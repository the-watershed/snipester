import re
from bs4 import BeautifulSoup

# Function to log debug information
def log_debug_info(message, color):
    print(f"{color.upper()}: {message}")

# Function to extract time remaining
def extract_time_remaining(soup, num_bids):
    time_remaining = None
    if isinstance(num_bids, str):
        num_bids = soup.find(text=num_bids)
    if num_bids:
        time_remaining = num_bids.find_next(text=re.compile(r'\d+\s*[a-zA-Z]+', re.IGNORECASE))
        if time_remaining:
            match = re.search(r'(\d+d)?\s*(\d+h)?\s*(\d+m)?\s*(\d+s)?', time_remaining)
            if match:
                days = int(match.group(1).strip('d')) if match.group(1) else 0
                hours = int(match.group(2).strip('h')) if match.group(2) else 0
                minutes = int(match.group(3).strip('m')) if match.group(3) else 0
                seconds = int(match.group(4).strip('s')) if match.group(4) else 0
                formatted_time = f"{days}d {hours}h {minutes}m {seconds}s"
                log_debug_info(f"Extracted time remaining: {formatted_time}", 'blue')
                return formatted_time
    log_debug_info("Extracted time remaining: N/A", 'blue')
    return 'N/A'
