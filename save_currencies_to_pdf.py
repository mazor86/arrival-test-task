import asyncio

import config
from request_currency import request_currency
from data_processing import create_plot, save_pdf

if __name__ == '__main__':
    currencies = asyncio.run(request_currency(config.CURRENCY_PAIRS, config.PERIOD))
    data = []
    for key, value in currencies.items():
        data.append(create_plot(key, value))
    save_pdf(data)
