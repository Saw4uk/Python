import pandas as pd

class OneYearStatisticsInfo:
    def __init__(self,middle_salary_by_year,vacancies_amount_by_year,middle_salary_by_year_for_vac,vacancies_amount_by_year_for_vac, year):
        self.middle_salary_by_year = middle_salary_by_year
        self.vacancies_amount_by_year = vacancies_amount_by_year
        self.middle_salary_by_year_for_vac = middle_salary_by_year_for_vac
        self.vacancies_amount_by_year_for_vac = vacancies_amount_by_year_for_vac
        self.year = year


class OneYearStatistics:
    currency_to_rub = {
            "AZN": 35.68,
            "BYR": 23.91,
            "EUR": 59.90,
            "GEL": 21.74,
            "KGS": 0.76,
            "KZT": 0.13,
            "RUR": 1,
            "UAH": 1.64,
            "USD": 60.66,
            "UZS": 0.0055
    }

    @staticmethod
    def read_file(main_tuple):
        file_name, vacancy_name = main_tuple
        readed_csv = pd.read_csv(f'{file_name}', delimiter=',')
        salary_table = readed_csv[['name','salary_from','salary_to','salary_currency']]
        salary_table = salary_table.assign(salary_middle=lambda row: (row.salary_from + row.salary_to)/2)
        salary_table['salary_middle'] = salary_table['salary_middle'] * salary_table['salary_currency'].apply(lambda y: OneYearStatistics.currency_to_rub[y])
        only_vac_name_table = salary_table.loc[salary_table['name'].str.contains(vacancy_name)]
        middle_salary_by_year = salary_table['salary_middle'].mean()
        vacancies_amount_by_year = len(salary_table['salary_middle'])
        middle_salary_by_year_for_vac = only_vac_name_table['salary_middle'].mean()
        vacancies_amount_by_year_for_vac = len(only_vac_name_table['salary_middle'])
        return OneYearStatisticsInfo(middle_salary_by_year,vacancies_amount_by_year,middle_salary_by_year_for_vac,vacancies_amount_by_year_for_vac,
                                     file_name[len(file_name)-8:len(file_name)-4])