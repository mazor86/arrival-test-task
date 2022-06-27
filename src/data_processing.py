import base64
import datetime
import os.path
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass
from io import BytesIO
import pdfkit
from jinja2 import Environment, FileSystemLoader

from src import settings


@dataclass
class CurrencyInfo:
    currency: str
    max_cur: float
    min_cur: float
    average_cur: float
    image: str


def create_plot(currency_pair: Tuple, data: List) -> Optional[CurrencyInfo]:
    """
    The create_plot function takes a currency and data as arguments.
    It returns an object of type CurrencyInfo, which contains the maximum value of the currency,
    the minimum value of the currency, and a base64-encoded string representation of a plot image.

    :param currency_pair:str: Specify which currency to plot
    :param data:Dict: Store the data that is returned by the api
    :return: The CurrencyInfo dataclass
    """
    img = BytesIO()
    if not data:
        return None
    df = pd.DataFrame(data).sort_values(by='date')
    plt.rcParams["figure.autolayout"] = True
    plt.title(f'{"/".join(currency_pair)} from {df.iloc[0]["date"]} to {df.iloc[-1]["date"]}')
    plt.plot(df['date'], df['value'], 'bo-')
    plt.xticks(rotation='vertical')
    plt.grid()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return CurrencyInfo(
        currency='/'.join(currency_pair),
        max_cur=df['value'].max(),
        min_cur=df['value'].min(),
        average_cur=df['value'].mean(),
        image=plot_url
    )


def save_pdf(currency_data: List[Optional[CurrencyInfo]], args: Dict):
    """
    The save_pdf function saves the currency data to a PDF file.

    :param currency_data:List[Optional[CurrencyInfo]]: Pass the currency data to the template
    :param args:Dict: Pass the args parameter
    """
    env = Environment(loader=FileSystemLoader(settings.TEMPLATE_DIR))
    template = env.get_template(settings.HTML_TEMPLATE)

    date_string = args[settings.DATE_PARAMETER_NAME]
    if date_string is None:
        date = datetime.date.today()
    else:
        date = datetime.datetime.strptime(date_string, settings.DATE_FORMAT).date()

    context = {
        'currencies_info': currency_data,
        'currency_pairs': args[settings.CURRENCY_PARAMETER_NAME],
        'from_date': date - datetime.timedelta(args[settings.PERIOD_PARAMETER_NAME]),
        'today': date
    }
    all_currencies = "_".join(args[settings.CURRENCY_PARAMETER_NAME]).replace('/', '')
    html_out = template.render(context)
    output_path = f'{all_currencies}_for_{date}.pdf'
    pdfkit.from_string(
        html_out,
        output_path=os.path.join(settings.BASE_DIR, output_path)
    )
