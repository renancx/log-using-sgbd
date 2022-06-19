from sqlite3 import connect
import psycopg2     #biblioteca para fazer a conexao com o banco
from cmath import log

#funcao para criar conexao no banco
def db_connect():
    connect = psycopg2.connect(

        host='localhost', 
        database='logtp2',
        user='postgres', 
        password='12345')
    return connect

def db_run(sql):
    connect=db_connect()
    cursor=connect.cursor()
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except(Exception, psycopg2.DatabaseError) as error:
        connect.rollback()
        return 1

#tabelas do banco
class Linha:
    def init(user):
        user.id=0
        user.firstColumn=''
        user.secondColumn=''

    def setId(user, id):
        user.id=id

    def setFirstColumn(user, firstColumn):
        user.firstColumn=firstColumn

    def setSecondColumn(user, secondColumn):
        user.secondColumn=secondColumn

#log - abertura e leitura
def openLog(file):
    try:
        f = open(file, 'r') #abre para leitura
        print('File open')
        return f
    except:
        print('File error')
        
def showLog(f):
    for line in f:  #printar linha por linha
        print(line)