#### Author - Konstantinos Georgopoulos ####
# Importing libraries
import numpy as np
import collections
from scipy.spatial.transform import Rotation

import warnings
warnings.filterwarnings("ignore")

### ----------------------- PART 2 -------------------------- ###
def expand_Ys(seq):
    '''Prepares the sequence according Y(\theta)=Z(90)X(\theta)Z-90 for a quantum computer where Y(\theta) is not applied
    - seq: the sequence for expansion; returns: a string containing the new operations'''
    spl = seq.split(",")
    for i, op in enumerate(spl):
        if (get_instr(op)=='Y'): spl[i] = 'Z(90),X(' + str(get_angle(op)) + '),Z(-90)'

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
    
    # Output as euler angles for the extrinsic x-y-z rotations
    res = combined_rotations.as_euler("XYZ", degrees=True)
    
    return res

def get_opt_res(opt):
    '''Returns the optimised sequence of gates.'''
    gates = ['X', 'Y', 'Z']
    # If gates have angle 0 or 360, they get eliminated
    res = [(gates[i] + '(' + str(round(opt[i])) + ')') for i in range(len(opt)) if round(opt[i])!=0 and round(opt[i])!=360]
    
    # If all the angles in the rotations are 0 or 360, then no operation is necessary
    return (','.join(res)) if res!=[] else ("No operation needed")

# Run Part 2
seq = input("Enter a sequence of pulses: ")
seq = seq.replace(" ", "")
seq = expand_Ys(seq)
opt = optimise_circuit_part2(seq)
opt = get_opt_res(opt)
opt = expand_Ys(opt)
print("Optimised sequence", opt)