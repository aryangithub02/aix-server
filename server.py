import http.server
import socketserver
import json
import os

# Render and other platforms provide PORT environment variable
PORT = int(os.environ.get('PORT', 8000))
JSON_FILE = 'participants_master.json'

class SyncHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Health check for Render
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'AX26 Sync Server is Online.')
        else:
            return super().do_GET()

    def do_POST(self):
        if self.path == '/save-json':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data)
                with open(JSON_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {'status': 'success', 'message': 'Data written to participants_master.json'}
                self.wfile.write(json.dumps(response).encode())
                print(f"[*] Updated {JSON_FILE} with current dashboard state.")
            except Exception as e:
                self.send_response(500)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(str(e).encode())
        else:
            super().do_POST()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

# Bind to 0.0.0.0 to allow external access in cloud environments
with socketserver.TCPServer(("0.0.0.0", PORT), SyncHandler) as httpd:
    print(f"AX26 Sync Server running on port {PORT}")
    httpd.serve_forever()
