"""
AUTHOR          : TS MOTSUMI
DATE PUBLISHED  : Jan 2026
LAST LOGIC EDIT : Dec 2025
FILE            : gates.py

PROJECT DESCRIPTION
-------------------
Alpha: Primitive Boolean gate library — the origin of the project.

This standalone module defines the foundation primitives
(OR, AND, NOT, NAND, NOR, XNOR, and a Buffer) used to construct larger gate-level netlists. 
It prioritizes:
    - Explicit boolean type enforcement for predictable simulation behavior.
    - Simple, deterministic output() methods for tracing.
    - Readable string representations to aid manual inspection, tracking and debugging.

Recommended reading order (sequential core flow for the whole project):
    1) gates.py         --> alpha logic gate primitives (current file)
    2) gates_tb_gui.py  --> interactive gate-level GUI testbench
       (later you can explore integrated_circuit.py and IC-specific GUIs)
"""

from abc import abstractmethod

# Abstract parent for all gates
class Gate:
    """
    Base class for primitive gates with explicit boolean inputs.

    Parameters:
        ----------
        number : int
        - Identifier for the gate (useful for tracing or netlist indexing).

        termi1 : bool, optional
        - First input terminal (default False  LOW).

        termi2 : bool, optional
        - Second input terminal (default False  LOW).

    Attributes:
        ----------
        number : int
        - Gate identifier retained for readability in traces.

        termi1 : bool
        - First input logic.

        termi2 : bool
        - Second input logic.

    NOTE:
        -----
        - This alpha design enforces boolean inputs up front to keep simulations deterministic.
        - Subclasses must implement output() to compute their logical function.
    """

    # Instantiation for the gate: id_number and its two input terminals
    def __init__(self, number: int, termi1: bool = False, termi2: bool = False):
        # Attempt to assign an id number for the gate (must be int)
        try:
            self.number = int(number)
        # If the id is not integrable, raise a type error
        except TypeError as e:
            raise TypeError(f"Type Error Detected!: {e}")

        # Verify that the terminal types are indeed boolean
        if self.check_type(termi1, termi2) == (True, True):
            self.termi1 = termi1
            self.termi2 = termi2
        # Otherwise raise a TypeError for both input terminals
        else:
            raise TypeError(f"INPUT TERMINAL VALUE NOT BOOLEAN: {type(termi1), type(termi2)}")

    # Terminal data types verified here (single- or dual-input gates)
    @staticmethod
    def check_type(terminal_1, terminal_2=None) -> tuple:
        """
        Return a tuple of boolean type checks for the provided terminals.

        Parameters:
            ----------
            terminal_1 : Any
            - First terminal value to be checked.

            terminal_2 : Any, optional
            - Second terminal value; if omitted, gate is treated as single-input.

        Returns:
            -------
            tuple or bool
            - (bool_is_type(terminal_1), bool_is_type(terminal_2)) for two-input gates,
            - or bool_is_type(terminal_1) for single-input gates.

        Side Effects:
            ------------
            Sets a global flag is_single_input_gate used by the string formatter to
            print appropriate terminal details.
        """
        
        global is_single_input_gate

        # Two-input gate: second terminal passed check both
        if terminal_2 != None:
            is_single_input_gate = False
            return (type(terminal_1) is type(bool()), type(terminal_2) is type(bool()))
        
        # Single-input gate: only terminal_1 provided
        else:
            is_single_input_gate = True
            return (type(terminal_1) is type(bool()))

    # Abstract output method for the gate
    @abstractmethod
    def output(self):
        """
        Compute and return the gate's logical output.

        Returns:
            -------
            bool
            - Output logic level derived from the current inputs.
        """
        pass

    # Returns a formatted string with the gate number and input terminal states
    def __str__(self):
        """
        Human-friendly representation of the gateS inputs (and optionally output).

        NOTE:
            -----
            Uses is_single_input_gate set by check_type() to format the terminals
            correctly when a gate has one versus two inputs.
        """
        return (
            f"\nGATE Nr: {self.number}\n"
            f"INPUT ONE IS : {'HIGH' if self.termi1 else 'FALSE'} \n"
            f"INPUT TWO IS : {'HIGH' if self.termi2 else 'FALSE'} \n"

            if is_single_input_gate else
            f"\nGATE Nr: {self.number}\n"
            f"INPUT ONE IS : {'HIGH' if self.termi1 else 'FALSE'} \n"
            f"INPUT TWO IS : {None} \n"
        )

# Logical OR gate
class OrGate(Gate):

    def __init__(self, number, termi1=False, termi2=False):
        super().__init__(number, termi1, termi2)

    def output(self):
        """
        Compute OR of two boolean inputs.

        Returns:
            -------
            bool
            - True if any input is True; otherwise False.

        Raises:
            ------
            TypeError
            - If either terminal is not boolean.
        """
        if self.check_type(self.termi1, self.termi2) == (True, True):
            return True if (bool(self.termi1) or bool(self.termi2)) else False
        else:
            raise TypeError(f"INPUT TERMINAL VALUE NOT BOOLEAN: {type(self.termi1), type(self.termi2)}")

    def __str__(self):
        # Include output for quick visual tracing in tests
        return (super().__str__() +
                f"OUTPUT'S NOW : {'HIGH' if self.output() else 'FALSE'} \n")

# Logical AND gate (alpha primitive)
class AndGate(Gate):

    def __init__(self, number, termi1=False, termi2=False):
        super().__init__(number, termi1, termi2)

    def output(self):
        """
        Compute AND of two boolean inputs.

        Returns:
            -------
            bool
            - True only if both inputs are True; otherwise False.

        Raises:
            ------
            TypeError
            - If either terminal is not boolean.
        """
        if self.check_type(self.termi1, self.termi2) == (True, True):
            return True if (bool(self.termi1) and bool(self.termi2)) else False
        else:
            raise TypeError(f"INPUT TERMINAL VALUE NOT BOOLEAN: {type(self.termi1), type(self.termi2)}")

    def __str__(self):
        return (super().__str__() +
                f"OUTPUT'S NOW : {'HIGH' if self.output() else 'FALSE'} \n")

# Logical NOT (inverter) gate (alpha primitive)."""
class NotGate(Gate):

    def __init__(self, number, termi1=False):
        super().__init__(number, termi1)

    def output(self):
        """
        Compute NOT of a single boolean input.

        Returns:
            -------
            bool
            - Inverted value of the single input.

        Raises:
            ------
            TypeError
            - If the terminal is not boolean.
        """
        if self.check_type(self.termi1) == (True):
            return (not True) if bool(self.termi1) else (not False)
        else:
            raise TypeError(f"INPUT TERMINAL VALUE NOT BOOLEAN: {type(self.termi1)}")

    def __str__(self):
        # Shows the computed output inline for quick diagnostics
        return super().__str__() + f"OUTPUT'S NOW : {'HIGH' if self.output() else 'LOW'}"

# Non-inverting buffer
class Buffer(Gate):

    def __init__(self, number, termi1=False):
        super().__init__(number, termi1)

    def output(self):
        """
        Pass-through of a single boolean input (driver stage concept).

        Returns:
            -------
            bool
            - Same value as the input (non-inverting).

        Raises:
            ------
            TypeError
            - If the terminal is not boolean.
        """
        if self.check_type(self.termi1) == (True):
            return True if bool(self.termi1) else False
        else:
            raise TypeError(f"INPUT TERMINAL VALUE NOT BOOLEAN: {type(self.termi1)}")

    def __str__(self):
        # Buffer prints both input and output (they MUST match here)
        return (
            f"\nGATE Nr: {self.number}\n"
            f"INPUT IS NOW : {'HIGH' if self.termi1 else 'FALSE'} \n"
            f"OUTPUT'S NOW : {'HIGH' if self.output() else 'FALSE'} \n"
        )

# Logical NOR (NOT-OR) gate
class NOrGate(Gate):

    def __init__(self, number, termi1=False, termi2=False):
        super().__init__(number, termi1, termi2)

    def output(self):
        """
        Compute NOR of two boolean inputs.

        Returns:
            -------
            bool
            - NOT(OR) of the inputs.

        Raises:
            ------
            TypeError
            - If either terminal is not boolean.
        """
        if self.check_type(self.termi1, self.termi2) == (True, True):
            return (not True) if (bool(self.termi1) or bool(self.termi2)) else (not False)
        else:
            raise TypeError(f"INPUT TERMINAL VALUE NOT BOOLEAN: {type(self.termi1), type(self.termi2)}")

    def __str__(self):
        return (super().__str__() +
                f"OUTPUT'S NOW : {'HIGH' if self.output() else 'FALSE'} \n")

# Logical NAND (NOT-AND) gate
class NAndGate(Gate):

    def __init__(self, number, termi1=False, termi2=False):
        super().__init__(number, termi1, termi2)

    def output(self):
        """
        Compute NAND of two boolean inputs.

        Returns:
            -------
            bool
            - NOT(AND) of the inputs.

        Raises:
            ------
            TypeError
            - If either terminal is not boolean.
        """
        if self.check_type(self.termi1, self.termi2) == (True, True):
            return False if (bool(self.termi1) and bool(self.termi2)) else True
        else:
            raise TypeError(f"INPUT TERMINAL VALUE NOT BOOLEAN: {type(self.termi1), type(self.termi2)}")

    def __str__(self):
        return (super().__str__() +
                f"OUTPUT'S NOW : {'HIGH' if self.output() else 'FALSE'} \n")

# Logical XNOR gate
class XNOrGate(Gate):

    def __init__(self, number, termi1=False, termi2=False):
        super().__init__(number, termi1, termi2)

    def output(self):
        """
        Compute XNOR (equivalence) of two boolean inputs.

        Returns:
            -------
            bool
            - True when inputs match; False otherwise.

        Raises:
            ------
            TypeError
            - If either terminal is not boolean.
        """
        if self.check_type(self.termi1, self.termi2) == (True, True):
            return True if (bool(self.termi1) is bool(self.termi2)) else False
        else:
            raise TypeError(f"INPUT TERMINAL VALUE NOT BOOLEAN: {type(self.termi1), type(self.termi2)}")

    def __str__(self):
        return (super().__str__() +
                f"OUTPUT'S NOW : {'HIGH' if self.output() else 'FALSE'} \n")

# Logical XNAND gate
class XNAndGate(Gate):

    def __init__(self, number, termi1=False, termi2=False):
        super().__init__(number, termi1, termi2)

    def output(self):
        """
        Compute the custom 'XNAND' behavior:

        Returns:
            -------
            bool
            - True if both inputs are LOW, or if inputs are unequal; otherwise False.

        Raises:
            ------
            TypeError
            - If either terminal is not boolean.
        """
        if self.check_type(self.termi1, self.termi2) == (True, True):
            return False if (bool(self.termi1) and bool(self.termi2)) else True
        else:
            raise TypeError(f"INPUT TERMINAL VALUE NOT BOOLEAN: {type(self.termi1), type(self.termi2)}")

    def __str__(self):
        return (super().__str__() +
                f"OUTPUT'S NOW : {'HIGH' if self.output() else 'FALSE'} \n")
