import unittest
import numpy as np
from matplotlib import pyplot as plt
from Assegnamento5 import VoltageData
#pylint: disable=invalid-name

class TestVoltageData(unittest.TestCase): #- [optional] rewrite the run_tests() function in sandbox/test_voltage_data.py as a sequence of proper UnitTests


    def setUp(self):
        self.data2=VoltageData.from_file('Sample_data_file.txt')
        self.t, self.v = np.loadtxt('Sample_data_file.txt', unpack=True)
        self.data =VoltageData(self.t , self.v)

    def test_len(self):
        self.assertEqual( len(self.t) , len(self.v) )

    def test_attribute(self):
        self.assertTrue(np.array_equal(self.data.voltages, self.v, equal_nan=True))
        self.assertTrue(np.array_equal(self.data.time, self.t, equal_nan=True))

    def test_square_parenthesis(self):
        self.assertAlmostEqual(self.v[3], self.data.voltages[3]) #Così potrebbe funzionare, getitem deve avere solo un valore in ingresso perchè così è definito il metodo speciale __getitem__
        self.assertAlmostEqual(self.t[-1], self.data.time[-1])

    def test_slicing(self):
        self.assertTrue(np.array_equal(self.v[1:5], self.data.voltages[1:5], equal_nan=True))


    def test_constructor_from_data_file(self):

        self.assertTrue(np.array_equal( self.data2.voltages, self.v , equal_nan=True))
        self.assertTrue(np.array_equal( self.data2.time, self.t , equal_nan=True))

    def test_iteration(self):
        for i, entry in enumerate(self.data):
            self.assertAlmostEqual( entry[1], self.v[i])
            self.assertAlmostEqual( entry[0], self.t[i])

    def test_interpolation(self):
        v5=self.data(self.data.time[5])
        self.assertTrue(np.abs(self.v[5]- v5< 1.e-5))

    def test_plot(self):
        self.data.plot(fmt='ko', markersize=6, label='normal voltage')
        x_grid = np.linspace(min(self.t), max(self.t), 200)
        plt.plot(x_grid, self.data(x_grid), 'r-', label='spline')
        plt.legend()
        plt.show()

    def test_print(self):
        print(self.data,'\n')
        print(repr(self.data))


if __name__=='__main__':
   unittest.main()
