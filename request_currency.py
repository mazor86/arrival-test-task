import asyncio
import datetime

import aiohttp
from typing import Generator, Tuple, Dict, Coroutine, List, Optional
from config import URL_TEMPLATE


def last_n_day_range(current_date: datetime.date, n_days: int) -> Generator[datetime.date, None, None]:
    for i in range(n_days):
        yield current_date + datetime.timedelta(i + 1 - n_days)


async def get_currency_for_date(
        session: aiohttp.ClientSession,
        date: datetime.date,
        currency: str) -> Optional[Dict]:

    url = URL_TEMPLATE.format(
        date=date.strftime("%Y-%m-%d"),
        from_currency=currency[:3],
        to_currency=currency[-3:]
    )
    async with session.get(url, ssl=False) as response:
        try:
            data = await response.json()
        except aiohttp.ClientError:
            return None
        return data


def get_tasks(
        session: aiohttp.ClientSession,
        currency: str,
        period: int
) -> List[Coroutine]:
    tasks = []
    current_date = datetime.date.today()
    for single_date in last_n_day_range(current_date, period):
        tasks.append(get_currency_for_date(session, single_date, currency))
    return tasks


async def request_currency(currencies: Tuple[str], period: int) -> Dict:
    """
    The request_currency function accepts a tuple of currencies and a period,
    and returns the data for each currency in the tuple. The function uses an asyncio
    coroutine to make requests asynchronously.

    :param currencies:Tuple[str]: Specify the currencies that are to be retrieved
    :param period:int: Specify the time period for which to get the currency data
    :return: A dictionary of currency names and their corresponding data
    """
    data = {}
    async with aiohttp.ClientSession() as session:
        for currency in currencies:
            tasks = get_tasks(session, currency, period)
            data[currency] = await asyncio.gather(*tasks)
    return data
