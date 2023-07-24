import argparse
from sys import argv
import aiohttp
import asyncio
import datetime


def date_list(days: int):
    count = 0
    current_date = datetime.date.today()
    list_date = []
    while count != days:
        previous_date = current_date -datetime.timedelta(days=count)
        if count == 0:
            list_date.append(current_date.strftime('%d.%m.%Y'))
        else:
            list_date.append(previous_date.strftime('%d.%m.%Y'))
        count += 1
    return list_date


async def get_currence_data(date: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.privatbank.ua/p24api/exchange_rates?date={date}') as response:
            result = await response.json()
            return result

def parser(command: str):
    parser = argparse.ArgumentParser(prog='ExchangeRate', description='Exchange rate')
    parser.add_argument('-d', dest='days', type=int, help='number days')
    parser.add_argument('-c', help='currence')
    args = parser.parse_args()
    return args


def controller(command: list):
    full_command = ''
    for el in command:
        full_command = full_command.join(el + ' ')
    arguments = parser(full_command)
    if arguments.days in range(11):
        list_date = date_list(arguments.days)
        for date in list_date:
            response = asyncio.run(get_currence_data(date))
            print(response.get('exchangeRate'))

    

if __name__ == '__main__':
    root_command, *command = argv
    controller(command)