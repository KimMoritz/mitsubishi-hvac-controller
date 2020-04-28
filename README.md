# mitsubishi-hvac-controller

## Description
This project is for controlling ir-controlled Mitsubishi heat pumps over WiFi or the Internet. It is easily set up and operated for anyone with a raspberry pi and a few cheap electronics components (schematic in progress). The app runs a Flask web server which controls the infrared diode connected to the Raspberry Pi. You create user accounts with credentials and permissions to access settings. User data and settings are stored in an embedded SQLite database via SQLAlchemy and passwords are hashed.

## Usage
To use, just clone the repo to your Raspberry Pi running Raspbian with Python 3.7+, set up the ir components according to the schematic (in progress), install the dependencies in the requirements file and run the run.py file. Make sure port 5000 is open and navigate to the local ip address (port 5000) of your Raspberry Pi to get started. By default, the admin login is admin@admin.com and password is admin. Change this upon first login via "Reset password" and create a new user via "Register user".
