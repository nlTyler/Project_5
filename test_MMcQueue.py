from unittest import TestCase
from unittest import main
import math

from MMcQueue import MMcQueue


class TestMMcQueue(TestCase):
    def setUp(self) -> None:
        self.lamdaj = [(20,), (24,), (5, 10, 10), (0,), (5, 10, 5), (5, 10, 5), (5, 10, 9), (10, 15, 15), (10, 15, 15), (5, 10, -5), (5, 10, "five")]
        self.lamda = [20, 24, 25, 0, 20, 20, 24, 40, 40, math.nan, math.nan]
        self.mu = [25, 25, 25, 25, 0, 25, 25, 25, 25, 25, 25]
        self.c = [1, 1, 1, 1, 1, 1, 2, 3, 3, 1, 1]
        self.is_valid = [True, True, True, False, False, True, True, True, True, False, False]
        self.is_feasible = [True, True, False, False, False, True, True, True, True, False, False]
        self._lamda = [20, 24, 25, math.nan, 20, 20, 24, 40, 40, math.nan, math.nan]
        self._mu = [25, 25, 25, 25, math.nan, 25, 25, 25, 25, 25, 25]

        self.lq = [3.2, 23.04, math.inf, math.nan, math.nan, 3.2, 0.287401247401247, 0.312910618792972,
                   0.312910618792972, math.nan, math.nan]
        self.l = [4, 24, math.inf, math.nan, math.nan, 4, 1.24740124740125, 1.91291061879297, 1.91291061879297,
                  math.nan, math.nan]
        self.w = [0.2, 1, math.inf, math.nan, math.nan, 0.2, 0.051975051975052, 4.78227654698243E-02,
                  4.78227654698243E-02, math.nan, math.nan]
        self.wq = [0.16, 0.96, math.inf, math.nan, math.nan, 0.16, 0.011975051975052, 7.82276546982429E-03,
                   7.82276546982429E-03, math.nan, math.nan]
        self.p0 = [0.2, 0.04, math.inf, math.nan, math.nan, 0.2, 0.351351351351351, 0.187165775401069,
                   0.187165775401069, math.nan, math.nan]
        self.wqk = [(0.16,), (0.96,), (math.inf,), (math.nan,), (math.nan,), (0.04, 0.1, 0.4),
                    (6.91891891891892E-03, 9.88416988416989E-03, 1.71072171072171E-02),
                    (4.21225832990539E-03, 6.31838749485808E-03, 1.17341482047364E-02),
                    (4.21225832990539E-03, 6.31838749485808E-03, 1.17341482047364E-02),
                    (1.46112886048988E-02, 3.13099041533546E-02, 0.375718849840255),
                    (math.nan, math.nan, math.nan),
                    (math.nan, math.nan, math.nan)]

        self.q = [MMcQueue(self.lamda[i], self.mu[i], self.c[i]) for i in range(0, len(self.lamda))]

        # print(self.x)

    def test_init(self):

        for i in range(0, len(self.q)):
            with self.subTest(lamda=self.lamda[i], mu=self.mu[i], c=self.c[i]):
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
            with self.subTest(lamda=self.lamda[i], mu=self.mu[i], c=self.c[i]):
                self.assertEqual(self.is_valid[i], self.q[i].is_valid())

    def test_feasible(self):
        for i in range(0, len(self.q)):
            with self.subTest(lamda=self.lamda[i], mu=self.mu[i], c=self.c[i]):
                self.assertEqual(self.is_feasible[i], self.q[i].is_feasible())

    def test_lq(self):
        # test the default instance
        for i in range(0, len(self.q)):
            with self.subTest(lamda=self.lamda[i], mu=self.mu[i], c=self.c[i]):
                if(math.isinf(self.lq[i])):
                    self.assertTrue(math.isinf(self.q[i].lq))
                elif(math.isnan(self.lq[i])):
                    self.assertTrue(math.isnan(self.q[i].lq))
                else:
                    self.assertAlmostEqual(self.lq[i], self.q[i].lq)

    def test_l(self):
        # test the default instance
        for i in range(0, len(self.q)):
            with self.subTest(lamda=self.lamda[i], mu=self.mu[i], c=self.c[i]):
                if(math.isinf(self.l[i])):
                    self.assertTrue(math.isinf(self.q[i].l))
                elif(math.isnan(self.l[i])):
                    self.assertTrue(math.isnan(self.q[i].l))
                else:
                    self.assertAlmostEqual(self.l[i], self.q[i].l)

    def test_wq(self):
        # test the default instance
        for i in range(0, len(self.q)):
            with self.subTest(lamda=self.lamda[i], mu=self.mu[i], c=self.c[i]):
                if(math.isinf(self.wq[i])):
                    self.assertTrue(math.isinf(self.q[i].wq))
                elif(math.isnan(self.wq[i])):
                    self.assertTrue(math.isnan(self.q[i].wq))
                else:
                    self.assertAlmostEqual(self.wq[i], self.q[i].wq)

    def test_w(self):
        # test the default instance
        for i in range(0, len(self.q)):
            with self.subTest(lamda=self.lamda[i], mu=self.mu[i], c=self.c[i]):
                if (math.isinf(self.w[i])):
                    self.assertTrue(math.isinf(self.q[i].w))
                elif (math.isnan(self.w[i])):
                    self.assertTrue(math.isnan(self.q[i].w))
                else:
                    self.assertAlmostEqual(self.w[i], self.q[i].w)

    def test_p0(self):
        # test the default instance
        for i in range(0, len(self.q)):
            with self.subTest(lamda=self.lamda[i], mu=self.mu[i], c=self.c[i]):
                if(math.isinf(self.p0[i])):
                    self.assertTrue(math.isinf(self.q[i].p0))
                elif(math.isnan(self.p0[i])):
                    self.assertTrue(math.isnan(self.q[i].p0))
                else:
                    self.assertAlmostEqual(self.p0[i], self.q[i].p0)

    def test_required_attributes(self):
        # force recalc cycle so that attributes created by _calc_metrics will exist
        x = MMcQueue(20, 25, 1)
        x._calc_metrics()

        # verify that required internal variables exist
        for v in ['_lamda', '_mu', '_c', '_lq', '_p0', '_recalc_needed']:
            with self.subTest(case=f'Required member: {v}'):
                self.assertTrue(v in dir(x))

        # verify that attributes for child classes do not exist
        for v in ['_sigma', '_lamda_k']:
            with self.subTest(case=f'Child class member: {v}'):
                self.assertFalse(v in dir(x))

    def test_derived_attributes(self):
        # force recalc cycle so that attributes created by _calc_metrics will exist
        x = MMcQueue(20, 25, 1)
        x._calc_metrics()

        # verify that derived variables do not exist as saved variables
        for v in ['_l', '_wq', '_w', '_r', '_ro', '_rho', '_utilization']:
            with self.subTest(case=f'Required member: {v}'):
                self.assertFalse(v in dir(x))

    def test_required_properties(self):
        # force recalc cycle so that attributes created by _calc_metrics will exist
        x = MMcQueue(20, 25, 1)
        x._calc_metrics()

        # verify that required properties exist
        for v in ['lamda', 'mu', 'c', 'lq', 'l', 'wq', 'w', 'r', 'ro', 'utilization']:
            with self.subTest(case=f'Required property: {v}'):
                self.assertTrue(isinstance(getattr(MMcQueue, v, None), property))


if __name__ == '__main__':
    main(verbosity=2)