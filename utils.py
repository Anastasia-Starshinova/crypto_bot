import requests
import json
from config import keys


class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionException('Введенные валюты должны быть разными\nПосмотрите ещё раз,'
                                      'какие валюты доступны\n'
                                      '/values')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту "{quote}"\nПосмотрите ещё раз,'
                                      'какие валюты доступны\n'
                                      '/values')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту "{base}"\nПосмотрите ещё раз,'
                                      'какие валюты доступны\n'
                                      '/values')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество "{amount}"\nПосмотрите ещё раз,'
                                      'как нужно вводить данные\n'
                                      '/help')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base
