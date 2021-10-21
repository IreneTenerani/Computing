import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
import matplotlib.pyplot as plt

class VoltageData(): #the class name must be VoltgeData 
    
    ''' Class for handling a sequence of voltage measurements at different times.
    '''
    def __init__(self, t, v): 
    
    self._time=np.array(t, dtype=np.float64) #returning a numpy array of type numpy.float64 of the quantity t
    self._voltages=np.array(v, dtype=np.float64)  
    
    self._dati=np.array([self.time, self.voltages]) # the values should be accessible with the familiar square parenthesis syntax: the  first index must refer to the entry, the second selects time (0) or voltage (1). Slicing must also work. (Manfreda usa np.column_stack ma secondo me è la stessa cosa)
    
    self.spline=InterpolatedUnivariateSpline(self._time, self._voltages) #building the spline
    
    def __len__(self): #calling the len() function on a class instance must return the number of entries
    ''' returning number of measurements'''
        return len(self._dati)  
         
    def __getitem__(self, item):
     ''' returning an item of the data array'''
         return self._dati[item]
         
    def __iter__(self): #the class must be iterable: at each iteration, a numpy array of two values (time and voltage) corresponding to an entry in the file must be returned
    ''' returning a numpy array of two values '''
    for i in range(len(self)):
        for j in range(len(self)):
            yield self._dati[i, j] #NOTA: non sono sicura che questo funzioni, provare anche self._dati[i][j] o altro
        
    def __call__(self, t): #the class must be callable, returning an interpolated value of the tension at a given time
    ''' returning an interpolated value of the tension at a given time t'''
      return self.spline(t) 
      
    def plot(self, ax): #The plot function must accept an 'ax' argument, so that the user can select the axes where the plot is added (with a new figure as default). The user must also be able to pass other plot options as usual