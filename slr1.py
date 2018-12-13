'''
E->E+T|T
T->T*F|F
F->(E)|A
A->1A|2A|3A|4A|5A|6A|7A|8A|9A|0|1|2|3|4|5|6|7|8|9
'''

'''
A->(A)A|ε
'''

'''
45
S->a|V=E
V->a
E->V|n
'''

#可以消除很简单的左递归，但复杂的消除不了，而且左递归只有五个格子YXWVU，ZYXWVU都不能用

import copy

FIRST = {}
FOLLOW = {}
FOLLOWF = {}
LAN = {}
LL1LAN = {}
EXLAN = []
ITEM = []
DFA = []	#[0]为代表 [1]为图上连线
TABLE = []
CH = []
DICT = {}
ACC = ''

def isterminal(ch):
	if not (ch >= "A" and ch <="Z"):
		return True
	else:
		return False

def first():
	for i in FIRST:
		FIRST[i] = getfirst(i)
	
	for i in FIRST:
		FIRST[i].sort()

def getfirst(tar):
	for i in LL1LAN[tar]:
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
	
def follow():
	for i in FOLLOW:
		FOLLOW[i] = getfollow(i)
		
	for i in FOLLOW:
		FOLLOW[i].sort()
	
def getfollow(tar):
	for i in LL1LAN:
		p = LL1LAN[i]
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

def closure(string):
	if string.index('.') == len(string) - 1:
		return [string]
#	item = ITEM
	tmp = [string]
	index = string.index('.')
	k = string[index + 1:]
	if not isterminal(k[0]):
		for i in ITEM:
			if i[0] == k[0]:
				if i[3] == '.':
					tmp.append(i)
					if len(i) > 4:
						if not isterminal(i[4]):
							if i != string:
								tmp.append(closure(i))
	k = []

	for i in tmp:
		if type(i) != str:
			for j in i:
				if j not in k:
					k.append(j)
		else:
			if i not in k:
				k.append(i)
	tmp = k

	return tmp

def getdfa():
	#搜索item['Z'][0]的闭包，加入状态0
	cl = closure(ITEM[0])
	DFA.append([cl, []])
	
	l = 0
	while l < len(DFA):
		'''
		if (DFA[l][0][0].index('.') == len(DFA[l][0][0]) - 1) and (len(DFA[l][0]) == 1):
			l += 1
			continue
		'''
		vis = [False for i in range(len(DFA[l][0]))]
		for indexi, i in enumerate(DFA[l][0]):
			if (i.index('.') == len(i) - 1):
				continue
			p = i.index('.')

			tmp = []
			posi = i.index('.')
			if len(i) > 4:
				ch = i[posi + 1]
			else:
				ch = ""
			for indexj, j in enumerate(DFA[l][0]):
				if not vis[indexj]:
					posj = j.index('.')
					if len(j) - 1 > posj:
						if j[posj + 1] == ch:
							newstr = j[:posj] + j[posj + 1] + '.' + j[posj + 2:]
							tmp.extend(closure(newstr))
							vis[indexj] = True
				
			if tmp != []:		
				pos = -1
				for index, j in enumerate(DFA):
					if j[0] == tmp:
						pos = index
				if pos == -1:
					DFA.append([tmp, []])
					DFA[l][1].append([ch, len(DFA) - 1])
				else:
					DFA[l][1].append([ch, pos])

		l += 1
		
def table():
	length = len(DFA)
	tmp = []
	for i in LAN:
		p = LAN[i]
		for j in p:
			for k in j:
				if isterminal(k):
					if k not in tmp:
						tmp.append(k)
	if 'ε' in tmp:
		tmp.remove('ε')
	tmp.sort()
	tmp.append('$')
	l = len(tmp)
	tmp1 = []
	for i in LAN:
			p = LAN[i]
			for j in p:
				for k in j:
					if not isterminal(k):
						if k not in tmp1:
							tmp1.append(k)
	
	print(LAN)
	print(LL1LAN)
	print(tmp1)

	tmp.extend(tmp1)
	CH.extend(tmp)
	TABLE = [[None for i in range(len(CH))] for j in range(len(DFA))]
	
	for index, i in enumerate(DFA):
		if len(i[1]) == 0:
			#由于代码原因，ITEM[1]被设定为acc项
			if(ITEM[1] == i[0][0]):
				p = CH.index('$')
				TABLE[index][p] = 'acc'
			else:
				for k in range(len(i[0])):
					t = i[0][k][:-1]
					p = EXLAN.index(t)
					for j in range(l):
						if CH[j] in FOLLOW[i[0][k][0]]:
							if TABLE[index][j] == None:		#SLR1可能会产生规约-规约冲突(?)，这里暂时先这么做
								TABLE[index][j] = 'r' + str(p)
		else:
			for j in i[1]:
				p = CH.index(j[0])
				if isterminal(j[0]):
					t = 's' + str(j[1])
				else:
					t = str(j[1])
				TABLE[index][p] = t
			
			for j in i[0]:
				if(ITEM[1] == j):
					p = CH.index('$')
					TABLE[index][p] = 'acc'
					break
				if(j.index('.') == len(j) - 1):
					j = j[:-1]
					if j in EXLAN:
						p = EXLAN.index(j)
						for k in range(l):
							if TABLE[index][k] == None:
								if CH[k] in FOLLOW[i[0][0][0]]:
									TABLE[index][k] = 'r' + str(p)
				
	return TABLE
	

def getlan():
	path = "slr1test.txt"
	infile = open(path, 'r')
	i = 0
	for line in infile.readlines():
		splitlist = line[3:].replace("\n", "").strip().split("|")
		if line[0] in LAN:
			LAN[line[0]].extend(splitlist)
			LAN[line[0]] = list(set(LAN[line[0]]))
		else:
			if i == 0:
				LAN['Z'] = [line[0]]
				ACC = line[0]
				LAN[line[0]] = splitlist
				FIRST['Z'] = []
				FOLLOW['Z'] = ['$']
				EXLAN.append('Z->' + line[0])
				ITEM.append('Z->.' + line[0])
				ITEM.append('Z->' + line[0] + '.')
				i += 1
			else:
				LAN[line[0]] = splitlist
				
		FIRST[line[0]] = []
		FOLLOW[line[0]] = []
		FOLLOWF[line[0]] = False

		for j in splitlist:
			if j != 'ε':
				EXLAN.append(line[0] + '->' + j)
				for k in range(len(j)):
					ITEM.append(line[0] + '->' + j[:k] + '.' + j[k:])
				ITEM.append(line[0] + '->' + j + '.')
			else:
				ITEM.append(line[0] + '->' + '.')
				EXLAN.append(line[0] + '->')

def getll1lan():
	strlist = ['Y', 'X', 'W', 'V', 'U']
	tmplan = {}
	pos = 0
	for i in LL1LAN.keys():
		p = LL1LAN[i]
		vis = [False for i in range(len(p))]
		for indexj, j in enumerate(p):
			if i == j[0]:	#左递归
				for indexk, k in enumerate(p):
					if i != k[0] and vis[indexk] == False:
						DICT[i] = strlist[pos]
						p[indexk] += strlist[pos]
						tmplan[strlist[pos]] = [j[1:] + strlist[pos], 'ε']
						FIRST[strlist[pos]] = []
						FOLLOW[strlist[pos]] = []
						FOLLOWF[strlist[pos]] = False
						pos += 1
						vis[indexk] = True
						break
				p.remove(j)
				
	for i in tmplan:
		LL1LAN[i] = tmplan[i]
					

def analyse(string, TABLE):
	print('%-10s' % "序号", end = "")
	print('%-16s' % "分析栈", end = "")
	print('%-16s' % "输入栈", end = "")
	print('%-16s' % "动作")
	Analyse = [['$', 0]]
	Istack = list(string)
	Istack.append('$')
	index = 1
	state = 0
	length = len(DFA)
	while True:
		if TABLE[state][CH.index('$')] == 'acc' and Istack == ['$']:
			print('%-10s' % index, end = "")
			s = ''
			for i in Analyse:
				s += i[0]
				s += str(i[1])
			print('%-16s' % s, end = "")
			
			s = ''
			for i in Istack:
				s += i
			print('%-16s' % s, end = "")
			if Istack == ['$']:
				print('%-16s' % "Acc")
			else:
				print('%-16s' % "分析失败！")
			return
			
		print('%-10s' % index, end = "")
		s = ''
		for i in Analyse:
			s += i[0]
			s += str(i[1])
		print('%-16s' % s, end = "")
		
		s = ''
		for i in Istack:
			s += i
		print('%-16s' % s, end = "")

		r = -1
		ss = -1
		sch = ''
		for indexi, i in enumerate(TABLE[state]):
			if i != None:
				if i[0] == 'r':
					r = int(i[1:])
				elif i[0] == 's':
					ss = int(i[1:])
					sch = CH[indexi]

		if r == -1:		#非规约
			try:
				pos = CH.index(Istack[0])
			except:
				print("分析失败！")
				return
				
			if TABLE[state][pos] == None:
				print("分析失败！")
				return
				
	#		print('shift', Istack[0])
			s = 'shift' + ' ' + Istack[0]
			print('%-16s' % s)
			
			k = 0
			if TABLE[state][pos][0] == 's':
				k = int(TABLE[state][pos][1:])
			else:
				k = int(TABLE[state][pos])
				
			state = k
			Analyse.append([Istack[0], state])

			Istack = Istack[1:]
			
		else:
			#待规约，也有可能出现s的情况，需特殊判断
			if ss != -1:
				#要移入的是Istack[0]，所以查TABLE[state][CH.index(Istack[0])] 是不是 's?'
				try:
					pos = CH.index(Istack[0])
				except:
					print("分析失败！")
					return
					
				if TABLE[state][pos] == None:
					print("分析失败！")
					return
					
				#		if sch == Istack[0]:	
				if TABLE[state][pos][0] == 's':
					s = 'shift' + ' ' + Istack[0]
					print('%-16s' % s)
					
					k = 0
					if TABLE[state][pos][0] == 's':
						k = int(TABLE[state][pos][1:])
					else:
						k = int(TABLE[state][pos])
						
					state = k
					Analyse.append([Istack[0], state])

					Istack = Istack[1:]
					index += 1
					continue
					
			#规约
			k = EXLAN[r]
			p = k.index('>')
			K = k[0]
			k = k[p+1:]
				
			s = 'reduce' + ' ' + str(r)
			print('%-16s' % s)
			
	#		print(Analyse)
			if k != '':
				Analyse = Analyse[:-len(k)]
	#		print(Analyse)
			state = Analyse[-1][1]
			
			if TABLE[state][CH.index(K)] == None:
				print("分析失败！")
				return
			
			Analyse.append([K, int(TABLE[state][CH.index(K)])])
			state = int(TABLE[state][CH.index(K)])
		
	#	print(Analyse)
		index += 1
		
	return
	
	
def main():
	global LL1LAN
	print("文法n行，->区分左右，$为终结符，ε为空串，大写非终结符，小写终结符，S为开始符号(放在第一行)，|是或：，Z为S'")
	getlan()
	print("拓广文法：")
	print(LAN)
	print(EXLAN)
	print("项目：")
	print(ITEM)

	LL1LAN = copy.deepcopy(LAN)
	getll1lan()
	print()
	print(LL1LAN)
	
	first()
	print("FIRST集：", FIRST)
	follow()
	for i in DICT:
		FOLLOW[i].extend(FIRST[DICT[i]])
		if 'ε' in FOLLOW[i]:
			FOLLOW[i].remove('ε')
	print("FOLLOW集：", FOLLOW)
	
	'''
	FOLLOW['E'] = ['$', '+', ')']
	FOLLOW['T'] = ['$', '+', ')', '*']
	FOLLOW['F'] = ['$', '+', ')', '*']
	'''
	
	getdfa()
	print()
	print("识别文法活前缀的DFA：")
	for index, i in enumerate(DFA):
		print(index, i)
	print()
	TABLE = table()
	print("SLR1分析表：")
	p = CH.index('$')
	print('%-6s' % "", end = "")
	for i in CH:
		print('%-6s' % i, end = "")
	print()
	for index, i in enumerate(TABLE):
		print('%-6s' % index, end = "")
		for j in i:
			if j != None:
				print('%-6s' % j, end = "")
			else:
				print('%-6s' % "", end = "")
		print()
	
	print()
	string = input("请输入要分析的字符串：")
	analyse(string, TABLE)

if __name__ == '__main__':
	main()
