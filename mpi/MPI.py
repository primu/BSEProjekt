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
    mpi_input_data_tag = 50 #dane
    mpi_output_data_tag = 60 #dane
    
    #lista wezłow bioracych udzial w przetwarzaniu
    result_arr = [0]*mpi_size

    recognized_letter = ''
    recognized_letter_prob = 0    
    
    nodes_arr = []
    if conf is None:
        nodes_arr = numpy.ones((mpi_size, 2))
    else: 
        nodes_arr = numpy.zeros((mpi_size, 2))
        conf_data = json.loads(conf)  
        for node in conf_data:
            if len(nodes_arr) > node['node']:
                nodes_arr[node['node']][0] = 1
                nodes_arr[node['node']][1] = node['letter']
            
    #przetwarzanie
    if mpi_rank == 0:        
        #rozeslanie danych do wezlow&odbior
        for i in range(1, mpi_size):
            if nodes_arr[i][0] > 0:
                mpi_comm.send([data, nodes_arr[i][1]], dest=i, tag=mpi_input_data_tag)	
    
        #oczekiwanie na dane z wezlow
        for i in range(1, mpi_size):
            if nodes_arr[i][0] > 0:
                result_arr[i] = mpi_comm.recv(source=i, tag=mpi_output_data_tag)
                if recognized_letter_prob < result_arr[i][0]:
                    recognized_letter_prob = result_arr[i][0]
                    recognized_letter = result_arr[i][1]
    
        #przetwarzanie wynikow    
        response = []
        main_response = []
        main_response.append({"letter": recognized_letter})
        for i in range(1, mpi_size):
            if nodes_arr[i][0] > 0:
                response.append({'node': i, 'prob': result_arr[i][0], 'letter': result_arr[i][1]})
            else:
                response.append({'node': i, 'prob': 0, 'letter': ''})
        
        main_response.append({"nodes": response})
    
        result.append(json.dumps(main_response))
        return True
    else:
        if (nodes_arr[mpi_rank][0] == 0):
            return False
        
        local_buff = []
        local_buff = mpi_comm.recv(source=0, tag=mpi_input_data_tag)
        tmp_data = local_buff[0]        
        tmp_letter = local_buff[1]
	  #
        #przetwarzanie w ramach sieci neuronowej...
        #
        prob = round(random.uniform(0.1, 1.0), 6)
        letter = chr(random.randint(97, 122))
        result = [prob, letter]
        mpi_comm.send(result, dest=0, tag=mpi_output_data_tag)
        
        return False
    
#tymczasowa konfiguracja wejsciowa
def tmp_input_conf():
    response = []
    for num in range(1, 4):
        response.append({'node': num, "letter": num})

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
status = process_data(tmp_input_conf(), tmp_data, result) #zamiast tmp_input_conf można dać None

if status == True:
    print(result[0])
