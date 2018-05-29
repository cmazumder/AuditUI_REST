import AuditUI_Task as API
import logging, pyodbc, sys


class AuditUI_DataTest:
    def __init__(self):

        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(funcName)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='myapp.log',
                            filemode='w')
        logging.info('Started at Test Suite AuditUI_DataTest ')

    def check_preRequisite(self, TaskObject, api_action_address, dbname, table):
        API_response = TaskObject.get_response(api_action_address=api_action_address)

        sql = r"SELECT TOP 1 * FROM [{0}].[dbo].[{1}]".format(dbname, table)
        try:
            conn = TaskObject.connect_db(database=dbname)
            if conn:
                API_db_hasData = TaskObject.execute_presise_SQLquery(sqlQuery=sql, database=dbname)
                if API_response and API_db_hasData:
                    return True
                else:
                    return False
        except pyodbc as E:
            # logging.ERROR('Connection issue %s', E)
            print E

    def run_test(self, Taskobject, testname, api_URL, db, table, datapoint_field, datapoint_value_field, test_sqlQuery):
        logging.info('Executing test for %s', testname)
        test_result = Taskobject.API_DB_responce_test(sqlQuery=test_sqlQuery, apiURL=api_URL,
                                                      datapoint=datapoint_field, db=db,
                                                      datapoint_value=datapoint_value_field)
        logging.info('Test %s evaluated to %s', testname, test_result)
        print "Test {0} is {1}".format(testname, test_result)

    def test_Dashboard_ManufactureCode(self, Taskobject, api_action_address, dbname, table, datapoint_field,
                                       datapoint_value_field):
        this_function_name = sys._getframe().f_code.co_name
        logging.info('Runing pre-req check for %s', this_function_name)
        prereq_test = self.check_preRequisite(TaskObject=Taskobject, api_action_address=api_action_address,
                                              dbname=dbname,
                                              table=table)
        logging.info('Pre-req for $s --> %s', this_function_name, prereq_test)
        if prereq_test:
            make_query = r"SELECT ComponentValue FROM [{0}].[dbo].[{1}] WHERE ComponentID = 'ManufacturerIdentifier'".format \
                (dbname, table)
            self.run_test(Taskobject=Taskobject, testname=this_function_name, api_URL=api_action_address,
                          db=dbname, table=table, datapoint_field=datapoint_field,
                          datapoint_value_field=datapoint_value_field, test_sqlQuery=make_query)

    def test_Dashboard_GMID(self, Taskobject, api_action_address, dbname, table, datapoint_field,
                            datapoint_value_field):
        this_function_name = sys._getframe().f_code.co_name
        logging.info('Runing pre-req check for %s', this_function_name)
        prereq_test = self.check_preRequisite(TaskObject=Taskobject, api_action_address=api_action_address,
                                              dbname=dbname,
                                              table=table)
        logging.info('Pre-req for $s --> %s', this_function_name, prereq_test)
        if prereq_test:
            make_query = r"SELECT ComponentValue FROM [{0}].[dbo].[{1}] WHERE ComponentID = 'ControllerGMID'".format \
                (dbname, table)
            self.run_test(Taskobject=Taskobject, testname=this_function_name, api_URL=api_action_address,
                          db=dbname, table=table, datapoint_field=datapoint_field,
                          datapoint_value_field=datapoint_value_field, test_sqlQuery=make_query)

    # def test_Dashboard_SupportedLevels(self, Taskobject, api_action_address, dbname, table, datapoint_field,
    #                         datapoint_value_field):
    #     logging.info('Test pre-req for test_Dashboard_SupportedLevels')
    #     prereq_test = self.check_preRequisite(TaskObject=Taskobject, api_action_address=api_action_address,
    #                                           dbname=dbname,
    #                                           table=table)
    #     logging.info('Pre-req for test_Dashboard_SupportedLevels %s', prereq_test)
    #     if prereq_test:
    #         logging.info('Testing test_Dashboard_SupportedLevels')
    #         make_query = r"SELECT ConfigValue FROM [{0}].[dbo].[{1}] WHERE ConfigID='LevelCountLimit'".format \
    #             (dbname, table)
    #         this_function_name = sys._getframe().f_code.co_name
    #         self.run_test(Taskobject=Taskobject, testname=this_function_name, api_URL=api_action_address,
    #                       db=dbname, table=table, datapoint=datapoint_field,
    #                       datapoint_value_field=datapoint_value_field, test_sqlQuery=make_query)


def main():
    TestApi = AuditUI_DataTest()
    TaskApi = API.API_AuditUI_process()

    TestApi.test_Dashboard_ManufactureCode(Taskobject=TaskApi, api_action_address='/dataservice/api/2/Components',
                                           dbname='misc',
                                           table='Component', datapoint_field='ManufacturerIdentifier', datapoint_value_field='s')
    TestApi.test_Dashboard_GMID(Taskobject=TaskApi, api_action_address='/dataservice/api/2/Components',
                                dbname='misc',
                                table='Component', datapoint_field='ControllerGMID', datapoint_value_field='s')
    # TestApi.test_Dashboard_SupportedLevels(Taskobject=TaskApi, api_action_address='/dataservice/api/2/Components',
    #                                        dbname='misc',
    #                                        table='Component', api_datapoint='LevelCountLimit')


if __name__ == "__main__":
    main()
