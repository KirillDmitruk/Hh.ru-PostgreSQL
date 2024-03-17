from abc import ABC, abstractmethod

import requests


class AbstractAPI(ABC):
    """Абстрактный класс с методом получения данных по API."""

    @abstractmethod
    def get_employers(self):
        pass


class HeadHunterData(AbstractAPI):
    """Класс получения данных по API"""

    def __init__(self):
        self.employers = []
        self.all_vacancies = []
        self.sort_emp = []
        self.sort_vac = []

    def get_employers(self):
        """
        Метод позволяет получить данные по определенным параметрам с сайта HH.ru
        :return: self.employers
        """
        params = {
            'area': 113,
            'only_with_vacancies': True,
            'per_page': 10
        }

        hh_url = 'https://api.hh.ru/employers'
        data = requests.get(hh_url, params=params).json()

        self.employers.extend(data['items'])

        return self.employers

    def get_sort_emp(self):
        """
        Метод добавляет компании из списка self.employers по заданным критериям в список self.sort_emp
        :return: self.sort_emp
        """
        self.sort_emp.clear()
        for emp in self.employers:
            emp_dict = {
                'id': f'{emp["id"]}',
                'name': f'{emp["name"]}',
                'url': f'{emp["alternate_url"]}',
                'vacancies_url': f"https://api.hh.ru/vacancies?employer_id={emp['id']}",
                'open_vacancies': emp["open_vacancies"]
            }

            self.sort_emp.append(emp_dict)

        return self.sort_emp

    def get_vacancies_from_employer(self):
        """
        Метод позволяет получить данные по определенным параметрам с сайта HH.ru
        :return: self.all_vacancies
        """
        for emp in self.sort_emp:
            hh_url = f'{emp["vacancies_url"]}'
            response = requests.get(hh_url).json()

            self.all_vacancies.extend(response['items'])

        return self.all_vacancies

    def get_sort_vacancies(self):
        """
        Метод получения отсортированного списка
        :return: self.sort_vac
        """
        for vac in self.all_vacancies:

            id_emp = f'{vac["id"]}'
            name = f'{vac["name"]}'
            area = f'{vac["area"]["name"]}'

            employer_id = f'{vac["employer"]["id"]}'
            employer_name = f'{vac["employer"]["name"]}'
            emp_url = f'{vac["employer"]["alternate_url"]}'
            vac_url = f'{vac["alternate_url"]}'

            if vac["salary"] is not None:
                currency = f'{vac["salary"]["currency"]}'
                if vac["salary"]["from"] is not None:

                    salary_from = vac["salary"]["from"]
                else:
                    salary_from = 0

                if vac["salary"]["to"] is not None:

                    salary_to = vac["salary"]["to"]
                else:
                    salary_to = 0
            else:
                salary_from, salary_to = 0, 0
                currency = 'RUR'

            vac_dict = {
                'id': id_emp,
                'name_vac': name,
                'area': area,
                'salary_from': salary_from,
                'salary_to': salary_to,
                'currency': currency,
                'employer_id': employer_id,
                'employer_name': employer_name,
                'employer_url': emp_url,
                'vacancy_url': vac_url
            }

            self.sort_vac.append(vac_dict)

        return self.sort_vac
