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

#checkpoints
commitedTransactions={}
checkpointStart= 0 #linha inicial do checkpoint

checkpointFuncional = False #nao teve checkpoint funcional
for line in range(len(log)-1,-1,-1):
	if 'CKPT' in log[line] and 'Start' in log[line]:
		checkpointStart=line
		for lineEndCkpt in range(len(log)-1,-1,-1):
			if 'End' in log[lineEndCkpt] and lineEndCkpt>line:
				checkpointFuncional=True #teve checkpoint funcional
				for lineCkpt in range(line,len(log)-1,1):
					if 'commit' in log[lineCkpt]:
						splitedCommit=log[lineCkpt].split(' ')
						commitedTransactions[splitedCommit[1][:-1]]='Nao visitado'
				break

lastStartLine=0
for line in range(len(log)-1,-1, -1):
	allStarts=True #encontrou todos os starts
	if 'unvisited' in commitedTransactions.values():
		allStarts=False #nao encontrou todos os starts
	if allStarts==True:
		break
	if 'start' in log[line] and 'CKPT' not in log[line]:
		splitedStart=log[line].split(' ')
		transaction=splitedStart[1][:-1]
		if transaction in commitedTransactions.keys():
			commitedTransactions[transaction]='visited'

	lastStartLine=line

transactionInependent=[] #transacao commitada independente de checkpoint
for line in range(0,len(log)-1,1):
	if 'commit' in log[line]:
		splitedCommit=log[line].split(' ')
		transactionInependent.append(splitedCommit[1][:-1])

#verificar se fez REDO
if checkpointFuncional==True:		
	print('Saida')
	for i in commitedTransactions.keys():
		print('Transacao',i,'realizou Redo')
	for line in range(lastStartLine, len(log)-1, 1):
		noMoreOrlessLine=log[line][1:-1]
		splitedLine=noMoreOrlessLine.split(',')
		if len(splitedLine)==4:
			if splitedLine[0] in commitedTransactions.keys():	
				sql='UPDATE log_table SET '+splitedLine[2]+ '='+splitedLine[3]+' WHERE id ='+splitedLine[1]
				execQuery(connect, sql)
else:
	print('Saida')
	for i in transactionInependent:
		print('A transacao ',i,' realizou REDO')
	for line in range(0, len(log)-1, 1):
		noMoreOrlessLine=log[line][1:-1]
		splitedLine=noMoreOrlessLine.split(',')
		if len(splitedLine)==4:
			if splitedLine[0] in transactionInependent:	
				sql='UPDATE log_table SET '+splitedLine[2]+ '='+splitedLine[3]+' WHERE id ='+splitedLine[1]
				execQuery(connect, sql)

#pegar as informacoes e mostrar o estado final do banco
cursor=connect.cursor()
query="select * from log_table"
cursor.execute(query)
logTestrecords=cursor.fetchall()
print('Estado final do banco de dados:')
print('', end = "")
for i in column:
	print(i+'' , end = "")
print('')

for row in logTestrecords:
	for i in row:
		print(i,'' , end = "")
	print('')

connect.close()
exit(0)