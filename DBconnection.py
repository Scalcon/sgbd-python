import mysql.connector 
import psycopg2
import json

from mysql.connector import Error
from psycopg2 import OperationalError

def mysqlConnect( userName, userPassword, dbName, hostName = None, portName = None ):
    connection = None

    try:
        connection = mysql.connector.connect(
            host = hostName,
            port = portName,
            user = userName,
            passwd = userPassword,
            database = dbName
        )
    except Error as e:
        print(f'Erro de conexao: {e}')
    return connection

def postgresqlConnect( userName, userPassword, dbName, hostName = None, portName = None ):
    connection = None
    try:
        connection = psycopg2.connect(
            host = hostName,
            port = portName,
            user = userName,
            passwd = userPassword,
            database = dbName
        )
        
    except OperationalError as e:
        print(f'Erro de conexao {e}')
    return connection

def loadJson( file = 'connections.json' ):
    with open(file, 'r') as f:
        return json.load(f)

def loadJson( dados, file = 'connections.json' ):
    with open(file, 'w') as f:
        return json.dump(dados, f)