from flask import Flask, request, render_template_string
import subprocess
import threading
import time
import os
import logging
from flask import Flask, request, render_template_string
import subprocess

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)

def check_internet_connection():
    time.sleep(30)  # Wait for 30 seconds before checking
    try:
        # Attempt to ping Google's DNS server to check for internet connectivity
        subprocess.check_call(['ping', '-c', '1', '8.8.8.8'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Internet connection established. Shutting down Flask app.")
        subprocess.run("sudo systemctl restart morening.service", shell=True, check=True)
        # Use os._exit(0) to terminate the entire process
        os._exit(0)
    except subprocess.CalledProcessError:
        print("No internet connection detected after 30 seconds.")

def set_wifi(ssid, password):
    subprocess.run("sudo nmcli device wifi rescan", shell=True, check=True)
    time.sleep(5)
    command = f"sudo nmcli dev wifi connect '{ssid}' password '{password}'"
    subprocess.run(command, shell=True, check=True)
    # Start a background thread to check for internet connectivity after setting Wi-Fi
    threading.Thread(target=check_internet_connection).start()

@app.route('/available_ssids', methods=['GET'])
def avilable_ssids_route():
    ssids = get_available_ssids()
    return jsonify({
            'success':  len(ssids) != 0,
            'ssids': ssids
        })

def get_available_ssids():
    try:
        # Ensure 'text=True' for string output and include error capture
        result = subprocess.check_output(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi', 'list'], text=True, stderr=subprocess.STDOUT)
        logging.info("Raw command output: %s", result)  # Log raw output for debugging

        ssids = result.strip().split('\n')
        logging.info("SSIDs after split: %s", ssids)

        ssids = list(filter(None, set(ssids)))
        logging.info("SSIDs after filter and set: %s", ssids)
        return ssids
    except subprocess.CalledProcessError as e:
        logging.error(f"Error fetching SSIDs: {e.output}")
        return []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        ssid = request.form['ssid']
        password = request.form['password']
        set_wifi(ssid, password)
        device_id  = 'noam'
        return jsonify({
            'message': 'WiFi settings updated. Trying to connect...',
            'device_id': device_id
        })
    
    ssids = get_available_ssids()
    logging.info(f'ssid:{ssids}')
    # Form with SSID dropdown
    ssid_options = ''.join(f'<option value="{ssid}">{ssid}</option>' for ssid in ssids)
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Connect to WiFi</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                padding: 20px;
                background-color: #f0f0f0;
            }
            form {
                background-color: #ffffff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px #cccccc;
                margin-bottom: 20px; /* Added space between forms */
            }
            label {
                font-weight: bold;
            }
            select, input[type="password"], input[type="submit"], input[type="button"], input[type="ssid"] {
                width: 100%;
                padding: 10px;
                margin: 8px 0;
                display: inline-block;
                border: 1px solid #ccc;
                border-radius: 4px;
                box-sizing: border-box;
            }
            input[type="submit"], input[type="button"] {
                width: auto;
                background-color: #4CAF50;
                color: white;
                cursor: pointer;
            }
            input[type="submit"]:hover, input[type="button"]:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <h2>Connect to WiFi</h2>
        <form method="post">
            <label for="ssid">SSID:</label>
            <input type="text" id="ssid" name="ssid" required><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password"><br>
            <input type="submit" value="Submit">
        </form>
        <!-- Refresh Button -->
        <form action="/" method="get">
            <input type="button" value="Refresh Networks" onclick="window.location.reload(true);">
        </form>
    </body>
    </html>
    ''', ssid_options=ssid_options)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
