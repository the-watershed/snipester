import re
from bs4 import BeautifulSoup

def log_debug_info(message, color='white'):
    print(f"\033[{color}m{message}\033[0m")

def parse_bid_information(data):
    """
    Parse bid information from either API response or HTML data
    """
    # If the data is already a dictionary (from eBay API)
    if isinstance(data, dict):
        log_debug_info(f"Using API data: {data}", 'green')
        return data
    
    # If the data is HTML (from traditional web scraping)
    try:
        soup = BeautifulSoup(data, 'html.parser')
        bid_info = {}

        # Extract title
        title = soup.find('h1')
        bid_info['Title'] = title.get_text(strip=True) if title else 'N/A'
        log_debug_info(f"Extracted title: {bid_info['Title']}", 'blue')

        # Extract number of bids
        num_bids = soup.find(text=re.compile(r'(\d+)\s*bids?', re.IGNORECASE))
        bid_info['Number of Bids'] = num_bids.strip() if num_bids else 'N/A'
        log_debug_info(f"Extracted number of bids: {bid_info['Number of Bids']}", 'blue')

        # Extract current bid amount
        current_bid = None
        if num_bids:
            current_bid = num_bids.find_previous(text=re.compile(r'US\s*\$?\d+(\.\d{2})?', re.IGNORECASE))
        bid_info['Current Bid'] = current_bid.strip() if current_bid else 'N/A'
        log_debug_info(f"Extracted current bid: {bid_info['Current Bid']}", 'blue')

        # Extract time remaining
        time_remaining = None
        if num_bids:
            time_remaining = num_bids.find_next(text=re.compile(r'\d+\s*[a-zA-Z]+', re.IGNORECASE))
        bid_info['Time Remaining'] = time_remaining.strip() if time_remaining else 'N/A'
        log_debug_info(f"Extracted time remaining: {bid_info['Time Remaining']}", 'blue')

        log_debug_info(f"Parsed bid information: {bid_info}", 'blue')
        return bid_info
    except Exception as e:
        log_debug_info(f"Error parsing data: {e}", 'red')
        return {"Title": "Error", "Number of Bids": "N/A", "Current Bid": "N/A", "Time Remaining": "N/A", "error": str(e)}
