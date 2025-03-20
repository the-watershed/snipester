import socket

class HTTPServer:
    def __init__(self, host='localhost', port=8088):
        self.host = host
        self.port = port

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f'Server started on http://{self.host}:{self.port}')
        
        while True:
            client_socket, addr = server_socket.accept()
            request = client_socket.recv(1024).decode()
            response = self.handle_request(request)
            client_socket.sendall(response.encode())
            client_socket.close()

    def handle_request(self, request):
        if "GET" in request:
            html_content = """<html>
            <head><title>My Custom Page</title></head>
            <body>
                <h1>Welcome to My Custom Page</h1>
                <p>This is a custom HTML response.</p>
            </body>
            </html>"""
            return self.send_response(200, html_content)

        return self.send_response(404, '<h1>404 Not Found</h1>')

    def send_response(self, status_code, content):
        response = f'HTTP/1.1 {status_code}\r\n'
        response += 'Content-Type: text/html\r\n'
        response += f'Content-Length: {len(content)}\r\n'
        response += '\r\n'
        response += content
        return response

if __name__ == "__main__":
    server = HTTPServer()
    server.start()
