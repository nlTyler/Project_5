from BaseQueue import BaseQueue
import math


class MMcQueue(BaseQueue):
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
        """
        Initializes the M/M/c queue with arrival rate (lamda), service rate (mu), and number of servers (c).
        Calculates queueing metrics using calc_metrics method.

        Args:
        lamda (float): Arrival rate.
        mu (float): Service rate.
        c (int): Number of servers.
        """
        super().__init__(lamda, mu)
        self.c = c  # Number of servers

    @property
    def c(self) -> int:
        """
        Getter for the number of servers (c).

        Returns:
        int: Number of servers.
        """
        return self._c

    @c.setter
    def c(self, value: int):
        """
        Setter for the number of servers (c).

        Args:
        value (int): Number of servers.
        """

        if not isinstance(value, int) or value <= 0:
            self._c = math.nan
        else:
            self._c = value
        self._recalc_needed = True

    @property
    def ro(self):
        """
        Getter for the traffic intensity.

        Returns:
        float: The traffic intensity.
        """
        return self.r /self.c

    def _calc_metrics(self):
        """
        Calculates queueing metrics: Lq, L, Wq, W, p0, ro, r, and utilization.
        """

        if not self.is_valid():
            self._lq = math.nan
            self._p0 = math.nan
        elif not self.is_feasible():
            self._lq = math.inf
            self._p0 = math.inf
        else:
            # Formulas for calculating p0 and lq
            term1 = sum((self.r ** i) / math.factorial(i) for i in range(self.c))
            term2 = (self.r ** self.c) / (math.factorial(self.c) * (1 - self.ro))
            self._p0 = 1 / (term1 + term2)
            num = self.r ** self.c * self.ro
            den = math.factorial(self.c) * (1 - self.ro) ** 2
            self._lq = self._p0 * num / den

    def is_feasible(self):
        """
                Check if the system is feasible (ro < 1).

                Returns:
                    bool: True if the system is feasible, False otherwise.
                """
        if self.is_valid():
            if self.ro >= 1:
                return False
        else:
            return False
        return True

    def __repr__(self) -> str:
        """
        Returns a string representation of the M/M/c queue object.

        Returns:
        str: Representation including class name, memory location, lamda, mu, and metrics.
        """
        return (f"<class '{self.__class__.__module__}.{self.__class__.__name__}'> "
                f"at {id(self)} has: lamda: {self.lamda}, mu: {self.mu}\n"
                f"\tLq: {self.lq:.4f}, L: {self.l:.4f}, Wq: {self.wq:.4f}, W: {self.w:.4f}\n"
                f"\tp0: {self.p0:.4f}, ro: {self.ro:.4f}, r: {self.r:.4f}, Utilization: {self.utilization:.2f}%, c: {self.c}")

    def __str__(self) -> str:
        """
        Returns a string representation of the M/M/c queue object with detailed metrics.

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
                f"\tUtilization: {self.utilization:.2f}%\n"
                f"\tc: {self.c}")
