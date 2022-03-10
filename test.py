#### Author - Konstantinos Georgopoulos ####
# Importing libraries
import numpy as np
import collections
from scipy.spatial.transform import Rotation
import random
import warnings
warnings.filterwarnings("ignore")

### ----------------------- PART 1 -------------------------- ###
def optimise_circuit_part1(rot_string):
    # Parse the string into a list of axis, rotation tuples -> [[axis, degrees], [axis, degrees], ...]
    extract_axis_and_rotations = [(rot_string[i], int(rot_string[i+2:].split(")", 1)[0])) for i in range(len(rot_string)) if rot_string[i] in 'XYZ']
    
#     # Accounts for negative angles as 360+(-angle) - needs a bit more work
#     for i in range(len(extract_axis_and_rotations)):
#         if (extract_axis_and_rotations[i][1]<0): extract_axis_and_rotations[i] = (extract_axis_and_rotations[i][0], 360+extract_axis_and_rotations[i][1])

    # Create a bunch of rotation objects as Euler objects of the form [x, y, z] where x, y, z are the relevant angles in degrees
    rotation_list = [Rotation.from_euler(axis, rotation, degrees=True) for axis, rotation in extract_axis_and_rotations]

    # Multiply them all together to get the final optimised rotation in the form of [X, Y, Z] angles
    # The result will only be returned in terms of the final two rotations necessary to represent the initial 
    # combined expression.
    combined_rotations = np.prod(rotation_list)
    
    # Output as extrinsic euler angles
    res = combined_rotations.as_euler("XYX", degrees=True)
    
    return res

def get_opt_res(opt):
    '''Returns the optimised sequence of gates.'''
    gates = ['X', 'Y', 'Z']
    # If gates have angle 0 or 360, they get eliminated
    res = [(gates[i] + '(' + str(round(opt[i])) + ')') for i in range(len(opt)) if round(opt[i])!=0 and round(opt[i])!=360]
    
    # If all the angles in the rotations are 0 or 360, then no operation is necessary
    return (','.join(res)) if res!=[] else ("No operation needed")

### ----------------------- PART 2 -------------------------- ###
def expand_Ys(seq):
    '''Prepares the sequence according Y(\theta)=Z(90)X(\theta)Z-90 for a quantum computer where Y(\theta) is not applied
    - seq: the sequence for expansion; returns: a string containing the new operations'''
    spl = seq.split(",")
    for i, op in enumerate(spl):
        if (get_instr(op)=='Y'):
            spl[i] = 'Z(90),X(' + str(get_angle(op)) + '),Z(-90)'

    seq = ','.join(spl)
    
    return seq

def get_instr(gate):
    '''Returns the instruction of the gate.'''
    s = gate.split("(") # Split on ( to get the operation type as a string
    
    return s[0]

def get_angle(gate):
    '''Returns the angle of the gate.'''
    s = gate.split("(") # Split on ( to separate the angle from the gate name
    s = int(s[1].replace(")", "")) # Remove the ) from the angle and make it an int
    
    return s

# def expand_Ys_alt(seq)

def optimise_circuit_part2(rot_string):
    '''Optimise the circuit for Part 2 of the exercises - returns: an array with the angles of the optimised rotations
    for [X, Y, Z]'''
    # Parse the string into a list of axis, rotation tuples -> [[axis, degrees], [axis, degrees], ...]
    extract_axis_and_rotations = [(rot_string[i], int(rot_string[i+2:].split(")", 1)[0])) for i in range(len(rot_string)) if rot_string[i] in 'XYZ']
    
#     # Accounts for negative angles as 360+(-angle) - needs a bit more work
#     for i in range(len(extract_axis_and_rotations)):
#         if (extract_axis_and_rotations[i][1]<0): extract_axis_and_rotations[i] = (extract_axis_and_rotations[i][0], 360+extract_axis_and_rotations[i][1])
        
    # Create a bunch of rotation objects as Euler objects of the form [x, y, z] where x, y, z are the relevant angles in degrees
    rotation_list = [Rotation.from_euler(axis, rotation, degrees=True) for axis, rotation in extract_axis_and_rotations]
    
    # Multiply them all together to get the final optimised rotation in the form of [X, Y, Z] angles
    # The result will only be returned in terms of the final two rotations necessary to represent the initial 
    # combined expression.
    combined_rotations = np.prod(rotation_list)
    
    # Output as euler angles for the x-y-z rotations
    res = combined_rotations.as_euler("XYZ", degrees=True)
    
    return res

### ----------------------- PART 3 -------------------------- ###
def calculate_runtime(seq, lx, lz, ly):
    '''Calculates the runtime of an quantum circuit (optimised or not). - seq: the circuit/sequence of rotations,
    lx, ly, lz: the runtime of an X, Y, Z gate; returns: the runtime of the circuit'''
    runtime = 0 # Initialise runtime
    seq = seq.split(",") # Prepare the sequence
    # Calculate the runtime
    for i in range(len(seq)):
        if (seq[i][0]=='X'): runtime += lx
        elif (seq[i][0]=='Y'): runtime += ly
        else: runtime += lz
            
    return runtime

### ----------------------- TESTING -------------------------- ###
# Comparing Part 1 and Part 2 outputs
def testing(inputs):
    '''Running tests for Parts 1 and 2 - it is important for the results to be the same
    for both parts. For part two, the relevant Y(\theta)=Z(90)X(\theta)Z(-90) is shown.'''
    for i in range(len(inputs)):
        print("\nInput examined:", inputs[i])
        seq1 = inputs[i].replace(", ", "")
        seq2 = inputs[i].replace(" ", "")
        seq2 = expand_Ys(seq2)
        opt1 = optimise_circuit_part1(seq1)
        opt2 = optimise_circuit_part2(seq2)

        print("Part 1 optimisation:", get_opt_res(opt1))

        opt2 = get_opt_res(opt2)
        opt2 = expand_Ys(opt2)
        print("Part 2 optimisation:", opt2)
    
    return None

def run_tests():
    '''Create some hardcoded inputs and run them as tests.'''
    inputs = [
        'X(90), X(90)', 
        'X(90), Y(180), X(90)', 
        'X(90), X(90), Y(90), X(180), Y(90)', 
        'Y(45), X(90), Y(45), Y(70), Y(70), X(90)', 
        'X(90), X(90), Y(180), X(90)', 
        'X(90), X(90), Y(90), X(180), Y(90), X(90), X(90), Y(90)'
    ]

    # Do the tests
    testing(inputs)
    
    return None

def run_tests_with_runtimes(lx, lz, ly):
    '''Create some hardcoded sequences and run them as tests, also calculating 
    the sequence runtime according to get lengths'''
    inputs = [
        'X(90), X(90)', 
        'X(90), Y(180), X(90)', 
        'X(90), X(90), Y(90), X(180), Y(90)', 
        'Y(45), X(90), Y(45), Y(70), Y(70), X(90)', 
        'X(90), X(90), Y(180), X(90)', 
        'X(90), X(90), Y(90), X(180), Y(90), X(90), X(90), Y(90)'
    ]

    # Do the tests
    testing_with_runtimes(inputs, lx, lz, ly)
    
    return None

def testing_with_runtimes(inputs, lx, lz, ly):
    '''Running tests for Parts 1 and 2 - it is important for the results to be the same
    for both parts. For part two, the relevant Y(\theta)=Z(90)X(\theta)Z(-90) is shown.'''

    for i in range(len(inputs)):
        print("\nInput examined:", inputs[i])
        pre_opt_runtime = calculate_runtime(inputs[i].replace(" ", ""), lx, lz, ly)
        seq1 = inputs[i].replace(", ", "")
        seq2 = inputs[i].replace(" ", "")
        seq2 = expand_Ys(seq2)
        opt1 = optimise_circuit_part1(seq1)
        opt2 = optimise_circuit_part2(seq2)
        
        # Results for Part 1 - optimised
        opt1 = get_opt_res(opt1)
        print("Optimised sequence for Part 1:", opt1)
        opt1_runtime = calculate_runtime(opt1, lx, lz, ly)

        # Results for Part 2 - optimised
        opt2 = get_opt_res(opt2)
        opt2 = expand_Ys(opt2)
        print("Optimised sequence for Part 2:", opt2)
        opt2_runtime = calculate_runtime(opt2, lx, lz, ly)
        
        # Results for Part 3 - runtime
        print("Runtime for initial sequence:", pre_opt_runtime)
        print("Runtime for optimised sequence for Part 1:", opt1_runtime)
        print("Runtime for optimised sequence for Part 2:", opt2_runtime)
    
    return None

def generate_random_sequence(length, operations):
    '''Generates a random sequence of specific length and random angles for X, Y, Z operations or a subset of them.'''        
    return (', '.join(["{}({})".format(random.choice(operations), random.randrange(361)) for i in range(length)]))

def random_seq_test():
    '''Generates a random sequence of a given length and operations subset and optimises it. Showcases
    the relevant tests'''
    length = 0
    operations = ['']
    length = int(input("Enter a desired length for the sequence: "))
    operations = list(input("Give desired operations as XYZ or a subset (no commas or spaces):"))
    
    seq = generate_random_sequence(length, operations)
    print("\nThe randomely generated sequence of gates:", seq, "\n")
    
    pre_opt_runtime = calculate_runtime(seq.replace(" ", ""), lx, lz, ly)
    seq1 = seq.replace(", ", "")
    seq2 = seq.replace(" ", "")
    seq2 = expand_Ys(seq2)
    opt1 = optimise_circuit_part1(seq1)
    opt2 = optimise_circuit_part2(seq2)

    # Results for Part 1 - optimised
    opt1 = get_opt_res(opt1)
    print("Optimised sequence for Part 1:", opt1)
    opt1_runtime = calculate_runtime(opt1, lx, lz, ly)

    # Results for Part 2 - optimised
    opt2 = get_opt_res(opt2)
    opt2 = expand_Ys(opt2)
    print("Optimised sequence for Part 2:", opt2)
    opt2_runtime = calculate_runtime(opt2, lx, lz, ly)

    # Results for Part 3 - runtime
    print("\nRuntime for initial sequence:", pre_opt_runtime)
    print("Runtime for optimised sequence for Part 1:", opt1_runtime)
    print("Runtime for optimised sequence for Part 2:", opt2_runtime)
    
    return None

# Run the tests
print("\n---------!!Running tests for optimised circuits (Part 1 and 2)!!---------")
run_tests()

# Run the tests with runtimes
print("\n---------!!Running tests with associated runtimes (Parts 1, 2 and 3)!!---------")
lz = float(input("Enter the length of gate Z in nanoseconds: "))
lx = float(input("Enter the length of gate X in nanoseconds: "))
ly = float(input("Enter the length of gate Y in nanoseconds: "))
run_tests_with_runtimes(lx, lz, ly)

# Run a test with randomely generated sequence
print("\n---------!!Running a test on a randomely generated sequence!!---------")
random_seq_test()