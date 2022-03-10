# OQC Technical Test

## Contents
- `part1.py`: the code implementing Part 1 of the technical test.
- `part2.py`: the code implementing Part 2 of the technical test.
- `test.py`: a few tests to showcase the results when running the implementation for Parts 1 and 2. Note: the resulting optimised sequences from each test have the same effect, but for Part 2 the Y gates will be replaced with a sequence of the form Z(90)Y(\theta)Z(-90).
- `part3.py`:

## Introduction
A quick introduction to the design decisions and ideas behind each implementation.

### Part 1
For Part 1 I used the Rotation module from the scipy library in Python (https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.html). This provides a very good way to deal with rotations on an XYZ plane, where each rotation has an associated angle. The workflow is devised as follows:
1. First parse the input sequence of gates/pulses in tuples of the form (operation, angle) where operation is X, Y or Z and angle is assumed to be an integer (float could also work).
2. Create rotation objects as Euler objects supported by the library and corresponding to each one of the operations. Intuitively, every rotation is mapped to a 1x3 matrix [x, y, z], where each entry is the respective rotation angle
3. Combine them all together to get the final optimised rotation in the form of [X, Y, Z] angles. The result will only be returned in terms of the final rotations necessary to represent the initial combined expression. This is essentially a product of the matrices.
4. Output the resulting optimised sequence on a readable format, for example, X(180),Y(90)

For a bit more info on the ideas behind behind spatial rotations and quaternions, look here: https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation. Furthermore, a nice mapping of an arbitrary quantum operator to a sequence of rotation and phase gates can be given by Barenco et al. in [1].

Note: I noticed that for the Euler axis x-y-x I get optimal rotation when the circuit for Part 1 only includes X or Y gates. If Z gates are added, then the Euler axis x-y-z, but this axis does not work  Changing the axis changes the result, so there is some interesting further studying that could go into this one!

### Part 2
The logic here is similar to Part 1 but with the difference that the operation $Y(\theta)$ is replaced by $Z(90),Y(\theta)Z(-90)$.

### Part 3
This section introduces the idea of a runtime for every gate in the quantum circuit. The optimisation of the circuit runtime follows naturally from the optimisation of the operation sequence, as minimising the number of gates leads to minimisation of the circuit runtime.

Hence, the code implemented in part3.py tries to calculate the runtime of each circuit/sequence. Furthermore, a LengthY is also taken into account, in order to be able to calculate the runtime of Part 1 and initial circuits and compare, which could lead to further interesting analytics.

It is noteworthy that, sometimes, the optimised sequence resulting from Part 2 (i.e., Y -> ZXZ transformation) might take longer to implement than the initial expansion. The reason for this is the fact that every Y gate has to be substituted by three gates ZXZ. That also depends on the runtimes of Y, X and Z gates.

### Part 4
The reasoning here needs to change a bit, as CNOT gates introduce entanglement between two qubits. It is therefore essential to be extra careful when optimising sequences that induce entanglement via CNOT gates.

## How to run
Each python file can be run via command line with the following steps:
1. Download the project.
2. Make sure the terminal or command prompt can run python (simply type python or python3 and then exit() to exit).
3. Navigate to the local directory where the project is located.
4. To run Part 1 simply type `python part1.py` and then input a sequence of gates pulses in the relevant format, for example, `X(90), X(90), Y(40), ...`; the resulting optimised sequence will be printed.
5. To run Part 2 follow similar steps to Part 1 by typing `python part2.py`
6. To run Part 3 follow similar steps to Parts 1 and 2 and type `python part3.py`.
7. 6. To run the assorted tests and experiments for all Parts, run `python test.py` - follow input requests and results that appear on screen.

## References
[1] A. Barenco, et.al. "Elementary gates for quantum computation", Physical Review A, DOI: https://journals.aps.org/pra/abstract/10.1103/PhysRevA.52.3457