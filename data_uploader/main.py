import csv
from dataclasses import dataclass
import requests


@dataclass
class Language:
    language: str
    position: int


@dataclass
class Headers:
    languages: list[Language]
    field_id_position: int = 0
    description_position: int = 0


file = open('data.csv', 'r', errors='ignore')
reader = csv.reader(file, delimiter=';')
headers = Headers(languages=[])
for row in reader:
    if reader.line_num == 1:
        for i in range(len(row)):
            if row[i] == 'field_id':
                headers.field_id_position = i
            elif row[i] == 'description':
                headers.description_position = i
            else:
                headers.languages.append(
                    Language(language=row[i], position=i)
                )
    else:
        response = requests.post(
            url='http://89.111.153.183:5000/api/admin/general_texts/new_field',
            params={
                'field_id': row[headers.field_id_position],
                'description': row[headers.description_position]
            }
        )
        response = response.json()
        if response['error']:
            print(f'{row[headers.field_id_position]}: {row[headers.description_position]}')
            print(response['message'])
            print('-'*50)
        for language in headers.languages:
            response = requests.post(
                url='http://89.111.153.183:5000/api/admin/general_texts/new_text',
                params={
                    'field_id': row[headers.field_id_position],
                    'language': language.language,
                    'text': row[language.position]
                }
            )
            response = response.json()
            if response['error']:
                print(f'{row[headers.field_id_position]}: {language.language}: {row[language.position]}')
                print(response['message'])
                print('-' * 50)
file.close()
print('Done')