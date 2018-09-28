import downloader
from marketvalue import marketvalue
from collections import defaultdict
import ast

def update_auctions(auctions_url):
    downloader.download_auctions(auctions_url, "auctions.json")
    print("Downloaded the auctions")
    auctions = downloader.load_auctions("auctions.json")
    print("Loaded the auctions")

    auctions_dict = defaultdict(list)
    for auc in auctions:
        if not auc["buyout"] == 0:
            unit_price = (auc["buyout"] / auc["quantity"]) / 10000

            dict_key = [str(auc["item"])]
            if("bonusLists" in auc):
                for bonus_id in auc["bonusLists"]:
                    dict_key.append(str(bonus_id["bonusListId"]))

            for i in range(0, auc["quantity"]):
                auctions_dict[repr(dict_key)].append(unit_price)

    return auctions_dict


def marketvalue_all(auctions_dict, region, api_key, locale):
    items = list()
    for i in auctions_dict.keys():
        items.append(i)

    count = len(items)
    marketvalues = []
    for i in range(0, len(items)):
        mv = marketvalue(ast.literal_eval(items[i]), auctions_dict[items[i]])
        marketvalues.append(mv)
        print("Done {} / {}".format(i, count))

    return marketvalues

def get_item_names(items, region, api_key, locale):
    print("Getting the name of items.")
    # The dict will be used in marketvalue_all() and the list will be written to the json file
    item_names_dict = {}
    item_names_list = []

    saved_items = downloader.load_items("items.json")
    if not len(saved_items) == 0:
        item_names_list = saved_items
        for element in item_names_list:
            item_names_dict[str(element["item"])] = element["name"]

    count = len(items)
    for i in range(0, count):
        item = items[i]

        if not str(item) in item_names_dict:
            name = downloader.get_item_name(item, region, api_key, locale)
            item_names_dict[str(item)] = name
            item_names_list.append({"item": str(item), "name": name})

            print("Name {} / {} complete.".format(i, count))

    downloader.write_items("items.json", item_names_list)
    print("Finished updating the names.")

    return item_names_dict
