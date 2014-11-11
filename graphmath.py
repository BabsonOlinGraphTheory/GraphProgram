"""
Olin Graph Program Fall 2014
Authors: Mafalda Borges, Josh Langowitz, Raagini Rameshwar
Python 3
"""
from math import *

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

def tensor_product(adj1, adj2):
    m=len(adj1)
    n=len(adj1[0])
    p=len(adj2)
    q=len(adj2[0])
    resadj=[]
    for i in range(m*p):
        resadj.append([None]*(n*q))
    for i in range(m):
        for j in range(n):
            for k in range(p):
                for l in range(q):
                    resadj[i*p+k][j*q+l]=adj1[i][j]*adj2[k][l]
    return resadj

def cartesian_product(adj1, adj2):
    return matrix_addition(tensor_product(adj1,identity(len(adj2))),tensor_product(identity(len(adj1)),adj2))

def strong_product(adj1,adj2):
    return matrix_addition(cartesian_product(adj1,adj2),tensor_product(adj1,adj2))