'''
未消除左递归，终结符与输入符仅支持单子符
S->ABc
A->a|ε
B->b|ε
'''

'''
A->BCc|gDB
B->bCDE|ε
C->DaB|ca
D->dD|ε
E->gAf|c
'''

'''
S->Ab 
A->a|B|ε
B->b|ε
'''

'''
E->TY
Y->+TY|ε
T->FZ
Z->*FZ|ε
F->(E)|i
'''

'''
S->T
T->(S)ST|ε
'''

'''
S->iEtST|a
T->εS|ε
E->b
'''

'''
S->(S)S|ε
'''

'''
E->TY
Y->+TY|ε
T->FX
F->(E)|i|-F
X->*FX|ε
'''


import copy

LAN = {}
FIRST = {}
FOLLOW = {}
FOLLOWF = {}
SELECT = {}
TABLE = []
NONCH = []
INCH = []
FIRSTCH = []

def isterminal(ch):
	if not (ch >= "A" and ch <="Z"):
		return True
	else:
		return False

def strcmp(x, y):
	if x < y:
		return True
	else:
		return False
	
def getlan():
	global FIRSTCH
	print("文法n行，->区分左右，$为终结符，ε为空串，大写非终结符，小写终结符，S一般为开始符号(放在第一行)，|是或：")
	path = "ll1test.txt"
	infile = open(path, 'r')
	i = 0
	for line in infile.readlines():
		splitlist = line[3:].replace("\n", "").strip().split("|")
		if line[0] in LAN:
			LAN[line[0]].extend(splitlist)
			LAN[line[0]] = list(set(LAN[line[0]]))
		else:
			LAN[line[0]] = splitlist
		FIRST[line[0]] = []
		FOLLOW[line[0]] = []
		FOLLOWF[line[0]] = False
		if i == 0:
			FOLLOW[line[0]] = ['$']
			FIRSTCH = line[0]
			i += 1

def first():
	'''
	1，先加入终结符
	2，如果出现非终结符
	若X->BCD,先检测到B，则先将first（B）中所有元素（除了空集）加入first（X），若first（B）中不存在空集, 即停止检测，若存在则向B的后面查看，将first（C）中所有元素（除了空集）加入first（X），再判断first（C）中是否有e…直到最后，若D之前的所有非终结符的first集中都含有e,就检测到D时，将first（D）也加入first（X），若first（D）中含有e,则将 e加入first（X）
	'''
	for i in FIRST:
		FIRST[i] = getfirst(i)
	
	for i in FIRST:
		FIRST[i].sort()

def getfirst(tar):
	for i in LAN[tar]:
		if len(i) == 1:
			if(isterminal(i)):
				FIRST[tar].append(i)	#是终结符直接加入first集
			else:
				FIRST[tar].extend(getfirst(i))	#非终结符则把这个非终结符的first集加入first集
		else:
			for index, j in enumerate(i):
				if j == 'ε':
					FIRST[tar].append(j)
					continue
				elif isterminal(j):
					FIRST[tar].append(j)
					break
				else:
					tmp = copy.deepcopy(getfirst(j))
					if 'ε' in tmp:
						if index == len(i) - 1:
							FIRST[tar].extend(tmp)
						else:
							tmp.remove('ε')
							FIRST[tar].extend(tmp)
					else:
						FIRST[tar].extend(tmp)
						break

	FIRST[tar] = list(set(FIRST[tar]))	#去重
	return FIRST[tar]

def calfirst(string):
	if string == 'ε':
		return ['ε']
	elif len(string) == 1 and isterminal(string):
		return [string]
	tmp = []
	for i in string:
		if isterminal(i):
			tmp.append(i)
			return tmp
		else:
			t = copy.deepcopy(FIRST[i])
			if 'ε' in t:
				t.remove('ε')
				tmp.extend(t)
			else:
				tmp.extend(t)
				return tmp
	return tmp

def follow():
	for i in FOLLOW:
		FOLLOW[i] = getfollow(i)
		
	for i in FOLLOW:
		FOLLOW[i].sort()
	
def getfollow(tar):
	for i in LAN:
		p = LAN[i]
		for j in p:
			j = list(j)
			for index, k in enumerate(j):		#在所有产生式中查找tar
				if k == tar:
					'''
					情况(2) A->αBβ，把FIRST(β)加入FOLLOW(B)，需连续处理
					'''
					if index < len(j) - 1:
						for index1 in range(index + 1, len(j)):
							if j[index1] == 'ε':
								continue
							elif isterminal(j[index1]):
								FOLLOW[tar].append(j[index1])
								break
							else:	#如果是非终结符
								tmp = copy.deepcopy(FIRST[j[index1]])
								if 'ε' in tmp:
									flag = True
									tmp.remove('ε')
								else:
									flag = False
								FOLLOW[tar].extend(tmp)
								'''
								情况(3) A->αBβ，把FIRST(β)包含ε，那么FOLLOW(A)加入FOLLOW(B)中
								'''
								if flag == True:
									pass
								else:
									break
							if index1 == len(j) - 1:
								tmp = copy.deepcopy(FIRST[j[index1]])
								if 'ε' in tmp:
									if tar != i:
										FOLLOW[tar].extend(getfollow(i))
								
					elif index == len(j) - 1:
						'''
						情况4
						'''
						if tar != i:
							FOLLOW[tar].extend(getfollow(i))

	FOLLOW[tar] = list(set(FOLLOW[tar]))
	FOLLOWF[tar] = True
	return FOLLOW[tar]

def select():
	SELECT = {}
	for i in LAN:
		p = LAN[i]
		for j in p:
			lan = i + '->' + j
			SELECT[lan] = []
			tmp = calfirst(j)
			for k in tmp:
				if k == 'ε':
					for l in FOLLOW[i]:
						SELECT[lan].append(l)
				else:
					SELECT[lan].append(k)
	
	for i in SELECT:
		SELECT[i] = list(set(SELECT[i]))
		SELECT[i].sort()
		
	return SELECT

def table():
	flag = True
	#NONCH/INCH 为表格行列(非终结符，输入符号)
	for i in FIRST:
		NONCH.append(i)
	
	for i in LAN:
		p = LAN[i]
		for j in p:
			j = list(j)
			for k in j:
				if k not in INCH and isterminal(k):
					INCH.append(k)
	if 'ε' in INCH:
		INCH.remove('ε')
	
	NONCH.sort()
	INCH.sort()
	INCH.append('$')
	TABLE = [[None for i in range(len(INCH))] for j in range(len(NONCH))]
	
	for i in LAN:
		p = LAN[i]
		for j in p:
			lan = i + '->' + j
			tmp = calfirst(j)
			for k in tmp:
				if k == 'ε':
					for l in FOLLOW[i]:
						if TABLE[NONCH.index(i)][INCH.index(l)] != None:
							print("冲突！")
							flag = False
						TABLE[NONCH.index(i)][INCH.index(l)] = lan
				else:
					if TABLE[NONCH.index(i)][INCH.index(k)] != None:
						print("冲突！")
						flag = False
					TABLE[NONCH.index(i)][INCH.index(k)] = lan
	
	return TABLE, flag

def analyse(string, TABLE):
	print('%-10s' % "序号", end = "")
	print('%-10s' % "分析栈", end = "")
	print('%-10s' % "输入栈", end = "")
	print('%-10s' % "动作")
	Istack = list(string)
	Istack.append('$')
#	print(Istack)
#	print(Istack[1:])
#	print(FIRSTCH)
	Analyse = [FIRSTCH, '$']
	i = 1
	while Analyse != ['$']:
		sa = ''
		for k in Analyse:
			sa += k
		si = ''
		for k in Istack:
			si += k
		print('%-10s' % i, end = "")
		print('%-10s' % sa, end = "")
		print('%-10s' % si, end = "")

		if not isterminal(Analyse[0]):
			if Analyse[0] in NONCH:
				posi = NONCH.index(Analyse[0])
			else:
				print('%-10s' % "分析失败！")
				return
			if Istack[0] in INCH:
				posj = INCH.index(Istack[0])
			else:
				print('%-10s' % "分析失败！")
				return
			print('%-10s' % TABLE[posi][posj])
			if TABLE[posi][posj] == None:
				print('%-10s' % "分析失败！")
				return
			else:
		#		print(TABLE[posi][posj])
				p = TABLE[posi][posj].index('>')
				s = TABLE[posi][posj][p+1:]
				s = list(s)
				while 'ε' in s:
					s.remove('ε')
				Analyse = s + Analyse[1:]
		#		print(Analyse)
		else:
			if Analyse[0] == Istack[0]:
				print('%-10s' % "匹配")
				Analyse = Analyse[1:]
				Istack = Istack[1:]
			else:
				print('%-10s' % "分析失败！")
				return
		i += 1
	if Analyse == ['$']:
		sa = ''
		for k in Analyse:
			sa += k
		si = ''
		for k in Istack:
			si += k
		print('%-10s' % i, end = "")
		print('%-10s' % sa, end = "")
		print('%-10s' % si, end = "")
		if len(Istack) == 1:
			print('%-10s' % "接受")
		else:
			print('%-10s' % "失败")
	return


def main():
	getlan()
	print(LAN)
	first()
	print("FIRST集：", FIRST)
	follow()
	follow()
	print("FOLLOW集：", FOLLOW)
	SELECT = select()
	print("SELECT集：", SELECT)
	TABLE, flag = table()
	print("LL1分析表：")
	print('%-10s' % "", end = "")
	for i in INCH:
		print('%-10s' % i, end = "")
	print()
	for indexi, i in enumerate(NONCH):
		print('%-10s' % i, end = "")
		for j in TABLE[indexi]:
			if j != None:
				print('%-10s' % j, end = "")
			else:
				print('%-10s' % "", end = "")
		print()
	
	if not flag:
		print()
		print("因为有冲突，所以没有分析")
		print("但我还是尽量分析下")
		string = input("请输入一个要分析的字符串：")
		analyse(string, TABLE)
	else:
		print()
		print("接下来分析字符串")
		string = input("请输入一个要分析的字符串：")
		analyse(string, TABLE)
	
	
if __name__ == '__main__':
	main()