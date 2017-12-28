#projektna naloga za Programiranje 1
#primerjava časov za ralične atletske discipline skozi leta

import csv
import json
import os
import re
import requests
from pprint import pprint

lists_directory = 'iaaf_lists'

category_discipline = {'sprints':(
                '100-metres', '200-metres', '400-metres'),
                'middlelong':(
                '800-metres', '1500-metres', '5000-metres', '10000-metres'
                )}
where = ['outdoor', 'indoor']
gender = ['women', 'men']
agegroup = ['senior', 'u18', 'u20']

re_block_result = re.compile(
    r'<tr data-id="\d+" >(?P<block>.*?)</tr>',
    flags=re.DOTALL
)

re_result_info = re.compile(
    r'<td data-th="Rank">(?P<rank>.*?)</td>'
    r'.*?'
    r'<td data-th="Mark">(?P<time>.*?)</td>'
    r'.*?'
    r'<td data-th="Competitor">.*?<a href="/athletes/athlete=(?P<id>\d+)">'
    r'(?P<name>.*?) <span class=.name-uppercase.>(?P<surname>.*?)</span></a>'
    r'.*?'
    r'<td data-th="DOB">(?P<DOB>.*?)</td>'
    r'.*?'
    r'<td data-th="Nat">.*?<img.*?/>(?P<nationality>.*?)</td>'
    r'.*?'
    r'<td data-th="Pos">(?P<position>.*?)</td>'
    r'.*?'
    r'<td data-th="Venue">(?P<venue>.*?)</td>'
    r'.*?'
    r'<td data-th="Date">(?P<date>.*?)</td>',
    re.DOTALL
    )

#problemi:
    #kako najti vse do Mixed race
    #kaj delajo Nonei na koncu
    #kodiranje dela neke probleme hmmm
def result_info(single_result):
    match = re.search(re_result_info, single_result)
    if match:
        result = match.groupdict()
        result['rank'] = int(result['rank'].strip()) if result['rank'].strip() != '' else None
        result['time'] = str(result['time']).strip()
        result['DOB'] = result['DOB'].strip()
        result['nationality'] = result['nationality'].strip()
        result['position'] = result['position'].strip()
        result['venue'] = result['venue'].strip()
        result['date'] = result['date'].strip()
        pprint( result)
        return result
    else:
        print('cannot read this result, im useless :(')
        print(single_result)



#choose category, discipline, where, gender and agegroup from lists upwards
def download_all_time_lists(
    category, discipline, where, gender, agegroup, directory
    ):
    os.makedirs(directory, exist_ok=True)
    for year in range(1999, 2018):
        try:
            url = (
                'https://www.iaaf.org/'
                'records/toplists/'
                '{}/{}/{}/{}/{}/{}'
            ).format(category, discipline, where, gender, agegroup, year)
            r = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(e)
            return None

        filename = 'iaaf_lists_{}_{}_{}_{}_{}.html'.format(
            discipline, where, gender, agegroup, year
            )
        path = os.path.join(directory, filename)
        with open(path, 'w', encoding='utf-8') as file_out:
            file_out.write(r.text)


def read_lists(directory):
    results = []
    for file_name in os.listdir(directory):
        path = os.path.join(directory, file_name)
        with open(path, 'r') as file:
            file_content = file.read()
            for single_result in re.finditer(re_block_result,file_content):
                results.append(result_info(single_result.group(0)))
    return results


def zapisi_json(podatki, ime_datoteke):
    with open(ime_datoteke, 'w') as datoteka:
        json.dump(podatki, datoteka, indent=2)


def zapisi_csv(podatki, polja, ime_datoteke):
    with open(ime_datoteke, 'w') as datoteka:
        pisalec = csv.DictWriter(datoteka, polja, extrasaction='ignore')
        pisalec.writeheader()
        for podatek in podatki:
            pisalec.writerow(podatek)


#UKAZI

##download_all_time_lists(
##    'middlelong', '5000-metres', 'outdoor', 'women', 'senior', lists_directory
##    )

results = read_lists(lists_directory)

zapisi_json(results, 'lists.json')



