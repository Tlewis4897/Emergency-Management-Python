import os
import json
from get_test_differences import sync_testing_vendors


def read_json(json_data: str):
    """reads a json file and returns the text as a dictionary"""
    try:
        with open(json_data, 'r') as json_file:
            get_json = json.load(json_file)
        return get_json
    except Exception as err:
        return err


def main():
    try:
        SCRIPT_PATH = os.path.abspath(__file__)
        CURRENT_DIR = os.path.abspath(os.path.join(SCRIPT_PATH, os.pardir))
        config = read_json(os.path.join(CURRENT_DIR, 'config.json'))
        fda_url = config['fda_url']
        survey_path = config['survey_path']
        sync_testing_vendors(config, fda_url, survey_path)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
