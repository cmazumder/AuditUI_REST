from database.misc.misc import MiscDatabase as misc_database_class
from database.vertex.vertex import VertexDatabase as vertex_database_class
from test.test_step import testTask as Test
import logging
import sys


class AuditUI_TestSuite:
    total_test_run = 0
    total_test_pass = 0
    total_test_fail = 0
    total_test_blocked = 0
    misc_db = None
    vertex_db = None

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(funcName)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='C:\LogPython\AuditUI_test1.log',
                            filemode='w')
        logging.info('Test Suite: Audit UI')

        self.misc_db = misc_database_class()
        self.vertex_db = vertex_database_class()

    def update_test_result(self, returned_result, test_name):
        """
        To update test execution count
        :param returned_result: Execution status
        :param test_name: pass the name from which method is called
        :return: None
        """
        if returned_result == 'Pass':
            self.total_test_pass += 1
        elif returned_result == 'Fail':
            self.total_test_fail += 1
        elif returned_result == 'BLOCKED':
            self.total_test_blocked += 1

        logging.info('%s --> %s', test_name, returned_result)
        logging.info('#####################################')

    def test_dashboard_Manufacture_Code(self, api_action_address):
        """
        Test Dashboard > Manufacture Code
        :param api_action_address: api address for test case
        :return: Nothing
        """

        logging.info('#####################################')

        self.total_test_run += 1
        this_function_name = sys._getframe().f_code.co_name
        logging.info('Runing pre-req check for %s', this_function_name)

        make_query = r"SELECT ComponentValue FROM [Misc].[dbo].[Component] WHERE ComponentID = 'ManufacturerIdentifier'"

        execution_status = Test.execute_test_steps(api_action_address=api_action_address, database_object=self.misc_db,
                                                   table='Component', test_sql_query=make_query, api_datapoint_value_toSearch='ManufacturerIdentifier',
                                                   api_datapoint_key_toGet='ComponentValue', test_name=this_function_name)

        self.update_test_result(
            returned_result=execution_status, test_name=this_function_name)

    def test_dashboard_GMID(self, api_action_address):
        """
        Test Dashboard > GMID
        :param api_action_address: api address for test case
        :return: Nothing
        """
        logging.info('#####################################')
        self.total_test_run += 1
        this_function_name = sys._getframe().f_code.co_name
        logging.info('Runing pre-req check for %s', this_function_name)

        make_query = r"SELECT ComponentValue FROM [Misc].[dbo].[Component] WHERE ComponentID = 'ControllerGMID'"

        execution_status = Test.execute_test_steps(api_action_address=api_action_address, database_object=self.misc_db,
                                                   table='Component', test_sql_query=make_query, api_datapoint_value_toSearch='ControllerGMID',
                                                   api_datapoint_key_toGet='ComponentValue', test_name=this_function_name)

        self.update_test_result(
            returned_result=execution_status, test_name=this_function_name)

    def test_dashboard_Supported_Levels(self, api_action_address):
        """
        Test Dashboard > Supported Levels
        NOTE: This test is specifically written to fail
        :param api_action_address: api address for test case
        :return: Nothing
        """
        logging.info('#####################################')
        self.total_test_run += 1
        this_function_name = sys._getframe().f_code.co_name
        logging.info('Runing pre-req check for %s', this_function_name)

        make_query = r"SELECT ConfigID FROM [Vertex].[dbo].[Config] WHERE ConfigID='LevelCountLimit'"

        execution_status = Test.execute_test_steps(api_action_address=api_action_address, database_object=self.misc_db,
                                                   table='Component', test_sql_query=make_query, api_datapoint_value_toSearch='LevelCountLimit',
                                                   api_datapoint_key_toGet='Value', test_name=this_function_name)

        self.update_test_result(
            returned_result=execution_status, test_name=this_function_name)

    def test_dashboard_CCCE_Limit(self, api_action_address):
        """
        Test Dashboard > CCCE
        NOTE: This test is specifically written to fail pre-req and be blocked
        :param api_action_address: api address for test case
        :return: Nothing
        """
        logging.info('#####################################')
        self.total_test_run += 1
        this_function_name = sys._getframe().f_code.co_name
        make_query = r"SELECT ConfigValue FROM [Vertex].[dbo].[Config] WHERE ConfigID='CCCETransferLimit'"

        execution_status = Test.execute_test_steps(api_action_address=api_action_address, database_object=self.vertex_db,
                                                   table='Config', test_sql_query=make_query, api_datapoint_value_toSearch='CCCETransferLimit',
                                                   api_datapoint_key_toGet='Value', test_name=this_function_name)

        self.update_test_result(
            returned_result=execution_status, test_name=this_function_name)
