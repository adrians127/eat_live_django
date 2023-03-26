from django.test import TestCase
from calculators.bmi_calculator import calculate_bmi
from calculators.water_calculator import water_calculate
from calculators.calories_calculator import *


class CalculatorTests(TestCase):
    def test_calculate_bmi(self):
        self.assertEqual(calculate_bmi(95, 186), 27.5)
        self.assertEqual(calculate_bmi(4, 290), -1)
        self.assertEqual(calculate_bmi(80, 0), -1)

    def test_water_calculate(self):
        self.assertEqual(water_calculate(21, "man"), 2500)
        self.assertEqual(water_calculate(50, "mAn"), 2500)
        self.assertEqual(water_calculate(50, "woman"), 2000)
        self.assertEqual(water_calculate(500, "woman"), -1)
        self.assertEqual(water_calculate(20, "blable"), 2500)
        self.assertEqual(water_calculate(20, 3000), -1)

    def test_calories_calculate(self):
        self.assertEqual(calculate_calories(59, 162, 40, "woman", 1.4), 1865)
        self.assertEqual(calculate_calories(80, 185, 35, "man", 1.2), 2226)
        self.assertEqual(calculate_protein(2226), (55.65, 111.3))
        self.assertEqual(calculate_fat(2226), (61.83, 86.57))
        self.assertEqual(calculate_carbohydrates(2226), (250.43, 361.73))
        self.assertEqual(calculate_nutritions(80, 185, 35, "man"),
                         (2226, (61.83, 86.57), (55.65, 111.3),  (250.43, 361.73)))
