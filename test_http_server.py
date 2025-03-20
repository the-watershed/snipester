import socket
import threading
from http import HTTPServer

def run_server():
    server = HTTPServer()
    server.start()

# Start the server in a separate thread
threading.Thread(target=run_server, daemon=True).start()

# Create a client to test the server
def test_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    import time
    time.sleep(1)  # Wait for the server to start
    client_socket.connect(('localhost', 8080))

    client_socket.sendall(b'GET / HTTP/1.1\r\nHost: localhost\r\n\r\n')
    response = client_socket.recv(4096)
    print(response.decode())
    client_socket.close()

# Run the test
test_server()
