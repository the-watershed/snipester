from http_engine import retrieve_information
from data_extraction import parse_bid_information
from snipester_utils import is_valid_link, display_info, start_countdown
from globals import refresh_in, retrieval_times, no_time_remaining_attempts

def update_refresh_in_label(self):
    global refresh_in
    if refresh_in > 0:
        refresh_in -= 0.01
    else:
        link = self.link_input.toPlainText()
        if is_valid_link(link):
            info = retrieve_information(link)
            if "Bidding ended on" in info:
                self.auction_ended()
                return
            bid_info = parse_bid_information(info)
            display_info(self, bid_info)
            if bid_info['Time Remaining'] == 'N/A':
                no_time_remaining_attempts += 1
                if no_time_remaining_attempts >= 3:
                    self.auction_ended()
                    return
            else:
                no_time_remaining_attempts = 0
                start_countdown(self, bid_info['Time Remaining'])
                refresh_in = self.calculate_refresh_interval(bid_info['Time Remaining']) - sum(retrieval_times) / len(retrieval_times)
    self.refresh_in_label.setText(f"Refresh In: {refresh_in:.2f} seconds")
