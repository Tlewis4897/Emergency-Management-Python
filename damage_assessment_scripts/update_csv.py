import os
import arcgis
import json
from arcgis.gis import GIS


def read_json(json_data: str):
    """reads a json file and returns the text as a dictionary"""
    try:
        with open(json_data, 'r') as json_file:
            get_json = json.load(json_file)
        return get_json
    except Exception as err:
        return err


def update_csv_management():
    SCRIPT_PATH = os.path.abspath(__file__)
    CURRENT_DIR = os.path.abspath(os.path.join(SCRIPT_PATH, os.pardir))
    config = read_json(os.path.join(CURRENT_DIR, 'config.json'))
    csv_filepaths = [config['csv_path']]
    gis = GIS(username=config['username'], password=config['pw'])
    try:
        for csv_file in csv_filepaths:
            csv_name = os.path.splitext(os.path.basename(csv_file))[0]
            online_item = gis.content.search(query='title: {}'.format(csv_name), item_type='CSV')[0]
            print(online_item.update({}, csv_file))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    update_csv_management()