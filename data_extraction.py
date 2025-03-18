import re
from bs4 import BeautifulSoup

# Function to log debug information
def log_debug_info(message, color='white'):
    print(f"\033[{color}m{message}\033[0m")

# Function to extract title
def extract_title(soup):
    title = soup.find('h1')
    log_debug_info(f"Extracted title: {title.get_text(strip=True) if title else 'N/A'}", 'blue')
    return title.get_text(strip=True) if title else 'N/A'

# Function to extract number of bids
def extract_number_of_bids(soup):
    num_bids = soup.find(text=re.compile(r'(\d+)\s*bids?', re.IGNORECASE))
    log_debug_info(f"Extracted number of bids: {num_bids.strip() if num_bids else 'N/A'}", 'blue')
    return num_bids.strip() if num_bids else 'N/A'

# Function to extract current bid amount
def extract_current_bid(soup, num_bids):
    current_bid = None
    if isinstance(num_bids, str):
        num_bids = soup.find(text=num_bids)
    if num_bids:
        current_bid = num_bids.find_previous(text=re.compile(r'US\s*\$?\d+(\.\d{2})?', re.IGNORECASE))
    log_debug_info(f"Extracted current bid: {current_bid.strip() if current_bid else 'N/A'}", 'blue')
    return current_bid.strip() if current_bid else 'N/A'

# Function to extract time remaining
def extract_time_remaining(soup, num_bids):
    time_remaining = None
    if isinstance(num_bids, str):
        num_bids = soup.find(text=num_bids)
    if num_bids:
        time_remaining = num_bids.find_next(text=re.compile(r'\d+\s*[a-zA-Z]+', re.IGNORECASE))
        if time_remaining:
            log_debug_info(f"Extracted time remaining: {time_remaining.strip()}", 'blue')
            return time_remaining.strip()
    log_debug_info("Extracted time remaining: N/A", 'blue')
    return 'N/A'

# Function to parse bid information from the HTML data
def parse_bid_information(data):
    soup = BeautifulSoup(data, 'html.parser')
    bid_info = {}

    bid_info['Title'] = extract_title(soup)
    bid_info['Number of Bids'] = extract_number_of_bids(soup)
    bid_info['Current Bid'] = extract_current_bid(soup, bid_info['Number of Bids'])
    bid_info['Time Remaining'] = extract_time_remaining(soup, bid_info['Number of Bids'])

    log_debug_info(f"Parsed bid information: {bid_info}", 'blue')
    return bid_info
