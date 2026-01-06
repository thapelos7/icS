

# **ICS: Gate‑Level Digital Logic & IC Simulation Suite**

Gate‑level digital logic simulation suite featuring primitive Boolean gates, IC abstractions, a full IC7447 decoder model, TTL‑74xx devices, and interactive PyQt5, Matplotlib testbenches. Built for EE students and embedded‑systems developers exploring digital logic, IC routing, and simulation design. 

This project models:

*   **Primitive logic gates**
*   **Integrated circuit abstractions**
*   **Full gate‑level IC7447 decoder**
*   **TTL 74xx families**
*   **Interactive GUI testbenches** (PyQt5)
*   **Graphical/non-GUI testbenches** (Matplotlib)

All simulations assume *ideal digital conditions* (Boolean‑only logic, no propagation delay, no debounce, no thermal effects).

***

## 📁 **Project Structure**

```text
src/
│
├── gates/                     # Primitive gates + GUI testbench
│   ├── gate_sim_gui_lv1.ui
│   ├── gates_tb_gui.py
│   └── __init__.py
│
├── IC_7447/                   # Full IC7447 model + GUI visualizer
│   ├── bcd_to_seven_seg_converter.py
│   ├── bcd_to_seven_seg_converter_tb.py
│   ├── Seven_Seg.ui
│   └── __init__.py
│
├── primitives/                # Gate primitives + IC abstraction
│   ├── gates.py
│   ├── integrated_circuit.py
│   └── __init__.py
│
├── ttl_74xx_ics/              # 7400, 7402, 7404, 7408
│   ├── ttl_74xx_ics.py
│   ├── ttl_74xx_ics_tb.py
│   └── __init__.py
│
└── pyproject.toml             # Entry points: run-gates-tb, run-sev_seg-tb
```

***

## 🔧 **Core Components**

### **1. Primitive Boolean Gate Library**

`premitives/ gates.py`

Implements:

*   AND, OR, NOT, NAND, NOR, XNOR, XNAND, BUFFER
*   strict boolean type checking
*   deterministic outputs
*   readable traces for debugging

***

### **2. Gate‑Level GUI Testbench**

`gates/ gates_tb_gui.py`

Features:

*   real‑time PyQt5 gate visualizer
*   truth table highlighting
*   terminal toggles
*   supports all primitive gates

***

### **3. IC Abstraction Layer**

`premitives/ integrated_circuit.py`

Provides:

*   pin‑map creation
*   power or ground validation
*   staged lifecycle: **inputs → process → outputs**
*   consistent embedded‑style structure

***

### **4. IC7447 Gate‑Level Decoder Model**

`IC_7447/ bcd_to_seven_seg_converter.py`

Full reconstruction of IC7447 architecture using:

*   Section A: input conditioning
*   Section B: blanking & control
*   Section C: NAND reductions
*   Section D: pre‑drivers
*   Section E: output combiners

Routing uses named nets (`lineA` to `lineJ`) for accuracy and to prevent frozen logic.

***

### **5. Seven‑Segment GUI Testbench**

`IC_7447/ bcd_to_seven_seg_converter_tb.py`

Displays a common‑anode 7‑segment indicator:

*   LOW = ON (lime)
*   HIGH = OFF (white)

***

### **6. TTL 74xx IC Implementations**

`ttl_74xx_ics/`

Includes:

*   **7400** Quad 2‑input NAND
*   **7402** Quad 2‑input NOR
*   **7404** Hex inverter
*   **7408** Quad 2‑input AND

Plus a Matplotlib-based pin‑state visualizer.

***

## ⚡ **Key Engineering Challenges & Solutions**

### **1. Signal routing through virtual lines**

**Problem:** logic collapsed early (stuck-at states).  
**Fix:** separate gate declaration (`interGates`) from routing (`setUP`) so nets resolve dynamically.

***

### **2. Limited gate terminal expansion**

**Problem:** Some nodes require >2 inputs.  
**Fix:** cascaded pre-gates (`x1_2`, `x3` …`xN`) to expand terminal capacity safely.

***

### **3. Stuck‑at suppression issues**

**Problem:** constructor‑time evaluation froze intermediate nodes.  
**Fix:** enforced staged processing:  
**inputs → setUP → outputs**

***

### **4. Large multi-stage IC segmentation**

**Problem:** IC7447 cannot be truth-table modeled accurately.  
**Fix:** datasheet‑driven sectioned architecture (A–E).

***

### **5. Deterministic ideal digital abstraction**

Assumptions:

*   HIGH = True, LOW = False
*   no debounce
*   no propagation delays
*   no electrical noise

Consistent behavior across all GUIs.

***

## 🚀 **Installation**

```bash
pip install -e .
```

***

## ▶️ **Run Testbenches**

### Gate-level simulator:

```bash
run-gates-tb
```

### Seven‑segment IC7447 visualizer:

```bash
run-sev_seg-tb
```

.
***
