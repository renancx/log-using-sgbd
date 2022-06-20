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