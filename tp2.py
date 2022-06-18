import psycopg2     #biblioteca para fazer a conexao com o banco

#funcao para criar conexao no banco
def conecta_db():
    connect = psycopg2.connect(

        host='localhost', 
        database='logtp2',
        user='postgres', 
        password='12345')

    return connect

#tabelas do banco
class Linha:
    def init(user):
        user.id=0
        user.firstColumn=''

    def setId(user, id):
        user.id=id

    def setFirstColumn(user, firstColumn):
        user.firstColumn=firstColumn
