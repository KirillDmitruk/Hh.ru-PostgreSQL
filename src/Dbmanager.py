import psycopg2

from config import config
from src.Hh_API import HeadHunterData


class DBManager:

    def __init__(self, params):
        self.params = params

    def create_connection(self, db_name: str):
        """Создаем соединение с БД."""
        self.conn = psycopg2.connect(dbname=db_name, **self.params)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def close_connection(self):
        """Закрытие соединения с БД."""
        self.cur.close()
        self.conn.close()

    def create_database(self, db_name: str):
        """Создание БД."""
        try:
            self.cur.execute(f"CREATE DATABASE {db_name}")
        except psycopg2.errors.DuplicateDatabase:
            self.cur.execute(f"DROP DATABASE {db_name}")
            self.cur.execute(f"CREATE DATABASE {db_name}")

        return 'База данных создана.'

    def create_tables(self):
        """Создание таблиц."""
        try:
            self.cur.execute("""
                CREATE TABLE vacancies 
                (
                    vacancy_id int,
                    vacancy_name varchar(100) NOT NULL,
                    employer_name varchar(100) NOT NULL,
                    employer_id varchar(100) NOT NULL,
                    area varchar(100) NOT NULL,
                    salary_from integer,
                    salary_to integer,
                    employer_url varchar(100) NOT NULL,
                    vacancy_url varchar(100) NOT NULL
                )
            """)

        except psycopg2.errors.DuplicateTable:
            self.cur.execute(f"DROP TABLE vacancies")
            self.cur.execute("""
                CREATE TABLE vacancies 
                (
                    vacancy_id int,
                    vacancy_name varchar(100) NOT NULL,
                    employer_name varchar(100) NOT NULL,
                    employer_id varchar(100) NOT NULL,
                    area varchar(100) NOT NULL,
                    salary_from integer,
                    salary_to integer,
                    employer_url varchar(100) NOT NULL,
                    vacancy_url varchar(100) NOT NULL
                )
            """)
        try:
            self.cur.execute("""
                CREATE TABLE employers 
                (
                    employer_id int PRIMARY KEY,
                    employer_name varchar(255) NOT NULL,
                    employer_url varchar(255) NOT NULL,
                    open_vacancies integer
                )
            """)
        except psycopg2.errors.DuplicateTable:
            self.cur.execute(f"DROP TABLE employers")
            self.cur.execute("""
                CREATE TABLE employers 
                (
                    employer_id int PRIMARY KEY,
                    employer_name varchar(255) NOT NULL,
                    employer_url varchar(255) NOT NULL,
                    open_vacancies integer
                )
            """)

        return 'Таблицы созданы.'

    def insert_data(self, vac_data, emp_data):
        """Заполнение БД данными."""

        for vac in vac_data:
            self.cur.execute("""
                INSERT INTO vacancies (vacancy_id, vacancy_name, employer_name, employer_id,
                area, salary_from, salary_to, employer_url, vacancy_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                             (vac['id'], vac['name_vac'], vac['employer_name'], vac['employer_id'],
                              vac['area'], vac['salary_from'], vac['salary_to'], vac['employer_url'],
                              vac['vacancy_url'])
                             )

        for emp in emp_data:
            self.cur.execute("""
                INSERT INTO employers (employer_id, employer_name, employer_url, open_vacancies)
                VALUES (%s, %s, %s, %s)
                """,
                             (emp['id'], emp['name'], emp['url'], emp['open_vacancies'])
                             )

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        self.cur.execute("""
            SELECT employer_name, open_vacancies FROM employers
            ORDER BY open_vacancies DESC
            """)
        companies = self.cur.fetchall()

        return companies

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
           названия вакансии, зарплаты и ссылки на вакансию."""
        self.cur.execute("""
            SELECT  employer_name, vacancy_name, salary_from, salary_to, vacancy_url FROM vacancies
            ORDER BY salary_from DESC
            """)
        vacancies = self.cur.fetchall()

        return vacancies

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""

        self.cur.execute("""
            SELECT salary_from, salary_to FROM vacancies
            """)
        salaries = self.cur.fetchall()

        self.salaries_list = []

        for row in salaries:
            if row[0] != 0 and row[1] != 0:
                self.salaries_list.append(((row[0] + row[1]) / 2))

            elif row[0] != 0 and row[1] == 0:
                self.salaries_list.append(row[0])

            else:
                continue

        return round(sum(self.salaries_list) / len(self.salaries_list), 2)

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        all_vacancies = self.get_all_vacancies()
        avg_salary = self.get_avg_salary()
        sort_vacancies_list = []

        for vac in all_vacancies:
            if vac[2] == 0 and vac[3] != 0:
                if vac[3] >= avg_salary:
                    sort_vacancies_list.append(vac)
            elif vac[2] != 0 and vac[3] == 0:
                if vac[2] >= avg_salary:
                    sort_vacancies_list.append(vac)
            elif vac[2] != 0 and vac[3] != 0:
                if vac[2] >= avg_salary:
                    sort_vacancies_list.append(vac)

        return sort_vacancies_list

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        vacancies_list = self.get_all_vacancies()
        sorted_vac_list = []

        for vac in vacancies_list:
            if keyword in vac[1]:
                sorted_vac_list.append(vac)

        return sorted_vac_list


if __name__ == '__main__':
    hh_data = HeadHunterData()
    hh_data.get_employers()
    hh_data.get_sort_emp()
    hh_data.get_vacancies_from_employer()
    hh_data.get_sort_vacancies()

    params = config()
    dbmanager = DBManager(params)
    dbmanager.create_connection('postgres')
    dbmanager.create_database('k')

    dbmanager.create_tables()
    dbmanager.insert_data(hh_data.get_sort_vacancies(), hh_data.get_sort_emp())
    # print(dbmanager.get_companies_and_vacancies_count())
    # print(dbmanager.get_all_vacancies())
    # dbmanager.get_avg_salary()
    # print(dbmanager.get_vacancies_with_higher_salary())
    print(dbmanager.get_vacancies_with_keyword('Агент'))
