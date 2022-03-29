import numpy as np
import raocp.core.cones as core_cones


class AVaR:
    """
    Risk item: Average Value at Risk class
    """

    def __init__(self, alpha, pi, node):
        """
        :param alpha: AVaR risk parameter
        :param pi: probabilities of children events at node
        :param node: current node

        Note: ambiguity sets of coherent risk measures can be expressed by conic inequalities,
                defined by a tuple (E, F, cone, b)
        """
        self.__alpha = alpha
        self.__num_children = len(pi)
        self.__pi = np.asarray(pi).reshape(self.__num_children, 1)
        self.__node = node

        self.__E = None
        self.__F = None
        self.__cone = None
        self.__b = None
        self.__make_e_cone_b()

    def __make_e_cone_b(self):
        eye = np.eye(self.__num_children)
        self.__E = np.vstack((self.__alpha*eye, -eye, np.ones((1, self.__num_children))))
        self.__F = np.zeros((2 * self.__num_children + 1, self.__num_children))
        self.__b = np.vstack((self.__pi, np.zeros((self.__num_children, 1)), 1))
        self.__cone = core_cones.Cart([core_cones.NonnegOrth(), core_cones.NonnegOrth(), core_cones.Zero()])

    # GETTERS
    @property
    def type(self):
        """Risk type"""
        return "AVaR"

    @property
    def alpha(self):
        """AVaR risk parameter alpha"""
        return self.__alpha

    @property
    def E(self):
        """Ambiguity set matrix E"""
        return self.__E

    @property
    def F(self):
        """Ambiguity set matrix F"""
        return self.__F

    @property
    def cone(self):
        """Ambiguity set cone"""
        return self.__cone

    @property
    def b(self):
        """Ambiguity set vector b"""
        return self.__b

    def __str__(self):
        return f"Risk item at node {self.__node}; type: AVaR, alpha: {self.__alpha}; cone: {self.__cone.type}"

    def __repr__(self):
        return f"Risk item at node {self.__node}; type: AVaR, alpha: {self.__alpha}; cone: {self.__cone.type}"
