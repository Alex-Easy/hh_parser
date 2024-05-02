import requests
import json
import bs4
from fake_headers import Headers

def get_fake_headers():
    return Headers(browser="chrome", os="win").generate()

def scrapping_information():
    response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2',
                        headers=get_fake_headers())
    if response.status_code != 200:
        print('Не удалось загрузить страницу!')
        return []

    page_data = bs4.BeautifulSoup(response.text, 'lxml')
    vacancies = page_data.findAll('div', class_='vacancy-serp-item-body')
    parsed_data = []

    for vacancy in vacancies:
        vacancy_name = vacancy.find('a', class_='bloko-link').text
        print(vacancy_name)
        link = vacancy.find('a', class_='bloko-link').get('href')
        try:
            salary = vacancy.find('span', class_='bloko-header-section-2').text.replace("u202f", " ").replace("xa0", " ")
        except:
            salary = 'зарплата не указана!'
        company_name = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace("xa0", " ")
        location = vacancy.findAll('div', class_='bloko-text')[1].text.replace("xa0", " ")

        parsed_data.append([vacancy_name, link, salary, company_name, location])

    return parsed_data

def convert_to_dict(parsed_data):
    return [dict(zip(['vacancy_name', 'link', 'salary', 'company_name', 'location'], row)) for row in parsed_data]

def write_json(parsed_data):
    with open('vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(parsed_data, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    data = scrapping_information()
    if data:
        write_json(convert_to_dict(data))
