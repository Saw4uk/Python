from AsyncLoader import AsyncLoader

file_name = "vacancies_by_year.csv"

#Splitter.splitCSV(file_name)

def main():
    print("Code started")
    AsyncLoader.GetStatistics(file_name, "Аналитик")

if __name__ == '__main__':
    main()