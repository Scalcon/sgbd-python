import sys
import DBconnection
import DBexport
import DBview
import getpass

class SysConfig:
     conn = None
     dbType = None
     view_range = 1000

def menu():
    print("Selecione uma das opções a seguir:")
    print("(1) Conectar a banco de dados;")
    print("(2) Mostrar banco de dados;")
    print("(3) Consultar tabela;")
    print("(4) Executar consulta em SQL;")
    print("(5) Exportar dados para arquivo JSON;")
    print("(6) Configurações;")
    print("(7) Sair")

def startConnection(config):
    print("Buscando dados de conexão...")
    jsonConn = DBconnection.loadJson()

    if jsonConn:
        print("Realizando conexão encontrada...")
        config.dbType = jsonConn.get('dbType')
        userName = jsonConn.get('user')
        userPassword = jsonConn.get('password')
        dbName = jsonConn.get('database')
        hostName = jsonConn.get('host')
        portName = int(jsonConn.get('port'))

        if config.dbType == 'mysql':
            config.conn = DBconnection.mysqlConnect(userName, userPassword, dbName, hostName, portName)
            config.dbType = 'mysql'
        elif config.dbType == 'postgresql':
            config.conn = DBconnection.postgresqlConnect(userName, userPassword, dbName, hostName, portName)
    else:
        print("Não foi encontrada nenhuma conexão realizada previamente.")


def exec(config):

    while True:
        menu()
        option = input("Opção: ")

        if option == '1':

                dbTypeNum = input("Digite (1) para banco MySQL ou (2) para PostgreSQL: ")

                host = 'localhost'
                port = 3306

                hostDefault = input("Host: ")
                portDefault = input("Porta: ")

                if hostDefault != '':
                    host = hostDefault

                if portDefault != '':
                    port = portDefault

                database = input("Nome do Banco: ")
                user = input("Usuário: ")
                pswd = getpass.getpass("Senha: ")

                if dbTypeNum == '1':
                    config.dbType = 'mysql'
                    config.conn =  DBconnection.mysqlConnect(user, pswd, database, host, port)
                elif dbTypeNum == '2':
                    config.dbType = 'postgresql'
                    config.conn =  DBconnection.postgresqlConnect(user, pswd, database, host, port)
                else:
                    print("Tipo de banco inválido.")

                if config.conn:
                    print("Conexão estabelecida.")
                    DBconnection.saveJson({'dbType': config.dbType, 'host': host, 'port': port,'database': database,'user': user, 'password': pswd})

        elif option == '2' and config.conn:
                DBview.view(config.conn, config.dbType)

        elif option == '3' and config.conn:
            table = input("Digite o nome da tabela: ")
            DBview.checkData(config.conn, table, config.view_range)

        elif option == '4' and config.conn:
            sql = input("Digite sua consulta em SQL: ")
            DBview.directQuery(config.conn, sql)

        elif option == '5' and config.conn:
            table = input("Digite o nome da tabela a ser exportada: ")
            cursor = config.conn.cursor()
            cursor.execute(f"SELECT * FROM {table}")
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            DBexport.exportJson(data, columns)

            print("Exportação concluída.")

        elif option == '6':
            #No momento a única coisa configurável pelo menu é o limite de visualização das tabelas, mas futuramente podem ser
            #adicionadas novas funções
            setting = input("Selecione o que deseja configurar:")
            print("(1) Limite de Visualização das Tabelas;")

            if setting == '1':
                config.view_range = input("Digite o novo limite máximo de busca:")

        elif option == '7':
            if config.conn:
                config.conn.close()
            print("Saindo...")
            sys.exit()
        else:
            print("Opção inválida. Tente novamente ou cheque sua conexão com o banco.") 


def main():
    config = SysConfig()

    startConnection(config)
    exec(config)               

if __name__ == "__main__":
    main()