import re
import json
import datetime
import requests
from bs4 import BeautifulSoup
from ebaysdk.trading import Connection as Trading
from ebaysdk.exception import ConnectionError
from globals import EBAY_APP_ID, EBAY_CERT_ID, EBAY_DEV_ID, EBAY_AUTH_TOKEN, USE_FALLBACK_SCRAPER

class eBayAPI:
    def __init__(self):
        self.app_id = EBAY_APP_ID
        self.cert_id = EBAY_CERT_ID
        self.dev_id = EBAY_DEV_ID
        self.auth_token = EBAY_AUTH_TOKEN
        self.api = None
        self.raw_response = None  # Store the raw response
        self.use_fallback = USE_FALLBACK_SCRAPER
        
        try:
            self.api = Trading(
                appid=self.app_id,
                certid=self.cert_id,
                devid=self.dev_id,
                token=self.auth_token,
                config_file=None,
                domain="api.ebay.com",  # Use production API
                debug=False
            )
        except Exception as e:
            self.api = None
            self.use_fallback = True
            print(f"Error initializing eBay API: {str(e)}")
        
    def check_api_credentials(self):
        """
        Check if the API credentials are valid using the eBay SDK
        """
        if self.use_fallback or self.api is None:
            return {
                "success": False,
                "message": "Using fallback scraper mode due to API configuration issues",
                "raw_response": "No API response - using web scraping fallback"
            }
            
        try:
            response = self.api.execute('GeteBayOfficialTime', {})
            self.raw_response = json.dumps(response.dict(), indent=2)
            
            return {
                "success": True,
                "message": f"API credentials are valid. eBay official time: {response.reply.Timestamp}",
                "raw_response": self.raw_response
            }
        except ConnectionError as e:
            self.use_fallback = True  # Switch to fallback mode on error
            return {
                "success": False,
                "message": f"API credentials validation failed: {str(e)}",
                "raw_response": str(e)
            }
        except Exception as e:
            self.use_fallback = True  # Switch to fallback mode on error
            return {
                "success": False,
                "message": f"Error checking API credentials: {str(e)}",
                "raw_response": "No response received"
            }

    def get_item_details(self, item_id, debug_handler=None):
        """
        Get details of an eBay item using the eBay SDK Trading API or fallback to scraping
        """
        if self.use_fallback or self.api is None:
            if debug_handler:
                debug_handler("<b>API Authentication Failed:</b> Using web scraping fallback method", 'yellow')
            return self._get_item_details_via_scraping(item_id, debug_handler)
            
        try:
            # Create request parameters
            request_dict = {
                'ItemID': item_id,
                'DetailLevel': 'ReturnAll'
            }
            
            # Log the request if debug handler is provided
            if debug_handler:
                debug_handler(f"<b>API Request:</b><br><pre style='margin-left:20px; background-color:#1a1a1a; padding:10px; color:#00ff00; white-space:pre-wrap;'>{json.dumps(request_dict, indent=2)}</pre>", 'cyan')
            
            # Execute the call
            response = self.api.execute('GetItem', request_dict)
            response_dict = response.dict()
            self.raw_response = json.dumps(response_dict, indent=2)
            
            # Log the response if debug handler is provided
            if debug_handler:
                debug_handler(f"<b>API Response:</b><br><pre style='margin-left:20px; background-color:#1a1a1a; padding:10px; color:#00ff00; white-space:pre-wrap;'>{self.raw_response}</pre>", 'cyan')
            
            return self._parse_item_details(response_dict, debug_handler)
            
        except ConnectionError as e:
            error_message = str(e)
            if debug_handler:
                debug_handler(f"<b>API Error:</b><br><pre style='margin-left:20px; background-color:#1a1a1a; padding:10px; color:#ff0000;'>{error_message}</pre>", 'red')
                debug_handler("<b>Falling back to web scraping method</b>", 'yellow')
            
            # Fall back to web scraping
            return self._get_item_details_via_scraping(item_id, debug_handler)
        except Exception as e:
            if debug_handler:
                debug_handler(f"<b>API Error:</b><br><pre style='margin-left:20px; background-color:#1a1a1a; padding:10px; color:#ff0000;'>{str(e)}</pre>", 'red')
                debug_handler("<b>Falling back to web scraping method</b>", 'yellow')
            
            # Fall back to web scraping
            return self._get_item_details_via_scraping(item_id, debug_handler)
        
    def _get_item_details_via_scraping(self, item_id, debug_handler=None):
        """
        Fallback method to get eBay item details via web scraping
        """
        url = f"https://www.ebay.com/itm/{item_id}"
        
        try:
            if debug_handler:
                debug_handler(f"<b>Web Scraping Request:</b> {url}", 'blue')
                
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            if debug_handler:
                debug_handler(f"<b>HTTP Status:</b> {response.status_code}", 'green')
            
            return self._parse_scraped_item_details(response.text, debug_handler)
            
        except Exception as e:
            if debug_handler:
                debug_handler(f"<b>Web Scraping Error:</b><br><pre style='margin-left:20px; background-color:#1a1a1a; padding:10px; color:#ff0000;'>{str(e)}</pre>", 'red')
            return {"error": f"Web scraping failed: {str(e)}"}
    
    def _parse_scraped_item_details(self, html_content, debug_handler=None):
        """
        Parse eBay item details from HTML content
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract title
            title_elem = soup.select_one("h1.x-item-title__mainTitle span")
            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            
            # Extract price
            price_elem = soup.select_one("div.x-price-primary span")
            price = price_elem.get_text(strip=True) if price_elem else "N/A"
            
            # Extract bid count
            bid_count_elem = soup.select_one("div.d-quantity__count")
            bid_count = bid_count_elem.get_text(strip=True) if bid_count_elem else "0 bids"
            
            # Extract time remaining
            time_elem = soup.select_one("span#vi-time-display time")
            time_remaining_raw = time_elem.get_text(strip=True) if time_elem else ""
            
            # Process time remaining to a format compatible with our system
            time_remaining_formatted = "N/A"
            time_remaining_english = "N/A"
            time_remaining_seconds = 0
            listing_status = "Unknown"
            
            if "ended" in time_remaining_raw.lower():
                time_remaining_formatted = "0d 00h 00m 00s"
                time_remaining_english = "Auction has ended"
                listing_status = "Ended"
            else:
                # Try to parse the time remaining text
                days, hours, minutes, seconds = 0, 0, 0, 0
                
                days_match = re.search(r'(\d+)\s*d', time_remaining_raw)
                if days_match: 
                    days = int(days_match.group(1))
                    
                hours_match = re.search(r'(\d+)\s*h', time_remaining_raw)
                if hours_match: 
                    hours = int(hours_match.group(1))
                    
                minutes_match = re.search(r'(\d+)\s*m', time_remaining_raw)
                if minutes_match: 
                    minutes = int(minutes_match.group(1))
                    
                seconds_match = re.search(r'(\d+)\s*s', time_remaining_raw)
                if seconds_match: 
                    seconds = int(seconds_match.group(1))
                
                time_remaining_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds
                time_remaining_formatted = f"{days}d {hours:02}h {minutes:02}m {seconds:02}s"
                time_remaining_english = f"{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds"
                listing_status = "Active"
                
            # Extract end time if available
            end_time_elem = soup.select_one("span#vi-time-display-end")
            end_time_text = end_time_elem.get_text(strip=True) if end_time_elem else "N/A"
            
            result = {
                "Title": title,
                "Current Bid": price,
                "Number of Bids": bid_count,
                "Time Remaining": time_remaining_formatted,
                "Time Remaining (English)": time_remaining_english,
                "Time Remaining (Seconds)": time_remaining_seconds,
                "End Time": end_time_text,
                "Listing Status": listing_status
            }
            
            if debug_handler:
                debug_handler(f"<b>Scraped Item Data:</b><br><pre style='margin-left:20px; background-color:#1a1a1a; padding:10px; color:#00ffff;'>{json.dumps(result, indent=2)}</pre>", 'cyan')
            
            return result
            
        except Exception as e:
            if debug_handler:
                debug_handler(f"<b>HTML Parsing Error:</b><br><pre style='margin-left:20px; background-color:#1a1a1a; padding:10px; color:#ff0000;'>{str(e)}</pre>", 'red')
            return {"error": f"HTML parsing failed: {str(e)}"}
        
    def _parse_item_details(self, response_dict, debug_handler=None):
        """
        Parse the response dictionary from the eBay SDK
        """
        try:
            # Check for errors
            ack = response_dict.get('Ack', '')
            if ack != 'Success' and ack != 'Warning':
                errors = response_dict.get('Errors', [])
                error_msg = errors[0].get('ShortMessage', 'Unknown error') if errors else 'API request was not successful'
                if debug_handler:
                    debug_handler(f"<b>API Error:</b> {error_msg}", 'red')
                    debug_handler("<b>Falling back to web scraping method</b>", 'yellow')
                
                # Fall back to web scraping if there's an API error
                item_id = response_dict.get('Item', {}).get('ItemID', '')
                if item_id:
                    return self._get_item_details_via_scraping(item_id, debug_handler)
                return {"error": error_msg}
            
            # Extract basic item details
            item = response_dict.get('Item', {})
            if not item:
                if debug_handler:
                    debug_handler("<b>API Error:</b> Item not found in response", 'red')
                return {"error": "Item not found in response"}
            
            title = item.get('Title', 'N/A')
            current_price = item.get('SellingStatus', {}).get('CurrentPrice', {})
            price_value = current_price.get('value', 'N/A')
            currency_id = current_price.get('_currencyID', 'USD')
            bid_count = item.get('BidCount', '0')
            end_time_text = item.get('EndTime', '')
            listing_status = item.get('ListingStatus', 'N/A')
            
            # Calculate time remaining
            time_remaining_formatted = "N/A"
            time_remaining_english = "N/A"
            time_remaining_seconds = 0
            
            if end_time_text:
                try:
                    # Parse datetime
                    end_time_dt = datetime.datetime.strptime(end_time_text, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=datetime.timezone.utc)
                    now = datetime.datetime.now(datetime.timezone.utc)
                    
                    # Calculate time difference
                    if end_time_dt > now:
                        delta = end_time_dt - now
                        time_remaining_seconds = delta.total_seconds()
                        
                        # Format time remaining
                        days, remainder = divmod(time_remaining_seconds, 86400)
                        hours, remainder = divmod(remainder, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        
                        time_remaining_formatted = f"{int(days)}d {int(hours):02}h {int(minutes):02}m {int(seconds):02}s"
                        time_remaining_english = f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds"
                    else:
                        time_remaining_formatted = "0d 00h 00m 00s"
                        time_remaining_english = "Auction has ended"
                        listing_status = "Ended"  # Force status to ended if past end time
                except (ValueError, TypeError) as e:
                    if debug_handler:
                        debug_handler(f"<b>Error parsing date:</b> {str(e)}", 'red')
            
            # Format bid count
            bid_count_formatted = f"{bid_count} {'bid' if bid_count == '1' else 'bids'}"
            
            # Format current price
            if price_value != 'N/A':
                current_price_formatted = f"{currency_id} {price_value}"
            else:
                current_price_formatted = "N/A"
            
            result = {
                "Title": title,
                "Current Bid": current_price_formatted,
                "Number of Bids": bid_count_formatted,
                "Time Remaining": time_remaining_formatted,
                "Time Remaining (English)": time_remaining_english,
                "Time Remaining (Seconds)": time_remaining_seconds,
                "End Time": end_time_text,
                "Listing Status": listing_status
            }
            
            if debug_handler:
                debug_handler(f"<b>Parsed Item Data:</b><br><pre style='margin-left:20px; background-color:#1a1a1a; padding:10px; color:#00ffff;'>{json.dumps(result, indent=2)}</pre>", 'cyan')
            
            return result
            
        except Exception as e:
            if debug_handler:
                debug_handler(f"<b>Error parsing response:</b><br><pre style='margin-left:20px; background-color:#1a1a1a; padding:10px; color:#ff0000;'>{str(e)}</pre>", 'red')
            return {"error": f"Error parsing SDK response: {str(e)}"}
    
    def extract_item_id_from_url(self, url):
        """
        Extract the eBay item ID from a URL
        """
        match = re.search(r'itm/(\d+)', url)
        if match:
            return match.group(1)
        return None

def retrieve_ebay_item_info(link, debug_handler=None):
    """
    Function to retrieve information about an eBay item using the eBay SDK
    """
    api = eBayAPI()
    
    # Check credentials first if debug_handler is provided
    if debug_handler:
        debug_handler("<b>Checking eBay API credentials using SDK...</b>", 'yellow')
        cred_check = api.check_api_credentials()
        if cred_check["success"]:
            debug_handler(f"<b>API Credentials Valid:</b> {cred_check['message']}", 'green')
        else:
            debug_handler(f"<b>API Credentials Invalid:</b> {cred_check['message']}", 'red')
        debug_handler(f"<b>Raw API Response:</b><br><pre style='margin-left:20px; background-color:#1a1a1a; padding:10px; color:#00ff00; white-space:pre-wrap;'>{cred_check['raw_response']}</pre>", 'cyan')
    
    item_id = api.extract_item_id_from_url(link)
    if item_id:
        if debug_handler:
            debug_handler(f"<b>Extracted Item ID:</b> {item_id}", 'green')
        return api.get_item_details(item_id, debug_handler)
    else:
        if debug_handler:
            debug_handler("<b>Error:</b> Invalid eBay item URL", 'red')
        return {"error": "Invalid eBay item URL"}
