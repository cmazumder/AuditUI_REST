import database.misc.misc as misc
import api.util as api_util
import logging
import sys


class testTask:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(funcName)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='C:\LogPython\TestTask.log',
                            filemode='w')
        logging.info('Started at Test Suite')

    @classmethod
    def check_prerequisite(cls, api_action_address, database_object, table_name):
        """
        To check if pre-requisite condition before test is met
        :param api_action_address: url to api
        :param database_object: object of the database class
        :param table_name: name of the table to verify if data is present
        :return: True if all conditions are met, else false
        """

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
            if sql_result[0] == api_result:
                return 'Pass'
            else:
                return 'Fail'
        except TypeError as E:
            logging.warning('SQL query result --> %s', sql_result)
            logging.warning('SQL query --> %s', test_sql_query)
            logging.error('Error message: %s', E.message)
            return 'Fail'

        logging.info('%s execution complete\n', testname)

    @classmethod
    def execute_test_steps(cls, api_action_address, database_object, table, test_sql_query, api_datapoint_value_toSearch, api_datapoint_key_toGet,
                           testname="API v/s database"):
        """
        Consolidated test steps
        :param api_action_address: url to api
        :param database_object: object of the database class
        :param table: table name from the database to test
        :param test_sql_query: query to fetch the data from database
        :param api_datapoint_value_toSearch: api tag lookup value
        :param api_datapoint_key_toGet: to denote the api tag containing the value of api_datapoint_value_toSearch
        :param testname:
        :return: Status of test (Pass/Fail)
        """
        logging.info('Runing pre-req check for %s', testname)
        prereq_test_result = cls.check_prerequisite(api_action_address=api_action_address, database_object=database_object,
                                                    table_name=table)
        logging.info('Pre-req for %s --> %s', testname, prereq_test_result)
        if prereq_test_result:
            test_api_database_result = cls.test_api_db_data(api_action_address=api_action_address, database_object=database_object,
                                                            api_datapoint_value_toSearch=api_datapoint_value_toSearch, api_datapoint_key_toGet=api_datapoint_key_toGet,
                                                            test_sql_query=test_sql_query, testname=testname)
            logging.info('Execution \'API vs database\' %s --> %s',
                         testname, test_api_database_result)
            if test_api_database_result == 'Pass':
                return 'Pass'
            elif test_api_database_result == 'Fail':
                return 'Fail'
            else:
                return 'BLOCKED'
        else:
            logging.info(
                'Did not execute %s --> BLOCKED', testname)
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
