import unittest
import numpy as np
from matplotlib import pyplot as plt
from Assegnamento5 import VoltageData
#pylint: disable=invalid-name

class TestVoltageData(unittest.TestCase): #- [optional] rewrite the run_tests() function in sandbox/test_voltage_data.py as a sequence of proper UnitTests


    def setUp(self):
        data2=VoltageData.from_file('Sample_data_file.txt') #Non ci interessa che data sia  un oggetto della classe unitest, deve solo essere della classe voltagedata
        self.t, self.v = np.loadtxt('Sample_data_file.txt', unpack=True)
        data =VoltageData(self.t , self.v)

    def test_len(self):
        self.assertEqual( len(self.t) , len(self.v) )

    def test_attribute(self):
        self.assertTrue(np.array_equal(data.voltages, self.v, equal_nan=True))
        self.assertTrue(np.array_equal(data.time, self.t, equal_nan=True))

    def test_square_parenthesis(self):
        self.assertAlmostEqual(self.v[3], data.voltages(3, 1)) #Così potrebbe funzionare, getitem deve avere solo un valore in ingresso perchè così è definito il metodo speciale __getitem__
        self.assertAlmostEqual(self.t[-1], data.__getitem__(-1, 0))

    '''def test_slicing(self):
        for i in range(5):
            self.assertTrue( self.v[i] , self.data.__getitem__(i, 1) ) #(v_data[1:5, 1] == v[1:5]) 
            Secondo me è self.v[1:5]=data.voltages[1:5]
    '''
    def test_constructor_from_data_file(self):
    
        self.assertTrue(np.array_equal( data2.voltages, self.v , equal_nan=True))
        self.assertTrue(np.array_equal( data2.time, self.t , equal_nan=True))

    def test_iteration(self):
        for i, entry in enumerate(data):
            self.assertAlmostEqual( entry[1], self.v[i])
            self.assertAlmostEqual( entry[0], self.t[i])

    def test_interpolation(self):
        v5=data(data.time[5])
        self.assertTrue(np.abs(self.v[5]- v5< 1.e-5))

    def test_plot(self):
        data.plot(fmt='ko', markersize=6, label='normal voltage')
        x_grid = np.linspace(min(self.t), max(self.t), 200)
        plt.plot(x_grid, data(x_grid), 'r-', label='spline')
        plt.legend()
        plt.show()

    def test_print(self):
        print(data,'\n')
        print(repr(data))


if __name__=='__main__':
   unittest.main()
