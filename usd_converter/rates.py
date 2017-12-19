from urllib.request import urlopen
from time import strftime
import json


class Rates():

    def __init__(self):
        """Initialize object and call update_rates method"""
        self.__data = ''
        self.last_updated = ''
        self.exchange_rates = dict()
        self.update_rates()


    def update_rates(self):
        """Call class' private methods to get/update with newest rates"""
        self.__get_exchange_rates()
        self.__parse_name_and_price()
        self.last_updated = strftime('%H:%M:%S %m/%d/%Y')


    def __get_exchange_rates(self):
        """Get current USD exchange rates and fill __data with json string"""
        website = 'https://finance.yahoo.com/webservice/v1/symbols/allcurrencies/quote?format=json'
        with urlopen(website) as response:
            source = response.read().decode('utf-8')
        self.__data = json.loads(source)


    def __parse_name_and_price(self):
        """Parse json string and fill rates dict with names and prices"""
        for item in self.__data['list']['resources']:
            name = item['resource']['fields']['name']
            price = item['resource']['fields']['price']
            if 'USD/' in name:
                self.exchange_rates[name[4:]] = price
            else:
                self.exchange_rates[name] = price

