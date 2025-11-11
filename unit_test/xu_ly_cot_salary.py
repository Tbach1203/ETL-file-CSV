import unittest
import pandas as pd
import numpy as np
import sys 
sys.path.insert(0, 'D:/DA_DE/DE/DEC_Unigap/Mini_Project')
import xu_ly_du_lieu

class TestProcessSalary(unittest.TestCase):
    
    def test_integer_million(self):
        """Test với số nguyên và từ 'triệu'"""
        self.assertEqual(xu_ly_du_lieu.process_salary('3 triệu'), 3000000)
        self.assertEqual(xu_ly_du_lieu.process_salary('10 Triệu'), 10000000)

    def test_multiple_numbers(self):
        """Test với nhiều số trong chuỗi (chỉ lấy số đầu tiên)"""
        self.assertEqual(xu_ly_du_lieu.process_salary('3 - 5 triệu'), 3000000)
        self.assertEqual(xu_ly_du_lieu.process_salary('4.2 - 6.8 triệu'), 4200000)
if __name__ == '__main__':
    # Chạy tests
    unittest.main(verbosity=2)