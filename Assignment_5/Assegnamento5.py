'''
Classe Voltage data per leggere un file in ingresso con due colonne
'''
import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
import matplotlib.pyplot as plt
#pylint: disable=invalid-name

class VoltageData(): #the class name must be VoltgeData

    ''' Class for handling a sequence of voltage measurements at different times.
    '''
    def __init__(self, t, v):
        '''
        the values should be accessible with the familiar square parenthesis syntax:
        the  first index must refer to the entry, the second selects time (0) or voltage (1).
        Slicing must also work.
        Mettendo ([t,v]) posso usare l'indice 0 per predere t e l'indice 1 per prendere v
        mettendo 0 o 1 al secondo posto nell'argomento dell'array.
        '''

        self._time=np.array(t, dtype=np.float64) #returning a numpy array of type numpy.float64
        self._voltages=np.array(v, dtype=np.float64)

        self._dati=np.column_stack((self._time, self._voltages))
        self.spline=InterpolatedUnivariateSpline(self._time, self._voltages) #building the spline


    @classmethod
    def from_file(cls, file_path):
        """ Alternate constructor from a data file, exploiting load_txt()"""
        cls._time, cls._voltages = np.loadtxt(file_path, unpack=True)
        return cls(cls._time , cls._voltages)

    @property
    def time(self):
        '''
        property per rendere time una variabile privata
        '''
        return self._dati[:,0]

    @property
    def voltages(self):
        '''
        property per rendere voltages una variabile privata
        '''
        return self._dati[:,1]

    def __len__(self):
        ''' returning number of measurements'''
        return len(self._dati)

    def __getitem__(self, index, column=0): #Mettere questa sintassi credo sia sbagliato perché il metodo magico getitem accetta solo un argomento oltre a self che è l'indice 
        ''' returning an item of the data array'''
        return self._dati[index, column]

    def __iter__(self):
        ''' returning a numpy array of two values '''
        for i in range(len(self)):
            yield self._dati[i, :] #NOTA: non sono sicura che questo returni qualcosa.


    def __repr__(self):
        '''genera linee senza separazione con (''.join(...)), e poi le unisce con '\n'
        '''
        return '\n'.join('{} {}'.format(row[0],row[1]) for row in self._dati)

    def __str__(self):
        '''genera linee senza separazione con (''.join(...)), e poi le unisce con '\n'
        '''
        return '\n'.join('{} {}'.format(row[0],row[1]) for row in self._dati)


    def __call__(self, t):
        ''' returning an interpolated value of the tension at a given time t'''
        return self.spline(t)

    def plot(self, ax=None, fmt='bo', **plot_options):
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
