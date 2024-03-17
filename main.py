from config import config
from src.Dbmanager import DBManager
from src.Hh_API import HeadHunterData


def main():
    while True:
        hh_data = HeadHunterData()
        hh_data.get_employers()
        hh_data.get_sort_emp()
        hh_data.get_vacancies_from_employer()
        hh_data.get_sort_vacancies()

        params = config()
        dbmanager = DBManager(params)
        dbmanager.create_connection('postgres')
        dbmanager.create_database('HeadHunter')

        dbmanager.create_tables()
        dbmanager.insert_data(hh_data.get_sort_vacancies(), hh_data.get_sort_emp())
        get_comp = dbmanager.get_companies_and_vacancies_count()
        all_vac = dbmanager.get_all_vacancies()
        avg_salary = dbmanager.get_avg_salary()
        higher_salary = dbmanager.get_vacancies_with_higher_salary()

        print('Привет! Для дальнейшей работы выберите одно из действий:\n'
              '1. Получить список всех компаний и количество вакансий.\n'
              '2. Получить список всех вакансий с указанием названия компании,'
              'названия вакансии, зарплаты и ссылки на вакансию.\n'
              '3. Получить среднюю зарплату по вакансиям.\n'
              '4. Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.\n'
              '5. Получает список всех вакансий по ключевому слову.')

        user_input = input('Введите число: ')

        if user_input == '1':
            for emp in get_comp:
                print(f'Название компании: {emp[0]}\n',
                      f'Количество вакансий: {emp[1]}\n')
            continue

        elif user_input == '2':
            for vac in all_vac:
                print(f'Название компании: {vac[0]}\n'
                      f'Название вакансии: {vac[1]}\n'
                      f'З/п от: {vac[2]}\n'
                      f'З/п до: {vac[3]}\n'
                      f'Ссылка на вакансию: {vac[4]}\n')
            continue

        elif user_input == '3':
            print(f'Средняя з/п по всем вакансиям: {avg_salary}')
            continue

        elif user_input == '4':
            for high in higher_salary:
                print(f'Название компании: {high[0]}\n'
                      f'Название вакансии: {high[1]}\n'
                      f'З/п от: {high[2]}\n'
                      f'З/п до: {high[3]}\n'
                      f'Ссылка на вакансию: {high[4]}\n')
            continue

        elif user_input == '5':
            user_keyword = input('Введите ключевое слово: ')
            kw_vacs = dbmanager.get_vacancies_with_keyword(user_keyword)
            for word in kw_vacs:
                print(f'Название компании: {word[0]}\n'
                      f'Название вакансии: {word[1]}\n'
                      f'З/п от: {word[2]}\n'
                      f'З/п до: {word[3]}\n'
                      f'Ссылка на вакансию: {word[4]}\n')
            continue

        else:
            print('Вы ввели не верные данные\n'
                  'Хотите продолжить работу с программой? (д/н)')

            user_int = input()

            if user_int == 'д':
                continue
            else:
                break


if __name__ == '__main__':
    main()
