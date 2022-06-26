import os

'''
Default values for the request:
CURRENCY_PAIRS - list of currency pairs. Each pair consists of two currencies
separated by "/"-symbol.
For the entire list of possible values, see the link
"https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies.json"

PERIOD - number of days for which data is needed.
DATE - on what date the data is needed. If DATE = None - data on today's date.
'''

CURRENCY_PAIRS = ('usd/rub', 'gel/rub')
PERIOD = 30
DATE = None

# Do not modify unnecessarily!
URL_TEMPLATE = 'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/{date}/currencies/{from_currency}/{' \
               'to_currency}.min.json'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(ROOT_DIR, 'templates')
HTML_TEMPLATE = 'currencies.html'
