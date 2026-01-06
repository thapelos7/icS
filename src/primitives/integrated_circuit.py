"""
AUTHOR          : TS MOTSUMI
DATE PUBLISHED  : Jan 2026
LAST LOGIC EDIT : Dec 2025
FILE            : integrated_circuit.py

PROJECT DESCRIPTION
-------------------
Base class for gate-level integrated circuits (ICs).

This standalone module defines IC, a minimal abstraction that future chips
can inherit from. It provides:
    - Power/ ground validation suitable for deterministic simulations.
    - Dynamic pin identification (terminal_identify) to create a pin netlist.
    - Abstract staged processing: inputs(), process(), output().

Sequential reading order (for project intuition)
    --------------------------------------------
    1) gates.py                              --> alpha logic gate primitives (origin)
    2) gates_tb_gui.py                       --> interactive GUI testbench/ visualizer for the core logic gates
    3) integrated_circuit.py                 --> premitive base IC abstraction (current file)
    4) bcd_to_seven_seg_converter.py         --> IC7447 routing
    5) bcd_to_seven_seg_converter_tb.py      --> interactive IC7447 visualizations testbench

    -- later you can explore ttl_74xx_ics.py, ttl_74xx_ics_tb.py and IC-specific GUIs

    ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ (optional) ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    ttl_74xx_ics.py, ttl_74xx_ics_tb.py --> basic applications of gate.py and integrated_circuit.py
""" 
from abc import abstractmethod as absm

# An abstract object representing the base of any integrated circuit
class IC:
    """
    Abstract base class for integrated circuits.

    Parameters:
        ----------
        pwr : bool
            Power rail state (True = VCC applied).
        gnd : bool
            Ground flag (False for normal operation).
        number_of_terminals : int
            Total package pins (including power/ground).

    Attributes:
        ----------
        pwr : bool
            Current power rail state.
        gnd : bool
            Current ground flag.
        number_of_terminals : int
            Pin count for the package.
        list_of_pins : dict[str, bool]
            Netlist-like mapping of pin names ("Pin1", ..., "PinN") to logic levels.
            where-by N is number of total pins of the IC

    NOTE:
        -----
        Subclasses should implement the staged lifecycle:
        1) inputs()  --> bind external pins
        2) process() --> build internal netlist/ routing, compute
        3) output()  --> (optional) return a representative final output
    """

from abc import abstractmethod as absm

# an abstract object of the integrated circuit is created
class IC:

    # instances of the IC object
    def __init__(self, pwr: bool, gnd: bool, number_of_terminals: int):
        """
        Initialize an IC with power and ground rails and a pin count.

        Raises
        ------
        TypeError
            If pwr or gnd are not boolean.
        """
        
        # verifies whether both gnd and pwr are bool type, else raise a type error
        if self.typechecker(pwr, gnd):
            self.pwr = pwr
            self.gnd = gnd

            self.number_of_terminals = number_of_terminals  # includes GND and VCC (pwr)

            self.list_of_pins = {}

        else:
            raise TypeError(type(pwr), type(gnd))
    
    # bool type varifier
    def typechecker(self, para1, para2) -> bool:
        """
        Return True if both parameters are boolean; otherwise False.

        NOTE:
            -----
            Kept minimal on purpose to emphasize alpha clarity over complexity.
            """ 
        return  True if type(para1) and type(para2) == bool else False
    
    # identification of terminals, returns the pin idS (numbers) and their respective states
    def terminal_identify(self) -> dict:
        """
        Create the pin map with default LOW states.

        Returns:
            -------
            dict[str, bool]
            - Mapping like {"Pin1": False, ..., f"Pin{N}": False}.

        NOTE:
            -----
            Pins are numbered starting at 1. Default LOW helps keep simulations
            deterministic until inputs are explicitly bound.
        """ 
        # individual pin numbers (x) starting at one instead of zero
        for x in range(1, self.number_of_terminals +1):

            # generating pin idS (pin numbers)
            pin_id = "Pin" + str(x)

            #  brute forcing every state to be False at origin
            self.list_of_pins[pin_id] = False

        # returns all the number of instatiated pins of the IC, all False
        return self.list_of_pins
    
# # # # # # # # # # # all the absract methods of this object # # # # # # # # # # #

    @absm
    def inputs(self):
        """
        Bind external pins for the IC.

        Implementations should write to self.list_of_pins to reflect 
        real package pins and control signals.
        """
        pass
    
    @absm
    def process(self):
        """
        Build internal netlist/ routing (wiring) and compute outputs.

        Typical staged flow in concrete ICs:
            1) Instantiate internal gates.
            2) Bind inputs.
            3) Route signals.
            4) Compute final outputs and write them back to pins.
        """
        pass

    @absm
    def output(self):
        """
        Return a representative output when powered; otherwise False.

        NOTE:
            -----
            Rule of thumb: no electrical system operates if VCC/ GND are wired incorrectly.
            Concrete ICs may choose to return a specific gate/ block output here.
        """
        
        if self.pwr and not self.gnd:
            return self.gate.output() 
        else:
            return False
        
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # returns well formated strS of all the necessary from the abstract process method
    def __str__(self):
        """
        Formatted-print the available pins and their current states.

        Returns:
            -------
            str
            - A human-readable view of the pin map after process().
            """
        return f"\nAvailable Pins: \n{self.process()}\n"
