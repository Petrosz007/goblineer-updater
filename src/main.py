from dotenv import load_dotenv
from os import getenv, path
from tqdm import tqdm
from json import dumps, dump
from marketvalue import marketvalue
from printer import start_process_print, success_process_print
from update import get_oauth_token, get_auction_data_status, get_auction_data, parse_auctions

def main():
    load_dotenv()

    start_process_print("Getting the OAuth token")
    oauth_token = get_oauth_token(getenv('OAUTH_CLIENT'), getenv('OAUTH_SECRET'))
    success_process_print("Getting the OAuth token")

    start_process_print("Getting the Auction House status")
    ah_status = get_auction_data_status(oauth_token, getenv("REGION"), getenv("REALM"), getenv("LOCALE"))
    success_process_print("Getting the Auction House data")

    start_process_print("Getting the Auction House data (may take some time based on your internet speed)")
    auction_data = get_auction_data(ah_status['url'])
    success_process_print("Getting the Auction House data (may take some time based on your internet speed)")

    print("\nParsing the data")
    parsed_auctions = parse_auctions(auction_data)

    print("\nCalculating marketvalues")
    marketvalues = []
    for item_ids, item_data in tqdm(parsed_auctions.items()):
        marketvalue_data = marketvalue(item_data)
        marketvalues.append({
            'item': item_ids[0], 'bonusIds': item_ids[1:], 
            'marketvalue': str(marketvalue_data['marketvalue']), 'quantity': str(marketvalue_data['quantity']), 'MIN': str(marketvalue_data['MIN'])
        })
    print("\n")

    start_process_print("Writing marketvalues to file")
    data_path = path.join(getenv('WOW_DIRECTORY'), '_retail_', 'Interface', 'AddOns', 'Goblineer', 'data.lua')

    with open(data_path, 'w') as f:
        f.write("goblineer_data = [" + dumps(marketvalues, separators=(',',':')) + "]")
    success_process_print("Writing marketvalues to file")


    print('\nDone!')


if __name__ == "__main__":
    main()
    