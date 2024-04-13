#!/bin/bash

# Variables
hotspot_connection_name="morening"
GPIO_PIN=17  # Change to the actual GPIO pin number

# Function to check internet connectivity
check_internet() {
    ping -c 4 8.8.8.8 > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "Internet is connected."
        return 1
    else
        echo "Internet is not connected."
        return 0
    fi
}

# Function to check GPIO pin status
check_gpio_pin() {
    # Export the GPIO pin
    echo $GPIO_PIN > /sys/class/gpio/export

    # Set the GPIO pin as an input
    echo "in" > /sys/class/gpio/gpio$GPIO_PIN/direction

    button_status=$(cat /sys/class/gpio/gpio$GPIO_PIN/value)
    echo button_status: $button_status
    # Unexport the GPIO pin
    echo $GPIO_PIN > /sys/class/gpio/unexport

}

switch_to_AP() {
    if ! nmcli -t -f GENERAL.STATE connection show $hotspot_connection_name | grep -q "activated"; then
        echo "AP is down, switching to AP..."
        sudo nmcli con up "$hotspot_connection_name"
        sudo systemctl start pairing_ui.service
        sleep 30
    else
        echo "AP is up, no action required."
    fi
}

# Main loop
while true; do
    check_internet
    internet_connected=$?

    if [ $internet_connected -eq 1 ]; then
        # Internet is connected, check GPIO pin
        gpio_status=$(check_gpio_pin)
        if [ "$gpio_status" -eq "1" ]; then
            echo "Waiting for 15 seconds to check pin status again..."
            sleep 15
            gpio_status=$(check_gpio_pin)
            if [ "$gpio_status" -eq "1" ]; then
                echo "Switching to hotspot mode..."
                switch_to_AP
            fi
        fi
    else
        # Internet is not connected, wait for 15 seconds before checking again
        echo "Internet connection lost, waiting for 15 seconds before double checking..."
        sleep 15
        # Double check internet connectivity
        check_internet
        internet_connected=$?
        if [ $internet_connected -ne 1 ]; then
            echo "Switching to hotspot mode due to no internet..."
            # switch_to_AP
        else
            echo "Internet connection restored."
        fi
    fi

    sleep 30 # Check every 30 seconds
done

