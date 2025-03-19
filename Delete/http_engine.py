import requests
# Mock implementation of retrieve_ebay_item_info if ebay_api is unavailable
def retrieve_ebay_item_info(link, debug_handler=None):
    """
    Mock implementation of retrieve_ebay_item_info if ebay_api is unavailable.
    Provides mock data for testing.
    """

    # Provide mock data for testing
    if debug_handler:
        debug_handler(f"Mock data returned for link: {link}", 'cyan')
    return {
        "Title": "Mock Item Title",
        "Current Price": "$100.00",
        "Time Remaining": "1d 2h 30m 15s",
        "Listing Status": "Active"
    }

def retrieve_information(link, debug_handler=None):
    """
    Retrieve information about an item from eBay API or directly from web if not eBay.
    Handles both eBay and non-eBay links.
    Logs the raw request and response data if debug_handler is provided.
    """

    """
    Retrieve information about an item from eBay API or directly from web if not eBay.
    Handles both eBay and non-eBay links.
    """

    """
    Retrieve information about an item from eBay API or directly from web if not eBay
    """
    try:
        # Check if it's an eBay link
        if "ebay.com" in link:
            # Use eBay API to get information if the link is an eBay link

            item_info = retrieve_ebay_item_info(link, debug_handler)
            if "error" in item_info:
                return f"Error retrieving information: {item_info['error']}"
            # For consistency with the rest of the application
            return item_info
        else:
            # For non-eBay links, use the original approach
            response = requests.get(link)
            response.raise_for_status()  # Raise an error for bad responses

            if debug_handler:
                debug_handler("<b>Non-eBay URL detected</b> - Using direct HTTP request", 'yellow')
                debug_handler(f"<b>HTTP Response Status:</b> {response.status_code}", 'green')
                debug_handler("<b>HTTP Response Headers:</b><br><pre style='margin-left:20px; background-color:#1a1a1a; padding:10px; color:#00ffff;'>" + 
                            "\n".join([f"{k}: {v}" for k, v in response.headers.items()]) + "</pre>", 'cyan')
            return response.text
    except requests.RequestException as e:
        if debug_handler:
            debug_handler(f"<b>HTTP Error:</b> {str(e)}", 'red')
        return f"Error retrieving information: {e}"
