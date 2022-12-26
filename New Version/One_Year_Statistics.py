import pandas as pd
import numpy as np

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
        return OneYearStatisticsInfo(middle_salary_by_year,vacancies_amount_by_year,middle_salary_by_year_for_vac,vacancies_amount_by_year_for_vac,
                                     file_name[len(file_name)-8:len(file_name)-4])