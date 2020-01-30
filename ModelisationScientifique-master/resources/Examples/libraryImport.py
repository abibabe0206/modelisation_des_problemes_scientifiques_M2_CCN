#!/usr/bin/python

import math
import argparse as agp

def get_ceil_value_of_a_float(float_number):
    return math.ceil(float_number)



if __name__ == "__main__":
    parser = agp.ArgumentParser()
    parser.add_argument("-float", "--float", type=float, required=True)
    args = parser.parse_args()

    float_number = args.float

    ceil_part = get_ceil_value_of_a_float(float_number)
    print("The smallest integer value greater than " + str(float_number) + " is " + str(ceil_part))