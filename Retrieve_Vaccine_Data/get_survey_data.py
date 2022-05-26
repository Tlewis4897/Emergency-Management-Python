import pandas as pd


def get_csv_data(survey_path):
    survey_123_path = pd.ExcelFile(survey_path)
    survey_choice_sheet = pd.read_excel(survey_123_path, 'choices')
    manufacture = survey_choice_sheet.loc[survey_choice_sheet['list_name'] == 'manufacturer']
    covid_tests = survey_choice_sheet.loc[survey_choice_sheet['list_name'] == 'testNames']
    corportate_manufactures = dict(zip(manufacture.name,
                                       manufacture.label))
    commercial_tests = dict(zip(covid_tests.label,
                            zip(covid_tests.filtervalue,
                                covid_tests.manufac)))
    comemercial_corp_tests_full = []
    for key, value in corportate_manufactures.items():
        for k, v in commercial_tests.items():
            if key == v[1]:
                comemercial_corp_tests_full.append([value, k, v[0]])
    return comemercial_corp_tests_full