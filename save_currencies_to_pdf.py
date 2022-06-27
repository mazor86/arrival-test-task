import asyncio

from src.request_currency import request_currency
from src.data_processing import create_plot, save_pdf
from src.parse_args import parse_args
from src.utils import args_optimization, get_clean_data
from src.colors import OKCYAN, ENDC

if __name__ == '__main__':
    args = parse_args()
    args['currency_table'] = args_optimization(args)
    raw_data = asyncio.run(request_currency(args))
    clean_data = get_clean_data(raw_data, args['currency_table'])

    data = []
    for key, value in clean_data.items():
        data.append(create_plot(key, value))
    save_pdf(data, args)
    print(f'{OKCYAN}Report created{ENDC}')
