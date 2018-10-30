from random import *
import copy
def AI(mat):
	def maximum_element(mat):
		flat = flatten(mat)
		m = max(flat)
		return m
	def monoton(row):
	    if row[0] > row[1]:
	        if row[1] >= row[2]:
	            if row[2] >= row[3]:
	                return (True, row)
	        return (False, row)
	    elif row[0] < row[1]:
	        if row[1] <= row[2]:
	            if row[2] <= row[3]:
	                return (True, row)
	        return (False, row)
	    else:
	        if row[1] > row[2]:
	            if row[2] >= row[3]:
	                return (True, row)
	            return (False, row)
	        elif row[1] < row[2]:
	            if row[2] <= row[3]:
	                return (True, row)
	            return (False, row)
	        else:
	            return (True, row)
	def scoremonoton(mat):
	    skor = 0
	    transmat = transpose(mat)
	    for row in mat:
	        if monoton(row)[0] == True:
	            skor += sum(row)
	        else:
	        	a = 3/2 
	        	b = 1
	        	if row[1] > row[2]:
	        		skor -= (a * maximum_element([row]) + b * row[1])
	        	else:
	        		skor -= (a * maximum_element([row]) + b * row[2])
	    for row in transmat:
	        if monoton(row)[0] == True:
	            skor += sum(row)
	        else:
	        	a = 3/2 
	        	b = 1
	        	if row[1] > row[2]:
	        		skor -= (a * maximum_element([row]) + b * row[1])
	        	else:
	        		skor -= (a * maximum_element([row]) + b * row[2])
	    return int(skor)
	def scoreedge(mat):
		skor = 0
		a = 1.75
		skor += (a**10) * (mat[3][0]) + (a**9) * (mat[2][0] + mat[3][1]) + (a**8) * (mat[1][0] + mat[2][1] + mat[3][2]) + (a**7) * (mat[0][0] + mat[1][1] + mat[2][2] + mat[3][3]) + (a**6) * (mat[0][1] + mat[1][2] + mat[2][3]) +\
		(a**5) * (mat[0][2] + mat[1][3]) + (a**4) * mat[0][3]
		return skor
	def leftpusher(row):
	        n = len(row)
	        i = 0
	        j = 0
	        while j < n:
	            if row[i] == 0:
	                row.remove(row[i])
	            else:
	                i += 1
	            j += 1
	        while len(row) < n:
	            row.append(0)
	        return row
	def combiner(row):
	        n = len(row)
	        i = 0
	        score = 0
	        while i < n-1:
	            if row[i] == row[i+1]:
	                score += 2 * row[i]
	                i += 2
	            else:
	                i += 1
	        return (row, score)
	def scoremerge(mat):
		skor1 = 0
		skor2 = 0
		skor3 = 0
		skor4 = 0
		for row in mat:
			skor1 += combiner(leftpusher(row))[1]
		transposed = transpose(mat)
		for row in transposed:
			skor2 += combiner(leftpusher(row))[1] 
		return skor1 + skor2
	def totalscorepos(mat):
		a = 0.9
		b = 1
		return a * scoremonoton(mat) + b * scoreedge(mat)
	def simulate(state):
		n = 1
		c = 50
		score = [0,0,0,0]
		states = []
		for i in range(n):
			simulatas, valid = up(state)
			if valid:
				score[0] = ((n-1) * (score[0]) + totalscorepos(get_matrix(simulatas)) + c * (get_score(simulatas) - get_score(state)))/n
				states.append(simulatas)
			else:
				score[0] = -1000000000000000
				states.append(simulatas)
			simulkiri, valid = left(state)
			if valid:
				score[1] = ((n-1) * (score[1]) + totalscorepos(get_matrix(simulkiri)) + c * (get_score(simulkiri) - get_score(state)))/n
				states.append(simulkiri)
			else:
				score[1] = -1000000000000000
				states.append(simulkiri)
			simulbawah, valid = down(state)
			if valid:
				score[2] = ((n-1) * (score[2]) + totalscorepos(get_matrix(simulbawah)) + c * (get_score(simulbawah) - get_score(state)))/n
				states.append(simulbawah)
			else:
				states.append(simulbawah)
				score[2] = -1000000000000000
			simulkanan, valid = right(state)
			if valid:
				score[3] = ((n-1) * (score[3]) + totalscorepos(get_matrix(simulkanan)) + c * (get_score(simulkanan) - get_score(state)))/n
				states.append(simulkanan)
			else:
				states.append(simulkanan)
				score[3] = -1000000000000000
		return (score, states)
	def move(state):
		def bestmove(state, n):
			if n == 1:
				return simulate(state)[0]
			else:
				newstate = simulate(state)
				newstate1 = ((newstate[0][0], newstate[1][0]), (newstate[0][1], newstate[1][1]), (newstate[0][2], newstate[1][2]), (newstate[0][3], newstate[1][3]))
				a = []
				for elem in newstate1:
					a.append(max(bestmove(elem[1], n-1)) + elem[0])
				return a
		n = 5
		k = bestmove(state, n)
		l = max(k)
		m = k.index(l)
		if l < -100000:
			if up(state)[1] == True:
				return "w"
			if left(state)[1] == True:
				return "a"
			if down(state)[1] == True:
				return "s"
			if right(state)[1] == True:
				return "d"	
		return ("w", "a", "s", "d")[m]
	return move(make_state(mat, 0, []))
