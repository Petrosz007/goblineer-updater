import json


def load():
    with open("config.json", 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data


def write_last_update(last_update):
    with open("config.json", 'r', encoding='utf-8') as f:
        data = json.load(f)

    data["last_updated"] = last_update

    with open('config.json', 'w') as outfile:
        json.dump(data, outfile)