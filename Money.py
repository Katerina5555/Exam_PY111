import random
from typing import Union
import requests
import json


class Money:
    wallet = []

    def __init__(self, name: Union[str, None], sum_of_money: float):
        self.name = name
        self.sum_of_money = sum_of_money
        Money.wallet.append(self)

        if self.sum_of_money < 0:
            raise ValueError("сумма не может быть отрицательной")

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, ' \
               f'{self.__class__.__name__}({self.sum_of_money})'

    def __str__(self):
        return f'{self.__class__.__name__}({self.sum_of_money}) ' \
               f'{self.__class__.__name__}({self.name} '

    @classmethod
    def __getitem__(cls):
        print(cls.wallet)

    def convert_to_valute(self):
        """
        Метод для конвертации валюты
        :return:
        - уточняет наличие возможности загрузки данных;
        - выводит время последней загрузки;
        - проверяет валюту конвертации;
        - конвертирует;
        - переносит переконвертированную валюту в нужный класс (НЕ ГОТОВО)
        """

        answer = input("Есть возможность загрузить файл с сайта ЦБ РФ?")

        if answer == "Да" or answer == "да":
            url = "https://www.cbr-xml-daily.ru/daily_json.js"
            price = requests.get(url, allow_redirects=True)
            open("CBR.json", 'wb').write(price.content)

        dict_ = json.load(open("CBR.json"))
        # print(dict.items(dict_['Valute']['USD']))
        print("Время последнего обновления файла в источнике: "
              + dict_["Date"])
        valute_name = str(input("Введите валюту в которую хотите "
                            "конвертировать (международное обозначение): "
                                  "")).upper()
        if valute_name != "RUB":
            exchange_rate = dict_['Valute'][valute_name]['Value']
            # print(b)

            if self.name != "RUB":
                exchange_rate_to_rub = dict_['Valute'][self.name]['Value']
                # print(exchange_rate_to_rub)
                if self.name != valute_name:
                    value_in_rub = self.sum_of_money * exchange_rate_to_rub
                    print(f'После конвертации сумма {self.sum_of_money} {self.name} составила '
                          f'{round((value_in_rub / exchange_rate), 2)} {valute_name}')
                else:
                    print(f"Операция не проведена. Вы пытаетесь конвертировать {self.name} в {self.name}")
            else:
                print(f'После конвертации сумма {self.sum_of_money} {self.name} составила '
                      f'{round((self.sum_of_money / exchange_rate), 2)} {valute_name}')
        else:
            if self.name != "RUB":
                exchange_rate_to_rub = dict_['Valute'][self.name]['Value']
                value_in_rub = self.sum_of_money * exchange_rate_to_rub
                print(f'После конвертации сумма {self.sum_of_money} {self.name} составила '
                      f'{round(value_in_rub, 2)} {valute_name}')
            else:
                print(f"Операция не проведена. Вы пытаетесь конвертировать {self.name} в {self.name}")

    # def sum_of_class(self):



class Rubles(Money):
    def __init__(self, name: Union[str, None], sum_of_money: float):
        self._name = name
        self.sum_of_money = sum_of_money
        super().__init__("RUB", sum_of_money)


class Euro(Money):
    def __init__(self, name: Union[str, None], sum_of_money: float):
        self._name = name
        self.sum_of_money = sum_of_money
        super().__init__("EUR", sum_of_money)

class Dollar(Money):
    def __init__(self, name: Union[str, None], sum_of_money: float):
        self._name = name
        self.sum_of_money = sum_of_money
        super().__init__("USD", sum_of_money)


if __name__ == '__main__':
    euro_1 = Euro('EUR', 5)
    euro_2 = Euro('EUR', 20)

    rubles_1 = Rubles('RUB', 100)
    rubles_2 = Rubles('RUB', 5000)

    Money.convert_to_valute(euro_2)
    print("В кошельке: ")
    Money.__getitem__()


