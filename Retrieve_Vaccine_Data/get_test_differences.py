import requests
from bs4 import BeautifulSoup
import re
from get_survey_data import get_csv_data
from send_notification import send_test_change_notif


def sync_testing_vendors(config, fda_url, survey_path):
    fda_test_req = requests.post(fda_url,
                                 headers={'content-type': 'application/json'})

    fda_test_html = BeautifulSoup(fda_test_req.text, 'lxml')
    fda_test_table = fda_test_html.select('tr')
    tests = []
    for test_data in fda_test_table[1:]:
        test_data_td = test_data.find_all('td')
        fda_test_type1 = BeautifulSoup(str(test_data_td[4])).get_text().strip().split(",")
        fda_test_type = [x.strip(' ') for x in fda_test_type1]
        test_types = str(test_data_td[2]).split('Letter of Authorization', 1)
        special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if(special_char.search(test_types[1]) is None):
            print('String does not contain any special characters.')
        else:
            if 'Home' and 'W' not in fda_test_type:
                pass
            else:
                if 'Home' in fda_test_type and 'W' in fda_test_type:
                    fda_test_type = 'OTCT,POCT'
                elif 'Home' in fda_test_type and 'W' not in fda_test_type:
                    fda_test_type = 'OTCT'
                elif 'W' in fda_test_type and 'Home' not in fda_test_type:
                    fda_test_type = 'POCT'
                test_names = test_types[1].split('">', 1)
                test_names = test_names[1].split('</a>', 1)[0]
                test_names = BeautifulSoup(str(test_names))
                manufacture_name = str(test_data_td[1]).replace('<td>', '').replace('<a data-entity-substitution="media_download" data-entity-type="media" data-entity-uuid="6592f4cd-6b45-4670-9f70-e4717c2fe803" href="/media/153925/download" title="iHealth Rapid TestAg Letter of Authorization "> </a>',' ')
                manufacture_name = manufacture_name.replace('<a data-entity-substitution="media_download" data-entity-type="media" data-entity-uuid="6592f4cd-6b45-4670-9f70-e4717c2fe803" href="/media/153925/download" title="iHealth Rapid TestAg Letter of Authorization "> </a>',' ')
                manufacture_name = manufacture_name.replace('</td>', '')
                manufacture_name = manufacture_name.replace(' Inc.', ', Inc.')
                manufacture_name = manufacture_name.replace(',, Inc.',
                                                            ', Inc.')
                tests.append([manufacture_name,
                              test_names.get_text(),
                              fda_test_type])
    first_tuple_list = [tuple(lst) for lst in tests]
    secnd_tuple_list = [tuple(lst) for lst in get_csv_data(survey_path)]
    first_set = set(first_tuple_list)
    secnd_set = set(secnd_tuple_list)
    s = first_set.symmetric_difference(secnd_set)
    mismatch_list = []
    for item in s:
        t = list(item)
        if t in tests:
            t.insert(len(t), 'Source: FDA Website')
        if t in get_csv_data(survey_path):
            t.insert(len(t), 'Source: Survey 123 CSV')
        mismatch_list.append(t)
    if len(mismatch_list) > 0:
        send_test_change_notif(config, mismatch_list)
    print(mismatch_list)
    return mismatch_list
