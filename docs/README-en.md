# FOC-Driver-Board

Three-Phase FOC BLDC Motor Driver Board — Pure Power Stage Design (MCU-Exclusive)

---

## 🎯 Project Overview

This project is a **Three-Phase FOC (Field-Oriented Control) BLDC Motor Driver Board** designed for driving brushless DC motors. The project adopts **AI-assisted hardware design methodology**, utilizing tools like Claude Code and Cursor for circuit analysis, parameter calculation, and design documentation.

### Core Specifications

| Parameter | Specification |
|-----------|---------------|
| **Product Type** | Three-Phase FOC BLDC Motor Driver (Power Stage Only) |
| **Drive Architecture** | EG2133 Three-Phase Half-Bridge Driver + 6×NCE6080K MOSFET |
| **Current Sensing** | RS624 Quad Op-Amp Differential Amplifier (3-Phase + Bus) |
| **Motor Rated Voltage** | 24V (Support 12-48V) |
| **Peak Current** | ≤80A |
| **Control Interface** | 6-CH PWM Input (3.3V/5V Compatible) |
| **Sampling Output** | 4-CH Current Output (I_U/I_V/I_W/I_BUS) |
| **Over-Current Protection** | Software Protection (MCU ADC Read) |

---

## 🤖 AI-Assisted Hardware Design Workflow

This project demonstrates a complete **AI-assisted embedded hardware design** workflow:

### Design Toolchain

| Tool | Purpose |
|------|---------|
| **Claude Code** | Circuit topology analysis, parameter calculation, documentation |
| **Cursor** | Schematic review, PCB layout suggestions, code generation |
| **LCEDA (EasyEDA)** | Schematic capture, PCB layout |
| **KiCad** | Schematic capture (alternative) |
| **Python** | Parameter calculation scripts, BOM management |

### AI Workflow

```
Requirements → Component Selection → Schematic Design → Parameter Calculation → PCB → Validation
    │                │                     │                  │                 │             │
    ▼                ▼                     ▼                  ▼                 ▼             ▼
Claude          Claude               Cursor              Claude             Cursor          Claude
Code            Code                  AI                  Code                AI             Code
(Text Analysis) (Selection)         (Layout)            (Calculation)       (DRC)          (Test Plan)
```

### Specific AI Use Cases

#### 1. Circuit Topology Analysis
```
Using Claude Code for FOC drive architecture analysis:
- Three-phase half-bridge driver circuit design
- Bootstrap circuit operation principle
- Current sensing scheme comparison (low-side vs series)
```

#### 2. Parameter Calculation Automation
```
Using Claude Code for parameter calculation:
- Bootstrap capacitor selection: Cboot = Qg × N / ΔV
- MOSFET power estimation: P = I² × Rds(on)
- Current sense amplifier gain calculation
- Thermal management analysis
```

#### 3. Design Documentation Generation
```
Using Claude Code for design documentation:
- Requirements specification
- Schematic netlist
- BOM (Bill of Materials)
- Validation test plan
```

#### 4. PCB Layout Review
```
Using Cursor AI for PCB review:
- Trace width verification (current density)
- Decoupling capacitor placement
- Thermal management evaluation
- Signal integrity analysis
```

---

## 📂 Project Structure

```
FOC-Driver-Board/
├── README.md              # Main documentation
├── LICENSE                # MIT License
├── docs/
│   ├── README-en.md       # English documentation
│   ├── 01-requirements.md # Requirements specification
│   ├── 02-constraints.md  # Design constraints
│   ├── 03-solution.md     # Complete solution
│   ├── 04-schematics.md   # Schematic netlist
│   ├── 05-validation.md   # Validation plan
│   └── bom.md             # Bill of Materials
└── scripts/
    └── calc.py            # Parameter calculation scripts
```

---

## 🔧 Core Technical Solution

### System Block Diagram

```
                    ┌─────────────────────────────────────────────┐
                    │              FOC Driver Board                │
                    │                                              │
PWM_H1 ──────┐      │  ┌─────────┐    ┌───────┐    ┌──────────┐   │
PWM_H2 ──────┤      │  │         │HO1 │ Q1    │    │          │   │─── U Output
PWM_H3 ──────┤      │  │         │───>│NCE6080│──> │          │   │
PWM_L1 ──────┼──────│  │ EG2133  │LO1 │ Q2    │    │ 3-Phase  │   │─── V Output
PWM_L2 ──────┤      │  │ 3-Ph    │───>│NCE6080│    │ Inverter │   │
PWM_L3 ──────┤      │  │ Half-   │    │       │    │          │   │
             │      │  │ Bridge  │HO2 │ Q3    │    │          │   │─── W Output
VCC_12V ─────┤      │  │ Driver  │───>│NCE6080│    │          │   │
GND ─────────┤      │  │         │LO2 │ Q4    │    │          │   │
             │      │  │         │───>│NCE6080│    │          │   │
VMOTOR(24V) ─┤      │  │         │HO3 │ Q5    │    │          │   │
GND_PWR ─────┤      │  │         │───>│NCE6080│    │          │   │
             │      │  │         │LO3 │ Q6    │    │          │   │
VCC_5V ──────┤      │  │         │───>│NCE6080│    │          │   │
             │      │  └─────────┘    └───────┘    └──────────┘   │
I_U ─────────┤<────│                                              │
I_V ─────────┤<────│  ┌─────────────────┐                        │
I_W ─────────┤<────│  │     RS624        │<── Rs_U/Rs_V/Rs_W     │
I_BUS ───────┤<────│  │  Op-A: U Current │──> I_U                 │
             │      │  │  Op-B: V Current │──> I_V                 │
             │      │  │  Op-C: W Current │──> I_W                 │
             │      │  │  Op-D: Bus Current──> I_BUS               │
             │      │  └─────────────────┘                        │
             │      │                                              │
             │      └─────────────────────────────────────────────┘
```

### Key Components

| Component | Part Number | Key Parameters | Package | Application |
|-----------|-------------|----------------|---------|-------------|
| 3-Ph Half-Bridge Driver | EG2133 | 3CH Independent, VCC 4.5-20V, IO +1.2A/-1.4A | TSSOP20 | Gate Drive |
| N-MOSFET | NCE6080K | 60V/80A, Rds(on) <8.5mΩ@VGS=10V | TO-252-2L | Power Switch |
| Quad Op-Amp | RS624 | 7MHz GBP, Rail-to-Rail, 2.5-5.5V Supply | SOIC-14 | Current Sense |

### Current Sensing Scheme

**Low-Side Shunt + Differential Amplifier** approach:

| Channel | Op-Amp | Gain | Range | Mid-Point Voltage |
|---------|--------|------|-------|-------------------|
| I_U / I_V / I_W | RS624 A/B/C | 10× | ±20A | 2.5V |
| I_BUS | RS624 D | 5× | 0~80A | 2.5V |

---

## 📊 AI Usage Statistics

> Actual AI-assisted design usage data for this project:

| Metric | Value |
|--------|-------|
| **Claude Code Sessions** | 15+ |
| **Cursor AI Queries** | 20+ |
| **Parameter Scripts** | 3 |
| **Design Documents** | 30+ pages |
| **Estimated Token Consumption** | 5M+ Tokens |

---

## 📝 License

MIT License - See [LICENSE](./LICENSE)
