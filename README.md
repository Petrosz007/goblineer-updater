# Goblineer updater

Goblineer updater calculates the marketvalue of all items currently on the auctionhouse and outputs it into a `.json` file. That file can be used for anything, but is required for the [Goblineer Addon](https://github.com/Petrosz007/goblineer-addon), [Goblineer Assistant](https://github.com/Petrosz007/goblineer-assistant), and [Quick Price Search](https://github.com/Petrosz007/goblineer-search)

## Setup
Open the `config_sample.json` and fill it in with your information. Rename it to `config.json`.
You can get your [Battle.net API key here](https://dev.battle.net/apps/mykeys).

Make sure that the `install_location` doesn't have any `\ \` characters. Replace all of the `\ \` with `/`

If you don't use the compiled .exe verion, you will need to install some version of [Python 3](https://www.python.org/downloads/).


## Usage
Run the `main.exe` file after creating the `config.json` file.

If you don't use the .exe use the `update.bat` file, it will run `main.py`.
Running `main.py` will run every calculation and in the end it will create the `mv_names.json` file.

### Using another locale: 
If you want to use another locale, not en_GB, change the locale setting in `config.json`. All item names are saved to the `items.json` file, so if you want to use another language **delete this file** so the languages won't mix. The program will download all the necessary items names from the new locale when you next run it, but it will take some time, it has to download 10 000+ item's data.

### Forcing an update:
If you want to run the program, but "It already has the latest data." open the config.json file and set `last_updated` to 0.
