#projektna naloga za Programiranje 1
#primerjava časov na 5000m skozi leta

import csv
import json
import os
import re
import requests
from pprint import pprint

lists_directory = 'iaaf_lists'

year_and_page = [(2001, 4), (2002, 5), (2003, 5), (2004, 5),
                 (2005, 5), (2006, 5), (2007, 5), (2008, 5),
                 (2009, 12), (2010, 16), (2011, 17), (2012, 19),
                 (2013, 19), (2014, 20), (2015, 20), (2016, 20),
                 (2017, 22)]

re_block_result = re.compile(
    r'<tr>\s*(?P<block><td data-th="Rank">.*?)</tr>',
    flags=re.DOTALL
)

re_result_info = re.compile(
    r'<td data-th="Rank">(?P<rank>.*?)</td>'
    r'.*?'
    r'<td data-th="Mark">(?P<time>.*?)</td>'
    r'.*?'
    r'<td data-th="Competitor">\s*<a href="/athletes/.*?">'
    r'\s*(?P<name>.*?)\s*</a>'
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
        #pprint( result)
        return result
    else:
        print('cannot read this result, im useless :(')
        #print(single_result)



#prenese vse tablice od leta 2001 naprej
def download_all_time_lists (directory):
    os.makedirs(directory, exist_ok=True)
    for (year, page) in year_and_page : 
        for p in range (1, page + 1):
            try:
                url = (
                'https://www.iaaf.org/records/toplists/middlelong/'
                '5000-metres/outdoor/women/senior/'
                '{}?regionType=world&page={}&bestResultsOnly=true'
                ).format(year, p)
                session = requests.Session()
                r = session.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                print(r.status_code)
                print(url)
        
            except requests.exceptions.RequestException as e:
                print(e)
                return None

            filename = 'iaaf_lists_5000m_ women_{}_{}.html'.format(
                        year, p)
            path = os.path.join(directory, filename)
            with open(path, 'w', encoding='utf-8') as file_out:
                file_out.write(r.text)

#prebere html datoteke v izbranem imeniku
def read_lists(directory):
    results = []
    for file_name in os.listdir(directory):
        path = os.path.join(directory, file_name)
        with open(path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            for single_result in re.finditer(re_block_result,file_content):
                results.append(result_info(single_result.group(0)))
    return results


def zapisi_json(podatki, ime_datoteke):
    with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
        json.dump(podatki, datoteka, indent=2)


def zapisi_csv(podatki, polja, ime_datoteke):
    with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
        pisalec = csv.DictWriter(datoteka, polja, extrasaction='ignore')
        pisalec.writeheader()
        for podatek in podatki:
            pisalec.writerow(podatek)


#UKAZI

## download_all_time_lists(lists_directory)
   
lists = read_lists(lists_directory)

zapisi_json(lists, 'lists.json')

polja = [
    'date', 'time', 'name', 'surname', 'rank', 'position',
    'DOB', 'venue', 'nationality',
]

zapisi_csv(lists, polja, 'lists.csv')


