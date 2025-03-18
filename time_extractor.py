import re
from bs4 import BeautifulSoup

def log_debug_info(message, color):
    # Placeholder function for logging debug information
    print(f"{color}: {message}")

# Function to extract time remaining
def extract_time_remaining(soup, num_bids):
    time_remaining = None
    if isinstance(num_bids, str):
        num_bids = soup.find(text=num_bids)
    if num_bids:
        time_remaining = None
        time_remaining = num_bids.find_next(text=re.compile(r'\d+\s*[a-zA-Z]+', re.IGNORECASE))
        if time_remaining:
            log_debug_info(f"Extracted time remaining: {time_remaining.strip()}", 'blue')
            return time_remaining.strip()
    log_debug_info("Extracted time remaining: N/A", 'blue')
    return 'N/A'
