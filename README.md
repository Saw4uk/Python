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

Время с асинхом

![image](https://user-images.githubusercontent.com/87923228/209461285-da1359c0-4e72-4598-a398-14fcf79f72e4.png)

