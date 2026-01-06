"""
AUTHOR          : TS MOTSUMI
DATE PUBLISHED  : Jan 2026
LAST LOGIC EDIT : Dec 2025
FILE            : BCD_to_Seven_Seg_Converter.py

PROJECT DESCRIPTION
-------------------

Gate-level, object-oriented model of the IC7447 (BCD-to-7-segment decoder).

This program emulates the internal architecture of the IC7447 using relative gate
classes and staged routing. It organizes logic into Sections A to E blocks. Which consists of:
    1. Input conditioning,
    2. Blanking/ control network, 
    3. Intermediate reductions, 
    4. Segment pre-drivers, and 
    5. Final segment Drivers. 

Signal distribution is performed via named nets (lineA..lineJ) in a dedicated
routing phase to avoid "stuck-at" behavior. The design reflects datasheet-driven behavior,
including blanking and lamp-test interactions, and writes segment outputs to pins:
a: Pin13, b: Pin12, c: Pin11, d: Pin10, e: Pin9, f: Pin15, g: Pin14. 

Sequential reading order (sequential project flow)
    --------------------------------------------
    1) gates.py                              --> primitive logic gates
    2) gates_tb_gui.py (GUI testbench)       --> interactive visualization
    3) integrated_circuit.py                 --> the base IC abstraction
    4) bcd_to_seven_seg_Converter.py         --> concrete IC7447 modeled on top (current file)
    5) bcd_to_seven_seg_converter_tb.py      --> interactive IC7447 visualizations testbench

    ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ (optional) ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    -- ttl_74xx_ics.py                       --> basic applications of gate.py and integrated_circuit.py
    -- ttl_74xx_ics_tb                       --> non-interactive graphical visualizations

TO NOTE:
    --------------------------------------------
    THIS PROGRAMME ASSUMES PERFECT (IDEAL) ENVIROMENTAL CONDITIONS WHERE-BY:

    ~ HIGH (True) AND LOW (False) ARE ABSTRACTIONS OF INSTANTANOUS STATES OF
      MAXIMUM VOLTAGE (V_MAX) AND MINIMUM VOLTAGE (V_MIN)

    ~ EXTERNAL STIMULATION FACTORS SUCH AS SWITCH DEBOUNCING, TEMPERATURES,
      PROPAGATION DELAY etc...HAVE BEEN NEGLETED
"""

from primitives.gates import *                   # primitive gates (AND, OR, NOT, NAND, NOR, Buffer) used to build the IC netlist 
from primitives.integrated_circuit import IC     # abstract IC base: pins, staged processing (inputs --> setUP --> outputs) 

class IC_7447(IC):
    """
    IC7447 — Common_anode BCD_to_7_segment decoder (gate_level model).

    Parameters:
        ----------
        pwr : bool
            Power rail state (True = powered).
        gnd : bool
            Ground reference (False for normal operation).
        number_of_terminals : int
            Package pin count (typically 16 for DIP).
        D, C, B, A : bool
            External BCD inputs (MSB D --> LSB A).

    NOTE:
        -----
        - This model follows a datasheetStyle architecture rather than a direct truth table
        - Final segment outputs are written to pins in process()
        - GUI layers may invert for visualization depending on common_anode conventions. 
        """

    def __init__(self, pwr, gnd, number_of_terminals, D, C, B, A):
        super().__init__(pwr, gnd, number_of_terminals)

        # External BCD inputs captured as attributes for binding in inputs()
        self.A = A
        self.B = B
        self.C = C
        self.D = D

        # Power rails and pin map initialization (all pins forced to default LOW)
        self.gnd = gnd
        self.pwr = pwr
        self.number_of_terminals = number_of_terminals
        self.list_of_pins = IC.terminal_identify(self)  # dynamic pin dictionary

    def interGates(self):
        """
        Declaration of internal gates (no wiring here).

        NOTE:
        Declaration Separated from routing. This stage only instantiates gate objects. 
        Signal wiring happens later in setUP() to prevent constructor-time evaluation 
        from becoming "stuck-at" when upstream inputs change. 
        """
        # SECTION A: input conditioning

        self.AA = NAndGate(1)
        self.AB = NAndGate(2)
        self.AC = NAndGate(3)
        self.AD = NotGate(1)
        self.AE = NotGate(1)

        # SECTION B: blanking/ control network

        self.BA = NotGate(2)

        # Gate terminal Expansion
        self.BB1_2 = NOrGate(1)
        self.BB3 = NOrGate(1)
        self.BB4 = NOrGate(1)
        self.BB5 = NOrGate(1)
        self.BB = NOrGate(1)    # final Gate output with 6 terminals

        self.BC = NotGate(2)

        # SECTION C: intermediate NAND reductions (feed downstream lines)

        self.CA = NAndGate(4)
        self.CB = NAndGate(5)
        self.CC = NAndGate(6)
        self.CD = NAndGate(7)

        # SECTION D: segment pre drivers and combinational mixes

        self.DA = AndGate(1)
        self.DB = AndGate(2)

        # Gate terminal Expansion
        self.DC1_2 = AndGate(3)  
        self.DC3 = AndGate(3)
        self.DC = AndGate(3)    # final Gate output with 4 terminals

        self.DD = AndGate(4)

        # Gate terminal Expansion
        self.DE1_2 = AndGate(5)
        self.DE = AndGate(5)    # final Gate output with 3 terminals

        # Gate terminal Expansion
        self.DF1_2 = AndGate(6)
        self.DF = AndGate(6)    # final Gate output with 4 terminals

        self.DH = AndGate(7)

        # Gate terminal Expansion
        self.DI1_2 = AndGate(8)
        self.DI = AndGate(8)    # final Gate output with 3 terminals

        # Gate terminal Expansion
        self.DJ1_2 = AndGate(9)
        self.DJ = AndGate(9)    # final Gate output with 3 terminals

        # Gate terminal Expansion
        self.DK1_2 = AndGate(10)
        self.DK = AndGate(10)   # final Gate output with 3 terminals

        # Gate terminal Expansion
        self.DL1_2 = AndGate(11)
        self.DL = AndGate(11)   # final Gate output with 3 terminals

        self.DM = Buffer(2)

        self.DP = AndGate(12)
        self.DQ = AndGate(13)
        self.DV = AndGate(14)

        # Gate terminal Expansion
        self.DW1_2 = AndGate(15)
        self.DW = AndGate(15)   # final Gate output with 3 terminals

        # Gate terminal Expansion
        self.DX1_2 = AndGate(16)
        self.DX = AndGate(16)   # final Gate output with 3 terminals

        # Gate terminal Expansion
        self.DY1_2 = AndGate(17)
        self.DY3 = AndGate(17)
        self.DY = AndGate(17)   # final Gate output with 4 terminals

        # SECTION E: final segment drivers (OR combinations to pins {a to g})

        # Gate terminal Expansion
        self.EA1_2 = OrGate(1)
        self.EA = OrGate(1)     # final Gate output with 3 terminals

        # Gate terminal Expansion
        self.EB1_2 = OrGate(2)
        self.EB = OrGate(2)     # final Gate output with 3 terminals

        self.EC = OrGate(3)

        # Gate terminal Expansion
        self.ED1_2 = OrGate(4)
        self.ED = OrGate(4)     # final Gate output with 3 terminals

        self.EE = OrGate(5)

        # Gate terminal Expansion
        self.EF1_2 = OrGate(6)
        self.EF = OrGate(6)     # final Gate output with 3 terminals

        self.EH = OrGate(7)

    def setUP(self):
        """
        Route signals across sections (builds connections from lineA to lineJ).

        This is the wiring phase: 
            - signals from Section A and 
            - the cascaded NOR blanking/ control network in Section B are fanned out to
            - intermediate reductions -- Section C and
            - Pre_drivers --> Section D, then ultimately combined by the final drivers --> Section E. 
        """
        # Line A: distribute AE inversion; used as a common control input
        self.lineA = self.AE.output()
        self.AA.termi2 = self.lineA
        self.AB.termi2 = self.lineA
        self.AC.termi2 = self.lineA
        self.BB.termi1 = self.lineA
        self.DY1_2.termi1 = self.lineA

        # Line B: cascaded NOR reduction (BB) --> BA (NOT) --> lineB
        ## Implements blanking/ control combining LT/ RBI with data dependent terms.
        self.BB3.termi1 = self.BB1_2.output()
        self.BB3.termi2 = self.AD.output()
        self.BB4.termi1 = self.BB3.output()
        self.BB4.termi2 = self.AC.output()
        self.BB5.termi1 = self.BB4.output()
        self.BB5.termi2 = self.AB.output()
        self.BB.termi1 = self.BB5.output()
        self.BB.termi2 = self.AE.output()
        self.BA.termi1 = self.BB.output()
        self.lineB = self.BA.output()

        # Distribute lineB (control) to intermediate reductions
        self.CA.termi2 = self.lineB
        self.CB.termi2 = self.lineB
        self.CC.termi2 = self.lineB
        self.CD.termi2 = self.lineB
        self.BA.termi1 = self.lineB  # feedback/ conditioning path

        # Line C: AB reduction fan out into multiple pre drivers
        self.CB.termi1 = self.AB.output()
        self.lineC = self.CB.output()
        self.DA.termi1 = self.lineC
        self.DD.termi1 = self.lineC
        self.DF1_2.termi2 = self.lineC
        self.DI1_2.termi2 = self.lineC
        self.DL1_2.termi2 = self.lineC
        self.DQ.termi2 = self.lineC
        self.DV.termi1 = self.lineC
        self.DX1_2.termi2 = self.lineC

        # Line D: AD inversion --> reduction --> distribution
        self.CD.termi1 = self.AD.output()
        self.lineD = self.CD.output()
        self.DA.termi2 = self.lineD
        self.DD.termi2 = self.lineD
        self.DH.termi2 = self.lineD

        # Line E: AA output fan out to several consumers
        self.lineE = self.AA.output()
        self.DB.termi1 = self.lineE
        self.DF.termi2 = self.lineE
        self.DI.termi2 = self.lineE
        self.DK.termi2 = self.lineE
        self.CA.termi1 = self.lineE

        # Line F: CC reduction --> broad fan out
        self.CC.termi1 = self.AC.output()
        self.lineF = self.CC.output()
        self.DB.termi2 = self.lineF
        self.DE1_2.termi1 = self.lineF
        self.DF1_2.termi1 = self.lineF
        self.DH.termi1 = self.lineF
        self.DK1_2.termi1 = self.lineF
        self.DL1_2.termi1 = self.lineF
        self.DP.termi2 = self.lineF
        self.DX1_2.termi1 = self.lineF

        # Line G: CA output --> consumers (including Buffer DM)
        self.lineG = self.CA.output()
        self.DC.termi2 = self.lineG
        self.DE.termi2 = self.lineG
        self.DJ.termi2 = self.lineG
        self.DL.termi2 = self.lineG
        self.DQ.termi1 = self.lineG
        self.DW.termi2 = self.lineG
        self.DX.termi2 = self.lineG
        self.DM.termi1 = self.lineG

        # Line H: AB output --> fan out into staged reductions
        self.lineH = self.AB.output()
        self.DC3.termi2 = self.lineH
        self.DE1_2.termi2 = self.lineH
        self.DJ1_2.termi2 = self.lineH
        self.DK1_2.termi2 = self.lineH
        self.DP.termi1 = self.lineH
        self.DY.termi2 = self.lineH

        # Line I: AC output --> additional staged reductions
        self.lineI = self.AC.output()
        self.DC1_2.termi2 = self.lineI
        self.DI1_2.termi1 = self.lineI
        self.DJ1_2.termi1 = self.lineI
        self.DV.termi2 = self.lineI
        self.DW1_2.termi2 = self.lineI
        self.DY3.termi2 = self.lineI

        # Line J: AD output --> used in further reduction stages
        self.lineJ = self.AD.output()
        self.DC1_2.termi1 = self.lineJ
        self.DW1_2.termi1 = self.lineJ
        self.DY1_2.termi2 = self.lineJ

        # SUB OUTPUTS: connect staged reductions to final pre drivers
        # These create a multi level reduction tree feeding the segment driver stage.
        self.DC3.termi1 = self.DC1_2.output()
        self.DC.termi1 = self.DC3.output()
        self.DE.termi1 = self.DE1_2.output()
        self.DF.termi1 = self.DF1_2.output()
        self.DI.termi1 = self.DI1_2.output()
        self.DJ.termi1 = self.DJ1_2.output()
        self.DK.termi1 = self.DK1_2.output()
        self.DL.termi1 = self.DL1_2.output()
        self.DW.termi1 = self.DW1_2.output()
        self.DX.termi1 = self.DX1_2.output()
        self.DY3.termi1 = self.DY1_2.output()
        self.DY.termi1 = self.DY3.output()

    def outputs(self):
        """
        Drive final segment outputs (Section E).

        OR combinations produce the segment pins:
            a --> Pin13, b --> Pin12, c --> Pin11,
            d --> Pin10, e --> Pin9, f --> Pin15, g --> Pin14. 
        """
        # Segment a (EA)
        self.EA1_2.termi1 = self.DC.output()
        self.EA1_2.termi2 = self.DB.output()
        self.EA.termi1 = self.EA1_2.output()
        self.EA.termi2 = self.DA.output()

        # Segment b (EB)
        self.EB1_2.termi1 = self.DF.output()
        self.EB1_2.termi2 = self.DE.output()
        self.EB.termi1 = self.EB1_2.output()
        self.EB.termi2 = self.DD.output()

        # Segment c (EC)
        self.EC.termi1 = self.DH.output()
        self.EC.termi2 = self.DI.output()

        # Segment d (ED)
        self.ED1_2.termi1 = self.DL.output()
        self.ED1_2.termi2 = self.DK.output()
        self.ED.termi1 = self.ED1_2.output()
        self.ED.termi2 = self.DJ.output()

        # Segment e (EE)
        self.EE.termi1 = self.DM.output()
        self.EE.termi2 = self.DP.output()

        # Segment f (EF)
        self.EF1_2.termi1 = self.DW.output()
        self.EF1_2.termi2 = self.DV.output()
        self.EF.termi1 = self.EF1_2.output()
        self.EF.termi2 = self.DQ.output()

        # Segment g (EH)
        self.EH.termi1 = self.DX.output()
        self.EH.termi2 = self.DY.output()

    def inputs(self):
        """
        Bind external BCD inputs and control pins to Section A/ B gates.

        Pin map
        -------
        Pin7 = A, Pin1 = B, Pin2 = C, Pin6 = D
        Pin3 = LT (Lamp Test), Pin5 = RBI (Ripple Blanking Input)  
        """
        # External BCD inputs --> pin dictionary
        self.list_of_pins["Pin7"] = self.A   # A
        self.list_of_pins["Pin1"] = self.B   # B
        self.list_of_pins["Pin2"] = self.C   # C
        self.list_of_pins["Pin6"] = self.D   # D

        # Control pins (can be toggled by higher layers; default LOW here)
        self.list_of_pins["Pin3"] = False    # LT
        self.list_of_pins["Pin5"] = False    # RBI
        # self.list_of_pins["Pin4"] = False  # BI/RBO (optional; not wired in this version) 

        # Section A — bind inputs
        self.AA.termi1 = self.list_of_pins["Pin7"]
        self.AB.termi1 = self.list_of_pins["Pin1"]
        self.AC.termi1 = self.list_of_pins["Pin2"]
        self.AD.termi1 = self.list_of_pins["Pin6"]
        self.AE.termi1 = self.list_of_pins["Pin3"]

        # Section B — control preprocessing for BB cascade
        self.BB1_2.termi1 = self.list_of_pins["Pin3"]
        self.BB1_2.termi2 = self.list_of_pins["Pin5"]
        self.BC.termi1 = self.list_of_pins["Pin5"]
        return self.list_of_pins

    def process(self):
        """
        Pipelined process overview:
            1) Instantiate gates (interGates).
            2) Bind inputs and control pins (inputs).
            3) Build routing nets and cascades (setUP).
            4) Drive segment outputs (outputs) and write final pin states.

        Returns:
            -------
            dict[str, bool]
                Pin map including final segment outputs:
                Pin13 = a, Pin12 = b, Pin11 = c, 
                Pin10 = d, Pin9 = e, Pin15 = f, Pin14 = g. 
        """
        
        if self.pwr and not self.gnd:
            self.interGates()
            self.list_of_pins = self.inputs()
            self.setUP()
            self.outputs()

            # Final pin writes — segment mapping (a to g)
            self.list_of_pins["Pin13"] = self.EA.output()  # a
            self.list_of_pins["Pin12"] = self.EB.output()  # b
            self.list_of_pins["Pin11"] = self.EC.output()  # c
            self.list_of_pins["Pin10"] = self.ED.output()  # d
            self.list_of_pins["Pin9"]  = self.EE.output()  # e
            self.list_of_pins["Pin15"] = self.EF.output()  # f
            self.list_of_pins["Pin14"] = self.EH.output()  # g
            return self.list_of_pins
        else:
            # Unpowered or grounded IC: leave pins as initialized, defaultly LOW
            return self.list_of_pins
