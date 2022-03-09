# OQC Technical Test

## Contents
- `part1.py`: the code implementing Part 1 of the technical test.
- `part2.py`: the code implementing Part 2 of the technical test.
- `test.py`: a few tests to showcase the results when running the implementation for Parts 1 and 2. Note: the resulting optimised sequences from each test will be the same, but for Part 2 the Y gate will be replaced with a sequence of the form Z(90)Y(\theta)Z(-90).

## How to run
Each python file can be run via command line with the following steps:
1. Download the project.
2. Make sure the terminal or command prompt can run python (simply type python or python3 and then exit() to exit).
3. Navigate to the local directory where the project is located.
4. To run Part 1 simply type `python part1.py` and then input a sequence of gates pulses in the relevant format, for example, `X(90), X(90), Y(40), ...`; the resulting optimised sequence will be printed.
5. To run Part 2 follow similar steps to Part 1 by typing `python part2.py`
6. To run the assorted tests, run `python test.py` - the results will appear on screen.