import logging
import pyodbc
import sys
from setup_File import Env_variable as config_variable


class VertexDatabase:
    cursor = None

    def __init__(self):
        """ constructor"""
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename=r'C:\LogPython\VertexDB.log',
                            filemode='w')
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        log_handler = logging.FileHandler(
            r'C:\LogPython\VertexDB.log', 'w', 'utf-8')
        log_handler.setLevel(logging.DEBUG)
        logging.info('Started at class VertexDatabase')

        """
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(funcName)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='myapp.log',
                            filemode='w')                
        """

        logging.info('Creating database connection to %s at server %s',
                     'Vertex', config_variable.get("db_server"))
        got_connection = self.database_connection()
        logging.info('Connected to database Vertex --> %s', got_connection)

    def database_connection(self):
        """
        Connect to database via prameters in configuration from imported setup_File
        :return: database_cursor of database
        """
        try:
            if config_variable.get("db_server") and config_variable.get("db_username") and config_variable.get("db_password"):
                db_connection = pyodbc.connect("DRIVER={{SQL Server}};SERVER={0}; database={1}; "
                                               "trusted_connection=yes;UID={2};PWD={3}".format(
                                                   config_variable.get(
                                                       "db_server"), 'Vertex',
                                                   config_variable.get(
                                                       "db_username"),
                                                   config_variable.get("db_password")))
                self.cursor = db_connection.cursor()
                logging.info(
                    'Got database connection to Vertex at %s', self.cursor)
                return self.cursor
            else:
                logging.warning(
                    'Cannot setup database connection to Vertex\n Missing parameter in Setup_File')
        except pyodbc.Error as E:
            logging.warning(
                'Cannot setup database connection to Vertex\n %s', E.message) 
        return None


    def __del__(self):
        """ destructor"""
        self.cursor.close()
        print "Closed"

    def execute_sql_query(self, sql_query):
        """
        Query database and fetch data
        :param sql_query: Sql text query
        :return: data
        """
        try:
            if not self.cursor:
                self.cursor = self.database_connection()

            self.cursor.execute(sql_query)
            data = self.cursor.fetchall()
            return data
        except Exception as E:
            logging.warning(
                'Problem with Vertex database database_cursor in execute query \n %s', E.message)
            return None


# def main():
#
#     vertex_db = VertexDatabase()
#     sql_query = r"SELECT * FROM [Vertex].[dbo].[Config]"
#     # print(config_variable.get("db_password"))
#
#     # print'Printing\n{}'.format(vertex_db.execute_sql_query(sql_query))
#     vertex_db.execute_sql_query(sql_query)
#
#     print 'bye'
#
#
# if __name__ == "__main__":
#     main()
