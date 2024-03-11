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

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        ssid = request.form['ssid']
        password = request.form['password']
        set_wifi(ssid, password)
        return 'WiFi settings updated. Trying to connect...'
    
    # Form for user input
    return render_template_string('''
                                  <form method="post">
                                      SSID: <input type="text" name="ssid"><br>
                                      Password: <input type="password" name="password"><br>
                                      <input type="submit" value="Submit">
                                  </form>
                                  ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
