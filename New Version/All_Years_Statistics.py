import math
import pandas as pd
from One_Year_Statistics import OneYearStatistics

from One_Year_Statistics import OneYearStatisticsInfo


class AllYearsStatistics:
    @staticmethod
    def sort_dic(dic):
        return dict(sorted(dic.items(), key=lambda item: float(item[1]), reverse=True))

    @staticmethod
    def get_ten_len(dic):
        result = {}
        for x in dic.keys():
            result[x] = dic[x]
            if len(result) == 10:
                return result
        return result

    @staticmethod
    def GetStatisticsByCities(full_file_name):
        full_file = pd.read_csv(full_file_name, delimiter=',')
        full_file = full_file[['name', 'salary_from', 'area_name', 'salary_to', 'salary_currency']]
        full_file = full_file.assign(salary_middle=lambda row: (row.salary_from + row.salary_to) / 2)
        full_file['salary_middle'] = full_file['salary_middle'] * full_file['salary_currency'].apply(
            lambda y: OneYearStatistics.currency_to_rub[y])
        all_towns_array = []
        towns_statistics_salary_dic = {}
        towns_statistics_amount_dic = {}
        groups_by_towns = full_file.groupby('area_name')
        for row in full_file.itertuples():
            if row[3] in all_towns_array:
                continue
            else:
                all_towns_array.append(row[3])
        for town in all_towns_array:
            current_group = groups_by_towns.get_group(town)
            if len(current_group) < len(full_file) / 100:
                continue
            else:
                towns_statistics_salary_dic[town] = math.ceil(current_group['salary_middle'].mean())
                towns_statistics_amount_dic[town] = len(current_group)
        towns_statistics_salary_dic = AllYearsStatistics.get_ten_len(AllYearsStatistics.sort_dic(towns_statistics_salary_dic))
        towns_statistics_amount_dic = AllYearsStatistics.get_ten_len(AllYearsStatistics.sort_dic(towns_statistics_amount_dic))
        return towns_statistics_amount_dic, towns_statistics_salary_dic

    @staticmethod
    def MergeStatistics(array_of_year_stat_objects: [OneYearStatisticsInfo], full_file_name: str):
        towns_statistics_amount_dic, towns_statistics_salary_dic = AllYearsStatistics.GetStatisticsByCities(full_file_name)
        dic_year_amount = {}
        dic_year_salary = {}
        vac_year_amount = {}
        vac_year_salary = {}
        for year_stat_object in array_of_year_stat_objects:
            dic_year_amount[year_stat_object.year] = year_stat_object.vacancies_amount_by_year
            dic_year_salary[year_stat_object.year] = math.ceil(year_stat_object.middle_salary_by_year)
            vac_year_amount[year_stat_object.year] = year_stat_object.vacancies_amount_by_year_for_vac
            vac_year_salary[year_stat_object.year] = math.ceil(year_stat_object.middle_salary_by_year_for_vac)
        print(dic_year_amount)
        print(dic_year_salary)
        print(vac_year_amount)
        print(vac_year_salary)
        print(towns_statistics_salary_dic)
        print(towns_statistics_amount_dic)

