import base64
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, Optional, List
from dataclasses import dataclass
from io import BytesIO
import pdfkit
from jinja2 import Environment, FileSystemLoader
import config


@dataclass
class CurrencyInfo:
    currency: str
    max_cur: float
    min_cur: float
    average_cur: float
    image: str


def create_plot(currency: str, data_raw: Dict) -> Optional[CurrencyInfo]:
    """
    The create_plot function takes a currency and data as arguments.
    It returns an object of type CurrencyInfo, which contains the maximum value of the currency,
    the minimum value of the currency, and a base64-encoded string representation of a plot image.

    :param currency:str: Specify which currency to plot
    :param data:Dict: Store the data that is returned by the api
    :return: The CurrencyInfo dataclass
    """
    img = BytesIO()
    data = list(filter(None, data_raw))
    df = pd.DataFrame(data)
    df.columns = ['date', currency]
    plt.rcParams["figure.autolayout"] = True
    plt.title(f'{currency.title()} from {df.iloc[0][ "date"]} to {df.iloc[-1][ "date"]}')
    plt.plot(df['date'], df[currency], 'bo-')
    plt.xticks(rotation='vertical')
    plt.grid()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return CurrencyInfo(
        currency=currency,
        max_cur=df[currency].max(),
        min_cur=df[currency].min(),
        average_cur=df[currency].mean(),
        image=plot_url
    )


def save_pdf(currency_data: List[Optional[CurrencyInfo]]):
    """
    The save_pdf function saves the currency data to a PDF file.

    :param currency_data:List[Optional[CurrencyInfo]]: Pass the list of currency information to the template
    """
    env = Environment(loader=FileSystemLoader(config.TEMPLATE_DIR))
    template = env.get_template(config.HTML_TEMPLATE)
    context = {
        'currencies_info': currency_data,
        'currency_pairs': config.CURRENCY_PAIRS,
        'from_date': datetime.date.today() - datetime.timedelta(config.PERIOD),
        'today': datetime.date.today()
    }
    all_currencies = "_".join(config.CURRENCY_PAIRS).replace('/', '')
    html_out = template.render(context)
    output_path = f'{all_currencies}_for_{datetime.datetime.now().date()}.pdf'
    pdfkit.from_string(html_out, output_path=output_path)
