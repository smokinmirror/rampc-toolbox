import unittest
import raocp.core as rc
import numpy as np


class TestScenarioTree(unittest.TestCase):

    __tree_from_markov = None
    __tree_from_iid = None

    @staticmethod
    def __construct_tree_from_markov():
        if TestScenarioTree.__tree_from_markov is None:
            p = np.array([[0.1, 0.8, 0.1],
                          [0.4, 0.6, 0],
                          [0, 0.3, 0.7]])
            v = np.array([0.5, 0.5, 0])
            (N, tau) = (4, 3)
            TestScenarioTree.__tree_from_markov = \
                rc.MarkovChainScenarioTreeFactory(p, v, N, tau).create()

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        TestScenarioTree.__construct_tree_from_markov()

    def test_markov_num_nodes(self):
        tree = TestScenarioTree.__tree_from_markov
        self.assertEqual(32, tree.num_nodes())

    def test_markov_ancestor_of(self):
        tree = TestScenarioTree.__tree_from_markov
        self.assertEqual(0, tree.ancestor_of(1))
        self.assertEqual(0, tree.ancestor_of(2))
        self.assertEqual(1, tree.ancestor_of(3))
        self.assertEqual(1, tree.ancestor_of(4))
        self.assertEqual(1, tree.ancestor_of(5))
        self.assertEqual(2, tree.ancestor_of(6))
        self.assertEqual(2, tree.ancestor_of(7))
        self.assertEqual(5, tree.ancestor_of(13))
        self.assertEqual(8, tree.ancestor_of(20))
        self.assertEqual(15, tree.ancestor_of(27))
        self.assertEqual(19, tree.ancestor_of(31))

    def test_markov_children_of(self):
        tree = TestScenarioTree.__tree_from_markov
        self.assertEqual(2, len(tree.children_of(0)))
        self.assertEqual(3, len(tree.children_of(1)))
        self.assertEqual(2, len(tree.children_of(2)))
        self.assertEqual(2, len(tree.children_of(5)))
        self.assertEqual(3, len(tree.children_of(6)))
        for idx in range(8, 20):
            self.assertEqual(1, len(tree.children_of(idx)))
        # TODO more testing

    def test_markov_stage_of(self):
        tree = TestScenarioTree.__tree_from_markov
        self.assertEqual(0, tree.stage_of(0))
        self.assertEqual(1, tree.stage_of(1))
        self.assertEqual(1, tree.stage_of(2))
        for idx in range(3, 8):
            self.assertEqual(2, tree.stage_of(idx))
        for idx in range(8, 20):
            self.assertEqual(3, tree.stage_of(idx))
        for idx in range(20, 32):
            self.assertEqual(4, tree.stage_of(idx))

    def test_markov_stage_of_failure(self):
        tree = TestScenarioTree.__tree_from_markov
        with self.assertRaises(ValueError):
            _ = tree.stage_of(-1)

    def test_markov_num_stages(self):
        tree = TestScenarioTree.__tree_from_markov
        self.assertEqual(4, tree.num_stages())

    def test_markov_nodes_at_stage(self):
        tree = TestScenarioTree.__tree_from_markov
        self.assertEqual(1, len(tree.nodes_at_stage(0)))
        self.assertEqual(2, len(tree.nodes_at_stage(1)))
        self.assertEqual(5, len(tree.nodes_at_stage(2)))
        self.assertEqual(12, len(tree.nodes_at_stage(3)))
        self.assertEqual(12, len(tree.nodes_at_stage(4)))
        self.assertEqual(8, tree.nodes_at_stage(3).start)
        self.assertEqual(20, tree.nodes_at_stage(3).stop)
        self.assertEqual(20, tree.nodes_at_stage(4).start)
        self.assertEqual(32, tree.nodes_at_stage(4).stop)

    def test_markov_probability_of_node(self):
        tol = 1e-10
        tree = TestScenarioTree.__tree_from_markov
        self.assertAlmostEqual(1, tree.probability_of_node(0), delta=tol)
        self.assertAlmostEqual(0.5, tree.probability_of_node(1), delta=tol)
        self.assertAlmostEqual(0.5, tree.probability_of_node(2), delta=tol)
        self.assertAlmostEqual(0.05, tree.probability_of_node(3), delta=tol)
        self.assertAlmostEqual(0.4, tree.probability_of_node(4), delta=tol)
        self.assertAlmostEqual(0.05, tree.probability_of_node(5), delta=tol)
        self.assertAlmostEqual(0.2, tree.probability_of_node(6), delta=tol)
        self.assertAlmostEqual(0.3, tree.probability_of_node(7), delta=tol)
        self.assertAlmostEqual(0.005, tree.probability_of_node(8), delta=tol)

    def test_markov_siblings_of_node(self):
        tree = TestScenarioTree.__tree_from_markov
        self.assertEqual(1, len(tree.siblings_of_node(0)))
        self.assertEqual(2, len(tree.siblings_of_node(1)))
        self.assertEqual(2, len(tree.siblings_of_node(2)))
        self.assertEqual(3, len(tree.siblings_of_node(3)))
        self.assertEqual(2, len(tree.siblings_of_node(7)))
        self.assertEqual(2, len(tree.siblings_of_node(11)))
        for i in range(20, 32):
            self.assertEqual(1, len(tree.siblings_of_node(i)))

    def test_markov_values(self):
        self.fail("not tested yet!")

    def test_markov_conditional_probabilities_of_children(self):
        tol = 1e-10
        tree = TestScenarioTree.__tree_from_markov
        for stage in range(tree.num_stages()):  # 0, 1, ..., N-1
            for node_idx in tree.nodes_at_stage(stage):
                self.assertAlmostEqual(1., sum(tree.conditional_probabilities_of_children(node_idx)), tol)



if __name__ == '__main__':
    unittest.main()