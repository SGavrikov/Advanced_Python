import requests
import json
from bs4 import BeautifulSoup
import fake_headers

def gen_headers():
    headers_gen = fake_headers.Headers(os='win', browser='chrome')
    return headers_gen.generate()

main_response = requests.get("https://spb.hh.ru/search/vacancy?text=python&area=1&area=2", headers=gen_headers())
main_html_data = main_response.text
main_soup = BeautifulSoup(main_html_data, 'lxml')
vacancy_list_tag = main_soup.find('div', id='a11y-main-content')
data = []
for vacancy_tag in vacancy_list_tag.find_all('div', class_='serp-item'):
    vacancy = {}
    title_tag = vacancy_tag.find('span', class_='serp-item__title')
    link = vacancy_tag.find('a', class_='bloko-link')['href']
    cash_tag = vacancy_tag.find('span', class_='bloko-header-section-2')
    company_tag = vacancy_tag.find('a', class_='bloko-link_kind-tertiary')
    city_tag = vacancy_tag.find_all('div', class_='bloko-text')[1]
    vacancy_response = requests.get(link, headers=gen_headers())
    vacancy_html_data = vacancy_response.text
    vacancy_soup = BeautifulSoup(vacancy_html_data, 'lxml')
    vacancy_description_tag = vacancy_soup.find('div', class_='g-user-content')
    if 'Django' in vacancy_description_tag.text and 'Flask' in vacancy_description_tag.text:
        vacancy['title'] = title_tag.text
        vacancy['link'] = link
        vacancy['salary'] = cash_tag.text.replace('\u202f000', '')
        vacancy['company'] = company_tag.text
        vacancy['city'] = city_tag.text
        data.append(vacancy)

with open('vacancy.json', 'w', encoding='utf-8') as outfile:
    json.dump(data, outfile)
