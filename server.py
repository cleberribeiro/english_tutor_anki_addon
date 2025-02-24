import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Dict, Any
from aqt.utils import showInfo
from aqt.qt import QApplication, Qt
from .anki_sync import create_card, show_message_safe

class RequestHandler(BaseHTTPRequestHandler):
    def send_json_response(self, data: Dict[str, Any], status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length == 0:
                self.send_json_response({"error": "Empty request"}, 400)
                return

            post_data = self.rfile.read(content_length)
            request = json.loads(post_data.decode("utf-8"))

            if request.get("action") == "create_card":
                params = request.get("params", {})
                model = params.get("model", "basic")
                fields = params.get("fields", {})

                if not fields:
                    self.send_json_response({"error": "Fields cannot be empty"}, 400)
                    return

                card_id = create_card(model, fields)
                if card_id:
                    self.send_json_response({"result": "success", "card_id": card_id})
                else:
                    self.send_json_response({"error": "Failed to create card"}, 500)
            else:
                self.send_json_response({"error": "Invalid action"}, 400)
        except json.JSONDecodeError:
            self.send_json_response({"error": "Invalid JSON"}, 400)
        except Exception as e:
            self.send_json_response({"error": str(e)}, 500)

class SafeHTTPServer(HTTPServer):
    def handle_error(self, request, client_address):
        show_message_safe(f"Erro no servidor: {request} {client_address}", True)

def run_server(host: str = "127.0.0.1", port: int = 8766) -> None:
    try:
        server_address = (host, port)
        httpd = SafeHTTPServer(server_address, RequestHandler)
        show_message_safe(f"Servidor do Add-on iniciado na porta {port}")
        httpd.serve_forever()
    except Exception as e:
        show_message_safe(f"Erro ao iniciar servidor: {e}", True)