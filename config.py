"""
Default values for the request:
CURRENCY_PAIRS - list of currency pairs. Each pair consists of two currencies
separated by "/"-symbol.
For the entire list of possible values, see the link
"https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies.json"

PERIOD - number of days for which data is needed.
DATE - in format "YYYY-MM-DD" on what date the data is needed. If DATE = None - data on today's date.
"""

CURRENCY_PAIRS = ['usd/rub', 'usd/rub']
PERIOD = 30
DATE = None
