
import math

from MMcQueue import MMcQueue


class MMcPriorityQueue(MMcQueue):
    """
    Represents a priority-based multi-server queueing system (M/M/c) extending MMcQueue.

    This class models a priority queueing system where multiple classes of priority are handled.
    It supports calculating metrics specific to each priority class, such as the average number
    of customers in the system and waiting times.

    Attributes:
        lamda (float): Aggregate arrival rate across all priority classes.
        mu (float): Service rate per server.
        c (int): Number of servers in the system.
        _lamda_k (tuple): Arrival rates for each priority class.
        utilization (float): System utilization percentage.
        ro (float): Traffic intensity across the system.
        p0 (float): Probability that the system is empty.
        _recalc_needed (bool): Flag indicating if metrics need recalculation.
    """

    def __init__(self, lamda: float, mu: float, c: int):
        """
                Initializes a priority-based M/M/c queue with aggregate and individual arrival rates.

                Args:
                    lamda (float): Total arrival rate across all classes.
                    mu (float): Service rate for each server.
                    c (int): Number of servers in the system.
                """
        super().__init__(lamda, mu, c)
        self._lamda_k = lamda

    @property
    def lamda_k(self):
        """
        Retrieves the tuple of arrival rates for each priority class.

        Returns:
            tuple: Individual lambda values for each priority class.
        """
        return self._lamda_k

    @lamda_k.setter
    def lamda_k(self, values: tuple):
        """
        Sets the tuple of arrival rates for each priority class and recalculates aggregate lamda.

        Args:
            values (tuple): Tuple containing lambda values for each priority class.
        """

        # Checks each value in tuple for validity
        for i in range(len(values)):
            if isinstance(values[i], float) and values[i] > 0:
                self._lamda_k = values
        # Calculates aggregate lamda
        self.lamda = self.simplify_lamda()
        self._recalc_needed = True


    @property
    def lamda(self):
        """
        Retrieves the aggregate arrival rate for the system.

        Returns:
            float: Total arrival rate (sum of lamda_k values).
        """
        return self._lamda

    @lamda.setter
    def lamda(self, value: float):
        """
        Sets the aggregate arrival rate based on the sum of lamda_k values.

        Args:
            value (float): The calculated aggregate arrival rate.
        """

        #Checks validity if lamda value
        if isinstance(value, (int, float)) and value > 0:
            self._lamda = self.simplify_lamda()
        else:
            self._lamda = math.nan

        if math.isnan(self._lamda):
            self._lamda_k = math.nan
        else:
            self._lamda_k = value

        self._recalc_needed = True

    def simplify_lamda(self):
        """
        Computes the aggregate arrival rate by summing individual lamda_k values.

        Returns:
            float: Sum of lamda_k values, or math.nan if data is invalid.
        """
        #Returns aggregate lamda
        return sum(self._lamda_k) if all(isinstance(val, (int, float)) for val in self._lamda_k) else math.nan

    def get_b_k(self, k: int) -> float:
        """
        Computes the blocking probability for priority class k.

        Args:
            k (int): Index of the priority class (1-based).

        Returns:
            float: Blocking probability for priority class k.
        """
        if k <= len(self._lamda_k):
            return math.nan
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
        Computes the average number of customers in the system for priority class k.

        Args:
            k (int): Index of the priority class (1-based).

        Returns:
            float: Average number of customers for the priority class.
        """
        return self.get_lamda_k(k) * self.get_w_k(k)

    def get_lamda_k(self, k: int) -> tuple:
        """
        Retrieves the arrival rate for a specific priority class k.

        Args:
            k (int): Index of the priority class (1-based).

        Returns:
            float: Arrival rate for priority class k.
        """
        if k <= 0 or k < len(self._lamda_k):
            return math.nan
        # Iterates through the tuple, lamda_k, and ensures that every value is valid
        for i in range(len(self._lamda_k)):
            try:
                if self._lamda_k[i] <= 0:
                    return math.nan
            except TypeError:
                return math.nan
        return self.lamda_k[k-1]

    def is_valid(self) -> bool:
        """
                Checks if the queue system parameters are valid.

                Returns:
                    bool: True if valid, otherwise False.
                """
        # Iterates through the tuple, lamda_k, and ensures that every value is valid
        for i in range(len(self._lamda_k)):
            try:
                if self._lamda_k[i] <= 0:
                    return False
            except TypeError:
                return False
        if math.isnan(self.mu):
            return False
        return True

    def get_lq_k(self, k: int) -> float:
        """
        Computes the average number of customers in the queue for priority class k.

        Args:
            k (int): Index of the priority class (1-based).

        Returns:
            float: Average queue length for priority class k.
        """
        return self.get_lamda_k(k) * self.get_wq_k(k)


    def get_ro_k(self, k: int) -> float:
        """
        Calculates the traffic intensity for priority class k.

        Args:
            k (int): Index of the priority class (1-based).

        Returns:
            float: Traffic intensity for priority class k.
        """
        return self.get_lamda_k(k) / (self.c * self.mu)

    def get_w_k(self, k: int) -> float:
        """
        Computes the average time a customer spends in the system for priority class k.

        Args:
            k (int): Index of the priority class (1-based).

        Returns:
            float: Average time in the system for priority class k.
        """
        return (1 / self.mu) + self.get_wq_k(k)

    def get_wq_k (self, k: int) -> float:
        """
        Computes the average waiting time in the queue for priority class k.

        Args:
            k (int): Index of the priority class (1-based).

        Returns:
            float: Average waiting time in the queue for priority class k.
        """
        return (1-self.ro) * self.wq / (self.get_b_k(k-1) * self.get_b_k(k))

    def __str__(self):
        """
        Provides a human-readable string representation of the MMcPriorityQueue object.

        Returns:
            str: Formatted string displaying queue metrics in a readable format.
        """
        priority_metrics = "\n\t".join([
            f"wq_{k + 1}: {self.get_wq_k(k + 1): .4f},  w_{k + 1}: {self.get_w_k(k + 1): .4f},"
            f"  lq_{k + 1}: {self.get_lq_k(k + 1): .4f},  l_{k + 1}: {self.get_l_k(k + 1): .4f}"
            for k in range(len(self.lamda_k))
        ])

        return (
            f"{self.__class__.__name__} __str__\n"
            f"<class '{self.__class__.__name__}'> at {id(self)} has:\n\t"
            f"lamda: {self.lamda}\n\tmu:\t{self.mu}\n\tLq:\t {self.lq:.4f}\n\tL:\t {self.l:.4f}\n\t"
            f"Wq:\t {self.wq:.4f}\n\tW:\t {self.w:.4f}\n\tp0:\t {self.p0:.4f}\n\t"
            f"RO:\t {self.ro:.4f}\n\tR:\t {self.r:.4f}\n\t"
            f"Utilization: {self.utilization:.2f}%\n\tc: {self.c}\n\t{priority_metrics}"
        )

    def __repr__(self):
        """
        Provides a detailed string representation of the MMcPriorityQueue object for debugging.

        Returns:
            str: Formatted string with detailed queue metrics.
        """
        priority_metrics = "\n\t".join([
            f"Wq_{k + 1}: {self.get_wq_k(k + 1): .4f},  W_{k + 1}: {self.get_w_k(k + 1): .4f},"
            f"  Lq_{k + 1}: {self.get_lq_k(k + 1): .4f},  L_{k + 1}: {self.get_l_k(k + 1): .4f}"
            for k in range(len(self.lamda_k))
        ])

        return (
            f"{self.__class__.__name__} __repr__\n"
            f"<class '{self.__class__.__name__}'> at {id(self)} has: lamda: {self.lamda}, mu: {self.mu}\n\t"
            f"Lq: {self.lq:.4f}, L: {self.l:.4f}, Wq: {self.wq:.4f}, W: {self.w:.4f}\n\t"
            f"p0: {self.p0:.4f}, ro: {self.ro:.4f}, r: {self.r:.4f}, Utilization: {self.utilization:.2f}%, c: {self.c}\n\t"
            f"{priority_metrics}"
        )