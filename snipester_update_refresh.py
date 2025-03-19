from http_engine import retrieve_information
from data_extraction import parse_bid_information
from link_mod import is_valid_link  # Import is_valid_link from link_mod
from snipester_utils import display_info, start_countdown, log_debug_info
from globals import refresh_in, retrieval_times, no_time_remaining_attempts
from snipester_refresh import calculate_refresh_interval_from_seconds

def update_refresh_in_label(self):
    global refresh_in
    if refresh_in > 0:
        refresh_in -= 0.01
    else:
        link = self.link_input.toPlainText()
        if is_valid_link(link):
            # Create a debug handler function if debug is enabled
            debug_handler = None
            if hasattr(self, 'debug_checkbox') and self.debug_checkbox.isChecked():
                debug_handler = lambda msg, color: log_debug_info(self, msg, color)

            # Get item info from eBay API
            item_info = retrieve_information(link, debug_handler)

            # Check for errors or auction end
            if isinstance(item_info, str) and "Error" in item_info:
                self.info_pane.setText(f"<font color='red'>{item_info}</font>")
                return

            if isinstance(item_info, dict) and "error" in item_info:
                self.info_pane.setText(f"<font color='red'>{item_info['error']}</font>")
                return

            if isinstance(item_info, dict) and item_info.get('Listing Status') == 'Ended':
                self.auction_ended()
                return

            # Process bid information
            bid_info = parse_bid_information(item_info)
            display_info(self, bid_info)

            if bid_info['Time Remaining'] == 'N/A':
                no_time_remaining_attempts += 1
                if no_time_remaining_attempts >= 3:
                    self.auction_ended()
                    return
            else:
                no_time_remaining_attempts = 0
                start_countdown(self, bid_info['Time Remaining'])

                # If we have time remaining in seconds directly from the API, use it
                if 'Time Remaining (Seconds)' in bid_info and isinstance(bid_info['Time Remaining (Seconds)'], (int, float)):
                    refresh_in = calculate_refresh_interval_from_seconds(bid_info['Time Remaining (Seconds)']) - sum(retrieval_times) / len(retrieval_times) if retrieval_times else 0
                else:
                    refresh_in = calculate_refresh_interval_from_seconds(self.calculate_refresh_interval(bid_info['Time Remaining'])) - sum(retrieval_times) / len(retrieval_times) if retrieval_times else 0

    self.refresh_in_label.setText(f"Refresh In: {refresh_in:.2f} seconds")
