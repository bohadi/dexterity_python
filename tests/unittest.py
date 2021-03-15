import unittest
import dexterity.core


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.ob = dexterity.core.Orderbook()
        # id, price, qty
        self.ob.add_order(1, 5, 3, "B")
        self.ob.add_order(2, 10, 4, "B")
        self.ob.add_order(3, 50, 33, "A")
        self.ob.add_order(4, 100, 44, "A")

    def test_bids_and_asks(self):
        bids = self.ob._all_bids()
        self.assertEqual(2, bids[1][0])
        self.assertEqual(10, bids[1][-2])
        self.assertEqual(4, bids[1][-1])

        asks = self.ob._all_asks()
        self.assertEqual(3, asks[0][0])
        self.assertEqual(50, asks[0][-2])
        self.assertEqual(33, asks[0][-1])
        return

    def test_remove_orders(self):
        bids_before = self.ob._all_bids()
        self.ob.remove_order(1)
        self.ob.remove_order(2)
        bids_after = self.ob._all_bids()

        self.assertNotEqual([], bids_before)
        self.assertEqual([], bids_after)
        return


if __name__ == "__main__":
    unittest.main()
