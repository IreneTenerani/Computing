import unittest
from matplotlib import pyplot as plt
from Assegnamento5 import VoltageData

class TestVoltageData(unittest.TestCase): #- [optional] rewrite the run_tests() function in sandbox/test_voltage_data.py as a sequence of proper UnitTests


  def setUp():
    t,v = numpy.loadtxt('sandbox/sample_data_file.txt', unpack=True)
    v_data=VoltageData(t,v)
    

if __name__=='__main__':
   unittest.main()