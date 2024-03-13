#!/bin/bash

# Define your WiFi SSID and Password
# SSID="my-hotspot"
# PASSWORD="my-password"

# Copy the service files to the systemd directory
sudo cp pairing_ui.service /etc/systemd/system/
sudo cp network-toggle.service /etc/systemd/system/

# Reload systemd to recognize the new services
sudo systemctl daemon-reload

# Enable and start the services
sudo systemctl enable pairing_ui.service
sudo systemctl start pairing_ui.service
sudo systemctl enable network-toggle.service
sudo systemctl start network-toggle.service

# Create and configure the access point
nmcli con add type wifi ifname wlan0 con-name $SSID autoconnect yes ssid $SSID
nmcli con modify $SSID 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared
nmcli con modify $SSID wifi-sec.key-mgmt wpa-psk
nmcli con modify $SSID wifi-sec.psk $PASSWORD

echo "Setup completed."
