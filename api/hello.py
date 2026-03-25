from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {'message': 'Hello from SpockPM API!'}
        self.wfile.write(json.dumps(response).encode())
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {'message': 'POST received', 'data': post_data.decode()}
        self.wfile.write(json.dumps(response).encode())

if __name__ == '__main__':
    PORT = 8000
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, handler)
    print(f'Server running on port {PORT}')
    httpd.serve_forever()