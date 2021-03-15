import sqlite3


class Orderbook(object):
    """
    Orderbook implementation with the following operations:
    1, 2) Add and remove orders by ID number look-up
    3) Print the quantity at the given price and side
    4) Print the price and quantity at the given level and side
    """

    @staticmethod
    def _side2int(side):
        """Sends the side (str) to the appropriate int
        >>> Orderbook._side2int("B")
        1
        >>> Orderbook._side2int("A")
        0
        """
        side_int = 1
        if side == "A":
            side_int = 0
        return side_int

    def __init__(self):
        """Orderbook constructor

        Creates an orderbook as an sqlite database.
        """
        # create the db in-memory
        self.con = sqlite3.connect(":memory:")
        self.cur = self.con.cursor()
        self.cur.execute(
            """CREATE TABLE orders (id integer PRIMARY KEY, isBid integer, price real, qty real)"""
        )
        self.con.commit()

    def close(self):
        """Close the db."""
        self.con.close()

    def _all_bids(self):
        query = """SELECT * FROM orders WHERE isBid=1"""
        return self.cur.execute(query).fetchall()

    def _all_asks(self):
        query = """SELECT * FROM orders WHERE isBid=0"""
        return self.cur.execute(query).fetchall()

    def add_order(self, order_id, price, qty, side):
        """Add an order.

        :param order_id: integer
        :param price: price level, double rounded to 4 decimals
        :param qty: quantity, double roudned to four decimals
        :param side: 'B' bid or 'A' ask
        """
        try:
            order_id = int(order_id)
            price = float(price)
            qty = float(qty)
            side = Orderbook._side2int(str(side))
        except ValueError:
            print("didnt typecheck when adding order")
            return

        self.cur.execute(
            "INSERT INTO orders VALUES (?, ?, ?, ?)", (order_id, side, price, qty)
        )

    def remove_order(self, order_id):
        """Remove an order.

        :param id: order ID, integer
        """
        try:
            order_id = int(order_id)
        except ValueError:
            print("didnt typecheck when removing order")
            return

        self.cur.execute("DELETE FROM orders WHERE id=?", (str(order_id),))

    def _fetch_P(self, price, side):
        query = f"""SELECT sum(qty) FROM orders
                            WHERE isBid={side} and price={price}"""
        return self.cur.execute(query).fetchall()[0][0]

    def print_quantity_at(self, price, side):
        """Print the quantity on the order book at given price and side.

        :param price: price level, double rounded to 4 decimals
        :param side: 'B' bid or 'A' ask
        """
        # commit pending transactions first
        self.con.commit()

        try:
            price = float(price)
            side = Orderbook._side2int(str(side))
        except ValueError:
            print("didnt typecheck when getting quantity at")
            return

        qty = self._fetch_P(price, side)

        if qty is None:
            # if empty price, print 0 qty  [(None,)]
            print(0)
        else:
            if qty.is_integer():
                qty = int(qty)
            print(qty)

    def _fetch_PL(self, level, side):
        # best bid highest, best ask lowest
        ordering = "DESC" if side else "ASC"
        query = f"""SELECT price,sum(qty)
                            FROM orders WHERE isBid={side}
                            GROUP BY price ORDER BY price {ordering}
                """

        results = self.cur.execute(query).fetchall()

        price, qty = 0, 0
        if int(level) - 1 < len(results):
            price, qty = results[level - 1]
            if price.is_integer():
                price = int(price)
            if qty.is_integer():
                qty = int(qty)
        return price, qty

    def print_level(self, level, side):
        """Print the price and quantity on the order book at given level and side.

        :param level: nth lowest Ask or nth highest Bid, integer >= 1
        :param side: 'B' bid or 'A' ask
        """
        # commit pending transactions first
        self.con.commit()

        try:
            level = int(level)
            side = Orderbook._side2int(str(side))
        except ValueError:
            print("didnt typecheck when getting price level")
            return

        price, qty = self._fetch_PL(level, side)
        print(f"{price},{qty}")
