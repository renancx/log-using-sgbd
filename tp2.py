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

#abre o arquivo txt
fileName='entradaLog.txt'
try:
    file=open(fileName, "r", encoding="utf-8")
except:
    print('Erro na abertura do arquivo')
    exit(0)

fileArray=file.read().splitlines()

log=[]
bd_inicial=[]

for i in fileArray:
	if(i.startswith("<")):
		log.append(i)
	else:
		bd_inicial.append(i)

numEspacos=0
for j in bd_inicial:
	if(j==''):
		numEspacos+=1	
for i in range(0,numEspacos,1):
	bd_inicial.remove('')

connect=db_connect()

bd_vetor=[]
for line in bd_inicial:
    splitedLine = line.split('=')
    for i in range(0,len(splitedLine),1):
        splitedLine[i]=splitedLine[i].strip()
        if ',' in splitedLine[i]:
            splitedLine[i]=splitedLine[i].split(',')
    splitedLine.append('Nao inserido')

    bd_vetor.append(splitedLine)

#excluindo a tabela se ela ja existe
sql='DROP TABLE IF EXISTS log_table'
execQuery(connect, sql)

column=[]
sqlColumns=''

for item in range(0,len(bd_vetor),1):
    if bd_vetor[item][0][0] not in column:
        sqlColumns=sqlColumns+','+bd_vetor[item][0][0]+' INT'
        column.appen(bd_vetor[item][0][0])

#criar tabela
sql='CREATE TABLE log_table (id INT'+sqlColumns+')'
execQuery(connect,sql)

zerosNum=''
for i in range(0,len(column),1):
	zerosNum = zerosNum+',0'

for item in range(0,len(bd_vetor),1):
    if bd_vetor[item][2]=='Nao inserido':
        sql = 'INSERT INTO log_table VALUES ('+bd_vetor[item][0][1]+zerosNum+')'
        execQuery(connect, sql)
        for itemTemp in range(0,len(bd_vetor),1):
            if bd_vetor[itemTemp][0][1]==bd_vetor[item][0][1]:
                bd_vetor[itemTemp][2]='Inserido'

for item in range(0,len(bd_vetor),1):
    sql='UPDATE log_table SET id = '+bd_vetor[item][0][1]+', '+bd_vetor[item][0][0]+' = '+bd_vetor[item][1]+' WHERE id ='+bd_vetor[item][0][1]
    execQuery(connect, sql)