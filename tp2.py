import psycopg2     #biblioteca para fazer a conexao com o banco

#Funcao para criar conexao no banco
def conecta_db():
    connect = psycopg2.connect(

        host='localhost', 
        database='logtp2',
        user='postgres', 
        password='12345')

    return connect
