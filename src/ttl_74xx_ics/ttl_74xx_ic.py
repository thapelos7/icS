"""
AUTHOR          : TS MOTSUMI
DATE PUBLISHED  : Jan 2026
LAST LOGIC EDIT : Dec 2025
FILE            : ttl_74xx_ic.py

PROJECT DESCRIPTION
--------------------
Contains object-oriented representations of common TTL integrated circuits (ICs),
including 7400 (Quad 2-Input NAND), 7404 (Hex Inverter), 7402 (Quad 2-Input NOR),
and 7408 (Quad 2-Input AND). Each IC class inherits from the base IC class and
simulates pin-level behavior through internal gate wiring.

Classes:
    --------
    IC_7400_QUAD_2_INPUT_NAND
    - Represents a 7400 IC with four NAND gates.

    IC_7404_HEX_INVERTER
    - Represents a 7404 IC with six NOT gates.

    IC_7402_QUAD_2_INPUT_NOR
    - Represents a 7402 IC with four NOR gates.

    IC_7408_QUAD_2_INPUT_AND
    - Represents a 7408 IC with four AND gates.

Sequential reading order (sequential project flow)
    --------------------------------------------
    1) gates.py                              --> alpha logic gate primitives 
    2) gates_tb_gui.py (GUI testbench)       --> interactive visualization
    3) integrated_circuit.py                 --> premitive base IC abstraction
    4) bcd_to_seven_seg_converter.py         --> concrete IC7447 modeled on top of the premitives
    5) bcd_to_seven_seg_converter_tb.py      --> interactive visualizations testbench

    ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ (optional) ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    -- ttl_74xx_ic.py (current file)         --> basic applications of gate.py and integrated_circuit.py
    -- ttl_74xx_ics_tb                       --> non-interactive graphical visualizations

TO NOTE:
    --------------------------------------------
    THIS PROGRAMME ASSUMES PERFECT (IDEAL) ENVIROMENTAL CONDITIONS WHERE-BY:

    ~ HIGH (True) AND LOW (False) ARE ABSTRACTIONS OF INSTANTANOUS STATES OF
      MAXIMUM VOLTAGE (V_MAX) AND MINIMUM VOLTAGE (V_MIN)

    ~ EXTERNAL STIMULATION FACTORS SUCH AS SWITCH DEBOUNCING, TEMPERATURES,
      PROPAGATION DELAY etc...HAVE BEEN NEGLETED
    
    ALSO THESE ARE Abstractions OF THE ttl 74xx ic
"""

from primitives.gates import *
from primitives.integrated_circuit import IC

# object of the 7400 integrated circuit inherits from IC
class IC_7400_QUAD_2_INPUT_NAND(IC):
    # instatiation of the 7400 ic
    def __init__(self, pwr: bool, gnd: bool, number_of_terminals: int):
        super().__init__(pwr, gnd, number_of_terminals)
        self.pwr = pwr  # the VCC pin
        self.gnd = gnd  # the GND pin
        # declaring the list of pins of the 7400 ic object from the parent object
        self.list_of_pins = IC.terminal_identify(self)

    # typical inputs pins that the 7400 ic will listen from
    def inputs(self):
        # all customizable through hardcording:
        # can only be either HIGH = True OR LOW = False
        self.list_of_pins["Pin1"] = True
        self.list_of_pins["Pin2"] = False
        self.list_of_pins["Pin5"] = False
        self.list_of_pins["Pin6"] = True
        self.list_of_pins["Pin8"] = False
        self.list_of_pins["Pin9"] = True
        self.list_of_pins["Pin12"] = True
        self.list_of_pins["Pin13"] = True
        return self.list_of_pins  # returns the updated 7400's inputs

    # outputs as according to the configured inputs
    def output(self):
        return super().output()  # returns the updated 7400's inputs

    # the process in which the ic endures, returning output list of pins in a dictionary
    def process(self) -> dict:
        self.gate = NAndGate(1, False, False)  # instatiation of gate
        self.list_of_pins = self.inputs()  # refresh
        # wiring the internal gates within the 7400 ic (object) approapriately
        self.gate.termi1 = self.list_of_pins["Pin1"]
        self.gate.termi2 = self.list_of_pins["Pin2"]
        self.list_of_pins["Pin3"] = self.output()
        self.gate.termi2 = self.list_of_pins["Pin5"]
        self.gate.termi1 = self.list_of_pins["Pin6"]
        self.list_of_pins["Pin4"] = self.output()
        self.list_of_pins["Pin7"] = self.pwr
        self.gate.termi2 = self.list_of_pins["Pin8"]
        self.gate.termi1 = self.list_of_pins["Pin9"]
        self.list_of_pins["Pin10"] = self.output()
        self.gate.termi2 = self.list_of_pins["Pin12"]
        self.gate.termi1 = self.list_of_pins["Pin13"]
        self.list_of_pins["Pin11"] = self.output()
        self.list_of_pins["Pin14"] = self.gnd
        return self.list_of_pins  # returns the updated 7400's inputs

    # returns well formated strS of all the necessary information from the parent obj
    def __str__(self) -> str:
        return super().__str__()


class IC_7404_HEX_INVERTER(IC):
    # instatiation of the 7404 ic
    def __init__(self, pwr, gnd, number_of_terminals):
        super().__init__(pwr, gnd, number_of_terminals)
        self.pwr = pwr  # the VCC pin
        self.gnd = gnd  # the GND pin
        # declaring the list of pins of the 7404 ic object from the parent object
        self.list_of_pins = IC.terminal_identify(self)

    # typical input pins that the 7404 will listen from
    def inputs(self):
        # all customizable through hardcording:
        # can only be either HIGH = True OR LOW = False
        self.list_of_pins["Pin2"] = True
        self.list_of_pins["Pin4"] = True
        self.list_of_pins["Pin6"] = True
        self.list_of_pins["Pin8"] = True
        self.list_of_pins["Pin10"] = True
        self.list_of_pins["Pin12"] = True
        return self.list_of_pins  # returns the updated 7404's inputs

    # the process in which the ic endures, returning output list of pins in a dictionary
    def process(self):
        self.gate = NotGate(1, False)  # instatiation of gate
        self.list_of_pins = self.inputs()  # refresh
        # wiring the internal gates within the 7404 ic (object) approapriately
        self.gate.termi1 = self.list_of_pins["Pin2"]
        self.list_of_pins["Pin1"] = self.output()
        self.gate.termi1 = self.list_of_pins["Pin4"]
        self.list_of_pins["Pin3"] = self.output()
        self.gate.termi1 = self.list_of_pins["Pin6"]
        self.list_of_pins["Pin5"] = self.output()
        self.list_of_pins["Pin7"] = self.gnd
        self.gate.termi1 = self.list_of_pins["Pin8"]
        self.list_of_pins["Pin9"] = self.output()
        self.gate.termi1 = self.list_of_pins["Pin10"]
        self.list_of_pins["Pin11"] = self.output()
        self.gate.termi1 = self.list_of_pins["Pin12"]
        self.list_of_pins["Pin13"] = self.output()
        self.list_of_pins["Pin14"] = self.pwr
        return self.list_of_pins  # returns the updated 7404's pins

    # outputs as according to the configured inputs
    def output(self):
        return super().output()  # returns the updated 7404's output

    # returns well formated strS of all the necessary information from the parent obj
    def __str__(self):
        return super().__str__()


class IC_7402_QUAD_2_INPUT_NOR(IC):
    # instatiation of the 7402 ic
    def __init__(self, pwr, gnd, number_of_terminals):
        super().__init__(pwr, gnd, number_of_terminals)
        self.pwr = pwr  # the VCC pin
        self.gnd = gnd  # the GND pin
        self.list_of_pins = IC.terminal_identify(self)  ## brute force call, initiation

    # typical input pins that the 7402 will listen from
    def inputs(self):
        # all customizable through hardcording:
        # can only be either HIGH = True OR LOW = False
        self.list_of_pins["Pin2"] = False
        self.list_of_pins["Pin3"] = False
        self.list_of_pins["Pin5"] = False
        self.list_of_pins["Pin6"] = False
        self.list_of_pins["Pin8"] = False
        self.list_of_pins["Pin9"] = False
        self.list_of_pins["Pin11"] = False
        self.list_of_pins["Pin12"] = False
        return self.list_of_pins  # returns the updated 7402's inputs

    # outputs as according to the configured inputs
    def output(self):
        return super().output()  # returns the updated 7402's output

    # the process in which the ic endures, returning output list of pins in a dictionary
    def process(self):
        self.gate = NOrGate(1, False, False)  # instatiation of gate
        self.list_of_pins = self.inputs()  ## refresh
        # wiring the internal gates within the 7402 ic (object) approapriately
        self.gate.termi1 = self.list_of_pins["Pin3"]
        self.gate.termi2 = self.list_of_pins["Pin2"]
        self.list_of_pins["Pin1"] = self.output()
        self.gate.termi2 = self.list_of_pins["Pin5"]
        self.gate.termi1 = self.list_of_pins["Pin6"]
        self.list_of_pins["Pin4"] = self.output()
        self.list_of_pins["Pin7"] = self.gnd
        self.gate.termi2 = self.list_of_pins["Pin8"]
        self.gate.termi1 = self.list_of_pins["Pin9"]
        self.list_of_pins["Pin10"] = self.output()
        self.gate.termi2 = self.list_of_pins["Pin11"]
        self.gate.termi1 = self.list_of_pins["Pin12"]
        self.list_of_pins["Pin13"] = self.output()
        self.list_of_pins["Pin14"] = self.pwr
        return self.list_of_pins  # returns the updated 7402's pins

    # returns well formated strS of all the necessary information from the parent obj
    def __str__(self):
        return super().__str__()


class IC_7408_QUAD_2_INPUT_NOR(IC):
    # instatiation of the 7408 ic
    def __init__(self, pwr, gnd, number_of_terminals):
        super().__init__(pwr, gnd, number_of_terminals)
        self.pwr = pwr  # the VCC pin
        self.gnd = gnd  # the GND pin
        self.list_of_pins = IC.terminal_identify(self)  ## brute force call, initiation

    # typical input pins that the 7408 will listen from
    def inputs(self):
        # all customizable through hardcording:
        # can only be either HIGH = True OR LOW = False
        self.list_of_pins["Pin1"] = True
        self.list_of_pins["Pin2"] = False
        self.list_of_pins["Pin4"] = False
        self.list_of_pins["Pin5"] = True
        self.list_of_pins["Pin9"] = False
        self.list_of_pins["Pin10"] = True
        self.list_of_pins["Pin12"] = True
        self.list_of_pins["Pin13"] = True
        return self.list_of_pins  # returns the updated 7408's inputs

    # outputs as according to the configured inputs
    def output(self):
        return super().output()  # returns the updated 7408's output

    # the process in which the ic endures, returning output list of pins in a dictionary
    def process(self):
        self.gate = AndGate(1, False, False)  # instatiation of gate
        self.list_of_pins = self.inputs()  ## refresh
        # wiring the internal gates within the 7408 ic (object) approapriately
        self.gate.termi1 = self.list_of_pins["Pin2"]
        self.gate.termi2 = self.list_of_pins["Pin1"]
        self.list_of_pins["Pin3"] = self.output()
        self.gate.termi2 = self.list_of_pins["Pin4"]
        self.gate.termi1 = self.list_of_pins["Pin5"]
        self.list_of_pins["Pin6"] = self.output()
        self.list_of_pins["Pin7"] = self.pwr
        self.gate.termi2 = self.list_of_pins["Pin9"]
        self.gate.termi1 = self.list_of_pins["Pin10"]
        self.list_of_pins["Pin8"] = self.output()
        self.gate.termi2 = self.list_of_pins["Pin12"]
        self.gate.termi1 = self.list_of_pins["Pin13"]
        self.list_of_pins["Pin11"] = self.output()
        self.list_of_pins["Pin14"] = self.gnd
        return self.list_of_pins  # returns the updated 7408's pins

    # returns well formated strS of all the necessary information from the parent obj
    def __str__(self):
        return super().__str__()
