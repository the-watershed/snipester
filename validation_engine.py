import re
from bs4 import BeautifulSoup

# Function to parse bid information from the HTML data
def parse_bid_information(data):
    soup = BeautifulSoup(data, 'html.parser')
    bid_info = {}

    # Extract title
    title = soup.find('h1')
    bid_info['Title'] = title.get_text(strip=True) if title else 'N/A'

    # Extract number of bids
    num_bids = soup.find(text=re.compile(r'(\d+)\s*bids?', re.IGNORECASE))
    bid_info['Number of Bids'] = num_bids.strip() if num_bids else 'N/A'

    # Extract current bid amount
    current_bid = None
    if num_bids:
        current_bid = num_bids.find_previous(text=re.compile(r'US\s*\$?\d+(\.\d{2})?', re.IGNORECASE))
    bid_info['Current Bid'] = current_bid.strip() if current_bid else 'N/A'

    # Extract time remaining
    time_remaining = None
    if num_bids:
        time_remaining = num_bids.find_next(text=re.compile(r'Ends in\s*\d+\s*[a-zA-Z]+', re.IGNORECASE))
    bid_info['Time Remaining'] = time_remaining.strip() if time_remaining else 'N/A'

    return bid_info
