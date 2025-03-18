from bs4 import BeautifulSoup

# Function to extract title
def extract_title(soup):
    title = soup.find('h1')
    return title.get_text(strip=True) if title else 'N/A'
