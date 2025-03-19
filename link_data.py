def extract_data_from_response(response):
    """
    Extract relevant auction-related data from the server response.
    """
    auction_data = {}
    try:
        # Example of extracting common auction fields
        auction_data['title'] = response.get('title', 'No title found')
        auction_data['price'] = response.get('price', 'No price found')
        auction_data['condition'] = response.get('condition', 'No condition found')
        auction_data['shipping'] = response.get('shipping', 'No shipping info found')
        auction_data['seller'] = response.get('seller', 'No seller info found')
        auction_data['end_time'] = response.get('end_time', 'No end time found')

        return auction_data
    except Exception as e:
        return {"error": f"Error extracting data: {str(e)}"}
