# Snipester - eBay Auction Monitor

A Python application to monitor eBay auctions and provide real-time updates on auction status.

## Installation

1. Clone the repository
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## eBay SDK Configuration

The application uses the official eBay SDK to interact with eBay's API. You'll need to:

1. Register as an eBay developer at https://developer.ebay.com
2. Create an application and get the necessary credentials
3. Update the credentials in `globals.py`:
   - EBAY_APP_ID
   - EBAY_CERT_ID
   - EBAY_DEV_ID
   - EBAY_AUTH_TOKEN

## Running the Application

```bash
python main.py
```

## Features

- Monitor eBay auctions in real-time
- Auto-refresh based on auction end time
- Debug mode to view API interactions
- Clean, modern UI with PyQt5
