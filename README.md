# Goblineer updater

Goblineer updater calculates the marketvalue of all items currently on the auctionhouse and outputs it into a `.json` file. That file can be used for anything, but is required for the [Goblineer Addon](https://github.com/Petrosz007/goblineer-addon), [Goblineer Assistant](https://github.com/Petrosz007/goblineer-assistant), and [Quick Price Search](https://github.com/Petrosz007/goblineer-search)

## Setup
Open the `config_sample.json` with a text editor. If you have never edited a .json file before, it is structured like this: `"key": "value"`. You will need to fill out these key-value pairs with your information. Example: If you want to set your realm to EU Ragnaros, change the region line to `"region": "eu",` and the realm line to `"realm": "ragnaros",`


You can get a Blizzard API key from here: https://dev.battle.net/apps/mykeys

The realm names should be changed to slugs, basically all lowercase, space is replaced with a `-` and special characters (`é``á`) are replaced with English characters (`e``a`) and the `'` gets removed. Example: `Pozzo dell'Eternità` becomes `pozzo-delleternita`. 


When you type in your install path replace any `\` characters with `/`.


 After you filled out `config_sample.json` rename in to `config.json`

If you don't use the compiled .exe verion, you will need to install some version of [Python 3](https://www.python.org/downloads/).


## Usage
Run the `main.exe` file after creating the `config.json` file.

`auto-update.bat` will run `main.exe` every 60 second, if you let it run in the background it will always update the addon with the latest data.

If you don't use the .exe use the `update.bat` file, it will run `main.py`.
Running `main.py` will run every calculation and in the end it will create the `mv_names.json` file.


### Forcing an update:
If you want to run the program, but "It already has the latest data." open the config.json file and set `last_updated` to 0.
