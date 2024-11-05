
import math

from MMcQueue import MMcQueue


class MMcPriorityQueue(MMcQueue):
    """
        Represents a multi-server queueing system (M/M/c) inheriting from BaseQueue.

        Attributes:
            lamda (float): Arrival rate.
            mu (float): Service rate.
            c (int): Number of servers.
            lq (float): Average number of customers in the queue.
            l (float): Average number of customers in the system.
            wq (float): Average time a customer spends waiting in the queue.
            w (float): Average time a customer spends in the system.
            p0 (float): Probability that the system is empty.
            ro (float): Traffic intensity.
            r (float): Average number of customers in the system including those in service.
            utilization (float): Utilization of the system in percentage.
        """

    def __init__(self, lamda: float, mu: float, c: int):
        super().__init__(lamda, mu, c)
        self._lamda_k = lamda

    @property
    def lamda_k(self):
        """
        Gets the tuple of arrival rates (lamda_k) for each priority class.

        Returns:
            tuple: Tuple containing individual lambda values for each priority class.
        """
        return self._lamda_k

    @lamda_k.setter
    def lamda_k(self, value: float):
        """
        Sets the tuple of arrival rates for each priority class and updates aggregate lamda.

        Args:
            value (tuple): Tuple containing individual lambda values for each priority class.
        """

        self.lamda = value


    @property
    def lamda(self):
        """
                Gets the aggregate arrival rate.

                Returns:
                    float: Aggregate arrival rate (sum of lamda_k values).
                """
        return self._lamda

    @lamda.setter
    def lamda(self, value: float):
        """
                Sets the aggregate arrival rate, recalculating it based on lamda_k values.

                Args:
                    value (tuple): Tuple containing individual lambda values for each priority class.
                """

        self._lamda = self.simplify_lamda()

        if math.isnan(self._lamda):
            self._lamda_k = (math.nan,)
        else:
            self._lamda_k = value

        self._recalc_needed = True

    def get_b_k(self, k: int) -> float:
        """
                Calculates the blocking probability for priority class k.

                Args:
                    k (int): Priority class index (1-based).

                Returns:
                    float: Blocking probability for the specified priority class.
                """
        if not isinstance(self.lamda, tuple):
            w_lamda = (self.lamda,)
        else:
            w_lamda = self.lamda
        if k != 0:
            rhoj = []
            for l in range(k):
                rhoj.append(w_lamda[l] / (self.c * self.mu))
            # Calculates the blocking probability
            return 1 - sum(rhoj)
        else:
            return 1

    def get_l_k(self, k: int) -> float:
        """
                Calculates the average number of customers in the system for priority class k.

                Args:
                    k (int): Priority class index (1-based).

                Returns:
                    float: Average number of customers in the system for the specified priority class.
                """
        if k <= 0:
            return math.inf
        else:
            return self.get_lamda_k * self.get_w_k

    def get_lamda_k(self, k: int) -> float:
        """
                Retrieves the arrival rate (lambda) for priority class k.

                Args:
                    k (int): Priority class index (1-based).

                Returns:
                    float: Arrival rate for the specified priority class.
                """
        return self.lamda_k[k-1]

    def get_lq_k(self, k: int) -> float:
        """
                Calculates the average number of customers in the queue for priority class k.

                Args:
                    k (int): Priority class index (1-based).

                Returns:
                    float: Average number of customers in the queue for the specified priority class.
                """
        return (self.get_lamda_k) * (self.get_wq_k)


    def get_ro_k(self, k: int) -> float:
        """
                Calculates the traffic intensity (ro) for priority class k.

                Args:
                    k (int): Priority class index (1-based).

                Returns:
                    float: Traffic intensity for the specified priority class.
                """
        return self.simplify_lamda() / (self.c * self.mu)

    def get_w_k(self, k: int) -> float:
        """
                Calculates the average time a customer spends in the system for priority class k.

                Args:
                    k (int): Priority class index (1-based).

                Returns:
                    float: Average time in the system for the specified priority class.
                """
        return (1 / self.mu) + self.get_wq_k

    def get_wq_k (self, k: int) -> float:
        """
                Calculates the average waiting time in the queue for priority class k.

                Args:
                    k (int): Priority class index (1-based).

                Returns:
                    float: Average waiting time in the queue for the specified priority class.
                """
        return (1-self.ro) * self.wq / (self.get_b_k(k-1) * self.get_b_k(k))
