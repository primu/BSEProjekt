# -*- coding: utf-8 -*-
"""
Created on Fri Apr 03 21:28:51 2015

@author: Maras
"""

# kod jest wysoce prototypowy - jak bedzie już wiadomo, jak to powinno zostać zaimplementowane to zrobię porządnie ;-)

import numpy
numpy.set_printoptions(threshold=numpy.nan)

#1
my_input = numpy.random.randint(256, size=(32, 32)) # zbior "a" w artykule 
A = numpy.random.randint(256, size=(1024, 100)) # baza danych / 100 probek 32x32 (po wektoryzacji)
vectorized_input = numpy.hstack(my_input)# na diagramie 1024x1

#2
U, D, V = numpy.linalg.svd(A) # D-diagonal/E

#3
H = numpy.dot(D, V)

#4/5
result = numpy.ones(shape=(1024,1))
at = vectorized_input.transpose()

result = numpy.dot(at, U)  
tmp_result = numpy.repeat(result, 100, axis=0)
new_result = tmp_result.reshape((1024, 100))

#6   
dist = numpy.linalg.norm(new_result[0]-H)
min_val = dist
min_id = 0
for i in range(1, 1024):
    dist = numpy.linalg.norm(new_result[i]-H)
    if (min_val > dist):
        min_val = dist
        min_id = i

#print ((min_val))
#print new_result[min_id]

#7...
matrix_input = str(new_result[0][min_id])
for i in range(1, 1024):
    matrix_input += ',' + str(new_result[i][min_id])
    
tmp_app_result = numpy.matrix(matrix_input)
app_result = tmp_app_result.reshape(32,32)
print(app_result)