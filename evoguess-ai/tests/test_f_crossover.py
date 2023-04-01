import unittest

from instance.module.variables import Interval, Backdoor
from algorithm.module.crossover import OnePoint, TwoPoint, Uniform


class RandomStateStub:
    def __init__(self, values=()):
        self.index = -1
        self.values = values

    def randint(self, *args):
        self.index += 1
        return self.values[self.index]

    def rand(self, *args):
        return self.values


class TestCrossover(unittest.TestCase):
    def test_one_point(self):
        crossover = OnePoint()
        backdoor = Backdoor(
            from_vars=Interval(start=1, length=8).variables()
        )

        crossover.random_state = RandomStateStub([6, 0])
        self.assertEqual(
            crossover.cross(
                backdoor.get_copy([1, 1, 0, 1, 1, 0, 1, 1]),
                backdoor.get_copy([0, 0, 0, 0, 1, 0, 0, 1])
            ),
            (
                backdoor.get_copy([0, 0, 0, 0, 1, 0, 1, 1]),
                backdoor.get_copy([1, 1, 0, 1, 1, 0, 0, 1])
            )
        )

        crossover.random_state = RandomStateStub([6, 1])
        self.assertEqual(
            crossover.cross(
                backdoor.get_copy([1, 1, 0, 1, 1, 0, 1, 1]),
                backdoor.get_copy([0, 0, 0, 0, 1, 0, 0, 1])
            ),
            (
                backdoor.get_copy([1, 1, 0, 1, 1, 0, 0, 1]),
                backdoor.get_copy([0, 0, 0, 0, 1, 0, 1, 1]),
            )
        )

    def test_two_point(self):
        crossover = TwoPoint()
        backdoor = Backdoor(
            from_vars=Interval(start=1, length=8).variables()
        )

        crossover.random_state = RandomStateStub([3, 6])
        self.assertEqual(
            crossover.cross(
                backdoor.get_copy([1, 1, 0, 1, 1, 0, 1, 1]),
                backdoor.get_copy([0, 0, 0, 0, 1, 0, 0, 1])
            ),
            (
                backdoor.get_copy([1, 1, 0, 0, 1, 0, 1, 1]),
                backdoor.get_copy([0, 0, 0, 1, 1, 0, 0, 1])
            )
        )

        crossover.random_state = RandomStateStub([7, 2])
        self.assertEqual(
            crossover.cross(
                backdoor.get_copy([1, 1, 0, 1, 1, 0, 1, 1]),
                backdoor.get_copy([0, 0, 0, 0, 1, 0, 0, 1])
            ),
            (
                backdoor.get_copy([1, 1, 0, 0, 1, 0, 0, 1]),
                backdoor.get_copy([0, 0, 0, 1, 1, 0, 1, 1])
            )
        )

    def test_uniform(self):
        backdoor = Backdoor(
            from_vars=Interval(start=1, length=8).variables()
        )

        crossover = Uniform()
        crossover.random_state = RandomStateStub(
            [0, 0.51, 0.1, 0.23, 0.9, 0.1, 0.8, 0.7]
        )
        self.assertEqual(
            crossover.cross(
                backdoor.get_copy([1, 1, 0, 1, 1, 0, 1, 1]),
                backdoor.get_copy([0, 0, 0, 0, 1, 0, 0, 1])
            ),
            (
                backdoor.get_copy([0, 1, 0, 0, 1, 0, 1, 1]),
                backdoor.get_copy([1, 0, 0, 1, 1, 0, 0, 1])
            )
        )

        crossover = Uniform(swap_prob=0.2)
        crossover.random_state = RandomStateStub(
            [0, 0.51, 0.1, 0.23, 0.9, 0.1, 0.8, 0.7]
        )
        self.assertEqual(
            crossover.cross(
                backdoor.get_copy([1, 1, 0, 1, 1, 0, 1, 1]),
                backdoor.get_copy([0, 0, 0, 0, 1, 0, 0, 1])
            ),
            (
                backdoor.get_copy([0, 1, 0, 1, 1, 0, 1, 1]),
                backdoor.get_copy([1, 0, 0, 0, 1, 0, 0, 1])
            )
        )
