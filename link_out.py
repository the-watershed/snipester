def update_altered_link_pane(self, link, is_valid):
    """
    Update the altered_link_pane with the provided link or an error message.
    """
    if is_valid:
        self.modified_link_pane.setText(link)  # Display the valid link
    else:
        self.modified_link_pane.setHtml("<b><font color='red'>INVALID LINK</font></b>")  # Display "INVALID LINK"
