import downloader
from marketvalue import marketvalue
from collections import defaultdict

def update_auctions(auctions_url):
    #downloader.download_auctions(auctions_url, "auctions.json")
    print("Downloaded the auctions")
    auctions = downloader.load_auctions("auctions.json")
    print("Loaded the auctions")

    auctions_dict = defaultdict(list)
    for auc in auctions:
        if not auc["buyout"] == 0:
            unit_price = (auc["buyout"] / auc["quantity"]) / 10000
            for i in range(0, auc["quantity"]):
                auctions_dict[auc["item"]].append(unit_price)

    return auctions_dict


def marketvalue_all(auctions_dict):
    items = list()
    for i in auctions_dict.keys():
        items.append(i)

    count = len(items)

    marketvalues = []
    for i in range(0, len(items)):
        mv = marketvalue(items[i], auctions_dict[items[i]])
        marketvalues.append(mv)
        print("Done {}/{}".format(i, count))

    return marketvalues
