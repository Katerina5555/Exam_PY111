import random
from typing import Union
import requests
import json


class Money:
    wallet = []

    def __init__(self, name: Union[str, None], sum_of_money: float):
        """
        :param name: международное обозначение валюты
        :param sum_of_money: сумма
        """
        self.name = name
        self.sum_of_money = sum_of_money
        Money.wallet.append(self)

        if self.sum_of_money < 0:
            raise ValueError("сумма не может быть отрицательной")

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, {self.sum_of_money})'

    def __str__(self):
        return f'{self.sum_of_money} {self.name}'

    @classmethod
    def __getitem__(cls):
        print(cls.wallet)

    def convert_to_valute(self, valute_name: str):

        """
        Метод для конвертации валюты
        :return:
        - уточняет наличие возможности загрузки данных;
        - выводит время последней загрузки;
        - проверяет валюту конвертации;
        - конвертирует;
        """

        answer = input("Есть возможность загрузить файл с сайта ЦБ РФ?").upper()

        if answer == "Да":
            url = "https://www.cbr-xml-daily.ru/daily_json.js"
            price = requests.get(url, allow_redirects=True)
            open("CBR.json", 'wb').write(price.content)

        dict_ = json.load(open("CBR.json"))
        print("Время последнего обновления файла в источнике: "
              + dict_["Date"])
        # valute_name = str(input("Введите валюту в которую хотите "
        #                         "конвертировать (международное обозначение): "
        #                           "")).upper()    # изменено на прямое определение при вводе метода
        if valute_name != "RUB":
            exchange_rate = dict_['Valute'][valute_name]['Value']

            if self.name != "RUB":
                exchange_rate_to_rub = dict_['Valute'][self.name]['Value']
                if self.name != valute_name:
                    value_in_rub = self.sum_of_money * exchange_rate_to_rub
                    Money.wallet.append((valute_name, round((value_in_rub / exchange_rate), 2)))
                    return f'После конвертации сумма {self.sum_of_money} {self.name} составила ' \
                           f'{round((value_in_rub / exchange_rate), 2)} {valute_name}'
                else:
                    return f"Операция не проведена. Вы пытаетесь конвертировать {self.name} в {self.name}"
            else:
                Money.wallet.append((valute_name, round((self.sum_of_money / exchange_rate), 2)))
                return f'После конвертации сумма {self.sum_of_money} {self.name} составила ' \
                       f'{round((self.sum_of_money / exchange_rate), 2)} {valute_name}'
        else:
            if self.name != "RUB":
                exchange_rate_to_rub = dict_['Valute'][self.name]['Value']
                value_in_rub = self.sum_of_money * exchange_rate_to_rub
                Money.wallet.append((valute_name, round(value_in_rub, 2)))
                return f'После конвертации сумма {self.sum_of_money} {self.name} составила' \
                       f'{round(value_in_rub, 2)} {valute_name}'

            else:
                return f"Операция не проведена. Вы пытаетесь конвертировать {self.name} в {self.name}"

    def __add__(self, other: "Money"):
        """
        Сложение экземпляров класса
        :param other: прибавляемый экземпляр. При различии валют,
        производится конвертацию в валюту первого вхождения
        :return: сумму денежных средств, в валюте первого входящего экземпляра
        """
        if self.name != other.name:
            Money.convert_to_valute(other, self.name)
            other.name, other.sum_of_money = Money.wallet[-1]
            Money.wallet.__delitem__(-1)
        return f'{Money(self.name, self.sum_of_money + float(other.sum_of_money))}'

    def __mul__(self, other: Union[int, float]):
        """
        Умножение экземпляра на число
        :param other: множитель, проверка на неотрицательность
        """
        if other < 0:
            raise ValueError("Множитель не может быть меньше нуля")
        return Money(self.name, self.sum_of_money * other)

    def __truediv__(self, other: Union[int, float]):
        """
        Деление экземпляра на число
        :param other: делитель, проверка на положительность
        :return: частное от деления
        """
        if other <= 0:
            raise ValueError("Делитель не может быть меньше или равен нулю")
        return Money(self.name, round((self.sum_of_money / other), 2))

    def __sub__(self, other: "Money"):
        """
        Разница двух экземпляров
        :param other: вычитаемый экземпляр, При различии валют,
        производится конвертацию в валюту первого вхождения
        :return: разница после вычитания в валюте первого элемента
        """
        if self.name != other.name:
            Money.convert_to_valute(other, self.name)
            other.name, other.sum_of_money = Money.wallet[-1]
            Money.wallet.__delitem__(-1)
        return f'{Money(self.name, self.sum_of_money - float(other.sum_of_money))}'

    def __ne__(self, other: "Money"):
        """
        Здесь и ниже 6 операций сравнения
        :param other: экземпляр, с которым сравниваем. При различии валют,
        производится конвертацию в валюту первого вхождения
        :return: Правда или Ложь
        """
        if self.name != other.name:
            Money.convert_to_valute(other, self.name)
            other.name, other.sum_of_money = Money.wallet[-1]
            Money.wallet.__delitem__(-1)
        return self.sum_of_money != other.sum_of_money

    def __eq__(self, other: "Money"):
        if self.name != other.name:
            Money.convert_to_valute(other, self.name)
            other.name, other.sum_of_money = Money.wallet[-1]
            Money.wallet.__delitem__(-1)
        return self.sum_of_money == other.sum_of_money

    def __lt__(self, other: "Money"):
        if self.name != other.name:
            Money.convert_to_valute(other, self.name)
            other.name, other.sum_of_money = Money.wallet[-1]
            Money.wallet.__delitem__(-1)
        return self.sum_of_money < other.sum_of_money

    def __gt__(self, other: "Money"):
        if self.name != other.name:
            Money.convert_to_valute(other, self.name)
            other.name, other.sum_of_money = Money.wallet[-1]
            Money.wallet.__delitem__(-1)
        return self.sum_of_money > other.sum_of_money

    def __le__(self, other: "Money"):
        if self.name != other.name:
            Money.convert_to_valute(other, self.name)
            other.name, other.sum_of_money = Money.wallet[-1]
            Money.wallet.__delitem__(-1)
        return self.sum_of_money <= other.sum_of_money

    def __ge__(self, other: "Money"):
        if self.name != other.name:
            Money.convert_to_valute(other, self.name)
            other.name, other.sum_of_money = Money.wallet[-1]
            Money.wallet.__delitem__(-1)
        return self.sum_of_money >= other.sum_of_money


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
    euro_1 = Money('EUR', 5)
    euro_2 = Money('EUR', 20)

    rubles_1 = Money('RUB', 100)
    rubles_2 = Money('RUB', 5000)

    # print(Money.convert_to_valute(euro_2, "USD"))
    # print("В кошельке: ")
    # Money.__getitem__()
    #
    # print(Money.convert_to_valute(rubles_2, "RUB"))
    # print("В кошельке: ")
    Money.__getitem__()
    print(Euro.__add__(rubles_1, euro_2))
    Money.__getitem__()
    print(Euro.__ne__(euro_2, rubles_2))
    Money.__getitem__()
    # print(Euro.__mul__(euro_1, 2))
    # Money.__getitem__()
    # print(Euro.__truediv__(euro_2, 2))
    # Money.__getitem__()



