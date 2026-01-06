
"""
AUTHOR          : TS MOTSUMI
DATE PUBLISHED  : Jan 2026
LAST LOGIC EDIT : Dec 2025
FILE            : BCD_to_Seven_Seg_Converter_tb.py

PROJECT DESCRIPTION
-------------------
PyQt5 GUI testbench for the IC7447 gate-level model.

This module provides a small UI that lets you toggle BCD inputs (A, B, C, D),
instantiates the IC_7447 from BCD_to_Seven_Seg_Converter.py, runs its staged
process() (declaration --> input bind --> routing --> outputs), and visualizes the
seven-segment state. In the common-anode convention, a segment is ON when the
corresponding output pin is LOW; the GUI maps that to a lime-colored rectangle.

Reading order suggestion (sequential project flow):
    1) gates.py                              --> primitive logic gates
    2) gates_tb_gui.py (GUI testbench)       --> interactive visualization
    3) integrated_circuit.py                 --> the base IC abstraction
    4) bcd_to_seven_seg_Converter.py         --> concrete IC7447 modeled on top
    5) bcd_to_seven_seg_converter_tb.py      --> interactive visualizations testbench (current file)

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

    ALSO REFLECTS THE IDEAL BEHAVIOUR OF THE 7447 IC BCD TO 7 SEG DISPLAY CYCLE
"""
import sys
from IC_7447.bcd_to_seven_seg_converter import *
import PyQt5.QtWidgets as qtw
from PyQt5.uic import loadUi

class SevenSegCA(qtw.QMainWindow):
    """
    Seven-segment common-anode visualizer for IC7447.

    The window exposes toggle buttons for BCD inputs (A TO D), recomputes the IC7447
    outputs on each change, and updates seven rectangles (a to g) to reflect segment
    states. Style convention: lime = segment ON (LOW pin), white = segment OFF (HIGH pin).
    """
    def __init__(self):
        # Initial button states: treat all BCD inputs as LOW (False)
        self.btnA_state = False
        self.btnB_state = False
        self.btnC_state = False
        self.btnD_state = False

        # Initialize the UI from the .ui file and set a fixed window geometry/title
        super(SevenSegCA, self).__init__()
        loadUi("Seven_Seg.ui", self)
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("IC_7447: Seven_Segment BCD Decoder -- TS MOTSUMI")

        # Connect all input toggles to a single handler (event-driven recompute)
        self.pushA.clicked.connect(self.button_triggered)
        self.pushB.clicked.connect(self.button_triggered)
        self.pushC.clicked.connect(self.button_triggered)
        self.pushD.clicked.connect(self.button_triggered)

    # Update the GUI segment tiles (A tog) based on pin states produced by IC7447
    def updateSegments(self):
        """
        Read segment pins (A tog) from self.states and update rectangles.

        Common-anode visualization rule:
        - Segment ON when pin is LOW   --> lime
        - Segment OFF when pin is HIGH --> white
        """
        # Map IC pins to segment states (A tog)
        self.a1_state = self.states["Pin13"]  # a
        self.b1_state = self.states["Pin12"]  # b
        self.c1_state = self.states["Pin11"]  # c
        self.d1_state = self.states["Pin10"]  # d
        self.e1_state = self.states["Pin9"]   # e
        self.f1_state = self.states["Pin15"]  # f
        self.g1_state = self.states["Pin14"]  # g

        # Apply styles — lime when ON (LOW), white when OFF (HIGH)
        if not self.a1_state:
            self.a1.setStyleSheet("background-color: lime")
        else:
            self.a1.setStyleSheet("background-color: white")

        if not self.b1_state:
            self.b1.setStyleSheet("background-color: lime")
        else:
            self.b1.setStyleSheet("background-color: white")

        if not self.c1_state:
            self.c1.setStyleSheet("background-color: lime")
        else:
            self.c1.setStyleSheet("background-color: white")

        if not self.d1_state:
            self.d1.setStyleSheet("background-color: lime")
        else:
            self.d1.setStyleSheet("background-color: white")

        if not self.e1_state:
            self.e1.setStyleSheet("background-color: lime")
        else:
            self.e1.setStyleSheet("background-color: white")

        if not self.f1_state:
            self.f1.setStyleSheet("background-color: lime")
        else:
            self.f1.setStyleSheet("background-color: white")

        if not self.g1_state:
            self.g1.setStyleSheet("background-color: lime")
        else:
            self.g1.setStyleSheet("background-color: white")

    # Handle any BCD toggle, recompute the IC, and refresh UI
    def button_triggered(self):
        """
        Capture toggle states (A TOD), instantiate IC7447 with current inputs,
        run process(), and update GUI segments accordingly.
        """
        # Reflect toggle states into labels and internal booleans
        if self.pushA.isChecked():
            self.btnA_state = True
            self.pushA.setText("True")
        else:
            self.btnA_state = False
            self.pushA.setText("False")

        if self.pushB.isChecked():
            self.btnB_state = True
            self.pushB.setText("True")
        else:
            self.btnB_state = False
            self.pushB.setText("False")

        if self.pushC.isChecked():
            self.btnC_state = True
            self.pushC.setText("True")
        else:
            self.btnC_state = False
            self.pushC.setText("False")

        if self.pushD.isChecked():
            self.btnD_state = True
            self.pushD.setText("True")
        else:
            self.btnD_state = False
            self.pushD.setText("False")

        # Instantiate and run the IC7447 model with the current BCD inputs
        # Staged evaluation inside process():
        #   interGates() --> inputs() --> setUP() --> outputs() --> pins (a to g)
        self.IC1 = IC_7447(
            True, False, 16,
            self.btnD_state, self.btnC_state, self.btnB_state, self.btnA_state
        )
        self.states = self.IC1.process()     # compute final pin states (keeps IC "awake")
        self.updateSegments()                # refresh visual representation (a to g segments)

def runner():
    app = qtw.QApplication(sys.argv)
    window = SevenSegCA()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    runner()
