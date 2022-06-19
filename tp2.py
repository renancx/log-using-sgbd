import psycopg2     #biblioteca para fazer a conexao com o banco

#funcao para criar conexao no banco
def db_connect():
    connect = psycopg2.connect(

        host='localhost', 
        database='logtp2',
        user='postgres', 
        password='12345')
    return connect

#executar query
def execQuery(connect, sql):
    cur=connect.cursor()
    cur.execute(sql)
    connect.commit()

