from typing import Dict, List
from src import settings


def args_optimization(args: Dict) -> Dict:
    """
    The args_optimization function takes a dictionary of arguments and transform currency list to a dictionary of currency pairs.
    The input is the args parameter, which is the argument list passed to an endpoint function. The result is
    a dictionary where each key represents one currency in the pair, and its value contains all currencies that
    can be traded against it.;

    :param args:Dict: Pass the list of currencies to the function
    """
    currency_table = {}
    currency_list = args[settings.CURRENCY_PARAMETER_NAME]
    for pair in currency_list:
        cur = pair.split('/')
        if cur[0] in currency_table:
            currency_table[cur[0]].append(cur[1])
        else:
            currency_table[cur[0]] = [cur[1]]
    return currency_table


def get_clean_data(data_list: List[Dict], currency_table: Dict) -> Dict:
    """
    The get_clean_data function takes in a list of dictionaries and a dictionary
    of currency pairs. It then creates an empty dictionary with keys that are tuples
    of the currency pair, and values that are lists of dictionaries containing the
    date and value for each exchange rate. The function loops through all items in
    the data

    :param data_list:List[Dict]: Store the data from the api
    :param currency_table:Dict: Store the currency pairs that we want to get data for
    :return: A dictionary with the following keys:
    """
    clean_data = {}
    for from_cur, to_cur in currency_table.items():
        for item in to_cur:
            clean_data[(from_cur, item)] = []

    for data in data_list:
        if data is None:
            continue
        for pair in clean_data:
            if pair[0] in data:
                clean_data[pair].append(
                    {
                        'date': data['date'],
                        'value': data[pair[0]][pair[1]]
                    }
                )
    return clean_data
