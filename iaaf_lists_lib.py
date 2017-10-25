#projektna naloga za Programiranje 1
#primerjava časov za ralične atletske discipline skozi leta

import requests
import re
import os
import csv


lists_directory = 'iaaf_lists'

category_discipline = {'sprints':(
                '100-metres', '200-metres', '400-metres'),
                'middlelong':(
                '800-metres', '1500-metres', '5000-metres', '10000-metres'
                )}
where = ['outdoor', 'indoor']
gender = ['women', 'men']
agegroup = ['senior', 'u18', 'u20']


re_competitor = re.compile(
    r'<a href="/athletes/athlete=(?P<id>\d+)">'
    r'(?P<name>.*?).*? (?P<surname>.*?)</span>',
    re.DOTALL
    )

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
            print(url)
        except requests.exceptions.RequestException as e:
            print(e)
            return None

        filename = 'iaaf_lists_{}_{}_{}_{}_{}.html'.format(
            discipline, where, gender, agegroup, year
            )
        path = os.path.join(directory, filename)
        with open(path, 'w', encoding='utf-8') as file_out:
            file_out.write(r.text)

def save_data_to_dict(file):
    rx = re.compile(
    r'<td data-th="Rank">(?P<rank>.?*)</td>'
    r'<td data-th="Mark">(?P<time>.?*)</td>',
    re.DOTALL
    )
    data = re.search(rx, file)











