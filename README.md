# Goblineer updater

Goblineer updater calculates the marketvalue of all items currently on the auctionhouse and outputs it to the Goblineer addon's folder. That file can be used for anything, but is required for the [Goblineer Addon](https://github.com/Petrosz007/goblineer-addon), [Goblineer Assistant](https://github.com/Petrosz007/goblineer-assistant), and [Quick Price Search](https://github.com/Petrosz007/goblineer-search)

---

## Installation

The program is written in Python3, you will need to install the latest verion from here: https://www.python.org/downloads/

The program requires some python packages to be installed, you can install them on windows by running the `setup.bat` file or running `pip install -r requirements.txt` in the command line.

---

## Setup

Open `sample.env` with a text editor. If you have never edited a .env file before, it is structured like this: `OPTION=value`. You will need to fill out these option-value pairs with your information. Example: If you want to set your realm to EU Ragnaros, change the region line to `REGION=eu,` and the realm line to `REALM=ragnaros`


You can get a Blizzard API key from here: https://develop.battle.net/
Here is the direct link to the client credential creation: https://develop.battle.net/access/clients/create
You only need to give it a name, click on create. On the Manage client page you will see a Client ID and a Client Secret, you will need to put those into the `.env` file, under OAUTH_CLIENT and OAUTH_SECRET.

The realm names should be changed to slugs, basically all lowercase, space is replaced with a `-` and special characters (`é` `á`) are replaced with English characters (`e` `a`) and the `'` gets removed. Example: `Pozzo dell'Eternità` becomes `pozzo-delleternita`. 

Your WOW_DIRECTORY is where you have your game installed, for example: `C:\Program Files (x86)\World of Warcraft`

### After you filled out `sample.env` rename in to `.env`

Example `.env` file:
```
OAUTH_CLIENT=<client id>
OAUTH_SECRET=<client secret>
REGION=eu
REALM=ragnaros
LOCALE=en_GB
WOW_DIRECTORY=E:\World of Warcraft
```
---

## Usage
Run the `goblineer-updater.py` file after creating the `.env` file. You can do that by double clicking it on windows (if .py files are run by the python interpreter you just installed) or opening a command line and running `python goblineer-updater.py`

If you have Python 2.x installed on your computer, run it with `python3 goblineer-updater.py`

Running the program will create a `data.lua` file in the Goblineer addon's folder in your World of Warcraft installation folder, in the path `World_of_Warcraft/_retail_/Interface/Addons/Goblineer/data.lua`

---

## Debugging
If the program closes instantly and you can't see the error message, on windows press Shift + Right Click in the program's directory and select Open Powershell window here and run `python goblineer-updater.py` In this window you can see what the error is, when you open an Issue on github, please include this error message aswell.
