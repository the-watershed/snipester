from link_mod import is_valid_link, strip_html_link
from link_out import update_altered_link_pane
from http_engine import retrieve_information
from snipester_utils import log_debug_info, display_info, start_countdown
from globals import refresh_in, retrieval_times, no_time_remaining_attempts

def heartbeat(self):
    """
    Handle the heartbeat logic, including on_refresh calls and periodic updates.
    """
    global refresh_in, retrieval_times, no_time_remaining_attempts

    # Check if the scrape link checkbox is checked
    if not self.ui.scrape_link_checkbox.isChecked():  # Access scrape_link_checkbox through self.ui
        log_debug_info(self, "Scrape Link checkbox is unchecked. Skipping scraping.", 'orange')
        return

    # Get the link from the input pane
    link = self.ui.link_input.toPlainText()  # Access link_input through self.ui
    log_debug_info(self, f"Original link: {link}", 'yellow', variables={"link": link})

    # Validate the link
    if not is_valid_link(link):
        update_altered_link_pane(self.ui, link, is_valid=False)  # Pass self.ui to update_altered_link_pane
        log_debug_info(self, "Invalid link provided.", 'red', variables={"link": link})
        return

    # Strip the link to its base form
    modified_link = strip_html_link(link)
    if modified_link:
        update_altered_link_pane(self.ui, modified_link, is_valid=True)  # Pass self.ui to update_altered_link_pane
        log_debug_info(self, f"Modified link: {modified_link}", 'green', variables={"modified_link": modified_link})
    else:
        update_altered_link_pane(self.ui, link, is_valid=False)  # Pass self.ui to update_altered_link_pane
        log_debug_info(self, "Invalid link provided after stripping.", 'red', variables={"link": link})
        return

    # Debug handler for logging
    debug_handler = None
    if self.ui.debug_checkbox.isChecked():  # Access debug_checkbox through self.ui
        debug_handler = lambda msg, color: log_debug_info(self, msg, color)

    # Retrieve information from the link
    item_info = retrieve_information(modified_link, debug_handler)
    if not item_info:
        log_debug_info(self, "Failed to retrieve item information.", 'red')
        return

    # Check for errors or auction end
    if isinstance(item_info, str) and "Error" in item_info:
        log_debug_info(self, f"Error retrieving item info: {item_info}", 'red', variables={"item_info": item_info})
        self.ui.info_pane.setText(f"<font color='red'>{item_info}</font>")  # Access info_pane through self.ui
        return

    if isinstance(item_info, dict) and "error" in item_info:
        log_debug_info(self, f"Error retrieving item info: {item_info['error']}", 'red', variables={"item_info": item_info})
        self.ui.info_pane.setText(f"<font color='red'>{item_info['error']}</font>")  # Access info_pane through self.ui
        return

    if isinstance(item_info, dict) and item_info.get('Listing Status') == 'Ended':
        self.auction_ended()
        return

    # Process and display bid information
    log_debug_info(self, "Information retrieved successfully.", 'blue', variables={"item_info": item_info})
    bid_info = parse_bid_information(item_info)
    log_debug_info(self, f"Parsed bid information: {bid_info}", 'blue', variables={"bid_info": bid_info})
    display_info(self.ui, bid_info)  # Pass self.ui to display_info

    # Handle countdown and refresh interval
    if bid_info['Time Remaining'] == 'N/A':
        no_time_remaining_attempts += 1
        if no_time_remaining_attempts >= 3:
            self.auction_ended()
            return
    else:
        no_time_remaining_attempts = 0
        start_countdown(self.ui, bid_info['Time Remaining'])  # Pass self.ui to start_countdown

        if 'Time Remaining (Seconds)' in bid_info and isinstance(bid_info['Time Remaining (Seconds)'], (int, float)):
            refresh_in = calculate_refresh_interval_from_seconds(bid_info['Time Remaining (Seconds)']) - sum(retrieval_times) / len(retrieval_times) if retrieval_times else 0
        else:
            refresh_in = calculate_refresh_interval_from_seconds(self.calculate_refresh_interval(bid_info['Time Remaining'])) - sum(retrieval_times) / len(retrieval_times) if retrieval_times else 0

    self.ui.refresh_in_label.setText(f"Refresh In: {refresh_in:.2f} seconds")  # Access refresh_in_label through self.ui
