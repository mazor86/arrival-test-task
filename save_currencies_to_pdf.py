import asyncio

import config
from request_currency import request_currency

if __name__ == '__main__':
    currencies = asyncio.run(request_currency(config.CURRENCY_PAIRS, config.PERIOD))
