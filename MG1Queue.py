
from numbers import Number

from BaseQueue import BaseQueue
import math


class MG1Queue(BaseQueue):
    """
    Represents a multi-server queueing system (M/G/1) inheriting from BaseQueue.

    Attributes:
        lamda (float): Arrival rate (λ), or average number of arrivals per time unit.
        mu (float): Service rate (μ), or average number of services completed per time unit.
        sigma (float): Standard deviation of service time.
        lq (float): Average number of customers in the queue.
        l (float): Average number of customers in the system (in queue + in service).
        wq (float): Average time a customer spends waiting in the queue.
        w (float): Average time a customer spends in the system.
        p0 (float): Probability that the system is empty.
        ro (float): Traffic intensity (arrival rate divided by service rate).
        r (float): Average number of customers in the system, including those in service.
        utilization (float): Utilization of the system as a percentage, representing the busy time of the server.
    """
    def __init__(self, lamda: float, mu: float, sigma: float = 0.0):
        """
        Initializes an M/G/1 queueing system with specified arrival rate, service rate, and service time standard deviation.

        Args:
            lamda (float): Arrival rate (average number of arrivals per time unit).
            mu (float): Service rate (average number of services completed per time unit).
            sigma (float): Standard deviation of the service time.
        """
        super().__init__(lamda, mu)
        self.sigma = sigma
        #self._recalc_needed = True


    @property
    def sigma(self) -> float:
        """
        Gets the standard deviation of the service time.

        Returns:
            float: The standard deviation of the service time.
        """
        return self._sigma

    @sigma.setter
    def sigma(self, value: float):
        """
        Sets the standard deviation of the service time, ensuring it is a non-negative number.

        Args:
            value (float): Standard deviation of the service time.

        Sets:
            self._sigma (float): If valid, sets to the given value; otherwise, sets as NaN.
        """
        # Ensures sigma value is valid
        if isinstance(value, Number) and value >= 0:
            self._sigma = value
        else:
            self._sigma = math.nan
        self._recalc_needed = True

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
            self._lq = ((self.lamda ** 2 * self.sigma ** 2) + self.r ** 2) / (2 * (1 - self.r))
            self._p0 = 1 - self.r

    def is_valid(self) -> bool:
        """
        Checks if the queue configuration is valid by ensuring sigma is a non-negative number.

        Returns:
            bool: True if sigma is valid and non-negative, False otherwise.
        """
        if not isinstance(self.sigma, Number):
            return False
        if math.isnan(self._sigma):
            return False
        if self.sigma < 0:
            return False
        return super().is_valid()

    def is_feasible(self) -> bool:
        """
                Checks if the queue configuration is feasible by verifying that arrival rate is less than service rate.

                Returns:
                    bool: True if arrival rate is less than service rate, False otherwise.
                """
        if self._lamda == self._mu:
            return False
        return super().is_valid()

    def __str__(self):
        """
        Provides a string representation of the MG1Queue instance.

        Returns:
            str: A formatted string displaying key metrics and attributes.
        """
        return (f"{self.__class__.__name__} __str__\n"
                f"<class '{self.__class__.__module__}.{self.__class__.__name__}'> at {id(self)} has: \n"
                f"\tlamda: {self.lamda}\n"
                f"\tmu:\t{self.mu}\n"
                f"\tLq:\t {self.lq:.4f}\n"
                f"\tL:\t {self.l:.4f}\n"
                f"\tWq:\t {self.wq:.4f}\n"
                f"\tW:\t {self.w:.4f}\n"
                f"\tp0:\t {self.p0:.4f}\n"
                f"\tRO:\t {self.ro:.4f}\n"
                f"\tR:\t {self.r:.4f}\n"
                f"\tUtilization: {self.utilization:.2f}%\n"
                f"\tSigma: {self.sigma:.2f}\n")

    def __repr__(self):
        """
        Provides a concise string representation of the MG1Queue instance for debugging.

        Returns:
            str: A formatted string displaying key metrics and attributes.
        """
        return (f"{self.__class__.__name__} __repr__\n"
                f"<class '{self.__class__.__module__}.{self.__class__.__name__}'> at {id(self)} has: "
                f"lamda: {self.lamda}, mu: {self.mu}\n"
                f"\tLq: {self.lq:.4f}, L: {self.l:.4f}, Wq: {self.wq:.4f}, W: {self.w:.4f}\n"
                f"\tp0: {self.p0:.4f}, ro: {self.ro:.4f}, r: {self.r:.4f}, "
                f"Utilization: {self.utilization:.2f}%, Sigma: {self.sigma:.2f}")
