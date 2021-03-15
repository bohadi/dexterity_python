import dexterity.util

import sqlite3


class Orderbook(object):
    """
    Orderbook implementation with the following operations:
    1, 2) Add and remove orders by ID number look-up
    3) Print the quantity at the given price and side
    4) Print the price and quantity at the given level and side
    """

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

    def add_order(self, order_id, price, qty, side):
        """Add an order.

        :param order_id: integer
        :param price: price level, double rounded to 4 decimals
        :param qty: quantity, double roudned to four decimals
        :param side: 'B' bid or 'A' ask
        """
        # typecheck
        order_id = int(order_id)
        price = float(price)
        qty = float(qty)
        side = str(side)[0]

        if side == "B":
            self.cur.execute(
                "INSERT INTO orders VALUES (?, 1, ?, ?)", (order_id, price, qty)
            )
        elif side == "A":
            self.cur.execute(
                "INSERT INTO orders VALUES (?, 0, ?, ?)", (order_id, price, qty)
            )

    def remove_order(self, order_id):
        """Remove an order.

        :param id: order ID, integer
        """
        order_id = int(order_id)
        self.cur.execute("DELETE FROM orders WHERE id=?", (str(order_id),))

    def print_quantity_at(self, price, side):
        """Print the quantity on the order book at given price and side.

        :param price: price level, double rounded to 4 decimals
        :param side: 'B' bid or 'A' ask
        """
        # commit pending transactions first
        self.con.commit()

        # typecheck
        price = float(price)
        side = str(side)[0]

        results = []
        if side == "B":
            results = self.cur.execute(
                """SELECT sum(qty) FROM orders WHERE isBid=1 and price=?""",
                (str(price),),
            ).fetchall()
        elif side == "A":
            results = self.cur.execute(
                """SELECT sum(qty) FROM orders WHERE isBid=0 and price=?""",
                (str(price),),
            ).fetchall()

        if len(results) == 0:
            # if empty price, print 0 qty
            print(0)
        else:
            qty = results[0][0]
            if qty.is_integer():
                qty = int(qty)
            print(qty)

    def print_level(self, level, side):
        """Print the price and quantity on the order book at given level and side.

        :param level: nth lowest Ask or nth highest Bid, integer >= 1
        :param side: 'B' bid or 'A' ask
        """
        # commit pending transactions first
        self.con.commit()

        # typecheck
        level = int(level)
        side = str(side)[0]

        results = []
        if side == "B":
            results = self.cur.execute(
                """SELECT price,sum(qty) FROM orders WHERE isBid=1
                                GROUP BY price ORDER BY price DESC"""
            ).fetchall()
        elif side == "A":
            results = self.cur.execute(
                """SELECT price,sum(qty) FROM orders WHERE isBid=0
                                GROUP BY price ORDER BY price ASC"""
            ).fetchall()

        if int(level) - 1 >= len(results):
            # if empty price level, print 0,0
            print("0,0")
        else:
            price, qty = results[level - 1]
            if price.is_integer():
                price = int(price)
            if qty.is_integer():
                qty = int(qty)
            print(f"{price},{qty}")
