from src.class_hh_api import HH_API
from src.class_DBManager import DBManager
from src.utils import load_companies, config
from src.class_vacancy import Vacancy


def main():

    database_name = 'hh_vacancies'
    file_companies_ids = 'data/companies.json'

    # loading companies from file
    companies = load_companies(file_companies_ids)

    # loading parameters database from database.ini
    params = config()

    # create database
    db_manager = DBManager(database_name, params)
    print(f'База SQL {db_manager.name} создана')

    # create api manager
    hh_api = HH_API()

    for company in companies:
        # getting info from company this id
        vacancies_info = hh_api.get_all_vacancies(company['id'])

        # send info about company in database
        db_manager.insert_data_company(vacancies_info[0])

        # creating list of vacancies
        vacancies = []
        for vacancy_info in vacancies_info:
            vacancy = Vacancy.create_vacancy_from_hh(vacancy_info)
            vacancies.append(vacancy)

        # insert vacancies in database
        db_manager.insert_data_vacancy(vacancies)

        print(f"Компания {company['name']} - количество вакансий", len(vacancies_info))
    print('Данные по вакансиям выбранных работодателей добавлены в базу данных SQL')

    # choosing method for working with database
    while True:

        print('''
Добрый день!
Выберите один из пунктов
1 - получить список всех компаний и количество вакансий у каждой компании
2 - получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
3 - получить среднюю зарплату по вакансиям
4 - получить список всех вакансий, у которых зарплата выше средней по всем вакансиям
5 - получить список всех вакансий, в названии которых содержится слово python
0 - выход''')

        user_input = input()
        if user_input == "1":
            db_manager.get_companies_and_vacancies_count()
        elif user_input == "2":
            db_manager.get_all_vacancies()
        elif user_input == "3":
            db_manager.get_avg_salary()
        elif user_input == "4":
            db_manager.get_vacancies_with_higher_salary()
        elif user_input == "5":
            db_manager.get_vacancies_with_keyword('python')
        elif user_input == "0":
            break
        else:
            print('Неверная команда')

if __name__ == "__main__":
    main()
