import math
from numbers import Number


class BaseQueue:
    """
        Base class for queueing system metrics calculation.

        Attributes:
            lamda (float): Arrival rate.
            mu (float): Service rate.
            p0 (float): Probability that there are zero customers in the system.
            lq (float): Average number of customers in the queue.
            recalc_needed (bool): Flag indicating whether metrics recalculation is needed.
            l (float): Average number of customers in the system.
            r (float): Traffic intensity (arrival rate / service rate).
            ro (float): Traffic intensity (same as _r).
            w (float): Average time a customer spends in the system.
            wq (float): Average time a customer spends waiting in the queue.
        utilization (float): Utilization factor of the system.
    """

    def __init__(self, lamda: float, mu: float):
        """
        Initialize BaseQueue with arrival rate (λ) and service rate (μ).

        Args:
        lamda (float): Arrival rate or rates (tuple for multiple sources).
        mu (float): Service rate.
        """

        self.lamda = lamda
        self.mu = mu
        self._p0 = math.nan
        self._lq = math.nan
        self._recalc_needed = True

    def __repr__(self):
        """
        Return a string representation of the BaseQueue object for debugging purposes.

        Returns:
        str: Representation of the BaseQueue object.
        """

        return f"<class 'BaseQueue.BaseQueue'> at {id(self)} has: " \
               f"lamda: {self.lamda}, mu: {self.mu}, " \
               f"Lq: {self.lq}, L: {self.l}, " \
               f"Wq: {self.wq}, W: {self.w}, " \
               f"p0: {self.p0}, ro: {self.ro:.4f}, " \
               f"r: {self.r:.4f}, Utilization: {self.utilization * 100:.2f}%"


    def __str__(self):
        """
        Return a string representation of the BaseQueue object.

        Returns:
        str: String representation including λ, μ, and recalculation status.
        """

        return f"BaseQueue __str__\n<class 'BaseQueue.BaseQueue'> at {id(self)} has: \n" \
               f"\tlamda: {self._lamda}\n" \
               f"\tmu:\t{self._mu}\n" \
               f"\tLq:\t{self._lq}\n" \
               f"\tL:\t{self.l}\n" \
               f"\tWq:\t{self.wq}\n" \
               f"\tW:\t{self.w}\n" \
               f"\tp0:\t{self.p0}\n" \
               f"\tRO:\t {self.ro:.4f}\n" \
               f"\tR:\t {self.r:.4f}\n" \
               f"\tUtilization:\t{self.utilization * 100:.2f}%"


    #Getter for lamda
    @property
    def lamda(self) -> float:
        """
        Getter for the arrival rate (λ).

        Returns:
        float: The arrival rate.
        """
        return self._lamda

    @lamda.setter
    def lamda(self, value:float):
        """
        Setter for the arrival rate (λ). Validates the input and marks recalculation as needed.

        Args:
        value (float): New arrival rate.
        """
        # Checks if lamda is a tuple, and returns the sum if it is
        if isinstance(value, tuple):
            if not all(isinstance(i, Number) and i > 0 for i in value):
                self._lamda = math.nan
            else:
                self._lamda = sum(value)
        # Checks if lamda is a valid number and returns the entered value if it is
        elif isinstance(value, Number):
            if value > 0:
                self._lamda = value
            else:
                self._lamda = math.nan
        else:
            self._lamda = math.nan
        self._recalc_needed = True

    #Getter for mu
    @property
    def mu(self) -> float:
        """
        Getter for the service rate (μ).

        Returns:
        float: The service rate.
        """
        return self._mu

    #Setter for mu
    @mu.setter
    def mu(self, value: float):
        """
        Setter for the service rate (μ). Validates the input and marks recalculation as needed.

        Args:
        value (float): New service rate.
        """
        # Checks if mu is a valid number and returns the entered value if it is
        if not isinstance(value, Number) or value <= 0:
            self._mu = math.nan
        else:
            self._mu = value
        self._recalc_needed = True

    @property
    def lq(self):
        """
        Getter for the average number of customers in the queue (Lq).

        Returns:
        float: The average number of customers in the queue.
        """
        if self._recalc_needed:
            self.calc_metrics()
        return self._lq

    @property
    def p0(self):
        """
        Getter for the probability that there are 0 customers in the queue.

        Returns:
        float: the probability that there are 0 customers in the queue.
        """
        if self._recalc_needed:
            self.calc_metrics()
        return self._p0

    def _get_recalc_needed(self):
        return self._recalc_needed

    @property
    def l(self):
        """
        Getter for the average number of customers in the system (L).

        Returns:
        float: The average number of customers in the system.
        """

        return self.lq + (self.lamda / self.mu)

    @property
    def r(self):
        """
        Getter for the traffic intensity (R).

        Returns:
        float: The traffic intensity.
        """

        return self.simplify_lamda() / self.mu

    @property
    def ro(self):
        """
        Getter for the traffic intensity.

        Returns:
        float: The traffic intensity.
        """

        return self.r

    @property
    def w(self):
        """
        Getter for the average time a customer spends in the system (W).

        Returns:
        float: The average time a customer spends in the system.
        """

        return self.wq + (1 / self.mu)

    @property
    def wq(self):
        """
        Getter for the average time a customer spends waiting in the queue (Wq).

        Returns:
        float: The average time a customer spends waiting in the queue.
        """
        return self.lq / self.lamda

    @property
    def utilization(self):
        """
        Getter for the utilization factor of the system.

        Returns:
        str: Utilization factor as a percentage.
        """
        return self.r

    def calc_metrics(self):
        """
        Calculate queueing system metrics including Lq, L, Wq, W, R, and utilization.
        """

        if not self.is_valid():
            self._lq = math.nan
            self._p0 = math.nan
        elif not self.is_feasible():
            self._lq = math.inf
            self._p0 = math.inf

    def is_valid(self):
        """
        Validate the input parameters (λ and μ).

        Returns:
        bool: True if inputs are valid, False otherwise.
        """

        # validate lambda
        if isinstance(self._lamda, tuple):
            for i in range(len(self._lamda)):
                if  isinstance(self._lamda[i], Number) and self._lamda[i] <= 0:
                    return False
        else:
            # ensures lamda is a valid number in a valid format
            if not isinstance(self._lamda, Number) or (self._lamda <= 0) or math.isnan(self._lamda):
                return False
        # ensures c and mu are in valid formats
        if not isinstance(self._mu, Number) or (self._mu <= 0) or math.isnan(self._mu):
            return False
        return True

    def simplify_lamda(self):
        """
        Calculates a simplified lamda value if λ is a tuple.

        Returns:
        float: The simplified lamda value.
        """
        if isinstance(self._lamda, tuple):
            w_lamda = self._lamda
        else:
            w_lamda = (self._lamda,)
        return sum(w_lamda)

    def is_feasible(self):
        """
        Check if the system is feasible (rho < 1).

        Returns:
            bool: True if the system is feasible, False otherwise.
        """
        if self.is_valid():
            rho = self.r
            # Ensures rho value is feasible
            if rho >= 1:
                return False
        else:
            return False
        return True