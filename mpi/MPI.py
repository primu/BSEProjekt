# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 12:35:10 2015

@author: Maras
"""

#TD:
#-asynchroniczne odbieranie danych
#-obsluga wyjatkow

#wywolanie z poziomu CMD
#mpiexec -np 5 python MPI.py

import json
import random
import numpy
from mpi4py import MPI

c_data = {}


def load_conf(input_file):
    with open(input_file) as conf_file:
        return json.load(conf_file)['main']
        
def process_data(conf, data, result):
    #inicjacja MPI
    mpi_comm = MPI.COMM_WORLD
    mpi_rank = mpi_comm.Get_rank()
    mpi_size = mpi_comm.Get_size()
    mpi_input_data_tag = 50 #dane (odbior)
    mpi_output_data_tag = 60 #dane (odbior)
    
    #lista wezłow bioracych udzial w przetwarzaniu
    nodes_arr = []    
    if conf is None:
        nodes_arr = [1]*mpi_size
    else: 
        nodes_arr = [0]*mpi_size
        conf_data = json.loads(conf);    
        for node in conf_data:
            if len(nodes_arr) > node['nodes']:
                nodes_arr[node['nodes']] = 1
            
    #przetwarzanie
    if mpi_rank == 0:        
        #rozeslanie danych do wezlow&odbior
        for i in range(1, mpi_size):
            if nodes_arr[i] > 0:
                mpi_comm.send(data, dest=i, tag=mpi_input_data_tag)	
    
        #oczekiwanie na dane z wezlow
        for i in range(1, mpi_size):
            if nodes_arr[i] > 0:
                nodes_arr[i] = mpi_comm.recv(source=i, tag=mpi_output_data_tag)
    
        #przetwarzanie wynikow
        response = []
        for i in range(1, mpi_size):
            if nodes_arr[i] > 0:
                response.append({'node': i, 'prob': nodes_arr[i]})
            else:
                response.append({'node': i, 'prob': 0})
    
        result.append(json.dumps(response))
        return True
    else:
        if (nodes_arr[mpi_rank] == 0):
            return False
        
        local_buff = []
        local_buff = mpi_comm.recv(source=0, tag=mpi_input_data_tag)
	  #
        #przetwarzanie w ramach sieci neuronowej...
        #
        result = round(random.uniform(0.1, 1.0), 6)
        mpi_comm.send(result, dest=0, tag=mpi_output_data_tag)
        
        return False
    
#tymczasowa konfiguracja wejsciowa
def tmp_input_conf():
    response = []
    for num in range(1, 4):
        response.append({'nodes': num})

    return json.dumps(response)     
       
#tymczasowe dane wejsciowe
tmp_data = {
    202, 254, 101, 
    15, 147, 78
    }

#
#
#
c_data = load_conf('conf.json')

result = []
status = process_data(tmp_input_conf(), tmp_data, result); #zamiast tmp_input_conf można dać None

if status == True:
    print(result[0])
