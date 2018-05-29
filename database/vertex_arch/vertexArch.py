import logging
import pyodbc
import sys
from setup_File import Env_variable as config_variable


class VertexArchDatabase:
    cursor = None

    def __init__(self):
        """ constructor"""
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename=r'C:\LogPython\DB.log',
                            filemode='w')
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        log_handler = logging.FileHandler(
            r'C:\LogPython\DB.log', 'w', 'utf-8')
        log_handler.setLevel(logging.DEBUG)
        logging.info('Started at class VertexArchDatabase')

        """
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(funcName)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='myapp.log',
                            filemode='w')                
        """

        logging.info('Creating database connection to %s at server %s',
                     'VertexArch', config_variable.get("db_server"))
        got_connection = self.database_connection()
        logging.info('Connected to database VertexArch --> %s', got_connection)

    def database_connection(self):
        """connect to database via parameters in configuration from imported setup_File """
        try:
            if config_variable.get("db_server") and config_variable.get("db_username") and config_variable.get("db_password"):
                db_connection = pyodbc.connect("DRIVER={{SQL Server}};SERVER={0}; database={1}; "
                                               "trusted_connection=yes;UID={2};PWD={3}".format(
                                                   config_variable.get(
                                                       "db_server"), 'VertexArch',
                                                   config_variable.get(
                                                       "db_username"),
                                                   config_variable.get("db_password")))
                self.cursor = db_connection.cursor()
                logging.info(
                    'Got database connection to VertexArch at %s', self.cursor)
                return self.cursor
            else:
                logging.warning(
                    'Cannot setup database connection to VertexArch\n Missing parameter in Setup_File')
        except pyodbc.Error as E:
            logging.warning(
                'Cannot setup database connection to VertexArch\n %s', E.message)
        return None

        # self.db_connection = pyodbc.connect("DRIVER={{SQL Server}};SERVER={0}; database={1}; "
        #                                         "trusted_connection=yes;UID={2};PWD={3}".format(
        #         config_variable.get("db_server"), database, config_variable.get("db_username"), config_variable.get("db_password")))

    def __del__(self):
        """ destructor"""
        self.cursor.close()
        print "Closed"

    def execute_sql_query(self, sql_query):
        """ query database and getch entire table for now """
        try:
            if not self.cursor:
                self.cursor = self.database_connection()

            self.cursor.execute(sql_query)
            # for row in self.cursor:
            #     print (row)
            #     return row
            data = self.cursor.fetchall()
            for row in data:
                print row
        except Exception as E:
            logging.warning(
                'Problem with objects\'s cursor in execute query \n %s', E.message)
            print E


def main():

    vertexArch_db = VertexArchDatabase()
    sql_query = r"SELECT * FROM [VertexArch].[Archive].[AuditDetail]"
    # print(config_variable.get("db_password"))

    # print'Printing\n{}'.format(vertexArch_db.execute_sql_query(sql_query))
    vertexArch_db.execute_sql_query(sql_query)

    print 'bye'


if __name__ == "__main__":
    main()
