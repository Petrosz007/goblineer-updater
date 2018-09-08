import urllib.request, json, ijson
import requests


def get_latest_data(region, realm, api_key):
    url = "https://" + region + ".api.battle.net/wow/auction/data/" + realm + "?locale=en_GB&apikey=" + api_key
    response = urllib.request.urlopen(url)
    data = json.load(response)

    return data["files"][0]


def get_auctions(url):
    f = urllib.request.urlopen(url)
    objects = ijson.items(f, 'auctions.item')
    return objects


def download_auctions(url, file_name):
    response = requests.get(url, stream=True)
    handle = open(file_name, "wb")
    for chunk in response.iter_content(chunk_size=512):
        if chunk:  # filter out keep-alive new chunks
            handle.write(chunk)


def load_auctions(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data["auctions"]
