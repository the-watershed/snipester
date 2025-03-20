import tkinter as tk
from debugger import setup_debugging, debug

def create_gui():
    setup_debugging()  # Set up debugging at the start
    debug("DEBUG: Starting GUI creation process", level='INFO')

    # Create the main window
    debug("Creating the main window", level='INFO')


    root = tk.Tk()

    root.title("Snipester")
    root.configure(bg='darkgrey')
    root.geometry("1000x600")  # Set minimum window size

    # Create the auction pane
    debug("Creating auction_pane", level='INFO')


    auction_pane = tk.Frame(root, bg='darkgrey')
    auction_pane.pack(pady=10)

    debug("Creating auction_pane_label", level='INFO')


    auction_pane_label = tk.Label(auction_pane, text="Enter Auction:", bg='darkgrey', fg='lightblue', anchor='w')
    auction_pane_label.pack(fill='x')

    debug("Creating auction_pane_entry", level='INFO')


    auction_pane_entry = tk.Text(auction_pane, bg='black', fg='#00FF00', width=40, height=4)  # Soda green
    auction_pane_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    # Define scrollbars with updated names
    auction_pane_scrollbar = tk.Scrollbar(auction_pane, command=auction_pane_entry.yview)
    auction_pane_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    auction_pane_entry.config(yscrollcommand=auction_pane_scrollbar.set)

    auction_pane.bind("<Button-1>", lambda event: (debug('Auction pane clicked'), auction_pane_entry.tag_add("sel", "1.0", "end")))  # Highlight all text on click


    auction_pane_entry.bind("<Button-1>", lambda event: (debug('Auction entry clicked'), auction_pane_entry.tag_add("sel", "1.0", "end")))  # Highlight all text on click



    # Create the second pane
    debug("Creating http_stripped", level='INFO')


    http_stripped = tk.Frame(root, bg='darkgrey')
    http_stripped.pack(pady=10)

    debug("Creating http_stripped_label", level='INFO')


    http_stripped_label = tk.Label(http_stripped, text="Stripped HTTP:", bg='darkgrey', fg='lightblue', anchor='w')
    http_stripped_label.pack(fill='x')

    debug("Creating http_stripped_entry", level='INFO')


    http_stripped_entry = tk.Text(http_stripped, bg='black', fg='#00FF00', width=40, height=4)  # Soda green
    http_stripped_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    # Define second scrollbar with updated name
    http_stripped_scrollbar = tk.Scrollbar(http_stripped, command=http_stripped_entry.yview)
    http_stripped_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    http_stripped_entry.config(yscrollcommand=http_stripped_scrollbar.set)

    # Create a submit button
    submit_button = tk.Button(root, text="Submit Auction", command=lambda: debug("Auction submitted!"))
    submit_button.pack(pady=10)

    # Start the GUI event loop

    debug("Starting the GUI event loop", level='INFO')
