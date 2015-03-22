# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 12:35:10 2015

@author: Maras
"""

#TD:
#-asynchroniczne odbieranie danych
#-przetwarzanie przy uzyciu wszystkich wezlow, gdy nie podano konfiguracji (processData)
#-obsluga wyjatkow

import json
import random
import numpy
from mpi4py import MPI

cData = {}
cData['numberOfProcesses'] = 2;


def loadConf(inputFile):
    with open(inputFile) as confFile:
        return json.load(confFile)['main']
        
def processData(conf, data, result):
    #lista wezłow bioracych udzial w przetwarzaniu    
    nodesArr = [0]*int(cData['numberOfProcesses'])
    nodesCount = 0
    confData = json.loads(conf);    
    for node in confData:
        nodesArr[node['nodes']] = 1
        nodesCount += 1

    #inicjacja MPI
    mpiComm = MPI.COMM_WORLD
    mpiRank = mpiComm.Get_rank()
    mpiSize = mpiComm.Get_size()
    mpiInputDataTag = 50 #dane (odbior)
    mpiOutputDataTag = 60 #dane (odbior)
    
    if mpiRank == 0:        
        #rozeslanie danych do wezlow&odbior
        for i in range(mpiSize):
            if nodesArr[i] > 0:
                mpiComm.send(data, dest=i, tag=mpiInputDataTag)	
    
        #oczekiwanie na dane z wezlow
        for i in range(mpiSize):
	      if nodesArr[i] > 0:
                nodesArr[i] = mpiComm.recv(source=i, tag=mpiOutputDataTag)
    
        #przetwarzanie wynikow
        response = []
        for i in range(mpiSize):
            if nodesArr[i] > 0:
                response.append({'node': i, 'prob': nodesArr[i]})
            else:
                response.append({'node': i, 'prob': 0})
    
        result.append(json.dumps(response))
        return True
    else:
        localBuff = []
        localBuff = mpiComm.recv(source=0, tag=mpiInputDataTag)
	  #
        #przetwarzanie w ramach sieci neuronowej...
        #
        result = round(random.uniform(0.1, 1.0), 6)
        mpiComm.send(result, dest=0, tag=mpiOutputDataTag)
        
        return False
    
#tymczasowa konfiguracja wejsciowa
def tmpInputConf():
    response = []
    for num in range(1, 4):
        response.append({'nodes': num})

    return json.dumps(response)     
       
#tymczasowe dane wejsciowe
tmpData = {
    202, 254, 101, 
    15, 147, 78
    }

#
#
#
cData = loadConf('conf.json')

result = []
status = processData(tmpInputConf(), tmpData, result);

if status == True:
    print(result[0])
