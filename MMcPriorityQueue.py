
import math

from MMcQueue import MMcQueue


class MMCPriorityQueue(MMcQueue):
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

    @property
    def lamda_k(self):
        """
        Getter for the number of servers (c).

        Returns:
        int: Number of servers.
        """
        return self._lamda_k

    @lamda_k.setter
    def lamda_k(self, value: float):
        """
        Setter for the number of servers (c).

        Args:
        value (int): Number of servers.
        """

        self.lamda = value


    @property
    def lamda(self):
        return self._lamda

    @lamda.setter
    def lamda(self, value: float):

        self._lamda = self.simplify_lamda()

        if math.isnan(self.lamda):
            self._lamda_k = (math.nan,)
        else:
            self._lamda_k = value

        self._recalc_needed = True

    def get_b_k(self, k: int) -> float:
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
        if k <= 0:
            return math.inf
        else:
            return self.get_lamda_k * self.get_w_k

    def get_lamda_k(self, k: int) -> float:
        return self.lamda_k[k-1]

    def get_lq_k(self, k: int) -> float:
        return self.get_lamda_k * self.get_wq_k


    def get_ro_k(self, k: int) -> float:
        return self.simplify_lamda() / (self.c * self.mu)

    def get_w_k(self, k: int) -> float:
        return self.get_wq_k + (1 / self.mu)

    def get_wq_k (self, k: int) -> float:
        return (1-self.ro) * self.wq / (self.get_b_k(k-1) * self.get_b_k(k))
