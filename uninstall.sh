#!/bin/bash

# Define your WiFi SSID
# Note: It's important to use the same SSID as used during the installation.
SSID="my-hotspot"

echo "Stop the services"
sudo systemctl stop pairing_ui.service
sudo systemctl stop network-toggle.service

echo "Disable the services"
sudo systemctl disable pairing_ui.service
sudo systemctl disable network-toggle.service

echo "Remove the service files from the systemd directory"
sudo rm /etc/systemd/system/pairing_ui.service
sudo rm /etc/systemd/system/network-toggle.service

echo "Reload systemd to remove the disabled services"
sudo systemctl daemon-reload
sudo systemctl reset-failed

echo "Remove the configured access point"
sudo nmcli con delete $SSID

echo "Uninstallation completed."
