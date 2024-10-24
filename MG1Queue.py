from BaseQueue import BaseQueue
import math


class MG1Queue(BaseQueue):
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
    def __init__(self, lamda: float, mu: float, sigma: float):
        """
        Initializes the M/M/c queue with arrival rate (lamda), service rate (mu), and number of servers (c).
        Calculates queueing metrics using calc_metrics method.

        Args:
        lamda (float): Arrival rate.
        mu (float): Service rate.
        c (int): Number of servers.
        """
        super().__init__(lamda, mu)
        self.sigma = sigma  # Number of servers

    @property
    def sigma(self) -> float:
        """
        Getter for the number of servers (c).

        Returns:
        int: Number of servers.
        """
        return self._sigma

    @sigma.setter
    def sigma(self, value: float):
        """
        Setter for the number of servers (c).

        Args:
        value (int): Number of servers.
        """

        self._sigma = value

    def calc_metrics(self):
        """
                Calculates queueing metrics: Lq, p0
        """
        if not self.is_valid():
            self._lq = math.nan
            self._p0 = math.nan
        elif not self.is_feasible():
            self._lq = math.inf
            self._p0 = math.inf
        else:
            self._lq = ((self.lamda ** 2 * self.sigma) + self.r ** 2) / (2 * (1 - self.r))
            self._p0 = 1 - (self.lamda / self.mu)

    def is_valid(self) -> bool:
        return self.sigma > 0

    def __repr__(self) -> str:
        """
        Returns a string representation of the M/G/1 queue object.

        Returns:
        str: Representation including class name, memory location, lamda, and mu.
        """
        return (f"<class '{self.__class__.__module__}.{self.__class__.__name__}'> "
                f"at {id(self)} has: "
                f"lamda: {self.lamda}, mu: {self.mu}\n"
                f"\tLq: {self.lq:.4f}, L: {self.l:.4f}, Wq: {self.wq:.4f}, W: {self.w:.4f}\n"
                f"\tp0: {self.p0:.4f}, ro: {self.ro:.4f}, r: {self.r:.4f}, Utilization: {self.utilization:.2f}%")

    def __str__(self) -> str:
        """
        Returns a string representation of the M/G/1 queue object with detailed metrics.

        Returns:
        str: Detailed representation including class name, memory location, lamda, mu, and metrics.
        """
        return (f"<class '{self.__class__.__module__}.{self.__class__.__name__}'> "
                f"at {id(self)} has: \n"
                f"\tlamda: {self.lamda}\n"
                f"\tmu:    {self.mu}\n"
                f"\tLq:    {self.lq:.4f}\n"
                f"\tL:     {self.l:.4f}\n"
                f"\tWq:    {self.wq:.4f}\n"
                f"\tW:     {self.w:.4f}\n"
                f"\tp0:    {self.p0:.4f}\n"
                f"\tRO:    {self.ro:.4f}\n"
                f"\tR:     {self.r:.4f}\n"
                f"\tUtilization: {self.utilization:.2f}%")