"""
AUTHOR          : TS MOTSUMI
DATE PUBLISHED  : Jan 2026
LAST LOGIC EDIT : Dec 2025
FILE            : ttl_74xx_ics_tb.py

PROJECT DESCRIPTION
-------------------
This script serves as a testbench for the TTL 74xx single IC at a time.

It demonstrates:
    - Instantiation of a digital IC object (e.g., 7400 Quad 2-Input NAND).
    - Displaying pin states after processing internal logic.
    - Visualizing pin states using Matplotlib stem plots with annotated labels.

Modules Used:
    -------------
    matplotlib.pyplot
    - For plotting pin states.

    ttl_74xx_ic
    - Contains IC class definitions for TTL 74xx series.

Sequential reading order (sequential project flow)
    --------------------------------------------
    1) gates.py                              --> alpha logic gate primitives
    2) gates_tb_gui.py (GUI testbench)       --> interactive visualization
    3) integrated_circuit.py                 --> premitive base IC abstraction with pins + staged lifecycle
    4) bcd_to_seven_seg_converter.py         --> concrete IC7447 modeled on top of the premitives
    5) bcd_to_seven_seg_converter_tb.py      --> interactive visualizations testbench

    ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ (optional) ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    -- ttl_74xx_ic.py                        --> basic applications of gate.py and integrated_circuit.py
    -- ttl_74xx_ics_tb (current file)        --> non-interactive graphical visualizations

TO NOTE:
    --------------------------------------------
    THIS PROGRAMME ASSUMES PERFECT (IDEAL) ENVIROMENTAL CONDITIONS WHERE-BY:

    ~ HIGH (True) AND LOW (False) ARE ABSTRACTIONS OF INSTANTANOUS STATES OF
      MAXIMUM VOLTAGE (V_MAX) AND MINIMUM VOLTAGE (V_MIN)

    ~ EXTERNAL STIMULATION FACTORS SUCH AS SWITCH DEBOUNCING, TEMPERATURES,
      PROPAGATION DELAY etc...HAVE BEEN NEGLETED
    
    ALSO THIS IS A GRAPHICAL NON-GUI TESTBENCH for the ttl 74xx ic
"""

import matplotlib.pyplot as plt
from ttl_74xx_ics.ttl_74xx_ic import *

def runner():

    # intatiation of a digital integrated circuit and displaying its pins and their states

    digi_ic = IC_7400_QUAD_2_INPUT_NAND(True, False, 14)
    print(digi_ic.process())

    # plotting the states with their pin numbers using matplotlib

    x = len(digi_ic.list_of_pins)
    x_axis = range(1, x+1)
    y_axis = list(digi_ic.list_of_pins.values())

    plt.stem(x_axis, y_axis, basefmt=' ')
    plt.grid(True)

    plt.xlabel("Pin Numbers")
    plt.ylabel("States (LOW=0, HIGH=1)")

    # formating the dirac plots with comments of the relavent states

    for i, j in zip(x_axis, y_axis):
        plt.text(i - .45, j + .01, f'({i}, {"HIGH"if j else "LOW"})')
    plt.show()

if __name__ == "__main__":
    runner()
