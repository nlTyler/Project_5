import math

from BaseQueue import BaseQueue
"""
    Represents a single-server queueing system (M/D/1) inheriting from BaseQueue.
    
    Attributes:
        lamda (float): Arrival rate.
        mu (float): Service rate.
        lq (float): Average number of customers in the queue.
        l (float): Average number of customers in the system.
        wq (float): Average time a customer spends waiting in the queue.
        w (float): Average time a customer spends in the system.
        p0 (float): Probability that the system is empty.
        ro (float): Traffic intensity (arrival rate divided by service rate).
        r (float): Average number of customers in the system including the one in service.
        utilization (float): Utilization of the system as a percentage of time the server is busy.
    """

class MD1Queue(BaseQueue):
    def __init__(self, lamda: float, mu: float):
        """
                Initializes an M/D/1 queueing system with given arrival and service rates.

                Args:
                    lamda (float): Arrival rate (average number of arrivals per time unit).
                    mu (float): Service rate (average number of services completed per time unit).
                """

        super().__init__(lamda, mu)

    def _calc_metrics(self):
        """
                Calculates queueing metrics: Lq, p0
        """

        # Checks if parameters are valid
        if not self.is_valid():
            self._lq = math.nan
            self._p0 = math.nan
        # Checks if parameters are feasible
        elif not self.is_feasible():
            self._lq = math.inf
            self._p0 = math.inf
        else:
            self._lq = self._lamda ** 2 / (2 * self.mu * (self.mu - self._lamda))
            self._p0 = 1 - (self._lamda / self._mu)

    def __repr__(self):
        """
        Returns a  string representation of the MD1Queue instance.
        """
        return (
            f"{self.__class__.__name__} __repr__\n"
            f"<class '{self.__class__.__module__}.{self.__class__.__name__}'> at {id(self)} has: lamda: {self._lamda}, mu: {self._mu}\n"
            f"\tLq:  {self._lq:.4f}, L:  {self.l:.4f}, Wq:  {self.wq:.4f}, W:  {self.w:.4f}\n"
            f"\tp0:  {self._p0:.4f}, ro:  {self.ro:.4f}, r:  {self.r:.4f}, Utilization: {self.utilization:.2f}%"
        )

    def __str__(self):
        """
        Returns a formatted string representation of the MD1Queue instance.
        """
        return (
            f"{self.__class__.__name__} __str__\n"
            f"<class '{self.__class__.__module__}.{self.__class__.__name__}'> at {id(self)} has: \n"
            f"\tlamda: {self._lamda}\n"
            f"\tmu: \t{self._mu}\n"
            f"\tLq: \t {self._lq:.4f}\n"
            f"\tL: \t {self.l:.4f}\n"
            f"\tWq: \t {self.wq:.4f}\n"
            f"\tW: \t {self.w:.4f}\n"
            f"\tp0: \t {self._p0:.4f}\n"
            f"\tRO: \t {self.ro:.4f}\n"
            f"\tR: \t {self.r:.4f}\n"
            f"\tUtilization: {self.utilization:.2f}%"
        )