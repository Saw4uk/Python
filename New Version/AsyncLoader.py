from multiprocessing import Pool
import concurrent.futures as pool
from One_Year_Statistics import OneYearStatistics
from FileSplitter import Splitter
from All_Years_Statistics import AllYearsStatistics
import os

class AsyncLoader:
    @staticmethod
    def SplitFile(file_name):
        Splitter.splitCSV(file_name)

    @staticmethod
    def GetStatistics(full_file_name, vacancy_name):
        directoryList = os.listdir(f'SplittedFile/{full_file_name[:-4]}')
        array_to_async = []
        for dirname in directoryList:
            array_to_async.append((f'SplittedFile/{full_file_name[:-4]}/{dirname}',vacancy_name))
        with Pool(6) as p:
            statistics_for_years_array = p.map(OneYearStatistics.read_file, array_to_async)
       #with pool.ThreadPoolExecutor(max_workers=3) as executer:
       #    statistics_for_years_array = executer.map(OneYearStatistics.read_file, array_to_async)
        AllYearsStatistics.MergeStatistics(statistics_for_years_array, full_file_name)