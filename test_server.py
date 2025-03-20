import socket
import logging

class HTTPServer:
    def __init__(self, host='localhost', port=8081):  # Changed port to avoid conflict
        self.host = host
        self.port = port
        logging.info(f'DEBUG: Initialized HTTPServer with host={self.host} and port={self.port}')

    def start_server(self):
        self.start()  # Call the existing start method

    def start(self): 
        logging.info(f'DEBUG: Server is initializing...')  # Log server initialization

        logging.info(f'DEBUG: Starting server on http://{self.host}:{self.port}')  # Log server start

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)

        while True: 
            logging.info(f'DEBUG: Server is now listening for connections...')  # Log when server starts listening

            client_socket, addr = server_socket.accept()
            logging.info(f"DEBUG: Accepted connection from {addr}")

            request = client_socket.recv(1024).decode()
            logging.info(f"DEBUG: Received request: {request}")

            response = self.handle_request(self.parse_request(request))
            client_socket.sendall(response.encode())
            logging.info(f"DEBUG: Sent response: {response}")

            client_socket.close()

    def parse_request(self, request):
        lines = request.splitlines()
        method, path, _ = lines[0].split()
        logging.info(f"DEBUG: Parsed request with method={method} and path={path}")

        return {'method': method, 'path': path}

    def handle_request(self, request):
        method = request.get('method')
        logging.info(f"DEBUG: Handling request with method={method}")

        if method == 'GET':
            return self.handle_get(request)
        elif method == 'POST':
            return self.handle_post(request)
        else:
            return self.send_response(405, 'Method Not Allowed')

    def handle_get(self, request):
        logging.info("DEBUG: Handling GET request")
        return self.send_response(200, '<h1>Hello, World!</h1>')

    def handle_post(self, request): 
        logging.info("DEBUG: Handling POST request") 
        return self.send_response(200, 'POST request received')

    def status(self):
        logging.info("DEBUG: Status endpoint called")
        return self.send_response(200, 'Server is running')

    def send_response(self, status_code, content):
        response = f'HTTP/1.1 {status_code}\r\n'
        response += 'Content-Type: text/html\r\n'
        response += f'Content-Length: {len(content)}\r\n'
        response += '\r\n'
        response += content
        return response

def start_server():
    server = HTTPServer()  # Create an instance of the HTTPServer
    print("Starting server...")
    server.start()  # Start the HTTP server
    print("Server started")