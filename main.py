#!/usr/bin/python3

import sys
import dexterity.core


def main():
    """ Entry point """

    ob = dexterity.core.Orderbook()

    for line in sys.stdin:
        cmd, *params = line.strip().split(",")

        if cmd == "A":
            ob.add_order(*params)
        elif cmd == "R":
            ob.remove_order(*params)
        elif cmd == "P":
            ob.print_quantity_at(*params)
        elif cmd == "PL":
            ob.print_level(*params)

        else:
            print("Command not one of A, R, P, PL.")

    ob.close()


if __name__ == "__main__":
    main()
