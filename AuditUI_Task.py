import requests
import json
import pyodbc
import logging
from requests.auth import HTTPBasicAuth
from coloredlogs import install
from setup_File import Env_variable as set_var


class API_AuditUI_process:
    cursor = None
    db_connection = None
    api_url_root = None

    def __init__(self):
        """logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='myapp1.log',
                            filemode='w')"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        LogHandler = logging.FileHandler('Log.log', 'w', 'utf-8')
        LogHandler.setLevel(logging.DEBUG)
        logging.info('Started at Test Suite API_AuditUI_process ')
        try:
            self.api_url_root = set_var.get("ApiURL_root")
        except Exception as E:
            logging.warning(
                'Issue while getting api_url_root from setup_File.py %s', E.message)
            self.halter()

    def halter(self, err=None):  # halter to exit out the program run
        if err:
            print err
        raw_input("\n\nPress ANY KEY to EXIT")
        exit()

    def connect_db(self, database):  # connect to the db and server as per setup and argument
        logging.info('Creating database connection to %s at server %s',
                     database, set_var.get("db_server"))
        if self.db_connection:
            self.cursor.close()
            del self.cursor
            self.db_connection.close()

        try:
            self.db_connection = pyodbc.connect("DRIVER={{SQL Server}};SERVER={0}; database={1}; "
                                                "trusted_connection=yes;UID={2};PWD={3}".format(
                                                    set_var.get("db_server"), database, set_var.get(
                                                        "db_username"),
                                                    set_var.get("db_password")))
            self.cursor = self.db_connection.cursor()
            logging.info('Got database connection to %s at %s',
                         database, self.cursor)
            return self.cursor
        except pyodbc.Error as E:
            logging.warning('Cannot setup database connection\n %s', E.message)
            return None

    def execute_presise_SQLquery(self, sqlQuery, database):  # Query the db
        try:
            if not self.cursor:
                self.cursor = self.connect_db(database=database)

            self.cursor.execute(sqlQuery)
            # for row in self.cursor:
            #     print (row)
            #     return row
            data = self.cursor.fetchall()
            for row in data:
                return row[0]

        except Exception as E:
            logging.warning(
                'Problem with objects\'s cursor in execute query \n %s', E.message)
            print E

    def get_response(self, api_action_address):  # GET response from API url in JSON
        api_get_url = self.api_url_root + api_action_address
        try:
            response = requests.get(api_get_url, auth=(
                'retail1', 'Retail1'), verify=False)
            if response.status_code != 200:
                raise ApiError('GET /tasks/ {}'.format(response.status_code))
            else:
                # for item in response.json():
                #     print'{}'.format(item)
                return response.json()
        except Exception as E:
            logging.warning(
                'Problem with GET at %s \n Error handled %s', api_get_url, E.message)

    def API_DB_responce_test(self, sqlQuery, apiURL, datapoint, db, datapoint_value):
        self.cursor = self.connect_db(db)
        sql_result = self.execute_presise_SQLquery(
            sqlQuery=sqlQuery, database=db)
        api_response = self.get_response(api_action_address=apiURL)
        for item in api_response:
            if datapoint in item.values():
                if sql_result == item.get("ComponentValue"):
                    return 'Pass'
        return 'Fail'

# def main():
#     server = r'172.26.18.110\SQLEXPRESS'
#     database = r'misc'
#     username = r'sa'
#     password = r'Password1'
#     table = r'Component'
#     sql_query = r"SELECT * FROM [misc].[dbo].[Component]"
#     make_query = r"SELECT ComponentValue FROM [{0}].[dbo].[{1}] WHERE ComponentID = 'ManufacturerIdentifier'".format(
#         database, table)
#
#     obj1 = API_AuditUI_process()
#     # obj1.connect_db(database=database)
#     # obj1.execute_presise_SQLquery(sqlQuery=sql_query)
#     result = obj1.API_DB_responce_test(sqlQuery=make_query, apiURL='/dataservice/api/2/Components',
#                                        datapoint='ManufacturerIdentifier', db=database)
#     print result
#
#
# if __name__ == "__main__":
#     main()
