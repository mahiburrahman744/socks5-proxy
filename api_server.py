from flask import Flask
import threading
import time
import socks5_server  # Import to access current_port

app = Flask(__name__)

@app.route('/get_port')
def get_port():
    return {'port': socks5_server.current_port}

if __name__ == '__main__':
    app.run(port=5000, debug=False)  # Run the Flask app
