import requests
from ebay_api import retrieve_ebay_item_info

# Custom HTTP/HTML engine to retrieve information from the server
def retrieve_information(link):
    try:
        # Check if it's an eBay link
        if "ebay.com" in link:
            # Use eBay API to get information
            item_info = retrieve_ebay_item_info(link)
            if "error" in item_info:
                return f"Error retrieving information: {item_info['error']}"
            # Convert API response to a format similar to what the HTML parsing expects
            return str(item_info)
        else:
            # For non-eBay links, use the original approach
            response = requests.get(link)
            response.raise_for_status()
            return response.text
    except requests.RequestException as e:
        return f"Error retrieving information: {e}"
