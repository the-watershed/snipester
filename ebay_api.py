import requests
import xml.etree.ElementTree as ET
from globals import EBAY_APP_ID, EBAY_CERT_ID, EBAY_DEV_ID, EBAY_AUTH_TOKEN

class eBayAPI:
    def __init__(self):
        self.app_id = EBAY_APP_ID
        self.cert_id = EBAY_CERT_ID
        self.dev_id = EBAY_DEV_ID
        self.auth_token = EBAY_AUTH_TOKEN
        self.api_url = "https://api.ebay.com/ws/api.dll"
        self.headers = {
            "X-EBAY-API-SITEID": "0",  # US site
            "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
            "X-EBAY-API-CALL-NAME": "",
            "X-EBAY-API-APP-NAME": self.app_id,
            "X-EBAY-API-CERT-NAME": self.cert_id,
            "X-EBAY-API-DEV-NAME": self.dev_id,
            "Content-Type": "text/xml"
        }

    def get_item_details(self, item_id):
        """
        Get details of an eBay item using the eBay Trading API
        """
        self.headers["X-EBAY-API-CALL-NAME"] = "GetItem"
        
        # Create XML request body
        xml_request = f"""<?xml version="1.0" encoding="utf-8"?>
        <GetItemRequest xmlns="urn:ebay:apis:eBLBaseComponents">
            <RequesterCredentials>
                <eBayAuthToken>{self.auth_token}</eBayAuthToken>
            </RequesterCredentials>
            <ItemID>{item_id}</ItemID>
            <DetailLevel>ReturnAll</DetailLevel>
        </GetItemRequest>"""
        
        response = requests.post(self.api_url, headers=self.headers, data=xml_request)
        
        if response.status_code == 200:
            return self._parse_item_details(response.text)
        else:
            return {"error": f"API request failed with status code {response.status_code}: {response.text}"}

    def _parse_item_details(self, xml_response):
        """
        Parse the XML response from the eBay API
        """
        try:
            root = ET.fromstring(xml_response)
            namespace = {"ns": "urn:ebay:apis:eBLBaseComponents"}
            
            # Extract basic item details
            item = root.find(".//ns:Item", namespace)
            if item is None:
                return {"error": "Item not found in response"}
            
            title = item.find("ns:Title", namespace)
            current_price = item.find(".//ns:CurrentPrice", namespace)
            bid_count = item.find("ns:BidCount", namespace)
            end_time = item.find("ns:EndTime", namespace)
            
            # Calculate time remaining (could be improved with proper datetime handling)
            time_remaining = "N/A"
            if end_time is not None:
                # In a real implementation, parse end_time and calculate time remaining
                pass
            
            return {
                "Title": title.text if title is not None else "N/A",
                "Current Bid": f"US ${current_price.text}" if current_price is not None else "N/A",
                "Number of Bids": f"{bid_count.text} bids" if bid_count is not None else "0 bids",
                "Time Remaining": time_remaining,
                "End Time": end_time.text if end_time is not None else "N/A"
            }
        except Exception as e:
            return {"error": f"Error parsing XML response: {str(e)}"}

    def extract_item_id_from_url(self, url):
        """
        Extract the eBay item ID from a URL
        """
        import re
        match = re.search(r'itm/(\d+)', url)
        if match:
            return match.group(1)
        return None

def retrieve_ebay_item_info(link):
    """
    Function to retrieve information about an eBay item using the eBay API
    """
    api = eBayAPI()
    item_id = api.extract_item_id_from_url(link)
    if item_id:
        return api.get_item_details(item_id)
    else:
        return {"error": "Invalid eBay item URL"}
