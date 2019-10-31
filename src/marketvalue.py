import numpy

def marketvalue(prices: dict) -> dict:
    """
    Calculates the marketvalue from the given prices

    Args:
        prices: dict: The prices to calculate from

    Returns:
        dict: The calculated marketvalue of the prices, the quantity of prices and the minimum of the prices

    Raises:
        TypeError: If the provided arguments are of the wrong type
    """

    # Type checking
    if not isinstance(prices, dict):
        raise TypeError

    # Count the total number of items
    count = numpy.sum(list(prices.values()))

    # If there are no items, the marketvalue is 0
    if count == 0:
        return {'marketvalue': 0, 'quantity': 0, 'MIN': 0}
    
    unit_prices = list(prices.keys())
    unit_prices.sort()
    minimum = unit_prices[0]

    # If there is only one price, we can return it
    if len(unit_prices) == 1:
        return {'marketvalue': minimum, 'quantity': count, 'MIN': minimum}

    # The algorithm screws up if the count is <= 3, so if it is we will just take the average
    if count <= 3:
        values = dict_to_list(prices)
        return {'marketvalue': numpy.average(values), 'quantity': count, 'MIN': minimum}

    # Step by step array check
    checked_item_count, current_percentage = [0,0]
    previous_price = minimum
    price_array = []
    for price in unit_prices:
        # If it passed 15% it will start checking if the price has increased by 20% from price to price
        if current_percentage > 0.15:
            if previous_price * 1.20 <= price:
                break

        price_array += dict_to_list({price: prices[price]})
        
        # End of the cycle, increase the count and percentage and store the current val as preious
        checked_item_count += prices[price]
        current_percentage = checked_item_count / count
        previous_price = price

        # Stop at 30% of the data
        if current_percentage > 0.30:
            price_array = price_array[:int(count * 0.30)]
            break

    # Calculate the standard deviation and high/low breakpoints
    deviation = numpy.std(price_array)
    average = numpy.average(price_array)
    breakpoint_low = average - deviation* 1.5
    breakpoint_high = average + deviation* 1.5

    # Throwing out the data outside of the breakpoint scope
    price_array_filtered = list(filter(lambda x: x >= breakpoint_low and x <= breakpoint_high, price_array))

    # Returning the average of the filtered prices
    marketvalue = numpy.average(price_array_filtered)

    return {'marketvalue': marketvalue, 'quantity': count, 'MIN': minimum}



def list_to_dict(l: list) -> dict:
    """
    Creates a dict, which stores the count of each value of the list
    """

    tmp = {}
    for x in set(l):
        tmp[x] = l.count(x)
    
    return tmp

def dict_to_list(d: dict) -> list:
    """
    Creates a list from the dict, which has the values as keys and the number of occurances as values
    """

    tmp = []
    for k, v in d.items():
        tmp.extend(v * [k])

    return tmp