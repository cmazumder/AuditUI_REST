import logging
import pyodbc
import sys
from setup_File import Env_variable as config_variable


class MiscDatabase:
    database_misc = None
    database_misc_cursor = None

    def __init__(self):
        """ constructor"""
        # logging.basicConfig(level=logging.DEBUG,
        #                     format='%(asctime)s %(levelname)-8s %(message)s',
        #                     datefmt='%a, %d %b %Y %H:%M:%S',
        #                     filename=r'C:\LogPython\MiscDB.log',
        #                     filemode='w')
        # logger = logging.getLogger(__name__)
        # logger.setLevel(logging.DEBUG)
        # log_handler = logging.FileHandler(
        #     r'C:\LogPython\MiscDB.log', 'w', 'utf-8')
        # log_handler.setLevel(logging.DEBUG)
        logging.info('Started at class MiscDatabase')

        """
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(funcName)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='myapp.log',
                            filemode='w')                
        """

        logging.info('Creating database connection to %s at server %s',
                     'Misc', config_variable.get("db_server"))
        self.database_connection()
        logging.info('Connected to database Misc; Cursor --> %s',
                     self.database_misc)

    def database_connection(self):
        """
        Connect to database via prameters in configuration from imported setup_File
        :return: database_cursor of database
        """
        try:
            if config_variable.get("db_server") and config_variable.get("db_username") and config_variable.get("db_password"):
                connection_string = r"DRIVER={{SQL Server}};SERVER={0}; database={1}; trusted_connection=yes;UID={2};PWD={3}".format(
                    config_variable.get("db_server"), 'Misc',
                    config_variable.get("db_username"),
                    config_variable.get("db_password"))

                self.database_misc = pyodbc.connect(connection_string)

                logging.info(
                    'Database connection to Misc at %s\t Cursor at %s', self.database_misc, self.database_misc.cursor())

                self.database_misc_cursor = self.database_misc.cursor()

            else:
                logging.warning(
                    'Cannot setup database connection to Misc\n Missing parameter in Setup_File')
        except pyodbc.Error as E:
            logging.warning(
                'Cannot setup database connection to Misc\n %s', E.message)
        return None

        # self.db_connection = pyodbc.connect("DRIVER={{SQL Server}};SERVER={0}; database={1}; "
        #                                         "trusted_connection=yes;UID={2};PWD={3}".format(
        #         config_variable.get("db_server"), database, config_variable.get("db_username"), config_variable.get("db_password")))

    def __del__(self):
        """ destructor"""
        logging.warning(
            'Destroy Misc --> %s', self.database_misc)
        self.database_misc.close()
        print "Closed"

    def execute_sql_query(self, sql_query):
        """
        Query database and fetch data
        :param sql_query: Sql text query
        :return: data
        """

        try:
            if self.database_misc:
                self.database_misc_cursor.execute(sql_query)
                data = self.database_misc_cursor.fetchall()
                result_list = [x[0] for x in data]
                if result_list:
                    return result_list
        except pyodbc.Error as E:
            logging.warning(
                'Problem with objects\'s database_cursor in execute query \n %s', E.args)
        return None


# def main():
#
#     misc_db = MiscDatabase()
#     sql_query = r"SELECT * FROM [misc].[dbo].[Component]"
#     # print(config_variable.get("db_password"))
#
#     # print'Printing\n{}'.format(misc_db.execute_sql_query(sql_query))
#     misc_db.execute_sql_query(sql_query)
#
#     print 'bye'
#
#
# if __name__ == "__main__":
#     main()
