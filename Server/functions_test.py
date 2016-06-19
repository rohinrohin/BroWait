from functions import *
import unittest

class TestSequenceFunctions(unittest.TestCase):

    def test_createPoints(self):
        x_val = [2, 3, 4, 5]
        y_val = [3, 4, 5, 6]
        y_val_incorrect_length = [3, 4]
        expected_data = [(2,3), (3,4), (4,5), (5,6)]
        self.assertListEqual(expected_data, createPoints(x_val, y_val))
        self.assertListEqual([], createPoints(x_val, y_val_incorrect_length))
        self.assertListEqual([], createPoints(x_val, "blah"))

    def test_getValidDataPoints(self):
        x_val = [20, 30, 45, 55, 66, 78, 89]
        y_val = [3, 4, 5, 6, 7, 8, 9]
        y_short = [3,4,5,6]
        expected_data_min_3 = ([20,30,45],[3,4,5])
        result_19 = getValidDataPoints(x_val, y_val, 19)
        result_25 = getValidDataPoints(x_val, y_val, 25)
        result_45 = getValidDataPoints(x_val, y_val, 45)
        result_500 = getValidDataPoints(x_val, y_val, 500)
        result_60 = getValidDataPoints(x_val, y_val, 60)
        self.assertTupleEqual(result_19, expected_data_min_3)
        self.assertTupleEqual(result_25, expected_data_min_3)
        self.assertTupleEqual(result_45, expected_data_min_3)
        self.assertTupleEqual(result_500, (x_val,y_val))
        self.assertTupleEqual(result_60, (x_val[0:5],y_val[0:5]))
        self.assertTupleEqual(([],[]), getValidDataPoints(x_val, y_short, 25))
        self.assertTupleEqual(([],[]), getValidDataPoints(x_val, y_short, "blah"))
        self.assertTupleEqual(([],[]), getValidDataPoints(x_val, "blah", 25))

suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)