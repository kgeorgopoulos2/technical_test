#### Author - Konstantinos Georgopoulos ####
# Importing libraries
import numpy as np
import collections
from scipy.spatial.transform import Rotation

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
    
    # Output as euler angles
    res = combined_rotations.as_euler("XYX", degrees=True)
    
    return res

def get_opt_res(opt):
    '''Returns the optimised sequence of gates.'''
    gates = ['X', 'Y', 'Z']
    # If gates have angle 0 or 360, they get eliminated
    res = [(gates[i] + '(' + str(round(opt[i])) + ')') for i in range(len(opt)) if round(opt[i])!=0 and round(opt[i])!=360]
    
    # If all the angles in the rotations are 0 or 360, then no operation is necessary
    return (','.join(res)) if res!=[] else ("No operation needed")

# Run Part 1
seq = input("Enter a sequence of pulses: ")
seq = seq.replace(", ", "")
opt = optimise_circuit_part1(seq)
print("Optimised sequence:", get_opt_res(opt))