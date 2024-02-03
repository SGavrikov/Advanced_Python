from pprint import pprint
import re

# Читаем адресную книгу в формате CSV в список contacts_list:
import csv

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# pprint(contacts_list)


def string_comb(str1, str2):  # Объединение двух строк с исключением дублирования и пустых строк:
    set1 = set()
    set2 = set()
    if str1 != '':
        set1.add(str1)
    if str2 != '':
        set2.add(str2)
    if str1 == '' and str2 == '':
        res_str = ''
    else:
        res_str = str(set1 | set2)[2:-2]
    return res_str


def correct_name(contacts_list):
    for contact in contacts_list:
        full_name_list = " ".join(contact[:3]).split()
        for record in range(len(full_name_list)):
            contact[record] = full_name_list[record]
    return contacts_list


def updating_phone_numbers(contacts_list):
    for contact in contacts_list:
        pattern = r"(\+7|8)(\W+|)(\d{3})(\W+|)(\d{3})(\W+|)(\d{2})(\W+|)(\d{2})(\D{0,10})(\d+|)(\)|)"
        result = re.match(pattern, contact[5])
        if result is not None:
            if result.group(11) != '':
                sub_pattern = r"+7(\3)\5-\7-\9 доб.\11"
            else:
                sub_pattern = r"+7(\3)\5-\7-\9"
            contact[5] = re.sub(pattern, sub_pattern, contact[5])
    return contacts_list


def remove_duplicate(contacts_list):
    result = []
    contacts_dict = {}
    for contact in contacts_list:  # Объединение данных для дублирующихся аккаунтов в словарь
        name = " ".join(contact[:2])
        if name in contacts_dict:
            for index in range(2, 7):
                result_contact = string_comb(contact[index], contacts_dict[name][index - 2])
                contact[index] = result_contact
                contacts_dict[name][index - 2] = result_contact
        contacts_dict[name] = contact[2:]

    result.append(contacts_list[0])  # Заполнение результирующего списка
    for contact in contacts_list:
        for value in result:
            if value[0].lower() == contact[0].lower() and value[1].lower() == contact[1].lower():
                break
        else:
            result.append([contact[0], contact[1]] + contacts_dict[" ".join(contact[:2])])
    return result


contacts_list = correct_name(contacts_list)
contacts_list = updating_phone_numbers(contacts_list)
correct_phonebook = remove_duplicate(contacts_list)


# 2. Сохраните получившиеся данные в другой файл.
# Код для записи файла в формате CSV:
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(correct_phonebook)
