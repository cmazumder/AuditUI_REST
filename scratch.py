import requests, json, pyodbc
# import pyodbc.Cursor as cursor
from requests.auth import HTTPBasicAuth
import logging

def connect_db(server, database, username, password):
    # cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=server;DATABASE=database;UID=username;PWD=password')
    # cnxn = pyodbc.connect(
    #   'DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cnxn = pyodbc.connect("DRIVER={{SQL Server}};SERVER={0}; database={1}; \
       trusted_connection=yes;UID={2};PWD={3}".format(server, database, username, password))
    cursor = cnxn.cursor()
    return cursor

def get_response(string):
    response = requests.get(string, auth=('retail1', 'Retail1'), verify=False)
    if response.status_code != 200:
        raise ApiError('GET /tasks/ {}'.format(response.status_code))
    else:
        for item in response.json():
            print'{}'.format(item)
    return response.json()


server = r'172.26.18.110\SQLEXPRESS'
database = r'misc'
username = r'sa'
password = r'Password1'
lnk = r'http://172.26.18.110/dataservice/api/2/Components'

cursor = connect_db(server, database, username, password)

print cursor


def execute_query(sqlQuery):
    cursor.execute(sqlQuery)
    # for row in cursor:
    #     print (row)
    return cursor

# sql_query = r"SELECT ComponentValue FROM [misc].[dbo].[Component] WHERE ComponentID = 'ManufacturerIdentifier'"
sql_query = r"SELECT * FROM [misc].[dbo].[Component]"
# sql_query = r"SELECT * FROM [vertex].[dbo].[EGM]"

# execute_query(sqlQuery=sql_query)
response = get_response(lnk)
print 'done'

def find_macth(response, value):
    for item in response:
        for k, v in item.items():
            if k == 'ComponentValue':
                REST_Value = v
            if k == 'ComponentId':
                if v == 'ManufacturerIdentifier':
                    REST_ID = v
                    print REST_Value
                    break;

