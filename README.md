# pi-pairing

## creating systemctl services
- `sudo nano /etc/systemd/system/pairing_ui.service`
- `sudo nano /etc/systemd/system/network-toggle.service`
- sudo systemctl daemon-reload
- sudo systemctl enable pairing_ui.service
- sudo systemctl start pairing_ui.service
- sudo systemctl enable network-toggle.service
- sudo systemctl start network-toggle.service

## create access point
- `nmcli con add type wifi ifname wlan0 con-name my-hotspot autoconnect yes ssid my-hotspot`
- `nmcli con modify my-hotspot 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared`
- `nmcli con modify my-hotspot wifi-sec.key-mgmt wpa-psk`
- `nmcli con modify my-hotspot wifi-sec.psk my-password`
- 
