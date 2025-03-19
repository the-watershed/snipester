import re
from bs4 import BeautifulSoup

# Function to extract current bid amount
def extract_current_bid(soup, num_bids):
    current_bid = None
    if isinstance(num_bids, str):
        num_bids = soup.find(text=num_bids)
    if num_bids:
        current_bid = num_bids.find_previous(text=re.compile(r'US\s*\$?\d+(\.\d{2})?', re.IGNORECASE))
    return current_bid.strip() if current_bid else 'N/A'
