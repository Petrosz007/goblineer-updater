import downloader, db, config

# Starting the DB connection
conn = db.db_start()
cursor = conn.cursor()

# Loading the config data
config_data = config.load()
api_key = config_data["api_key"]
region = config_data["region"]
realm = config_data["realm"]
last_updated = config_data["last_updated"]

# Getting the latest data from the Blizzard API
latestData = downloader.get_latest_data(region, realm, api_key)
auctionsUrl = latestData["url"]
last_modified = latestData["lastModified"]
print("Got the new data")

# If there is new data it will update
if not last_modified == last_updated:
    config.write_last_update(last_modified)

    # downloader.download_auctions(auctionsUrl, "auctions.json")
    print("Downloaded the auctions")
    auctions = downloader.load_auctions("auctions.json")
    print("Loaded the auctions")

    bigQuery = "INSERT INTO auctions (auc, item, owner, buyout, quantity) VALUES "
    for i in range(0, len(auctions)):
        auc = auctions[i]
        bigQuery += "({}, {} , \"{}\", {}, {}), ".format(+auc["auc"], auc["item"], auc["owner"], auc["buyout"], auc["quantity"])

        if i % 2000 == 0:
            cursor.execute(bigQuery[:-2] + ";")
            bigQuery = "INSERT INTO auctions (auc, item, owner, buyout, quantity) VALUES "

    cursor.execute(bigQuery[:-2] + ";")

    # Delete the auctions which are bid only
    cursor.execute("DELETE FROM auctions WHERE buyout=0")

    print("Done!")

# If the data is not new, do nothing
else:
    print("Already have the latest data")

conn.close()
