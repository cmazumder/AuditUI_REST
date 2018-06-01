import requests
import json
import logging
from requests.auth import HTTPBasicAuth
from setup_File import Env_variable as config_variable

api_url_root = None

try:
    api_url_root = config_variable.get("ApiURL_root")
except Exception as E:
    logging.warning(
        'Issue while getting api_url_root from setup_File.py %s', E.message)


def halter(self, err=None):  # halter to exit out the program run
    if err:
        print err
    raw_input("\n\nPress ANY KEY to EXIT")
    exit()


def get_api_json_response(api_action_address):
    """
    GET response from API url in JSON
    :param api_action_address: the api datapoint address
    :return: JSON response if found, else None
    """
    global api_url_root
    api_get_url = api_url_root + api_action_address
    try:
        response = requests.get(api_get_url, auth=(
            config_variable.get('api_username'), config_variable.get('api_password')), verify=False)
        if response.status_code != 200:
            raise ApiError('GET /tasks/ {}'.format(response.status_code))
        else:
            # for item in response.json():
            #     print'{}'.format(item)
            return response.json()
    except Exception as E:
        logging.warning(
            'Problem with GET at %s \n Error handled %s', api_get_url, E.message)
    return None


def get_api_datapoint_value(api_action_address, api_datapoint_value_toSearch, api_datapoint_key_toGet, api_key_toFetch=None):
    """
    Extract the value from the api response given the datapoint
    :param api_action_address: url to api
    :param api_datapoint_value_toSearch: to denote the api tag lookup value
    :param api_datapoint_key_toGet: to denote the api tag containing the value of api_datapoint_value_toSearch
    :param api_key_toFetch: Furture use, and unused for now
    :return: value of the api data point
    """
    api_response = get_api_json_response(api_action_address=api_action_address)
    if api_response:
        for item in api_response:
            if api_datapoint_value_toSearch in item.values():
                return item.get(api_datapoint_key_toGet)
    return None


# def main():
#     """logging.basicConfig(level=logging.DEBUG,
#                         format='%(asctime)s %(levelname)-8s %(message)s',
#                         datefmt='%a, %d %b %Y %H:%M:%S',
#                         filename='myapp1.log',
#                         filemode='w')"""
#     logger = logging.getLogger(__name__)
#     logger.setLevel(logging.DEBUG)
#     log_handler = logging.FileHandler('C:\LogPython\DB', 'w', 'utf-8')
#     log_handler.setLevel(logging.DEBUG)
#     logging.info('Got API root address')
#
#
# if __name__ == "__main__":
#     main()
