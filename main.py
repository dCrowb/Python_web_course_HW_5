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


async def build_response(data):
    exchange_rate = data.get('exchangeRate')
    tmp_dict = {}
    response = {}
    for rate in exchange_rate:
        if rate.get('currency') in currency_list:
            tmp_dict.update({rate.get('currency'):{
                'sale': rate.get('saleRate'),
                'purchase': rate.get('purchaseRate')
            }
                             })
        response.update({data.get('date'): tmp_dict})    
    return response



async def get_currency_data():
        exchange_data_list = []
        async with aiohttp.ClientSession() as session:
            try:
                for date in list_date:
                    async with session.get(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}') as response:
                        result = await response.json()
                        result = await build_response(result)
                        exchange_data_list.append(result)
            except aiohttp.ClientConnectorError as err:
                print(f'Connection error: https://api.privatbank.ua/p24api/exchange_rates?json&date={date}', str(err))
        return exchange_data_list
            

async def get_exchange():
    result = await get_currency_data()
    print(result)
    return result

def parser(command: str):
    parser = argparse.ArgumentParser(prog='ExchangeRate', description='Exchange rate')
    parser.add_argument('-d', dest='days', type=int, help='number days')
    parser.add_argument('-c', dest='currency', help='currency')
    args = parser.parse_args()
    return args

  
if __name__ == '__main__':
    root_command, *command = argv
    full_command = ''

    for el in command:
        full_command = full_command.join(el + ' ')
    arguments = parser(full_command)

    if not arguments.currency:
        currency_list = ['EUR', 'USD']
    else:
        currency_list = arguments.currency

    list_date = date_list(arguments.days)
    if arguments.days in range(11):
        asyncio.run(get_exchange())
    else:
        print('-d must be from 1 to 10')