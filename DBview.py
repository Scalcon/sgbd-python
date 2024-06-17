import mysql.connector 
import psycopg2

from prettytable import PrettyTable
from anytree import Node, RenderTree

def view( conn, dbType ):
    cursor = conn.cursor()

    if dbType == 'postgresql':
        cursor.execute( """
                       SELECT table_name
                       FROM information_schema.tables
                       WHERE table_schema = 'public'
                    """)
        
    elif dbType == 'mysql':
        cursor.execute("SHOW TABLES")

    tables = cursor.fetchall()
    
    root = Node("Database")
    for table in tables:
        print(f'Tabela: {table[0]}')

        cursor.execute("""
                       SELECT column_name, data_type, character_maximum_length, is_nullable
                       FROM INFORMATION_SCHEMA.COLUMNS 
                       WHERE table_name = '{table[0]'}
                    """)
        
        columns = cursor.fetchall()
        t = PrettyTable(['Column', 'Type','Size', 'Null'])

        tableNode = Node(table[0], parent = root)

        for column in columns:
            size = column[2] if len(column) > 2 else ''
            null = column[3] if len(column) > 3 else ''
            t.add_row([column[0], column[1], size, null])

            Node(f'{column[0]}: column[1]', parent = tableNode)
        print(t)

        if dbType == 'postgresql':
            cursor.execute(f"""
                        SELECT kcu.column_name
                        FROM information_schema.table_constraints tc 
                        JOIN information_schema.key_column_usage kcu 
                        ON tc.constraint_name = kcu.constraint_name
                        WHERE tc.table_name = '{table[0]}' AND tc.constraint_type = 'PRIMARY KEY'
                    """)
        elif dbType == 'mysql':
            cursor.execute(f"""
                        SELECT column_name
                        FROM information_schema.key_column_usage
                        WHERE table_name = '{table[0]}' AND constraint_name = 'PRIMARY'
                    """)
        
        primaryKeys = cursor.fetchall()
        if primaryKeys:
            print("Primary Keys:", ", ".join([chave[0] for chave in primaryKeys]))
        print("\n")

def checkData(conn, table, range = 1000):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table} LIMIT {range}")
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    t = PrettyTable(columns)
    for row in data:
        t.add_row(row)
    print(t)

def directQuery(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    t = PrettyTable(columns)
    for row in data:
        t.add_row(row)
    print(t)