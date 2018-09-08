import downloader, db, config, update, marketvalue

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
auctions_url = latestData["url"]
last_modified = latestData["lastModified"]
print("Got the new data")

# If there is new data it will update
#if not last_modified == last_updated:
config.write_last_update(last_modified)

update.update_auctions(cursor, auctions_url)
update.marketvalue_all(cursor)
#print(marketvalue.marketvalue(1727, cursor))

print("Done!")

# If the data is not new, do nothing
#else:
#    print("Already have the latest data")

conn.close()
