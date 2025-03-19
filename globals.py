from PyQt5.QtCore import QTimer

# eBay API credentials for SDK
EBAY_APP_ID = "TerryJur-watcher-PRD-a8fa80b40-07f67c5f"
EBAY_CERT_ID = "SBX-8f8eaeb990d7-8cfc-4587-a688-99f3"
EBAY_DEV_ID = "f815c236-cec7-43ff-afa0-7ad56af2590a"
EBAY_AUTH_TOKEN = "v^1.1#i^1#I^3#r^1#p^3#f^0#t^Ul4xMF8zOjA0MjU3QUNDMzk5MzBDQ0M4RUJBN0NEMjNBOTUyMzJDXzFfMSNFXjEyODQ="

# Option to use fallback web scraping instead of the API
USE_FALLBACK_SCRAPER = True  # Set to True to use web scraping when API fails

# Application state variables
refresh_interval = 600000  # Initialize refresh_interval with a default value
refresh_timer = QTimer()
refresh_in = refresh_interval / 1000.0  # Initialize refresh_in with the default refresh interval
timer = None  # Initialize timer as None
no_time_remaining_attempts = 0  # Initialize counter for no time_remaining attempts
retrieval_times = []  # List to store retrieval times
total_seconds = 0
end_datetime = None
bid_info = {}
