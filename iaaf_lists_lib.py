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

re_block_result = re.compile(
    r'<tr data-id="\d+" >(?P<block>.*?)</tr>',
    flags=re.DOTALL
)

re_competitor = re.compile(
    r'<a href="/athletes/athlete=(?P<id>\d+)">'
    r'(?P<name>.*?)<span class=.name-uppercase.>(?P<surname>.*?)</span>',
    re.DOTALL
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


def result_info(single_result):
    match = re_result_info.search(single_result)
    if match:
        result = match.groupdict()
##        result['rank'] = int(result['rank']) if result['rank'] else None
##        result['time'] = result['time'].strip
##        result['DOB'] = result['DOB']
        #print(result['rank'], result['time'], result['DOB'])
        return result
        print('match')
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
            for single_result in re_block_result.finditer(file_content):
                results.append(result_info(single_result.group(0)))
    return results


#UKAZI

##download_all_time_lists(
##    'middlelong', '5000-metres', 'outdoor', 'women', 'senior', lists_directory
##    )

lists = read_lists(lists_directory)


