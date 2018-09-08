import downloader
from marketvalue import marketvalue

def update_auctions(cursor, auctions_url):
    #downloader.download_auctions(auctions_url, "auctions.json")
    print("Downloaded the auctions")
    auctions = downloader.load_auctions("auctions.json")
    print("Loaded the auctions")

    bigQuery = "INSERT INTO auctions (auc, item, owner, buyout, quantity) VALUES "
    for i in range(0, len(auctions)):
        auc = auctions[i]
        bigQuery += "({}, {} , \"{}\", {}, {}), ".format(auc["auc"], auc["item"], auc["owner"], auc["buyout"],
                                                         auc["quantity"])

        if i % 2000 == 0:
            cursor.execute(bigQuery[:-2] + ";")
            bigQuery = "INSERT INTO auctions (auc, item, owner, buyout, quantity) VALUES "

    cursor.execute(bigQuery[:-2] + ";")

    # Delete the auctions which are bid only
    cursor.execute("DELETE FROM auctions WHERE buyout=0")


def marketvalue_all(cursor):
    for row in cursor.execute("SELECT count(DISTINCT item) as count FROM auctions"):
        count = row[0]

    items = []
    for row in cursor.execute("SELECT DISTINCT item FROM auctions ORDER BY item ASC"):
        items.append(int(row[0]))

    bigQuery = "INSERT INTO marketvalue (item, marketvalue, quantity) VALUES "
    for i in range(0, len(items)):
        mv = marketvalue(items[i], cursor, False)

        bigQuery += "({}, {}, {}), ".format(mv["item"], mv["marketvalue"], mv["quantity_sum"])
        if i % 100 == 0:
            cursor.execute(bigQuery[:-2] + ";")
            bigQuery = "INSERT INTO marketvalue (item, marketvalue, quantity) VALUES "
            print("Done {}/{}".format(i, count))

    cursor.execute(bigQuery[:-2] + ";")
    print("Done {}/{}".format(count, count))

