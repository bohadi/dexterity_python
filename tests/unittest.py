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
        """The orderbook should add bids and asks."""
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
        """The orderbook should remove bids and asks."""
        bids_before = self.ob._all_bids()
        self.ob.remove_order(1)
        self.ob.remove_order(2)
        bids_after = self.ob._all_bids()

        self.assertNotEqual([], bids_before)
        self.assertEqual([], bids_after)
        return

    def test_quantity_at_price(self):
        """The orderbook should give aggregate quantity at a given price."""
        self.ob.add_order(10, 5, 3, "B")

        qty = self.ob._fetch_P(5, "B")
        self.assertEqual(6, qty)

        qty = self.ob._fetch_P(10, "B")
        self.assertEqual(4, qty)

        qty = self.ob._fetch_P(100, "B")
        self.assertIsNone(qty)
        return

    def test_price_level(self):
        """The orderbook should give the nth best bid/ask price and aggregate quantity."""
        ap3, aq3 = self.ob._fetch_PL(3, "A")
        ap2, aq2 = self.ob._fetch_PL(2, "A")
        ap1, aq1 = self.ob._fetch_PL(1, "A")

        self.assertEqual((  0,  0), (ap3, aq3))
        self.assertEqual((100, 44), (ap2, aq2))
        self.assertEqual(( 50, 33), (ap1, aq1))

        bp1, bq1 = self.ob._fetch_PL(1, "B")
        bp2, bq2 = self.ob._fetch_PL(2, "B")
        bp3, bq3 = self.ob._fetch_PL(3, "B")

        self.assertEqual(( 10,  4), (bp1, bq1))
        self.assertEqual((  5,  3), (bp2, bq2))
        self.assertEqual((  0,  0), (bp3, bq3))


if __name__ == "__main__":
    unittest.main()
