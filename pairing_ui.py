from flask import Flask, request, render_template_string
import subprocess
import threading
import time
import os

app = Flask(__name__)

def check_internet_connection():
    time.sleep(30)  # Wait for 30 seconds before checking
    try:
        # Attempt to ping Google's DNS server to check for internet connectivity
        subprocess.check_call(['ping', '-c', '1', '8.8.8.8'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Internet connection established. Shutting down Flask app.")
        # Use os._exit(0) to terminate the entire process
        os._exit(0)
    except subprocess.CalledProcessError:
        print("No internet connection detected after 30 seconds.")

def set_wifi(ssid, password):
    command = f"sudo nmcli dev wifi connect '{ssid}' password '{password}'"
    subprocess.run(command, shell=True, check=True)
    # Start a background thread to check for internet connectivity after setting Wi-Fi
    threading.Thread(target=check_internet_connection).start()

def get_available_ssids():
    try:
        # Ensure 'text=True' for string output and include error capture
        result = subprocess.check_output(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi', 'list'], text=True, stderr=subprocess.STDOUT)
        ssids = result.strip().split('\n')
        
        # Filter out duplicates and empty lines
        ssids = list(filter(None, set(ssids)))
        return ssids
    except subprocess.CalledProcessError as e:
        print(f"Error fetching SSIDs: {e.output}")
        return []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        ssid = request.form['ssid']
        password = request.form['password']
        set_wifi(ssid, password)
        return 'WiFi settings updated. Trying to connect...'
    
    ssids = get_available_ssids()
    print(ssids)
    # Form with SSID dropdown
    ssid_options = ''.join(f'<option value="{ssid}">{ssid}</option>' for ssid in ssids)
    return render_template_string('''
                                  <form method="post">
                                      SSID: <select name="ssid">
                                        {{ssid_options}}
                                        </select><br>
                                      Password: <input type="password" name="password"><br>
                                      <input type="submit" value="Submit">
                                  </form>
                                  ''', ssid_options=ssid_options)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
