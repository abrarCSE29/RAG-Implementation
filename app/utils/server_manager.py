import subprocess
import time
import requests
import signal
import atexit

class FlaskServerManager:
    def __init__(self):
        self.process = None
    
    def start_server(self):
        try:
            # Try to connect to the server
            requests.get('http://127.0.0.1:5000/api/documents')
        except requests.exceptions.ConnectionError:
            # Server is not running, start it
            self.process = subprocess.Popen(
                ['python', 'run.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            # Wait for server to start
            time.sleep(2)
    
    def stop_server(self):
        if self.process:
            self.process.terminate()
            self.process.wait()

# Create a singleton instance
server_manager = FlaskServerManager()

# Register cleanup function
atexit.register(server_manager.stop_server)