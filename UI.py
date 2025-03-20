import tkinter as tk

def create_gui(): 
    # Create the main window
    print("DEBUG: Creating the main window")
    root = tk.Tk()

    root.title("Snipester")
    root.configure(bg='darkgrey')
    root.geometry("1000x600")  # Set minimum window size

    # Create the auction pane
    print("DEBUG: Creating auction_pane")
    auction_pane = tk.Frame(root, bg='darkgrey')
    auction_pane.pack(pady=10)

    print("DEBUG: Creating auction_pane_label")
    auction_pane_label = tk.Label(auction_pane, text="Enter Auction:", bg='darkgrey', fg='lightblue', anchor='w')
    auction_pane_label.pack(fill='x')

    print("DEBUG: Creating auction_entry")
    auction_entry = tk.Text(auction_pane, bg='black', fg='#00FF00', width=40, height=4)  # Soda green
    auction_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    auction_pane.bind("<Button-1>", lambda event: auction_entry.tag_add("sel", "1.0", "end"))  # Highlight all text on click

    auction_pane_scrollbar = tk.Scrollbar(auction_pane, command=auction_entry.yview)

    scrollbar1.pack(side=tk.RIGHT, fill=tk.Y)
    auction_entry.config(yscrollcommand=scrollbar1.set)

    # Create the second pane
    print("DEBUG: Creating http_stripped")
    http_stripped = tk.Frame(root, bg='darkgrey')
    http_stripped.pack(pady=10)

    print("DEBUG: Creating http_stripped_label")
    http_stripped_label = tk.Label(http_stripped, text="Stripped HTTP:", bg='darkgrey', fg='lightblue', anchor='w')
    http_stripped_label.pack(fill='x')

    print("DEBUG: Creating http_stripped_entry")
    http_stripped_entry = tk.Text(http_stripped, bg='black', fg='#00FF00', width=40, height=4)  # Soda green
    http_stripped_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    http_stripped_scrollbar = tk.Scrollbar(http_stripped, command=http_stripped_entry.yview)

    scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
    http_stripped_entry.config(yscrollcommand=scrollbar2.set)

    # Start the GUI event loop
    print("DEBUG: Starting the GUI event loop")
    root.mainloop()
