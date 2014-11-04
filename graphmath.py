"""
Olin Graph Program Fall 2014
Authors: Mafalda Borges, Josh Langowitz, Raagini Rameshwar
Python 3
"""

def identity(m=1):
	"""
	create identity matrix of size m
	"""
    return [[int(i==j) for i in range(m)] for j in range(m)]

def matrix_addition(mat1,mat2):
	"""
	adds 2 dimensional matrices of the same size
	"""
    newmat=[]
    for i in range(len(mat1)):
        newmat.append(vector_addition(mat1[i],mat2[i]))
    return newmat

def vector_addition(vec1,vec2):
	"""
	adds 1 dimensional vectors of the same size
	"""
    newvec=[]
    for i in range(len(vec1)):
        newvec.append(vec1[i]+vec2[i])
    return newvec