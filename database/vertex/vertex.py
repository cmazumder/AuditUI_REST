import logging
import pyodbc

from setup_File import Env_variable as config_variable


class VertexDatabase:
    cursor = None

    database_vertex = None
    database_vertex_cursor = None

    def __init__(self):
        """ constructor"""
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
        self.database_connection()
        logging.info('Connected to database Vertex; Cursor --> %s',
                     self.database_vertex)

    def database_connection(self):
        """
        Connect to database via prameters in configuration from imported setup_File
        :return: database_cursor of database
        """
        try:
            if config_variable.get("db_server") and config_variable.get("db_username") and config_variable.get(
                    "db_password"):
                connection_string = r"DRIVER={{SQL Server}};SERVER={0}; database={1}; trusted_connection=yes;UID={2};PWD={3}".format(
                    config_variable.get("db_server"), 'Vertex',
                    config_variable.get("db_username"),
                    config_variable.get("db_password"))

                self.database_vertex = pyodbc.connect(connection_string)

                logging.info(
                    'Database connection to Vertex at %s\t Cursor at %s', self.database_vertex, self.database_vertex.cursor())

                self.database_vertex_cursor = self.database_vertex.cursor()

            else:
                logging.warning(
                    'Cannot setup database connection to Vertex\n Missing parameter in Setup_File')
        except pyodbc.Error as E:
            logging.error(
                'Cannot setup database connection to Vertex\n %s', E.message)
        return None

    def __del__(self):
        """ destructor"""
        logging.warning(
            'Destroy Vertex --> %s', self.database_vertex)
        self.database_vertex.close()

    def execute_sql_query(self, sql_query):
        """
        Query database and fetch data
        :param sql_query: Sql text query
        :return: data
        """

        try:
            if self.database_vertex:
                self.database_vertex_cursor.execute(sql_query)
                data = self.database_vertex_cursor.fetchall()
                result_list = [x[0] for x in data]
                if result_list:
                    return result_list
        except pyodbc.Error as E:
            logging.error(
                'Problem with objects\'s vertex_cursor in execute query \n %s', E.args)
        return None
