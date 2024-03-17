# ***HeadHunter parser***

## ***Описание проекта***
### ***В рамках проекта необходимо получить данные о компаниях и вакансиях с сайта hh.ru, спроектировать таблицы в БД PostgreSQL и загрузить полученные данные в созданные таблицы.***

## ***Структура***

### **src**
Работа с БД:
* [Dbmanager.py](https://github.com/KirillDmitruk/Hh.ru-PostgreSQL/blob/main/src/Dbmanager.py)
* create_connection - создание соединения с БД
* close_connection - закрытие соединения с БД.
* create_database - создание БД.
* create_tables - создание таблиц.
* insert_data - заполнение таблиц данными.
* get_companies_and_vacancies_count - Получение списка всех компаний и количество вакансий у каждой компании.
* get_all_vacancies - получение списка всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.
* get_avg_salary - получение средней зарплаты по вакансиям.
* get_vacancies_with_higher_salary -  получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям.
* get_vacancies_with_keyword - получение списка всех вакансий, в названии которых содержатся переданные в метод слова.

Получение информации по API:
* [Hh_API.py](https://github.com/KirillDmitruk/Hh.ru-PostgreSQL/blob/main/src/Hh_API.py)
* class AbstractAPI - абстрактный класс с методом получения данных по API.
* class HeadHunterData - класс получения данных по API.
* get_employers - получение данных по определенным параметрам с сайта HH.ru.
* get_sort_emp - метод добавляет компании из списка self.employers по заданным критериям в список self.sort_emp.
* get_vacancies_from_employer - получение данные по определенным параметрам с сайта HH.ru.
* get_sort_vacancies - получение отсортированного списка.

Взаимодействие с программой:
* [main.py](https://github.com/KirillDmitruk/Hh.ru-PostgreSQL/blob/main/main.py)
