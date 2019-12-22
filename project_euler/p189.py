'''
Created on 02-Jan-2016

@author: Srinivas Gunti
'''
# triangle coloring
from copy import copy
from collections import deque
from itertools import count
from time import clock
from timeit import timeit
normalize_counter = count(1)

def _norm(X):
    if X[0]==1:
        X = map(lambda x: (x+2)%3,X)
    elif X[0]==2:
        X = map(lambda x: (x+1)%3,X)
    try:
        i = 1
        while X[i]==0:
            i+=1
        if X[i]==2:
            X = map(lambda x: -x%3,X)
    except IndexError:
        pass
    return X

SavedNormals = {}
def normalize(X):
#     print 'Normalize %d:'%normalize_counter.next()
#     print '\t%s'%X
    if len(X)==1:
        return (0,)
    
    Y = _norm(X[::-1])
    X = _norm(X)
    return tuple(min(X,Y))
    
def genUpSols(oldsol,newsol=None):
    if not newsol:
        newsol = []
    l = len(newsol)
    if len(oldsol)+1==l:
        yield newsol
    else:
        newsol.append(None)
        for i in xrange(3):
            if (l==len(oldsol) or i!=oldsol[l]) and (l==0 or i!=oldsol[l-1]):
                newsol[l] = i
                for UpSol in genUpSols(oldsol, copy(newsol)):
                    yield UpSol                
                        
def genDownSols(oldsol,newsol = None):
    if not newsol:
        newsol = []
    l = len(newsol)
    if len(oldsol)==l:
        yield newsol
    else:
        newsol.append(None)
        for i in xrange(3):
            if i!=oldsol[l]:
                newsol[l] = i
                for DownSol in genDownSols(oldsol, copy(newsol)):
                    yield DownSol
def genSols(oldsol,oldup):
    if oldup:
        return genUpSols(oldsol)
    else:
        return genDownSols(oldsol)

SavedSols = {}    
def Sols(oldsol,oldup):
    if len(oldsol)==0:
        return {(0,):3}
    oldsol = tuple(oldsol)
    try:
        return SavedSols[(oldsol,oldup)]
    except KeyError:
        D = {}
        for i in genSols(oldsol, oldup):
            j = normalize(i)
            D.setdefault(j,0)
            D[j]+=1    
        SavedSols.setdefault((oldsol,oldup),D)
        return D

SavedAnswers = {}
def Answer(n, oldsol=None, i=0):
    if (oldsol,i) in SavedAnswers:
        return SavedAnswers[(oldsol,i)]
    if i==0:
        D = Sols([],False) # at 0 level
    else:
        D = Sols(oldsol, i%2==0)
    if i==2*(n-1):
        return sum(D.itervalues())
    A = 0
    for k,v in D.iteritems():
        A+= v*Answer(n,k,i+1)
    SavedAnswers[(oldsol,i)] = A
    return A


def T1():
    print Answer(8)

print timeit(T1, number=1)