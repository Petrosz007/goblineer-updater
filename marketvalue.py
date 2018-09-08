from decimal import Decimal
from math import ceil
from statistics import stdev


def marketvalue(item, cursor, insert_into_db):
    data = []
    quantity_sum = 0
    for row in cursor.execute("SELECT sum(quantity) as quantity FROM auctions where item=?", [item]):
        quantity_sum = int(row[0])

    if quantity_sum == 0:
        if insert_into_db:
            return 0
        else:
            return {"item": item, "marketvalue": 0, "quantity_sum": 0}

    for row in cursor.execute("""SELECT owner, buyout, quantity, (buyout / quantity) AS unit_price
                                FROM auctions
                                WHERE item=?
                                ORDER BY unit_price ASC""", [item]):

        data.append({"owner": row[0], "buyout": row[1], "quantity": row[2], "unit_price": row[3]})

    if quantity_sum == 1:
        marketvalue = number_format(data[0]["unit_price"])
        if insert_into_db:
            cursor.execute("INSERT INTO marketvalue (item, marketvalue, quantity) VALUES (?, ?, ?)", [item, marketvalue, quantity_sum])
            return marketvalue
        else:
            return {"item": item, "marketvalue": marketvalue, "quantity_sum": quantity_sum}

    # Actually starting the marketvalue calculations
    market_array = []
    market_value_array = []

    # Puts each unit_price into the market_array (if quantity = 100 it will put the unit_price in 100 times)
    for auction in data:
        for i in range(0, auction["quantity"]):
            market_array.append(number_format(auction["unit_price"]))

    market_array_count = len(market_array)

    # After it is through 15% of the auctions, any increase of 20% or more in price from one auction to the next will trigger the algorithm to throw out that auction and any above it. It will consider at most the lowest 30% of the auctions.
    if market_array_count <= 4:
        for i in range(int(ceil(market_array_count * 0.15)), market_array_count + 1):
            if i == market_array_count:
                market_value_array = market_array[0:i + 1]
            elif market_array[i-1] * 1.30 >= market_array[i]:
                market_value_array = market_array[0:i + 1]

    # If the difference between the 15% and 30% value is less than 30% it will not count step by step, it will get the average of the cheapest 30%
    else:
        market_value_array = step_by_step_array_check(0, int(ceil(market_array_count * 0.30)), market_array)

    if len(market_value_array) <= 2:
        marketvalue = float(round(Decimal(sum(market_value_array) / len(market_value_array)), 2))
        if insert_into_db:
            cursor.execute("INSERT INTO marketvalue (item, marketvalue, quantity) VALUES (?, ?, ?)",
                           [item, marketvalue, quantity_sum])
            return marketvalue
        else:
            return {"item": item, "marketvalue": marketvalue, "quantity_sum": quantity_sum}

    # Calculation standard deviations
    standard_deviation = stdev(market_value_array)
    market_value_array_average = sum(market_value_array) / len(market_value_array)
    deviation_break_low = market_value_array_average - standard_deviation * 1.5
    deviation_break_high = market_value_array_average + standard_deviation * 1.5

    # Doesn't add the data to the new list with lower/higher than the average +- standard deviation * 1.5
    if standard_deviation == 0:
        market_value_array_calculated = market_value_array
    else:
        market_value_array_calculated = []
        for mv in market_value_array:
            if not (mv < deviation_break_low) and not (mv > deviation_break_high):
                market_value_array_calculated.append(mv)

    marketvalue = float(round(Decimal(sum(market_value_array_calculated) / len(market_value_array_calculated)), 2))
    if(insert_into_db):
        cursor.execute("INSERT INTO marketvalue (item, marketvalue, quantity) VALUES (?, ?, ?)",
                       [item, marketvalue, quantity_sum])
        return marketvalue
    else:
        return {"item": item, "marketvalue": marketvalue, "quantity_sum": quantity_sum}


def step_by_step_array_check(start, max, market_array):
    marketvalue_array = []

    for i in range(start, max):
        if i == max:
            marketvalue_array = market_array[0:i + 1]
        elif market_array[i] * 1.30 >= market_array[i + 1]:
            marketvalue_array = market_array[0:i + 1]

    if len(marketvalue_array) == 0:
        return market_array[0:max]

    return marketvalue_array


def number_format(num):
    return float(round(Decimal(num / 10000), 2))