from unittest import TestCase
from unittest import main
import math

from MG1Queue import MG1Queue


class TestMG1Queue(TestCase):
    def setUp(self) -> None:
        self.lamda = [20, 24, 25, 0, 20, 0, 24, 20, 24, "twenty", 20, "twenty", (5, 10, 5), (5, 10, -5), (5, 10, "five"), 20, 20]
        self.mu = [25, 25, 25, 25, 0, 25, 25, 25, 25, 25, "twenty-five", "twenty-five", 25, 25, 25, 25, 25]
        self.sigma = [0, 0, 0, 0, 0, 0.02, 0.02, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, -0.04, "invalid"]

        self.is_valid = [True, True, True, False, False, False, True, True, True, False, False, False, True, False, False, False, False]
        self.is_feasible = [True, True, False, False, False, False, True, True, True, False, False, False, True, False, False, True, True]
        self._lamda = [20, 24, 25, math.nan, 20, math.nan, 24, 20, 24, math.nan, 20.0, math.nan, 20.0, math.nan, math.nan, 20.0, 20.0]
        self._mu = [25, 25, 25, 25, math.nan, 25, 25, 25, 25, 25.0, math.nan, math.nan, 25.0, 25.0, 25.0, 25.0, 25.0]
        self._sigma = [0, 0, 0, 0, 0, 0.02, 0.02, 0.04, 0.04, 0.04, 0.0, 0.0, 0.4, 0.4, 0.4, math.nan, math.nan]

        self.lq = [1.6, 11.52, math.inf, math.nan, math.nan, math.nan, 14.4, 3.2, 23.04, math.nan, math.nan, math.nan, 3.2, math.nan, math.nan, math.nan, math.nan]
        self.l = [2.4, 12.48, math.inf, math.nan, math.nan, math.nan, 15.36, 4, 24, math.nan, math.nan, math.nan, 4.0, math.nan, math.nan, math.nan, math.nan]
        self.w = [0.12, 0.52, math.inf, math.nan, math.nan, math.nan, 0.64, 0.2, 0.999999999999999, math.nan, math.nan, math.nan, 0.20, math.nan, math.nan, math.nan, math.nan]
        self.wq = [0.08, 0.48, math.inf, math.nan, math.nan, math.nan, 0.6, 0.16, 0.959999999999999, math.nan, math.nan, math.nan, 0.16, math.nan, math.nan, math.nan, math.nan]
        self.p0 = [0.2, 0.04, math.inf, math.nan, math.nan, math.nan, 0.04, 0.2, 0.04, math.nan, math.nan, math.nan, 0.2, math.nan, math.nan, math.nan, math.nan]

        self.q = [MG1Queue(self.lamda[i], self.mu[i], self.sigma[i]) for i in range(0, len(self.lamda))]

        # print(self.x)

    def test_init(self):

        for i in range(0, len(self.q)):
            with self.subTest(lamda=self.lamda[i], mu=self.mu[i], sigmas=self.sigma[i]):
                if math.isnan(self._lamda[i]):
                    self.assertTrue(math.isnan(self.q[i].lamda))
                else:
                    self.assertEqual(self._lamda[i], self.q[i].lamda)

                if math.isnan(self._mu[i]):
                    self.assertTrue(math.isnan(self.q[i].mu))
                else:
                    self.assertEqual(self._mu[i], self.q[i].mu)

    def test_valid(self):

        for i in range(0, len(self.q)):
            with self.subTest(lamda=self.lamda[i], mu=self.mu[i], sigmas=self.sigma[i]):
                self.assertEqual(self.is_valid[i], self.q[i].is_valid())

    def test_feasible(self):
        for i in range(0, len(self.q)):
            with self.subTest(lamda=self.lamda[i], mu=self.mu[i], sigmas=self.sigma[i]):
                self.assertEqual(self.is_feasible[i], self.q[i].is_feasible())

    def test_lq(self):
        # test the default instance
        for i in range(0, len(self.q)):
            with self.subTest(lamda=self.lamda[i], mu=self.mu[i], sigmas=self.sigma[i]):
                if(math.isinf(self.lq[i])):
                    self.assertTrue(math.isinf(self.q[i].lq))
                elif(math.isnan(self.lq[i])):
                    self.assertTrue(math.isnan(self.q[i].lq))
                else:
                    self.assertAlmostEqual(self.lq[i], self.q[i].lq)

    def test_l(self):
        # test the default instance
        for i in range(0, len(self.q)):
            with self.subTest(lamda=self.lamda[i], mu=self.mu[i]):
                if(math.isinf(self.l[i])):
                    self.assertTrue(math.isinf(self.q[i].l))
                elif(math.isnan(self.l[i])):
                    self.assertTrue(math.isnan(self.q[i].l))
                else:
                    self.assertAlmostEqual(self.l[i], self.q[i].l)

    def test_wq(self):
        # test the default instance
        for i in range(0, len(self.q)):
            with self.subTest(lamda=self.lamda[i], mu=self.mu[i], sigma=self.sigma[i]):
                if(math.isinf(self.wq[i])):
                    self.assertTrue(math.isinf(self.q[i].wq))
                elif(math.isnan(self.wq[i])):
                    self.assertTrue(math.isnan(self.q[i].wq))
                else:
                    self.assertAlmostEqual(self.wq[i], self.q[i].wq)

    def test_w(self):
        # test the default instance
        for i in range(0, len(self.q)):
            with self.subTest(lamda=self.lamda[i], mu=self.mu[i]):
                if (math.isinf(self.w[i])):
                    self.assertTrue(math.isinf(self.q[i].w))
                elif (math.isnan(self.w[i])):
                    self.assertTrue(math.isnan(self.q[i].w))
                else:
                    self.assertAlmostEqual(self.w[i], self.q[i].w)

    def test_p0(self):
        # test the default instance
        for i in range(0, len(self.q)):
            with self.subTest(lamda=self.lamda[i], mu=self.mu[i]):
                if(math.isinf(self.p0[i])):
                    self.assertTrue(math.isinf(self.q[i].p0))
                elif(math.isnan(self.p0[i])):
                    self.assertTrue(math.isnan(self.q[i].p0))
                else:
                    self.assertAlmostEqual(self.p0[i], self.q[i].p0)

    def test_required_attributes(self):
        # force recalc cycle so that attributes created by _calc_metrics will exist
        x = MG1Queue(20, 25, 5)
        x._calc_metrics()

        # verify that required internal variables exist
        for v in ['_lamda', '_mu', '_sigma', '_lq', '_p0', '_recalc_needed']:
            with self.subTest(case=f'Required member: {v}'):
                self.assertTrue(v in dir(x))

        # verify that attributes for child classes do not exist
        for v in ['_c', '_lamda_k']:
            with self.subTest(case=f'Child class member: {v}'):
                self.assertFalse(v in dir(x))

    def test_derived_attributes(self):
        # force recalc cycle so that attributes created by _calc_metrics will exist
        x = MG1Queue(20, 25, 5)
        x._calc_metrics()

        # verify that derived variables do not exist as saved variables
        for v in ['_l', '_wq', '_w', '_r', '_ro', '_rho', '_utilization']:
            with self.subTest(case=f'Required member: {v}'):
                self.assertFalse(v in dir(x))

    def test_required_properties(self):
        # force recalc cycle so that attributes created by _calc_metrics will exist
        x = MG1Queue(20, 25, 5)
        x._calc_metrics()

        # verify that required properties exist
        for v in ['lamda', 'mu', 'sigma', 'lq', 'l', 'wq', 'w', 'r', 'ro', 'utilization']:
            with self.subTest(case=f'Required property: {v}'):
                self.assertTrue(isinstance(getattr(MG1Queue, v, None), property))


if __name__ == '__main__':
    main(verbosity=2)