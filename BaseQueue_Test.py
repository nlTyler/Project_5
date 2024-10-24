from unittest import TestCase
from unittest import main
import math
import BaseQueue as q


class BaseQueue_Test(TestCase):
    def setUp(self) -> None:
        self.queue = q.BaseQueue(20.0, 25.0)

    def test_initialization(self):
        """Test that the BaseQueue initializes correctly."""
        self.assertAlmostEqual(self.queue.lamda, 20.0)
        self.assertAlmostEqual(self.queue.mu, 25.0)
        self.assertTrue(math.isnan(self.queue.lq))  # Check if lq is NaN
        self.assertTrue(math.isnan(self.queue.p0))  # Check if p0 is NaN

    def test_validity(self):
        """Test the validity of different lamda and mu values."""
        valid_cases = [(20, 25)]
        invalid_cases = [(20, 0), (0, 0), (-5, 10), (10, -2), ("twenty", 30)]

        for lamda, mu in valid_cases:
            with self.subTest(lamda=lamda, mu=mu):
                queue = q.BaseQueue(lamda, mu)
                self.assertTrue(queue.is_valid())

        for lamda, mu in invalid_cases:
            with self.subTest(lamda=lamda, mu=mu):
                queue = q.BaseQueue(lamda, mu)
                self.assertFalse(queue.is_valid())

    def test_lamda_setter(self):
        """Test the lamda setter and its effects on state."""
        self.queue.lamda = 30
        self.assertEqual(self.queue.lamda, 30)
        self.assertTrue(self.queue.is_valid())
        self.assertFalse(self.queue.is_feasible())

        # Test with an invalid value
        self.queue.lamda = -10
        self.assertTrue(math.isnan(self.queue.lamda))
        self.assertFalse(self.queue.is_valid())

    def test_mu_setter(self):
        """Test the mu setter and its effects on state."""
        self.queue.mu = 40
        self.assertEqual(self.queue.mu, 40)
        self.assertTrue(self.queue.is_valid())
        self.assertTrue(self.queue.is_feasible())

        # Test with an invalid value
        self.queue.mu = 0
        self.assertTrue(math.isnan(self.queue.mu))
        self.assertFalse(self.queue.is_valid())

    def test_queue_metrics(self):
        """Test calculated metrics like rho."""
        self.assertAlmostEqual(self.queue.ro, 0.8)  # Check initial ro
        self.queue.lamda = 30
        self.assertAlmostEqual(self.queue.ro, 1.2)  # Check updated ro


if __name__ == '__main__':
    main(verbosity=2)