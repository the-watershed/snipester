from PyQt5.QtCore import QTimer

# eBay API credentials
EBAY_APP_ID = "TerryJur-watcher-SBX-38f8eaeb9-a9cf5b8b"
EBAY_CERT_ID = "SBX-8f8eaeb990d7-8cfc-4587-a688-99f3"
EBAY_DEV_ID = "f815c236-cec7-43ff-afa0-7ad56af2590a"
EBAY_AUTH_TOKEN = "v^1.1#i^1#p^3#f^0#I^3#r^1#t^Ul4xMF83OjU4MEI5QTU2MUJCQzFDM0VENzc4MEE4RDcyNkQ2MkI5XzFfMSNFXjEyODQ="

refresh_interval = 600000  # Initialize refresh_interval with a default value
refresh_timer = QTimer()
refresh_in = refresh_interval / 1000.0
timer = None  # Initialize timer as None
no_time_remaining_attempts = 0  # Initialize counter for no time_remaining attempts
retrieval_times = []  # List to store retrieval times
total_seconds = 0
end_datetime = None
bid_info = {}
