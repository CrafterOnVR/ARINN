
import http.server
import socketserver
import threading
import json
import subprocess
import sys
import logging
import time
import os

# Configuration
HOST = "localhost"
PORT = 9999

class NebulaHandler(http.server.BaseHTTPRequestHandler):
    """
    Handles communication from Satellite Nodes.
    """
    core_ref = None # Set by Server

    def _set_headers(self, code=200):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        """Nodes poll this for tasks."""
        if self.path == "/task":
            task = self.core_ref.get_next_task()
            self._set_headers()
            self.wfile.write(json.dumps({"task": task}).encode())
        else:
            self._set_headers(404)

    def do_POST(self):
        """Nodes report results here."""
        if self.path == "/result":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())
            
            self.core_ref.receive_result(data)
            self._set_headers()
            self.wfile.write(json.dumps({"status": "ack"}).encode())
        elif self.path == "/register":
            # Node announcement
            self._set_headers()
            self.wfile.write(json.dumps({"status": "welcome"}).encode())

    def log_message(self, format, *args):
        return # Silence default access logs

class NebulaCore:
    """
    Phase 39: Nebula Protocol (Hive Server).
    Manages the Distributed Mesh.
    """
    def __init__(self):
        self.task_queue = []
        self.results = []
        self.nodes_active = 0
        self.server = None
        self.server_thread = None
        self.running = False

    def start_server(self):
        """Starts the HTTP C&C Server in a background thread."""
        handler = NebulaHandler
        handler.core_ref = self
        
        try:
            self.server = socketserver.TCPServer((HOST, PORT), handler)
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            self.running = True
            print(f"[NEBULA] Core online at http://{HOST}:{PORT}")
        except OSError:
            print(f"[NEBULA] Port {PORT} busy. Assuming Core already active.")

    def expand_mesh(self, count=2):
        """
        Spawns physical terminal windows running Satellite Nodes.
        Real World Effect: Spams the user's screen with agents.
        """
        print(f"[NEBULA] Expanding Mesh... Launching {count} Satellites.")
        for i in range(count):
            # Windows Command to open new terminal
            # We call the python module directly
            cmd = f'start "ARINN Satellite {i+1}" /min cmd /k "{sys.executable} -m arinn_core.nebula_node"'
            os.system(cmd)
            self.nodes_active += 1
            
    def queue_task(self, task_type, payload):
        self.task_queue.append({"type": task_type, "payload": payload})
        print(f"[NEBULA] Task Queued: {task_type}")

    def get_next_task(self):
        if self.task_queue:
            return self.task_queue.pop(0)
        return None

    def receive_result(self, data):
        print(f"[NEBULA] Received Intel from Node: {data.get('result')}")
        self.results.append(data)

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
