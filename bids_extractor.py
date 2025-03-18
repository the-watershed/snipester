import re
from bs4 import BeautifulSoup

# Function to extract number of bids
def extract_number_of_bids(soup):
    num_bids = soup.find(text=re.compile(r'(\d+)\s*bids?', re.IGNORECASE))
    return num_bids.strip() if num_bids else 'N/A'
