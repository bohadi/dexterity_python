#!/bin/bash


echo "▒▒▒▒▒▒▒▒▒▒▒▒▒▒ DOCTEST START ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒"
python3 -m doctest -v dexterity/core.py dexterity/util.py
echo "▒▒▒▒▒▒▒▒▒▒▒▒▒▒ DOCTEST END ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒"

echo ""
echo ""

echo "▒▒▒▒▒▒▒▒▒▒▒▒▒▒ UNIT TESTS START ▒▒▒▒▒▒▒▒▒▒▒▒▒▒"
python3 -m unittest tests/unittest.py
echo "▒▒▒▒▒▒▒▒▒▒▒▒▒▒ UNIT TESTS END ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒"

echo ""
echo ""

echo "▒▒▒▒▒▒▒▒▒▒▒▒▒▒ INTEGRATION TESTS START ▒▒▒▒▒▒▒▒▒▒▒▒▒▒"
cat tests/1.input | python main.py > tests/my/1.output
cat tests/2.input | python main.py > tests/my/2.output
cat tests/3.input | python main.py > tests/my/3.output
cat tests/4.input | python main.py > tests/my/4.output
cat tests/5.input | python main.py > tests/my/5.output
cat tests/6.input | python main.py > tests/my/6.output

echo "Diffing example inputs"

diff -s tests/my/1.output tests/check/1.output
diff -s tests/my/2.output tests/check/2.output
diff -s tests/my/3.output tests/check/3.output
diff -s tests/my/4.output tests/check/4.output
diff -s tests/my/5.output tests/check/5.output
diff -s tests/my/6.output tests/check/6.output
echo "▒▒▒▒▒▒▒▒▒▒▒▒▒▒ INTEGRATION TESTS END ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒"
