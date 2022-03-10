#### Author - Konstantinos Georgopoulos ####
# Importing libraries
import numpy as np
import collections
from scipy.spatial.transform import Rotation
import warnings
warnings.filterwarnings("ignore")

### ----------------------- PART 3 -------------------------- ###
#### CALCULATING AND COMPARING TEST RUNTIMES ####
def calculate_runtime(seq, lx, lz, ly):
    '''Calculates the runtime of an quantum circuit (optimised or not). - seq: the circuit/sequence of rotations,
    lx, ly, lz: the runtime of an X, Y, Z gate; returns: the runtime of the circuit'''
    runtime = 0
    seq = seq.split(",")
    for i in range(len(seq)):
        if (seq[i][0]=='X'): runtime += lx
        elif (seq[i][0]=='Y'): runtime += ly
        else: runtime += lz
            
    return runtime

# Taking inputs
seq = input("Enter a sequence of pulses: ")
lz = float(input("Enter the length of gate Z in nanoseconds: "))
lx = float(input("Enter the length of gate X in nanoseconds: "))
ly = float(input("Enter the length of gate Y in nanoseconds: "))
print("Gate Z is of length", lz, "ns.")
print("Gate X is of length", lx, "ns.")
print("Gate Y is of length", ly, "ns.")
print(calculate_runtime(seq, lx, lz, ly))