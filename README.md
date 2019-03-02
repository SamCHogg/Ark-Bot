# Ark-Bot

A Discord Bot for controlling an ARK server.

This was written for the [RWK RP Server](https://warringkingdoms.wixsite.com/thecenter).

### Requirements:
* Python 3.7
* [ARK-Server-Tools](https://github.com/FezVrasta/ark-server-tools)
* [ARK-Tools](https://github.com/Qowyn/ark-tools)
* `screen`

### How to run

* `pip install -r requirements.txt`
* Rename `empty_config.py` to `config.py` and populate the values
* Ensure ARK-Server-Tools is already running
* Place the `ark-tools.jar` in the same directory as ARK-Bot
* Run with `start-ark-bot.sh`. I recommend doing this in a `screen` session.
