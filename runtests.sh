#!/bin/bash


echo "▒▒▒▒▒▒▒▒▒▒▒▒▒▒ DOCTEST START ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒"
python3 -m doctest -v dexterity/core.py dexterity/util.py
echo "▒▒▒▒▒▒▒▒▒▒▒▒▒▒ DOCTEST END ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒"

echo ""
echo ""

echo "▒▒▒▒▒▒▒▒▒▒▒▒▒▒ UNIT TESTS START ▒▒▒▒▒▒▒▒▒▒▒▒▒▒"
python3 -m unittest tests/unittest.py
echo "▒▒▒▒▒▒▒▒▒▒▒▒▒▒ UNIT TESTS END ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒"


