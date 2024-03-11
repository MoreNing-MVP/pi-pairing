from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)

def set_wifi(ssid, password):
    subprocess.call(['sudo', 'nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password])

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
    app.run(host='0.0.0.0', port=80)
