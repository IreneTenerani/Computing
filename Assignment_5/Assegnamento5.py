import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
import matplotlib.pyplot as plt

class VoltageData(): #the class name must be VoltgeData

    ''' Class for handling a sequence of voltage measurements at different times.
    '''
    def __init__(self, t, v):

        self._time=np.array(t, dtype=np.float64) #returning a numpy array of type numpy.float64 of the quantity t
        self._voltages=np.array(v, dtype=np.float64)

        self._dati=np.column_stack((self._time, self._voltages)) # the values should be accessible with the familiar square parenthesis syntax: the  first index must refer to the entry, the second selects time (0) or voltage (1). Slicing must also work. Mettendo ([t,v]) posso usare l'indice 0 per predere t e l'indice 1 per prendere v mettendo 0 o 1 al secondo posto nell'argomento dell'array.

        self.spline=InterpolatedUnivariateSpline(self._time, self._voltages) #building the spline


    @classmethod
    def from_file(cls, file_path):
        """ Alternate constructor from a data file, exploiting load_txt()"""
        cls._time, cls._voltages = np.loadtxt(file_path, unpack=True)
        return cls(cls._time , cls._voltages)

    @property #definisco le property di time e voltages per renderle variabili private
    def time(self):
        return self._dati[:,0]

    @property
    def voltages(self):
        return self._dati[:,1]

    def __len__(self): #calling the len() function on a class instance must return the number of entries
        ''' returning number of measurements'''
        return len(self._dati)

    def __getitem__(self, index, column=0):
        ''' returning an item of the data array'''
        return self._dati[index, column]

    def __iter__(self): #the class must be iterable: at each iteration, a numpy array of two values (time and voltage) corresponding to an entry in the file must be returned
        ''' returning a numpy array of two values '''
        for i in range(len(self)):
            yield self._dati[i, :] #NOTA: non sono sicura che questo returni qualcosa.


    #- the print() function must work on class instances. The output must show one entry (time and voltage), as well as the entry index, per line.- the class must also have a debug representation, printing just the values row by row. NON SO COSA CAMBI TRA LE DUE RICHIESTE

    def __repr__(self): #generiamo linee senza separazione con (''.join(...)), e poi uniamo queste linee con '\n'
        return '\n'.join('{} {}'.format(row[0],row[1]) for row in self._dati) #manfreda scrive solo self invece di self._dati

    def __str__(self):
         return '\n'.join('{} {}'.format(row[0],row[1]) for row in self._dati) #manfreda scrive solo self invece di self._dati e con un formato più bello ma dovrebbe funzionare anche lui


    def __call__(self, t): #the class must be callable, returning an interpolated value of the tension at a given time
        ''' returning an interpolated value of the tension at a given time t'''
        return self.spline(t)

    def plot(self, ax=None, fmt='bo', **plot_options): #The plot function must accept an 'ax' argument, so that the user can select the axes where the plot is added (with a new figure as default). The user must also be able to pass other plot options as usual
       """ Draw the data points using matplotlib.pyplot."""
       # The user can provide an existing figure to add the plot, otherwise we
       # create a new one.
       if ax is not None:
           plt.sca(ax) # sca (Set Current Axes) selects the given figure
       else:
           ax = plt.figure('voltage_vs_time')
       plt.plot(self.time, self.voltages, fmt, **plot_options)
       plt.xlabel('Time [s]')
       plt.ylabel('Voltage [mV]')
       plt.grid(True)
       return ax # We return the axes, just in case
