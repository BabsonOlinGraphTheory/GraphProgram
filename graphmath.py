#create identity matrix of size m
def identity(m=1):
    return [[int(i==j) for i in range(m)] for j in range(m)]
#adds 2 dimensional matrices of the same size
def matrix_addition(mat1,mat2):
    newmat=[]
    for i in range(len(mat1)):
        newmat.append(vector_addition(mat1[i],mat2[i]))
    return newmat
#adds 1 dimensional vectors of the same size
def vector_addition(vec1,vec2):
    newvec=[]
    for i in range(len(vec1)):
        newvec.append(vec1[i]+vec2[i])
    return newvec