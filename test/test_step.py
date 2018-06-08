import logging

import api.util as api_util
from webUI.interface import Interface as audit_ui

audit_ui_task = audit_ui()  # global object for audit_ui

class testTask:
    api_result = {}
    database_result = {}
    web_ui_result = {}

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(funcName)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='C:\LogPython\AuditUI_TestRun.log',
                            filemode='w')
        logging.info('Started at Test Step')


    @classmethod
    def check_prerequisite(cls, api_action_address, database_object, table_name, test_name='PreRequsite'):
        """
        To check if pre-requisite condition before test is met
        :param test_name:
        :param api_action_address: url to api
        :param database_object: object of the database class
        :param table_name: name of the table to verify if data is present
        :return: True if all conditions are met, else false
        """
        logging.info('Runing pre-req check for %s', test_name)
        sql_query_text = r"SELECT TOP 1 * FROM {}".format(table_name)
        api_url_data = api_util.get_api_json_response(api_action_address)
        db_table_data = database_object.execute_sql_query(
            sql_query=sql_query_text)
        if api_url_data and db_table_data:
            return True
        else:
            return False

    @classmethod
    def test_api_db_data(cls, api_action_address, database_object, api_datapoint_value_toSearch, api_datapoint_key_toGet, test_sql_query, testname="API v/s database"):
        """
        Compare database vs API REST call
        :param api_action_address: url to api
        :param database_object: object of the database class
        :param api_datapoint_value_toSearch: to denote the api tag lookup value
        :param api_datapoint_key_toGet: to denote the api tag containing the value of api_datapoint_value_toSearch
        :param test_sql_query:
        :param testname: Name of the test that is using this method at execution
        :return: Result of test (Pass/Fail)
        """
        logging.info('Executing test for %s', testname)
        sql_result = database_object.execute_sql_query(
            sql_query=test_sql_query)

        api_result = api_util.get_api_datapoint_value(
            api_action_address=api_action_address, api_datapoint_value_toSearch=api_datapoint_value_toSearch, api_datapoint_key_toGet=api_datapoint_key_toGet)
        try:
            logging.info('Database value: %s', sql_result[0])
            logging.info('REST value: %s', api_result)
            if sql_result[0] == api_result:
                logging.info('Test PASS')
                return 'Pass'
            else:
                logging.info('Test FAIL')
                return 'Fail'
        except TypeError as E:
            logging.warning(
                'SQL result is NULL for query --> %s', test_sql_query)
            logging.error('Error message: %s', E.message)
            return 'BLOCKED'

    @classmethod
    def test_api_ui_data(cls, api_action_address, api_datapoint_value_toSearch, api_datapoint_key_toGet, ui_url,
                         ui_xpath_to_value, testname="API v/s UI"):
        """
        Compare database vs API REST call
        :param api_action_address: url to api
        :param api_datapoint_value_toSearch: to denote the api tag lookup value
        :param api_datapoint_key_toGet: to denote the api tag containing the value of api_datapoint_value_toSearch
        :param ui_url:
        :param ui_xpath_to_value:
        :param testname: Name of the test that is using this method at execution
        :return: Result of test (Pass/Fail)
        """

        logging.info('Executing test for %s', testname)
        global audit_ui_task
        audit_ui_task.navigate_to_url(ui_url)
        ui_result = audit_ui_task.get_ui_value_xpath(ui_xpath_to_value)

        api_result = api_util.get_api_datapoint_value(
            api_action_address=api_action_address, api_datapoint_value_toSearch=api_datapoint_value_toSearch,
            api_datapoint_key_toGet=api_datapoint_key_toGet)
        try:
            logging.info('UI value: %s', ui_result)
            logging.info('REST value: %s', api_result)
            if ui_result == api_result:
                logging.info('Test PASS')
                return 'Pass'
            else:
                logging.info('Test FAIL')
                return 'Fail'
        except TypeError as E:
            logging.warning('Result is NULL')
            logging.error('Error message: %s', E.message)
            return 'BLOCKED'

    @classmethod
    def execute_test_steps(cls, api_action_address, database_object, table, test_sql_query,
                           api_datapoint_value_toSearch, api_datapoint_key_toGet, ui_url, ui_xpath_to_value,
                           test_name="TestStep"):
        """
        Consolidated test steps into one
        :param api_action_address: url to api
        :param database_object: object of the database class
        :param table: table name from the database to test
        :param test_sql_query: query to fetch the data from database
        :param api_datapoint_value_toSearch: api tag lookup value
        :param api_datapoint_key_toGet: to denote the api tag containing the value of api_datapoint_value_toSearch
        :param test_name:
        :return: Status of test (Pass/Fail)
        """

        prereq_test_result = cls.check_prerequisite(api_action_address=api_action_address,
                                                    database_object=database_object, table_name=table, test_name=test_name)
        logging.info('Pre-req for %s --> %s', test_name, prereq_test_result)
        if prereq_test_result:
            test_api_database_result = cls.test_api_db_data(api_action_address=api_action_address,
                                                            database_object=database_object,
                                                            api_datapoint_value_toSearch=api_datapoint_value_toSearch,
                                                            api_datapoint_key_toGet=api_datapoint_key_toGet,
                                                            test_sql_query=test_sql_query, testname=test_name)

            logging.info('Execution \'API vs database\' %s --> %s',
                         test_name, test_api_database_result)

            test_api_ui_result = cls.test_api_ui_data(api_action_address=api_action_address,
                                                      api_datapoint_value_toSearch=api_datapoint_value_toSearch,
                                                      api_datapoint_key_toGet=api_datapoint_key_toGet,
                                                      ui_url=ui_url,
                                                      ui_xpath_to_value=ui_xpath_to_value,
                                                      testname=test_name
                                                      )
            if test_api_database_result == 'Pass' and test_api_ui_result == 'Pass':
                return 'Pass'
            else:
                return 'Fail'
        else:
            logging.info(
                'Did not execute %s --> BLOCKED', test_name)
            return 'BLOCKED'


# def main():
#     obj1 = testTask()
#     misc_db = misc.MiscDatabase()
#     result = obj1.check_prerequisite(
#         r'/dataservice/api/2/Components', misc_db, 'Component')
#
#     print result
#
#
# if __name__ == "__main__":
#     main()
