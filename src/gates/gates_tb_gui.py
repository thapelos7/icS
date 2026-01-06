"""
AUTHOR          : TS MOTSUMI
DATE PUBLISHED  : Jan 2026
LAST EDIT       : Dec 2025
FILE            : gates_tb_gui.py

PROJECT DESCRIPTION
-------------------
Alpha GUI: Interactive testbench for primitive logic gates.

This standalone PyQt5 application lets you toggle two input terminals (termi1, termi2),
select a gate primitive (OR, AND, NOT, NOR, NAND, XNOR, XNAND, BUFFER), and observe the output
in real time. It also displays the truth table for the selected gate and highlights the
row that matches the current input state.

Sequential reading order (recommended sequential project flow):
    1) gates.py                         --> alpha primitive logic gates
    2) gates_tb_gui.py                  --> interactive GUI testbench/ visualizer (current file)
    3) integrated_circuit.py            --> premitive base IC abstraction (pins + staged processing)
    4) bdc_to_seven_seg_converter.py    --> solid concrete application using IC7447
    5) bcd_to_seven_seg_converter_tb.py --> interactive visualizations testbench

TO NOTE:
    -----
    - The GUI is intentionally minimal, ideal for being deterministic (Boolean-only inputs and outputs).
    - The “XNAND” gate is a non-standard primitive, but its included to demonstrate how
    custom truth tables can be explored in early experimental scenarios.
    
    ALSO THIS PROGRAMME ASSUMES PERFECT (IDEAL) ENVIROMENTAL CONDITIONS WHERE-BY:

        ~ HIGH (True) AND LOW (False) ARE ABSTRACTIONS OF INSTANTANOUS STATES OF
        MAXIMUM VOLTAGE (V_MAX) AND MINIMUM VOLTAGE (V_MIN)
        
        ~ EXTERNAL STIMULATION FACTORS SUCH AS SWITCH DEBOUNCING, TEMPERATURES,
        PROPAGATION DELAY etc...HAVE BEEN NEGLETED
"""

import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
from PyQt5.uic import loadUi

# import alpha primitives: OrGate, AndGate, NotGate, NOrGate, NAndGate, XNOrGate, XNAndGate, Buffer
from primitives.gates import *

class MainWindow(qtw.QMainWindow):
    """
    Main GUI window for the logic gate testbench.

    Features:
        --------
        - Gate selection via combo box (OR/ AND/ NOT/ NOR/ NAND/ XNOR/ XNAND/ BUFFER).
        - Toggle button(s) for input terminals (termi1, termi2) or (termi1 only).
        - Live output indicator (emoji + label) and gate banner color.
        - Read-only truth table; current input row auto-selected.

    Signals:
        -------
        state_changed : pyqtSignal(bool)
        - Emitted when either input terminal toggles; triggers UI refresh.

    NOTE:
        -----
        - For the single-input NOT gate and BUFFER gate, termi2 is hidden, only termi1 is priviledged
        - The truth table is populated for quick reference and teaching clarity.
        """

    state_changed = qtc.pyqtSignal(bool)

    # Initialize window, wire UI events, and set default states
    def __init__(self):

        super(MainWindow, self).__init__()
        loadUi("gate_sim_gui_lv1.ui", self)
        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle("Ideal Logic Gate Simulator -- TS MOTSUMI")

        # Default input states (LOW = False)
        self.termi1_state = False
        self.termi2_state = False

        # Create selectable gates
        gates = ["OR Gate", "AND Gate", "NOT Gate", "NOR Gate", "NAND Gate", "XNOR Gate", "XNAND Gate", "BUFFER Gate"]
        self.combo_box.addItems(gates)

        # Event wiring
        self.combo_box.currentTextChanged.connect(self.UI)
        self.termi1.clicked.connect(self.termi1_pressed)
        self.termi2.clicked.connect(self.termi2_pressed)
        self.state_changed.connect(self.UI)

        # Truth-table widget setup ( 5 rows: header + 4 input combinations; 3 columns: | A | B | Output | )
        self.truth_table.setRowCount(5)
        self.truth_table.setColumnCount(3)
        ## unedditable
        self.truth_table.setEditTriggers(qtw.QAbstractItemView.NoEditTriggers)

    # # # # Input toggle handlers # # # #

    # Toggle terminal 1 state and signal UI refresh
    def termi1_pressed(self):
        self.termi1_state = not self.termi1_state
        self.state_changed.emit(self.termi1_state)

    # Toggle terminal 2 state and signal UI refresh
    def termi2_pressed(self):
        self.termi2_state = not self.termi2_state
        self.state_changed.emit(self.termi2_state)

    # # # # Formatted contents for table cells # # # #

    # Return a centered table item containing '1' (HIGH)
    def one(self):
        self.ones = qtw.QTableWidgetItem("1")
        self.ones.setTextAlignment(qtc.Qt.AlignCenter)
        return self.ones

    # Return a centered table item containing '0' (LOW)
    def zero(self):
        self.zeros = qtw.QTableWidgetItem("0")
        self.zeros.setTextAlignment(qtc.Qt.AlignCenter)
        return self.zeros

    # # # # Helper: compute which truth-table row matches current input state # # # #

    def select_row(self):
        """
        Return the truth-table row index corresponding to (termi1, termi2).

        Rows:
            ----
            1: 0, 0
            2: 0, 1
            3: 1, 0
            4: 1, 1
        """

        if not self.termi1_state and not self.termi2_state:
            return 1
        elif not self.termi1_state and self.termi2_state:
            return 2
        elif self.termi1_state and not self.termi2_state:
            return 3
        elif self.termi1_state and self.termi2_state:
            return 4

    # # # # Gate selection and truth-table population # # # #

    def which_gate(self, text):
        """
        Return an instantiated gate corresponding to current combo box selection.

        Also configures the truth table and visibility of termi2 for NOT and BUFFER.

        Parameters:
            ----------
            text : str
            - Gate label from the combo box.

        Returns:
            -------
            Gate
            - A gate instance (OrGate, AndGate, NotGate, NOrGate, NAndGate, XNOrGate, XNAndGate, Buffer).
        """
        
        if text == "NOT Gate":
            # Mirror second terminal and hide related UI; set truth table for 1-input gate
            self.termi2_state = self.termi1_state
            self.termi2.setVisible(False)
            self.line_2.setVisible(False)

            # Truth-table outputs for NOT (A only): 
            ## A = 0 --> 1, A = 1 --> 0. 
            ## Hide terminal's 2 column & 3, 4 rows
            self.truth_table.setItem(1, 2, self.one())
            self.truth_table.setItem(2, 2, self.zero())
            self.truth_table.setItem(3, 2, self.zero())
            self.truth_table.setItem(4, 2, self.zero())
            self.truth_table.setColumnHidden(1, True)
            self.truth_table.setRowHidden(2, True)
            self.truth_table.setRowHidden(3, True)

            self.chosen_gate = NotGate(1, self.termi1_state)
            return self.chosen_gate
        
        elif text == "BUFFER Gate":
            # set truth table for 1-input gate
            self.termi2_state = self.termi1_state
            self.termi2.setVisible(False)
            self.line_2.setVisible(False)

            # Truth-table outputs for BUFFER (A only): 
            ## A = 0 --> 0, A = 1 --> 1
            ## Hide terminal's 2 column & 3, 4 rows
            self.truth_table.setItem(1, 2, self.zero())
            self.truth_table.setItem(2, 2, self.one())
            self.truth_table.setItem(3, 2, self.one())
            self.truth_table.setItem(4, 2, self.one())
            self.truth_table.setColumnHidden(1, True)
            self.truth_table.setRowHidden(2, True)
            self.truth_table.setRowHidden(3, True)

            self.chosen_gate = Buffer(1, self.termi1_state)
            return self.chosen_gate

        # Restore visibility for two-input gates and reset table layout
        else:
            self.termi2.setVisible(True)
            self.line_2.setVisible(True)
            self.truth_table.setColumnHidden(1, False)
            self.truth_table.setRowHidden(2, False)
            self.truth_table.setRowHidden(3, False)

            if text == "OR Gate":
                # OR truth table
                self.truth_table.setItem(1, 2, self.zero())
                self.truth_table.setItem(2, 2, self.one())
                self.truth_table.setItem(3, 2, self.one())
                self.truth_table.setItem(4, 2, self.one())
                self.chosen_gate = OrGate(1, self.termi1_state, self.termi2_state)
                return self.chosen_gate

            elif text == "AND Gate":
                # AND truth table
                self.truth_table.setItem(1, 2, self.zero())
                self.truth_table.setItem(2, 2, self.zero())
                self.truth_table.setItem(3, 2, self.zero())
                self.truth_table.setItem(4, 2, self.one())
                self.chosen_gate = AndGate(1, self.termi1_state, self.termi2_state)
                return self.chosen_gate

            elif text == "NOR Gate":
                # NOR truth table
                self.truth_table.setItem(1, 2, self.one())
                self.truth_table.setItem(2, 2, self.zero())
                self.truth_table.setItem(3, 2, self.zero())
                self.truth_table.setItem(4, 2, self.zero())
                self.chosen_gate = NOrGate(1, self.termi1_state, self.termi2_state)
                return self.chosen_gate

            elif text == "NAND Gate":
                # NAND truth table
                self.truth_table.setItem(1, 2, self.one())
                self.truth_table.setItem(2, 2, self.one())
                self.truth_table.setItem(3, 2, self.one())
                self.truth_table.setItem(4, 2, self.zero())
                self.chosen_gate = NAndGate(1, self.termi1_state, self.termi2_state)
                return self.chosen_gate

            elif text == "XNOR Gate":
                # XNOR truth table (equivalence)
                self.truth_table.setItem(1, 2, self.one())
                self.truth_table.setItem(2, 2, self.zero())
                self.truth_table.setItem(3, 2, self.zero())
                self.truth_table.setItem(4, 2, self.one())
                self.chosen_gate = XNOrGate(1, self.termi1_state, self.termi2_state)
                return self.chosen_gate

            elif text == "XNAND Gate":
                # XNAND (non-standard): outputs 1 for 00, 01, 10; outputs 0 for 11
                self.truth_table.setItem(1, 2, self.one())
                self.truth_table.setItem(2, 2, self.one())
                self.truth_table.setItem(3, 2, self.one())
                self.truth_table.setItem(4, 2, self.zero())
                self.chosen_gate = XNAndGate(1, self.termi1_state, self.termi2_state)
                return self.chosen_gate

    # # # # UI refresh # # # #

    def UI(self):
        """
        Refresh all visual elements based on current inputs and selected gate.

        Updates:
            -------
            - Gate banner text + color.
            - Output emoji (🔵 for HIGH, 🟠 for LOW) and label.
            - Terminal labels (HIGH/ LOW).
            - Truth-table row selection for current states of (termi1, termi2).
        """
        text = self.combo_box.currentText()

        # Gate banner color: skyblue when output HIGH, orange when LOW
        color1 = "background-color: skyblue;"
        color2 = "background-color: orange;"

        # Instantiate gate and compute output
        chosen_gate_output = self.which_gate(text).output()

        # Top banner + output status
        self.gate.setText(f"GATE: {text.strip("Gate")}")
        self.output.setText(f"{'🔵' if chosen_gate_output else '🟠'}")
        self.termi1.setText(f"{'HIGH' if self.termi1_state else 'LOW'}")
        self.termi2.setText(f"{'HIGH' if self.termi2_state else 'LOW'}")
        self.output_label.setText(f"{'HIGH' if chosen_gate_output else 'LOW'}")

        # Apply banner color based on output
        self.gate.setStyleSheet(f"{color1 if chosen_gate_output else color2 }")

        # Truth-table: select row matching current inputs
        self.truth_table.setSelectionBehavior(qtw.QAbstractItemView.SelectRows)
        self.truth_table.selectRow(self.select_row())

# # # # Entrypoint # # # #

def runner():
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    runner()