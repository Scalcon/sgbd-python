import mysql.connector 
import psycopg2

from prettytable import PrettyTable
from anytree import Node, RenderTree

def view(conn, dbType):
    cursor = conn.cursor()

    root = Node("Database")

    if dbType == 'postgresql':
        cursor.execute("""
                       SELECT table_name
                       FROM information_schema.tables
                       WHERE table_schema = 'public'
                       AND table_type = 'BASE TABLE'
                    """)
        tables = cursor.fetchall()

        cursor.execute("""
                       SELECT table_name
                       FROM information_schema.views
                       WHERE table_schema = 'public'
                    """)
        views = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            table_node = Node(table_name, parent=root)

            cursor.execute(f"""
                           SELECT column_name, data_type, character_maximum_length, is_nullable
                           FROM information_schema.columns 
                           WHERE table_name = '{table_name}'
                        """)
            columns = cursor.fetchall()

            t = PrettyTable(['Column', 'Type', 'Size', 'Null'])
            for column in columns:
                size = column[2] if len(column) > 2 else ''
                null = column[3] if len(column) > 3 else ''
                t.add_row([column[0], column[1], size, null])
                Node(f'{column[0]}: {column[1]}', parent=table_node)
            print(f'Table: {table_name}')
            print(t)

        for view in views:
            view_name = view[0]
            view_node = Node(view_name, parent=root)
            print(f'View: {view_name}')

    elif dbType == 'mysql':
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
        views = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            table_node = Node(table_name, parent=root)

            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()

            t = PrettyTable(['Field', 'Type', 'Null', 'Key', 'Default', 'Extra'])
            for column in columns:
                t.add_row(column)
                Node(f'{column[0]}: {column[1]}', parent=table_node)
            print(f'Table: {table_name}')
            print(t)

        for view in views:
            view_name = view[0]
            view_node = Node(view_name, parent=root)
            print(f'View: {view_name}')

    for pre, fill, node in RenderTree(root):
        print(f"{pre}{node.name}")

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