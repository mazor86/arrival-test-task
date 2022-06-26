import argparse
import datetime
import sys

sys.path.append('..')
import config


def currency_checker(pair):
    currencies = pair.split('/')
    if (
            len(currencies) != 2
            or any(cur not in config.POSSIBLE_CURRENCIES for cur in currencies)
    ):
        raise argparse.ArgumentTypeError('Incorrect currency')
    return pair


def period_checker(period):
    try:
        time_period = int(period)
    except ValueError:
        raise argparse.ArgumentTypeError('Period must be positive number not greater than 365')
    if time_period <= 0 or time_period > 365:
        raise argparse.ArgumentTypeError('Period must be positive number not greater than 365')
    return time_period


def date_checker(date_string):
    try:
        date = datetime.datetime.strptime(date_string, config.DATE_FORMAT)
    except ValueError:
        raise argparse.ArgumentTypeError('Wrong date format')
    if date > datetime.datetime.now():
        raise argparse.ArgumentTypeError('The specified date is longer than the current one')
    # Double conversion is used to avoid 1-digit day/month error like 2020-2-1 instead 2020-02-01
    return date.strftime(config.DATE_FORMAT)


def parse_args():
    parser = argparse.ArgumentParser(
        description='''
        This script requests exchange rates on the date from API(https://github.com/fawazahmed0/currency-api)
        for the specified period and saves it to pdf.
        '''
    )
    parser.add_argument(
        '-c', '--currencies',
        type=currency_checker,
        nargs='+',
        default=config.CURRENCY_PAIRS,
        help='currency pairs for the report, format of pair "cur1/cur2"'
    )
    parser.add_argument(
        '-p', '--period',
        type=period_checker,
        default=config.PERIOD,
        help='number of days for the report'
    )
    parser.add_argument(
        '-d', '--date',
        type=date_checker,
        default=config.DATE,
        help='date of the report'
    )
    args = parser.parse_args()
    return vars(args)
