from typing import Dict
from src import settings


def args_optimization(args: Dict):
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
    args[settings.CURRENCY_PARAMETER_NAME] = currency_table
