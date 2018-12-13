'''
18
S->aA|bB
A->cA|d                                       
B->cB|d
'''

'''
24
S->A|B
A->aAb|c
B->aBd|d
'''

'''
A->(A)|a
'''

'''
A->(A)A|ε
'''

'''
S->aA
A->cA|d
'''

'''
E->aA
E->bB
A->cA
A->d
B->cB
B->d
'''

'''
E->E+T|T
T->T*F|F
F->(E)|a
'''

import copy

LAN = {}
EXLAN = []
ITEM = []
DFA = []	#[0]为代表 [1]为图上连线
TABLE = []
CH = []
ACC = ''

def isterminal(ch):
	if not (ch >= "A" and ch <="Z"):
		return True
	else:
		return False

def closure(string):
	if string.index('.') == len(string) - 1:
		return [string]
	item = ITEM
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
#	print("yyr", cl)
	
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
			'''
			if p == len(i) - 2:	#待规约
				newstr = i[:p] + i[p + 1] + '.' + i[p + 2:]
				
				pos = -1
				for index, j in enumerate(DFA):
					if j[0] == [newstr]:
						pos = index
				if pos == -1:
					DFA.append([[newstr], []])
					DFA[l][1].append([i[p + 1], len(DFA) - 1])
				else:
					DFA[l][1].append([i[p + 1], pos])
			
				vis[indexi] = True
				continue
				
				如果非待规约项
				
			
			else:
			'''
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
#	tmp1.sort()
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
				t = i[0][0][:-1]
				p = EXLAN.index(t)
				for j in range(l):
			#		pass
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
								TABLE[index][k] = 'r' + str(p)

				
	return TABLE
	

def getlan():
	path = "lr0test.txt"
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
				EXLAN.append('Z->' + line[0])
				ITEM.append('Z->.' + line[0])
				ITEM.append('Z->' + line[0] + '.')
				i += 1
			else:
				LAN[line[0]] = splitlist

		for j in splitlist:
			if j != 'ε':
				EXLAN.append(line[0] + '->' + j)
				for k in range(len(j)):
					ITEM.append(line[0] + '->' + j[:k] + '.' + j[k:])
				ITEM.append(line[0] + '->' + j + '.')
			else:
				ITEM.append(line[0] + '->' + '.')

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
		for i in TABLE[state]:
			if i != None:
				if i[0] == 'r':
					r = int(i[1:])
				elif i[0] == 's':
					ss = int(i[1:])

		if r == -1:		#非规约
			pos = CH.index(Istack[0])
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
				pos = CH.index(Istack[0])
				if ss == pos:
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
					continue
					
			k = EXLAN[r]
			p = k.index('>')
			K = k[0]
			k = k[p+1:]
		#	print("reduce", r)
			s = 'reduce' + ' ' + str(r)
			print('%-16s' % s)
			
			Analyse = Analyse[:-len(k)]
			state = Analyse[-1][1]
			Analyse.append([K, int(TABLE[state][CH.index(K)])])
			state = int(TABLE[state][CH.index(K)])
		
	#	print(Analyse)
		index += 1
		
	return
	
	
def main():
	print("文法n行，->区分左右，$为终结符，ε为空串，大写非终结符，小写终结符，S为开始符号(放在第一行)，|是或：，Z为S'")
	getlan()
	print("拓广文法：")
	print(LAN)
	print(EXLAN)
	print("项目：")
	print(ITEM)
	
	getdfa()
	print()
	print("识别文法活前缀的DFA：")
	for index, i in enumerate(DFA):
		print(index, i)
	print()
	TABLE = table()
	print("LR0分析表：")
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