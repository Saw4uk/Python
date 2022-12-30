# Python
## Задание с тестами

Тесты на Salary

![image](https://user-images.githubusercontent.com/87923228/206996286-51ac22b2-0aa3-4022-b998-0f7b8759af79.png)

# Задание на профилирование

Все пропрофилировал
![image](https://user-images.githubusercontent.com/87923228/206998264-e66afb98-6d30-41ff-afa3-c07a49d914b1.png)

# 3.2.1

Код загружен, класс Splitter

![image](https://user-images.githubusercontent.com/87923228/208239070-0874b3e6-c315-469b-b6e4-9c2358ccdfec.png)

Разбивает на файлы по годам

![image](https://user-images.githubusercontent.com/87923228/208239096-e92fdc94-19ea-4ad0-9fb0-5f4dcc1fea46.png)

# 3.2.2

Реализовать асинхронное выполнение кода решил следующим образом. Так как у меня выполнение всех статистических функция начинается сразу после инициализации экземпляра класса Statistics, то я должен создавать экземпляры этих классов в разных потоках. Таким образом был немного изменен код создания экземпляров класса.


```py
    def __init__(self):
        file_name = "vacancies_by_year.csv"  # ("Введите название файла: ")
        vacancy_name = "Аналитик"  # input("Введите название профессии: ")
        directoryList = os.listdir(f'SplittedFile/{file_name[:-4]}')
        array_to_async = []
        x = []
        for dirname in directoryList:
            array_to_async.append((f'{dirname}.csv',vacancy_name))
        with Pool(6) as p:
            x = p.map(StartProgramm.AsyncFunc, array_to_async)
```

Я собираю все разбитые ранее файлы в один список по именам файлов из директории, а затем создаю список параметров для асинхронной функции. После этого я получаю переменную - массив, в которой хранятся все результаты выполненных функций. Далее по программе я вызываю создание экземпляра класса MainStatistics, который собирает все значения в кучу.

```py
class MainStatistics:

    def sum_to_main_town_array_town_amount(self, dic_to_summ):
        for key in dic_to_summ.keys:
            if self.dic_towns_amount[key] is None:
                self.dic_towns_amount[key] = dic_to_summ[key]
                continue
            self.dic_towns_amount[key] += dic_to_summ[key]

    def __init__(self,array_of_stat_objects):
        self.dic_year_salaries = {}
        self.dic_year_amount = {}
        self.dic_towns_amount = {}
        self.dic_towns_salaries = {}
        self.dic_vac_amount = {}
        self.dic_vac_salaries = {}
        for stat in array_of_stat_objects:
            self.sum_to_main_town_array_town_amount(stat.dic_year_amount)
            self.dic_year_salaries[stat.dic_year_salaries.keys[0]] = stat.dic_year_salaries[stat.dic_year_salaries.keys[0]]
            self.dic_year_amount[stat.dic_year_amount.keys[0]] = stat.dic_year_amount[stat.dic_year_amount.keys[0]]
            self.dic_vac_salaries[stat.dic_vac_salaries.keys[0]] = stat.dic_vac_salaries[stat.dic_vac_salaries.keys[0]]
            self.dic_vac_amount[stat.dic_vac_amount.keys[0]] = stat.dic_vac_amount[stat.dic_vac_amount.keys[0]]

        self.print_formatted()
        Report.generate_files(self, array_of_stat_objects[0].vacancy_name)


    def print_formatted(self):
        """Ввыодит результат статистической обработки в отформатированном виде"""
        self.final_year_salar = self.get_format_dic(self.dic_year_salaries, self.dic_year_amount)
        self.final_year_amount = self.dic_year_amount
        print(f"Динамика уровня зарплат по годам: {self.final_year_salar}")
        print(f"Динамика количества вакансий по годам: {self.final_year_amount}")
        self.final_vac_salar = self.get_format_dic(self.dic_vac_salaries, self.dic_vac_amount)
        self.final_vac_amount = self.dic_vac_amount
        print(
            f"Динамика уровня зарплат по годам для выбранной профессии: {self.final_vac_salar}")
        print(f"Динамика количества вакансий по годам для выбранной профессии: {self.final_vac_amount}")
        self.final_town_salar = self.get_ten_len(
            self.sort_dic(self.get_format_dic(self.dic_towns_salaries, self.dic_towns_amount)))
        self.final_town_amount = self.get_ten_len((self.get_parts()))
        print(
            f"Уровень зарплат по городам (в порядке убывания): {self.final_town_salar}")
        print(f"Доля вакансий по городам (в порядке убывания): {self.final_town_amount}")

    def get_format_dic(self, dic, amdic):
        """Форматирует исходный словарь

        :param amdic: Словарь количества вакансий
        :type amdic: dict
        :param dic: Словарь обьема зарплат
        :type dic: dict

        :return: Отформатированный словарь
        """
        resultdic = {}
        for year in dic.keys():
            if amdic[year] == 0:
                resultdic[year] = 0
                return resultdic
            resultdic[year] = int(dic[year] / amdic[year])
        return resultdic

    def get_ten_len(self, dic):
        """Форматирует исходный словарь до длины в 10

        :param dic: Словарь обьема зарплат
        :type dic: dict

        :return: Первые 10 пар словаря
        """
        result = {}
        for x in dic.keys():
            result[x] = dic[x]
            if len(result) == 10:
                return result
        return result

    def get_parts(self):
        """Формирует словарь в 10 частей с долями

        :return: Словарь в 10 частей с долями
        """
        dic_parts = {}
        for town in self.dic_towns_amount.keys():
            to_add = self.dic_towns_amount[town] / self.total_count
            if to_add > 0.01:
                dic_parts[town] = round(to_add, 4)
            else:
                continue
        return self.get_ten_len(self.sort_dic(dic_parts))

    def sort_dic(self, dic):
        """Сортирует словарь по значениям

        :param dic: Словарь обьема зарплат
        :type dic: dict

        :return: Отсортированный словарь
        """
        return dict(sorted(dic.items(), key=lambda item: float(item[1]), reverse=True))
```
Часть функционала обычного класса статистики переехала сюда, так как нам уже не нужна работа с частями массивов, нам нужны только итоговые значения. 
После получения итогового класса MainStatistics, в котором содержится результат обработки всех файлов, программа продолжает работать по тому-же сценарию, что и в случае, если бы работа велась в синхронном режиме.

Время без асинха

![image](https://user-images.githubusercontent.com/87923228/208296844-c94f9df6-1227-41d0-b709-f0e9b5114e88.png)

Время с multiprocessing

![image](https://user-images.githubusercontent.com/87923228/209461697-4192dfaf-4523-43ea-a453-0b0c5bc389cd.png)

# 3.2.3

Время с concurrent futures

![image](https://user-images.githubusercontent.com/87923228/209461659-3d99ca5a-551e-48ac-aeba-db521fa4cf21.png)

# 3.3.1
Код класса подсчета

```py
import pandas as pd
import pprint


class CurrencyCounter:
    @staticmethod
    def GetStatisticsByCities(full_file_name):
        full_file = pd.read_csv(full_file_name, delimiter=',')
        full_file = full_file[['name', 'salary_from', 'area_name', 'salary_to', 'salary_currency']]
        all_currencies_dict = {}
        for row in full_file.itertuples():
            if row[5] not in all_currencies_dict.keys():
                all_currencies_dict[row[5]] = 1
            else:
                all_currencies_dict[row[5]] += 1
        result_array = []
        for currency in all_currencies_dict.items():
            if str(currency[0]) != 'nan' and currency[1] > 5000:
                result_array.append(str(currency[0]))
        print(result_array)
        pprint.pprint(all_currencies_dict, width=1)
```

Вывод подсчета количества вакансий с валютами

![image](https://user-images.githubusercontent.com/87923228/209464331-5513149b-149d-41e3-b726-c3705189c957.png)

Подходящие валюты

![image](https://user-images.githubusercontent.com/87923228/209464527-5bf398ef-c7a5-41a6-9fed-b96ec69b9f4c.png)

Код класса поиска границ отбора валют

```py
    @staticmethod
    def GetFirstAndLastDate(full_file_name):
        full_file = pd.read_csv(full_file_name, delimiter=',')
        full_file = full_file[['published_at']]
        full_file.sort_values(by='published_at',ascending=False)
        first_date = full_file['published_at'].iloc[-1][:7]
        last_date = full_file['published_at'].iloc[0][:7]
        print(full_file)
        print(first_date)
        print(last_date)
```

Даты

![image](https://user-images.githubusercontent.com/87923228/209464967-ae388188-6456-4634-85e6-24b4d5fc4fcd.png)

Выгрузка курсов валют

![image](https://user-images.githubusercontent.com/87923228/209468094-49a424a0-5a67-4519-97e6-31b727ec7fac.png)


Класс загрузки Апи
Новый код с защитой данных и првоеркой валюты
```py
import xml.etree.ElementTree as ET
import pandas as pd
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
                    result_dic[key].append(None)
        df = pd.DataFrame(result_dic)
        df.to_csv("Currencies.csv", index=False)



CBLoader.GetValutesDataFrame(0, 0)
```
# 3.2.2
```py
    @staticmethod
    def read_file(main_tuple):
        def add_middle_salary(row):
            if not pd.isnull(row.salary_from) and not pd.isnull(row.salary_to):
                return (row.salary_from + row.salary_to) / 2
            else:
                if not pd.isnull(row.salary_to):
                    return  row.salary_to
                else:
                    if not pd.isnull(row.salary_from):
                        return row.salary_from
                    else:
                        return np.nan

        def calculate_salary(row):
            try :
                x = row['salary_middle']
                y = row['published_at'][:7]
                z = row['salary_currency']
                if z == 'RUR':
                    v = 1
                else:
                    v = currencies_df.loc[y][z]
                return x * v
            except :
                return np.nan

        file_name, vacancy_name, currencies_df = main_tuple
        readed_csv = pd.read_csv(file_name, delimiter=',')
        salary_table = readed_csv[['name','salary_from','salary_to','salary_currency', 'published_at']]
        
        salary_table['salary_middle'] = salary_table.apply(add_middle_salary, axis = 1)
        salary_table['salary'] = salary_table.apply(calculate_salary, axis = 1)
        salary_table = salary_table.drop(['salary_from', 'salary_to', 'salary_currency', 'salary_middle'], axis=1)[salary_table['salary'].notna()]
        
        only_vac_name_table = salary_table.loc[salary_table['name'].str.contains(vacancy_name)]
        middle_salary_by_year = salary_table['salary'].mean()
        
        vacancies_amount_by_year = len(salary_table['salary'])
        middle_salary_by_year_for_vac = only_vac_name_table['salary'].mean()
        
        vacancies_amount_by_year_for_vac = len(only_vac_name_table['salary'])
        return OneYearStatisticsInfo(
        middle_salary_by_year,
        vacancies_amount_by_year,
        middle_salary_by_year_for_vac,
        vacancies_amount_by_year_for_vac,
        file_name[len(file_name)-8:len(file_name)-4])
```

Первые сто вакансий

![image](https://user-images.githubusercontent.com/87923228/209562610-254661ad-d7b2-4370-a31b-bd43a1e51c6f.png)
# 3.3.3

Код класса выгрузки
```py
class API_loader:
    @staticmethod
    def parse_response(hour):
        def get(dict, key):
            try:
                return dict.get(key)
            except:
                return None
        result_array = []
        for x in range(20):
            for i in range(5):
                res = requests.get(f'https://api.hh.ru/vacancies'
                                   f'?specialization=1'
                                   f'&per_page=100'
                                   f'&page={x}'
                                   f'&date_from=2022-12-26T{hour:02}:00:00'
                                   f'&date_to=2022-12-26T{hour + 1:02}:00:00')
                if res.status_code == 200:
                    print(x)
                    parsedJson = json.loads(res.text)["items"]
                    result_array.append(pd.DataFrame([{'name': get(item, 'name'),
                                          'salary_from': get(get(item, 'salary'), 'from'),
                                          'salary_to': get(get(item, 'salary'), 'to'),
                                          'salary_currency': get(get(item, 'salary'), 'currency'),
                                          'area_name': get(get(item, 'area'), 'name'),
                                          'published_at': get(item, 'published_at')} for item in parsedJson]))
                    break
        return pd.concat(result_array, ignore_index=True)

    @staticmethod
    def Load_API():
        final_dataframe_array = []
        for x in range(0, 23):
            final_dataframe_array.append(API_loader.parse_response(x))
        return pd.concat(final_dataframe_array, ignore_index=True)


API_loader.Load_API().to_csv('API_3_3_3.csv')

```

Выгрузка вакансий за день 
![image](https://user-images.githubusercontent.com/87923228/209676940-6bcd46f8-c788-406b-a126-f09352a8ae83.png)

## 3.4.1 - 3.4.3

Report PDF
![image](https://user-images.githubusercontent.com/87923228/209947494-62018b8a-8539-4b3a-9ce1-9819a28a093c.png)


![image](https://user-images.githubusercontent.com/87923228/209947384-f30ee130-f191-4631-a06a-3ae03a6d4185.png)

![image](https://user-images.githubusercontent.com/87923228/209947401-a6d0e8e9-acc6-4108-8f8c-c629de2d120d.png)

![image](https://user-images.githubusercontent.com/87923228/209947410-0607b269-751e-496b-b728-7331661d4287.png)

![image](https://user-images.githubusercontent.com/87923228/209947368-50ad3bca-671b-4f72-884d-bce3cbbe2621.png)



