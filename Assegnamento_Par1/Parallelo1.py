# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 11:47:34 2021

@author: laura
"""
import math
import multiprocessing
import random
import threading
import time
import matplotlib.pyplot as plt
import numpy 

class Timer(object):
    def __init__(self, name=None):
        self.name = name
        self.timee=0

    def __enter__(self):
        self.tstart = time.time()

    def __exit__(self, type, value, traceback):
        if self.name:
            print('[%s]' % self.name, end=' ') #Se gli hai dato un nome allora stampa il nome, di default è None (definito nell'init) quindi se non gli dai niente non entra nell'if 
        self.timee=(time.time() - self.tstart)
        print('Elapsed: %s' % (time.time() - self.tstart))
        self.output()

    def output(self):
        return self.timee

def primi(N):
    nprimi=[]
    n=N
    while N>1:
        div, count= 2,0
        while div <=N/2 and count==0:
            if N%div==0:
                count+=1
            div+=1
        if count==0:
            nprimi.append(N)
        N-=1
        
    somma=sum(nprimi)
    output=[n, somma]
   #print(nprimi)
    return output

def mp_worker(nums, output_q):
    ''' Funzione worker che viene invocata in un processo. 
    Parameters
    ----------
    nums : lista
        è una lista di numeri sui cui applicare la funzione primi. 
    output_q : multiprocessing.queue
        è la coda del processo.

    Returns
    -------
    None.

    '''
    outdict = {}
    for n in nums:
        outdict[n]=primi(n)
    output_q.put(outdict)
    
    #Debugging
    #print(outdict)
    #print(output_q.get())
    
def mp_primi(nums, nprocs):
    '''
    Ogni processo prende un pezzo di nums e una coda per prendere l'output
    Parameters
    ----------
    nums : lista
        Lista di numeri su cui applicare la funzione primi.
    nprocs : int
        Numero di processi da inizializzare

    Returns
    -------
    resultdict : dizionario
         Dizionario contenente lista di due elementi di numeri primi

    '''
    out_q=multiprocessing.Queue()
    chunksize=int(math.ceil(len(nums)/float(nprocs))) #Dimensione del pezzo di lista da dare a ogni worker
    procs = []
    
    for i in range(nprocs):
        p=multiprocessing.Process(target=mp_worker, args=(nums[chunksize*i:chunksize*(i+1)], out_q))
        procs.append(p)
        p.start()
        #time.sleep(1)
    resultdict = {}
    
    for i in range (nprocs):
        resultdict.update(out_q.get()) #La coda scivola dopo aver preso l'ultimo elemento quindi non c'è bisogno di usare l'indice
        
    for p in procs:
        p.join()
    
    print (procs)
    
    return resultdict

def serial_primi(nums):
    return {n: primi(n) for n in nums}

def thread_worker(nums, outdict):
    ''' Funzione worker che viene invocata in un thread. 
    Parameters
    ----------
    nums : lista
        è una lista di numeri sui cui applicare la funzione primi. 
    outdict : dizionario
        dizionario in cui vengono salvati i risultati

    Returns
    -------
    None.

    '''
    
    for n in nums:
        outdict[n]=primi(n)
    
def thread_primi(nums, nthreads):
    '''
    Ogni thread prende in ingresso un chunksize di nums e il suo dizionario di output

    Parameters
    ----------
    nums : lista
        è una lista di numeri sui cui applicare la funzione primi. 
    nthreads : int
        numero di thread che vogliamo instanziare

    Returns
    -------
    outdict : dizionari
        merge di tutti i di tutti i singoli dizionari dei thread

    '''
    chunksize=int(math.ceil(len(nums)/float(nthreads))) #Dimensione del pezzo di lista da dare a ogni worker
    threads = []
    
    outs = [{} for i in range(nthreads)]
    
    for i in range(nthreads):
        # Create each thread, passing it its chunk of numbers to factor and output dict.
        t = threading.Thread(target=thread_worker, args=(nums[chunksize * i:chunksize * (i + 1)], outs[i]))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Merge all partial output dicts into a single dict and return it
    return {k: v for out_d in outs for k, v in out_d.items()} #Ritorna un dizionario creato spacchettando la lista di dizionari outs e il dizionario out_d per chaive e valore
    
    
    
def plot(elapsed):
    plt.rcdefaults() #usa il plot di default
    fig, ax = plt.subplots()
    laby = ('Serial','Thread 2','Process 2','Thread 4','Process 4','Thread 8','Process 8')
    y_pos = numpy.arange(len(laby))
    ax.barh(y_pos, elapsed, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(laby)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Elapsed time')
    ax.set_title('Serial, threads, processes comparison')
    plt.show()
    #wait()
          

def benchmark(nums):
    print('Running benchmark...')
    elapsed_times=[]

    tserial=Timer('serial')
    with tserial as qq:
        print('runnung serial')
        s_d = serial_primi(nums)
    elapsed_times.append(tserial.output())

    for numparallel in [2, 4, 8]:
        tthread=Timer('threaded %s' % numparallel) #stampa threaded e il numero di thread usati 
        with tthread as qq:
            print('runnung thread')
            t_d = thread_primi(nums, numparallel)
        elapsed_times.append(tthread.output())
        tmpar=Timer('mp %s' % numparallel)
        with tmpar as qq:
            print('runnung process')
            m_d = mp_primi(nums, numparallel)
        elapsed_times.append(tmpar.output())
    
    print (elapsed_times)
    plot(elapsed_times)


if __name__=='__main__':
    N=10000
    list=[]
    while N<25000:
        list.append(N)
        N+=1
    #print(mp_primi(list,2))
    #print(primi(90))
    #print(serial_primi(list))
    #print(thread_primi(list, 8))
    
    benchmark(list)
    
