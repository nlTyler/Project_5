from unittest import TestCase
from unittest import main
import math
import BaseQueue as q


class TestBaseQueue(TestCase):
    def setUp(self) -> None:
        self.x = q.BaseQueue(20.0, 25.0)

    def test_init(self):
        self.assertAlmostEqual(20.0, self.x._lamda)
        self.assertAlmostEqual(25.0, self.x._mu)
        self.assertTrue(math.isnan(self.x.lq))
        self.assertTrue(math.isnan(self.x.p0))

    def test_is_valid(self):
        lamda = (20, 0, 20, 0, "twenty", 20, "twenty")
        mu = (25, 25, 0, 0, 25, "twenty-five", "twenty-five")
        expected = (True, False, False, False, False, False, False)

        for i in range(len(lamda)):
            with self.subTest(case=f'Lamda: {lamda[i]}, Mu: {mu[i]}'):
                testq = q.BaseQueue(lamda[i], mu[i])
                self.assertEqual(expected[i], testq.is_valid())

        # self.fail()
        return

    def test_is_feasible(self):
        lamda = (20, 0, 20, 0, 25, 40, "twenty", 20, "twenty")
        mu = (25, 25, 0, 0, 25, 25, 25, "twenty-five", "twenty-five")
        expected = (True, False, False, False, False, False, False, False, False)

        for i in range(len(lamda)):
            with self.subTest(case=f'Lamda: {lamda[i]}, Mu: {mu[i]}'):
                testq = q.BaseQueue(lamda[i], mu[i])
                self.assertEqual(expected[i], testq.is_feasible())
        return

    def test_calc_lq(self):
        self.assertTrue(math.isnan(self.x.lq))

        # change lamda and/or mu and ensure that lq is still nan
        self.x.lamda = 22
        self.assertTrue(math.isnan(self.x.lq))

        self.x.mu = 27
        self.assertTrue(math.isnan(self.x.lq))

    def test_lamda(self):
       # test getter
        self.assertEqual(20, self.x.lamda)

        # test setter with valid/feasible value
        self.x.lamda = 24
        self.assertEqual(24, self.x.lamda)
        self.assertEqual(True, self.x.is_valid())
        self.assertEqual(True, self.x.is_feasible())

        # test setter with valid/infeasible value
        self.x.lamda = 25
        self.assertEqual(25, self.x.lamda)
        self.assertEqual(True, self.x.is_valid())
        self.assertEqual(False, self.x.is_feasible())

        # test setter with valid/infeasible value
        self.x.lamda = 0
        self.assertTrue(math.isnan(self.x.lamda))
        self.assertEqual(False, self.x.is_valid())
        self.assertEqual(False, self.x.is_feasible())

        # test invalid values
        self.x.lamda = -20
        self.assertTrue(math.isnan(self.x.lamda))
        self.assertEqual(False, self.x.is_valid())
        self.assertEqual(False, self.x.is_feasible())

        self.x.lamda = "twenty"
        self.assertTrue(math.isnan(self.x.lamda))
        self.assertEqual(False, self.x.is_valid())
        self.assertEqual(False, self.x.is_feasible())

        # test setter with tuple input
        self.x.lamda = (5, 10, 5)
        self.assertAlmostEqual(20.0, self.x.lamda)
        self.assertTrue(self.x.is_valid())
        self.assertTrue(self.x.is_feasible())

        self.x.lamda = (5, 10, 25)
        self.assertAlmostEqual(40.0, self.x.lamda)
        self.assertTrue(self.x.is_valid())
        self.assertFalse(self.x.is_feasible())

        self.x.lamda = (5, 10, -5)
        self.assertTrue(math.isnan(self.x.lamda))
        self.assertFalse(self.x.is_valid())
        self.assertFalse(self.x.is_feasible())

        self.x.lamda = (5, 10, "five")
        self.assertTrue(math.isnan(self.x.lamda))
        self.assertFalse(self.x.is_valid())
        self.assertFalse(self.x.is_feasible())

    def test_mu(self):
        self.assertEqual(25, self.x._mu)

        # test getter
        self.assertEqual(25, self.x.mu)

        # test setter with valid/feasible value
        self.x.mu = 30
        self.assertEqual(30, self.x.mu)
        self.assertEqual(True, self.x.is_valid())
        self.assertEqual(True, self.x.is_feasible())

        # test setter with valid/infeasible value
        self.x.mu = 15
        self.assertEqual(15, self.x.mu)
        self.assertEqual(True, self.x.is_valid())
        self.assertEqual(False, self.x.is_feasible())

        # test setter with valid/infeasible value
        self.x.mu = 1
        self.assertEqual(1, self.x.mu)
        self.assertEqual(True, self.x.is_valid())
        self.assertEqual(False, self.x.is_feasible())

        # test setter with invalid values
        self.x.mu = 0
        self.assertTrue(math.isnan(self.x.mu))
        self.assertEqual(False, self.x.is_valid())
        self.assertEqual(False, self.x.is_feasible())

        self.x.mu = -25
        self.assertTrue(math.isnan(self.x.mu))
        self.assertEqual(False, self.x.is_valid())
        self.assertEqual(False, self.x.is_feasible())

        self.x.mu = "twenty-five"
        self.assertTrue(math.isnan(self.x.mu))
        self.assertEqual(False, self.x.is_valid())
        self.assertEqual(False, self.x.is_feasible())

    def test_r(self):
        self.assertAlmostEqual(0.80, self.x.r)

        self.x.lamda = 25
        self.assertAlmostEqual(1.0, self.x.r)

        self.x.lamda = 37.5
        self.assertAlmostEqual(1.5, self.x.r)


    def test_ro(self):
        self.x = q.BaseQueue(20.0, 25.0)
        self.assertAlmostEqual(0.80, self.x.ro)

        self.x.lamda = 25
        self.assertAlmostEqual(1.0, self.x.ro)

        self.x.lamda = 37.5
        self.assertAlmostEqual(1.5, self.x.ro)


    def test_lq(self):
        # lq should always be nan for a BaseQueue instance
        self.assertTrue(math.isnan(self.x.lq))

        # force lq to something else just to verify that we get the value correctly
        self.x._lq = 100
        self.x._recalc_needed = False
        self.assertEqual(100, self.x.lq)

    def test_l(self):
        self.assertTrue(math.isnan(self.x.l))
        # self.assertEqual(None, self.x.l)

        # force lq to something else just to verify that we get the value correctly
        self.x._lq = 3.2
        self.x._recalc_needed = False
        self.assertAlmostEqual(4.0, self.x.l)

    def test_wq(self):
        self.assertTrue(math.isnan(self.x.wq))

        # force lq to something else just to verify that we get the value correctly
        self.x._lq = 3.2
        self.x._recalc_needed = False
        self.assertAlmostEqual(0.16, self.x.wq)

    def test_w(self):
        # self.x = q.BaseQueue(20.0, 25.0)
        self.assertTrue(math.isnan(self.x.w))

        # force lq to something else just to verify that we get the value correctly
        self.x._lq = 3.2
        self.x._recalc_needed = False
        self.assertAlmostEqual(0.20, self.x.w)


if __name__ == '__main__':
    main(verbosity=2)


