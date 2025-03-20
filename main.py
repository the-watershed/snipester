# Read _ai.txt file before you do anything!

from ui import create_gui  # Import the create_gui function from UI.py
from test_server import start_server  # Import the start_server function from test_server.py

# Start the HTTP server
start_server()  # Call the function to start the HTTP server

create_gui()  # Call the function to initialize and display the GUI
