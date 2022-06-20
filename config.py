import os

URL_TEMPLATE = 'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/{date}/currencies/{from_currency}/{' \
               'to_currency}.min.json'
CURRENCY_PAIRS = ('usd/rub', 'gel/rub')
PERIOD = 30
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(ROOT_DIR, 'templates')
HTML_TEMPLATE = 'currencies.html'
