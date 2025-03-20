import socket

class HTTPServer:
    def __init__(self, host='localhost', port=8081):  # Changed port to avoid conflict
        self.host = host
        self.port = port
        print(f'DEBUG: Initialized HTTPServer with host={self.host} and port={self.port}')

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f'DEBUG: Starting server on http://{self.host}:{self.port}')
        
        while True:
            client_socket, addr = server_socket.accept()
            print(f"DEBUG: Accepted connection from {addr}")
            request = client_socket.recv(1024).decode()
            print(f"DEBUG: Received request: {request}")
            response = self.handle_request(self.parse_request(request))
            client_socket.sendall(response.encode())
            print(f"DEBUG: Sent response: {response}")
            client_socket.close()

    def parse_request(self, request):
        lines = request.splitlines()
        method, path, _ = lines[0].split()
        print(f"DEBUG: Parsed request with method={method} and path={path}")
        return {'method': method, 'path': path}

    def handle_request(self, request):
        method = request.get('method')
        print(f"DEBUG: Handling request with method={method}")
        if method == 'GET':
            return self.handle_get(request)
        elif method == 'POST':
            return self.handle_post(request)
        else:
            return self.send_response(405, 'Method Not Allowed')

    def handle_get(self, request):
        print("DEBUG: Handling GET request")
        return self.send_response(200, '<h1>Hello, World!</h1>')

    def handle_post(self, request):
        print("DEBUG: Handling POST request")
        return self.send_response(200, 'POST request received')

    def send_response(self, status_code, content):
        response = f'HTTP/1.1 {status_code}\r\n'
        response += 'Content-Type: text/html\r\n'
        response += f'Content-Length: {len(content)}\r\n'
        response += '\r\n'
        response += content
        return response
