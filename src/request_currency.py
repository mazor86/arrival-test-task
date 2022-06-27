import asyncio
import datetime
import aiohttp
from typing import Generator, Dict, List, Optional, Coroutine, Tuple

from src import settings


def last_n_day_range(on_date: datetime.date, n_days: int) -> Generator[datetime.date, None, None]:
    """
    The last_n_day_range function returns a generator that yields the last n days
    from on_date.

    :param on_date:datetime.date: Specify the date that is used to calculate the range
    :param n_days:int: Define the number of days to be included in the range
    :return: A generator object that can be iterated over
    """
    for i in range(n_days):
        yield on_date + datetime.timedelta(i + 1 - n_days)


async def get_currency(
        session: aiohttp.ClientSession,
        url: str
) -> Optional[Dict]:
    """
    The get_currency coroutine accepts a session object and a url string.
    It then makes an HTTP GET request to the specified url, parses the response as JSON,
    and returns it. If there is an error making the request or parsing of the response's data,
    None is returned.

    :param session:aiohttp.ClientSession: Make requests
    :param url:str: Pass the url of the api that we want to get data from
    :return: A dictionary containing the currency data
    """
    async with session.get(url, ssl=False) as response:
        try:
            data = await response.json()
        except aiohttp.ClientError:
            return None
        # add date if a response doesn't contain it
        if 'date' not in data:
            data['date'] = url.split('/')[-3]
        return data


def get_tasks(
        session: aiohttp.ClientSession,
        urls: List[str]
) -> List[Coroutine]:
    """
    The get_tasks function accepts a list of URLs and returns a list of tasks.
    Each task is an async function that will call the get_currency function.

    :param session:aiohttp.ClientSession: Make the http requests
    :param urls:List[str]: Pass a list of urls to the get_tasks function
    :return: A list of coroutines
    """
    tasks = []
    for url in urls:
        task = get_currency(session, url)
        tasks.append(task)

    return tasks


def get_urls(args: Dict) -> List[str]:
    """
    The get_urls function accepts a dictionary of arguments and returns a list of URLs.

    The function accepts the following parameters:

        date - A string representing the date to retrieve rates for, in YYYY-MM-DD format. If not specified, it defaults to today's date.

        period - An integer representing the

    :param args:Dict: Pass in the currency_table
    :return: The list of urls to be downloaded
    """
    urls = []
    if args[settings.DATE_PARAMETER_NAME] is not None:
        date = datetime.datetime.strptime(
            args[settings.DATE_PARAMETER_NAME],
            settings.DATE_FORMAT
        )
    else:
        date = datetime.datetime.today()
    for single_date in last_n_day_range(date, args[settings.PERIOD_PARAMETER_NAME]):
        for currency in args['currency_table']:
            url = settings.URL_TEMPLATE.format(
                date=single_date.strftime("%Y-%m-%d"),
                from_currency=currency
            )
            urls.append(url)
    return urls


async def request_currency(args: Dict) -> Tuple:
    """
    The request_currency function accepts a dictionary of arguments and returns a list of dictionaries.
    The request_currency function accepts the following parameters:
        args - A dictionary containing the following keys:
            currency - The name of the ocurrency to retrieve data for (e.g., 'USD')
            start_date - The date
            period - Number of days for a report

    :param args:Dict: Pass in the arguments that are passed into the function
    :return: A list of dictionaries, one for each request
    """
    async with aiohttp.ClientSession() as session:
        urls = get_urls(args)
        tasks = get_tasks(session, urls)
        data = await asyncio.gather(*tasks)
    return data
