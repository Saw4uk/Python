import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import requests


class Valute:
    num_code: int
    char_code: str
    nominal: int
    name: str
    value: float

    def __init__(self, num_code: int, char_code: str, nominal: int, name: str, value: float) -> None:
        self.num_code = num_code
        self.char_code = char_code
        self.nominal = nominal
        self.name = name
        self.value = value

    def ToRub(self):
        return round(self.value / self.nominal, 5)


class CBLoader:

    @staticmethod
    def month_year_iter(start_month, start_year, end_month, end_year):
        ym_start = 12 * start_year + start_month - 1
        ym_end = 12 * end_year + end_month - 1
        for ym in range(ym_start, ym_end):
            y, m = divmod(ym, 12)
            yield m + 1, y

    @staticmethod
    def ResponseParser(xml_string) -> list:
        xml = ET.fromstring(xml_string)
        valutes_array = []
        for first in xml:
            temp = [i.text for i in first]
            valutes_array.append(Valute(int(temp[0]), temp[1], int(temp[2]), temp[3], float(temp[4].replace(',', '.'))))
        return valutes_array

        # parseResponse

    @staticmethod
    def GetValutesDataFrame(last_date, first_date):
        result_dic = {'date' : [], 'USD' : [], 'EUR' : [], 'KZT' : [], 'UAH' : [], 'BYR' : []}
        for month, year in CBLoader.month_year_iter(10, 2003, 8, 2022):
            xml = requests.get(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req=01/{month:02}/{year}&d=0').text
            valutes_array = CBLoader.ResponseParser(xml)
            result_dic['date'].append(f'{year}-{month:02}')
            for valute in valutes_array:
                if valute.char_code not in result_dic.keys(): continue
                result_dic[valute.char_code].append(valute.ToRub())
            for key, value in result_dic.items():
                if not result_dic[key] or len(result_dic[key]) != len(result_dic['date']):
                    result_dic[key].append(np.nan)
        df = pd.DataFrame(result_dic)
        df.to_csv("Currencies.csv", index=False)



CBLoader.GetValutesDataFrame(0, 0)
