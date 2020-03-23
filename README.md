# mitsubishi-hvac-controller

This project is for controlling ir-controlled Mitsubishi heat pumps over WiFi or the Internet. It is easily set up and operated for anyone with a raspberry pi and a few cheap electronics components (schematic in progress).

The app runs a Flask web server which controls the infrared diode connected to the Raspberry Pi. You create user accounts with credentials and permissions to access settings. User data and settings are stored in an embedded SQLite database and passwords are hashed.

To use, just clone the repo, set up the ir components, install the dependencies in the requirements file and run the web server.
