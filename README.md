# Ark-Bot

A Discord bot for controlling an ARK Server using [ark-server-tools](https://github.com/arkmanager/ark-server-tools).

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
