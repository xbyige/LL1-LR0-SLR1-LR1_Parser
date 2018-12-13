'''
E->E+T|T
T->T*F|F
F->(E)|A
A->1A|2A|3A|4A|5A|6A|7A|8A|9A|0|1|2|3|4|5|6|7|8|9|ε
'''

'''
E->EOE|(E)|A
O->+|-|*
A->1A|2A|3A|4A|5A|6A|7A|8A|9A|0|1|2|3|4|5|6|7|8|9|ε
'''

#还是消除简单左递归
#重写LR0和SLR1中的TABLE以及ANALYSE函数，条理更清晰

import copy

LAN = {}
FIRST = {}
EXLAN = []
ITEM = []
DICT = {}
DFA = []	#[0]为代表 其中[0][0]为项目字符串,[0][1]为搜索符 [1]为图上连线
CH = []
CL = []

def isterminal(ch):
	if not (ch >= "A" and ch <="Z"):
		return True
	else:
		return False
		
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
		for j in i[0]:		#先填reduce项
			if len(j[0]) - 1 == j[0].index('.'):
				string = j[0][:-1]
				pos = EXLAN.index(string)
				if pos == 0:
					TABLE[index][CH.index(j[1])] = 'acc'
				else:
					TABLE[index][CH.index(j[1])] = 'r' + str(pos)
		
		for j in i[1]:		#再填Action/Goto项
			if isterminal(j[0]):
				TABLE[index][CH.index(j[0])] = 's' + str(j[1])
			else:
				TABLE[index][CH.index(j[0])] = str(j[1])
		
	return TABLE

def closure(item):
	global CL
	string = item[0]
	search = item[1]
	if string.index('.') == len(string) - 1:
		return [item]
	
	tmp = [item]
	index = string.index('.')
	k = string[index + 1:]
#	print(item)
#	print(k)
	if not isterminal(k[0]):
		for i in ITEM:
			if i[0] == k[0]:
				if i[3] == '.':
				#	tmp.append([i, search])	#需增加搜索符
					w = []
					if len(k) == 1:		# .走到了最后就继承搜索符
						w = [i, search]
						tmp.append(w)
						if len(w[0]) > 4:
							if not isterminal(w[0][4]):
								if w not in CL:
									CL.append(w)
							#	if w[0] != string:
									tmp.append(closure(w))
									CL.remove(w)
					else:
						if isterminal(k[1]):
							w = [i, k[1]]
							tmp.append(w)
							if len(w[0]) > 4:
								if not isterminal(w[0][4]):
							#		if w[0] != string:
									if w not in CL:
										CL.append(w)
										tmp.append(closure(w))
										CL.remove(w)
										
						else:
							t = list(set(calfirst(k[1:])))
							if t == ['ε'] or len(t) == 0:
								w = [i, k[1]]
								tmp.append(w)
								if len(w[0]) > 4:
									if not isterminal(w[0][4]):
										if w not in CL:
											CL.append(w)
								#		if w[0] != string:
											tmp.append(closure(w))
											CL.remove(w)
							else:
								for x in t:
									if x != 'ε':
										w = [i, x]
										tmp.append(w)
										if len(w[0]) > 4:
											if not isterminal(w[0][4]):
											#	if w[0] != string:
												if w not in CL:
													CL.append(w)
													tmp.append(closure(w))
													CL.remove(w)
						
	k = []
	
	for i in tmp:
		if type(i[0]) == list:
			for j in i:
				if j not in k:
					k.append(j)
		else:
			if i not in k:
				k.append(i)
		
	tmp = k
	
	return tmp
	
def getdfa():
	cl = closure([ITEM[0], '$'])
	DFA.append([cl, []])
	l = 0
	while l < len(DFA):
		vis = [False for i in range(len(DFA[l][0]))]
		for indexi, i in enumerate(DFA[l][0]):
			if i[0].index('.') == len(i[0]) - 1:
				continue
				
			p = i[0].index('.')
			tmp = []
			posi = i[0].index('.')
			
			if len(i[0]) > 4:
				ch = i[0][posi + 1]
			else:
				ch = ""
			
			for indexj, j in enumerate(DFA[l][0]):
				if not vis[indexj]:
					posj = j[0].index('.')
					if len(j[0]) - 1 > posj:
						if j[0][posj + 1] == ch:
							newstr = j[0][:posj] + j[0][posj + 1] + '.' + j[0][posj + 2:]
							tmp.extend(closure([newstr, j[1]]))	#没想好，对于外部应该是直接继承，先这么写看效果
							#去重
							k = []
							for i in tmp:
								if type(i[0]) == list:
									for j in i:
										if j not in k:
											k.append(j)
								else:
									if i not in k:
										k.append(i)		
							tmp = k
							
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

def getlan():
	path = "lr1test.txt"
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
				EXLAN.append('Z->' + line[0])
				ITEM.append('Z->.' + line[0])
				ITEM.append('Z->' + line[0] + '.')
				i += 1
			else:
				LAN[line[0]] = splitlist
				
		FIRST[line[0]] = []

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
		
		if Istack[0] not in CH:
			print('分析失败！')
			return
		
		if TABLE[state][CH.index(Istack[0])] == None:
			print('分析失败！')
			return
		else:
			if TABLE[state][CH.index(Istack[0])][0] == 's':
				s = 'shift ' + Istack[0]
				print('%-16s' % s)
				pos = int(TABLE[state][CH.index(Istack[0])][1:])
				Analyse.append([Istack[0], pos])
				Istack = Istack[1:]
				state = pos
			elif TABLE[state][CH.index(Istack[0])][0] == 'r':
				pos = int(TABLE[state][CH.index(Istack[0])][1:])
				s = 'reduce ' + str(pos)
				print('%-16s' % s)
				lan = EXLAN[pos]
				p = lan.index('>')
				K = lan[0]
				k = lan[p+1:]
				if k != '':
					Analyse = Analyse[:-len(k)]
					
				state = Analyse[-1][1]
				if TABLE[state][CH.index(K)] == None:
					print("分析失败！")
					return
				
				Analyse.append([K, int(TABLE[state][CH.index(K)])])
				state = int(TABLE[state][CH.index(K)])
				
			else:
				s = 'shift ' + Istack[0]
				print('%-16s' % s)
				pos = int(TABLE[state][CH.index(Istack[0])])
				Analyse.append([Istack[0], pos])
				Istack = Istack[1:]
				state = pos
				
		index += 1

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
		
	getdfa()
	print()
	print("识别文法活前缀的DFA：")
	for index, i in enumerate(DFA):
		print(index, i)
	print()
		
	TABLE = table()
	print()
	print("LR1分析表：")
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
	