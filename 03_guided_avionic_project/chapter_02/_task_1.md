# Hardware Software Interface (HSI.json) - Guided Tutorial

## Table of Contents
1. [What is HSI?](#what-is-hsi)
2. [HSI Goals and Importance](#hsi-goals-and-importance)
3. [STM32F407 Pin Overview](#stm32f407-pin-overview)
4. [HSI.json Structure](#hsijson-structure)
5. [Field Reference](#field-reference)
6. [Step-by-Step Guide](#step-by-step-guide)
7. [Protocol Examples](#protocol-examples)
8. [Running Validation](#running-validation)
9. [Common Mistakes](#common-mistakes)

---

## What is HSI?

**Hardware Software Interface (HSI)** is a detailed technical document that bridges the gap between **Hardware Design** and **Software Development**. It serves as a definitive reference for how software interacts with the physical hardware (pins, protocols, electrical signals).

### Key Definition:
> HSI.json is a **structured inventory of all microcontroller pins**, their configurations, protocols, voltage levels, and connections to external systems.

### Who Uses It?
- **Firmware Developers**: Know exactly which pins control which functions
- **Hardware Engineers**: Ensure pin assignments match physical schematic
- **System Integrators**: Map signals to external connectors and devices
- **Test Engineers**: Verify connections match requirements
- **Maintenance Personnel**: Understand system configuration long after development

---

## HSI Goals and Importance

### Primary Goals:

1. **Single Source of Truth**
   - One document that everyone references
   - Prevents conflicting pin assignments
   - Eliminates "I didn't know that pin was used" problems

2. **Enable Automated Validation**
   - Scripts can check for duplicate pins
   - Verify voltage levels are compatible
   - Ensure required protocols are properly configured

3. **Facilitate Code Generation**
   - Auto-generate `#define` statements in firmware
   - Create device tree overlays
   - Generate initialization code

4. **Support Requirements Traceability**
   - Each HSI entry can link to SES (System Engineering Specification) requirements
   - Track how requirements are implemented at the hardware level
   - Enable audit trails and compliance verification

5. **Document External Interfaces**
   - Shows which internal pins connect to external connectors
   - Specifies voltage levels and protocols
   - Enables proper interface design and testing

### Real-World Impact:
Without HSI:
- Developer 1 uses PA0 for LED
- Developer 2 uses PA0 for sensor reading
- System fails mysteriously during integration

With HSI:
- Pin conflict detected before code is even written
- Clear documentation for commissioning and maintenance

---

## STM32F407 Pin Overview

The STM32F407 microcontroller features:

### Pin Configuration:
- **LQFP176 package** (176 pins total)
- **9 GPIO ports**: A, B, C, D, E, F, G, H, I
- **Port sizes**: Most ports have 16 pins (P0-P15), H has 2, I has 8
- **Pin voltage**: 3.3V logic levels (5V tolerant on most pins)

### Available Protocols:
- **UART/USART**: Universal async/sync serial communication
- **SPI**: Serial Peripheral Interface for high-speed sensor communication
- **I2C**: Inter-IC, multi-device bus communication
- **ADC**: Analog-Digital Converter for analog sensor inputs
- **GPIO**: General Purpose Input/Output for simple digital signals
- **CAN**: Controller Area Network (automotive/industrial)
- **USB**: Universal Serial Bus
- **Ethernet**: Network communication

### Port Distribution:
```
Port A: PA0-PA15  (16 pins, mostly general purpose)
Port B: PB0-PB15  (16 pins, includes I2C, SPI)
Port C: PC0-PC15  (16 pins, mostly ADC inputs)
Port D: PD0-PD15  (16 pins, GPIO)
Port E: PE0-PE15  (16 pins, GPIO)
Port F: PF0-PF15  (16 pins, GPIO)
Port G: PG0-PG15  (16 pins, GPIO)
Port H: PH0-PH1   (2 pins, special)
Port I: PI0-PI7   (8 pins, GPIO)
```

---

## HSI.json Structure

The HSI.json file is a **JSON array** where each element represents one physical pin configuration:

```json
[
  {
    "pin_id": "PA0",                    // Physical pin identifier
    "pin_number": 23,                   // LQFP176 package pin number
    "port": "A",                        // Port (A-I)
    "alternate_function": "UART4_TX",  // Hardware module
    "direction": "output",              // input / output / open_drain / bidirectional
    "signal_name": "STANDBY_PIN",       // Functional signal name
    "protocol": "UART",                 // Communication protocol
    "voltage_level": "3.3V",            // Electrical voltage
    "pull_configuration": "none",       // Pull-up/pull-down config
    "description": "UART4 Transmitter", // Human-readable description
    "connected_to": "DATA_CONNECTOR_PIN_5",  // External connection
    "external_requirements": "AEME-SYS-0007" // Linked SES requirement
  }
]
```

---

## Field Reference

### Core Fields (Always Required):

#### 1. **pin_id**
- **Format**: `P[A-I][0-9]` (e.g., PA0, PB15, PC3)
- **Purpose**: Unique identifier for the pin
- **Example**: `PA0`, `PD14`, `PI7`

#### 2. **pin_number**
- **Type**: Integer (1-176 for STM32F407)
- **Purpose**: Physical pin location in LQFP176 package
- **Example**: `23`, `88`, `41`
- **Reference**: See STM32F407 datasheet pinout table

#### 3. **port**
- **Valid Values**: A, B, C, D, E, F, G, H, I
- **Purpose**: GPIO port (each port has independent configuration)
- **Example**: `A`, `B`, `C`
- **Constraint**: Must match pin_id letter (PA0 → port A)

#### 4. **direction**
- **Valid Values**:
  - `input`: Receives signals (sensor data, external commands)
  - `output`: Sends signals (LED control, relay switching)
  - `open_drain`: Bidirectional with pull-up (I2C, multi-master buses)
  - `bidirectional`: Simultaneous input and output capability
- **Purpose**: Data flow direction
- **Examples**:
  - Sensor input → `input`
  - LED control → `output`
  - I2C clock/data → `open_drain`

#### 5. **signal_name**
- **Type**: Descriptive string
- **Purpose**: Functional name in the system (not the pin name)
- **Convention**: UPPERCASE_WITH_UNDERSCORES
- **Examples**: 
  - `STANDBY_PIN`
  - `ENGINE_POWER_ON_OFF_PIN`
  - `HMI_LED_RED`

#### 6. **protocol**
- **Valid Values**: UART, SPI, I2C, ADC, GPIO, CAN, USB, Ethernet
- **Purpose**: Communication method used
- **Examples**:
  - UART for serial communication to external systems
  - SPI for fast sensor readout
  - I2C for multi-sensor buses
  - ADC for analog voltage measurement

#### 7. **voltage_level**
- **Type**: Voltage specification
- **Common Values**:
  - `3.3V`: Standard digital signal
  - `0V-3.3V`: Analog signal range
  - `0V-24V`: Industrial signal with voltage divider
  - `0V-24V (via resistive divider to 0V-3.3V)`: Industrial input with conditioning
- **Purpose**: Electrical specification for interface design
- **Critical for**: Hardware integration and safety

#### 8. **description**
- **Type**: Multi-line string
- **Purpose**: Human-readable explanation
- **Include**: Function, purpose, special considerations
- **Example**: 
  ```
  UART2 Transmitter - sends engine power control signal. 
  Must respect 500ms delay between commands. 
  Active high, 3.3V logic.
  ```

### Optional but Recommended Fields:

#### 9. **alternate_function**
- **Type**: String
- **Purpose**: Hardware module designation
- **Examples**: UART4_TX, SPI1_MOSI, I2C1_SCL, ADC123_IN10
- **Use**: Helps firmware developers use correct configurations

#### 10. **pull_configuration**
- **Valid Values**: 
  - `none`: No pull-up or pull-down
  - `pull-up`: Pin pulled to VCC when floating
  - `pull-down`: Pin pulled to GND when floating
  - `external-pullup`: Pull-up resistor on PCB
  - `external-pulldown`: Pull-down resistor on PCB
- **Purpose**: Electrical stability
- **When to use**:
  - UART RX → `pull-up` (bus idle state)
  - SPI MISO → `pull-up` (multi-device safety)
  - GPIO input from open-drain → `pull-up` (bus design)

#### 11. **connected_to**
- **Type**: String
- **Purpose**: What external system this connects to
- **Examples**:
  - `DATA_CONNECTOR_PIN_5`: External connector pin
  - `POWER_CONNECTOR_PIN_3`: Power connector
  - `Internal`: No external connection (e.g., onboard LED)
  - `Sensor_Module_1`: External daughter board

#### 12. **external_requirements**
- **Type**: Requirement ID (from SES.json)
- **Purpose**: Traceability to higher-level requirements
- **Example**: `AEME-SYS-0007` (links to system requirement)
- **Benefit**: Enables requirement tracking and audit trails

---

## Step-by-Step Guide

### Step 1: Gather Hardware Information

**Collect these documents:**
1. STM32F407 Datasheet (pinout table and electrical specs)
2. Hardware schematic (shows physical connections)
3. SES.json file (system requirements)
4. External interface documentation (connectors, signals)

**Key information to find:**
```
For each hardware connection:
- Which STM32 pin is used?
- What LQFP176 pin number is it?
- What is the alternate function (UART, SPI, etc.)?
- What voltage levels are involved?
- What external device/connector is it connected to?
- Which system requirement does it satisfy?
```

### Step 2: Identify All Pin Groups

**Group pins by protocol:**

**UART Pins** (Serial Communication)
- Find all UART1, UART2, UART3, UART4, UART5 instances
- Note TX (output) and RX (input) pins
- Record baud rate and voltage levels

**Example UART Group:**
```
UART2_TX: PA2  (output, 3.3V, sends commands)
UART2_RX: PA3  (input, 3.3V, receives responses)
```

**SPI Pins** (High-Speed Sensor Bus)
- Identify SPI1, SPI2, SPI3 instances
- Find MOSI (Master Out), MISO (Master In), SCK (Clock)
- Find all Chip Select (CS) pins (usually GPIO)

**Example SPI Group:**
```
SPI1_MOSI: PB5  (output)
SPI1_MISO: PB4  (input)
SPI1_SCK:  PB3  (output)
CS_SENSOR1: PE4 (GPIO output, active low)
CS_SENSOR2: PE5 (GPIO output, active low)
```

**I2C Pins** (Multi-Device Bus)
- Locate I2C1, I2C2, I2C3 instances
- SCL (clock) and SDA (data) are always bidirectional
- Note pull-up resistor values from schematic

**Example I2C Group:**
```
I2C1_SCL: PB6  (open_drain, with external pull-up)
I2C1_SDA: PB7  (open_drain, with external pull-up)
```

**ADC Pins** (Analog Inputs)
- Find ADC1, ADC2, ADC3 input channels
- Note voltage range (often 0V-3.3V or 0V-24V with divider)
- Record which sensor each measures

**Example ADC Group:**
```
ANALOG_INPUT_1: PC0  (ADC123_IN10, 0V-24V via divider)
ANALOG_INPUT_2: PC1  (ADC123_IN11, 0V-24V via divider)
```

**GPIO Pins** (Simple Digital I/O)
- Identify remaining GPIO pins
- Note if they're used for LEDs, buttons, relays, etc.

**Example GPIO Group:**
```
HMI_LED_RED:    PD12  (output, active high)
HMI_LED_GREEN:  PD13  (output, active high)
HMI_LED_YELLOW: PD14  (output, active high)
```

### Step 3: Create Initial JSON Structure

Create a new HSI.json file with empty array:

```json
[
]
```

### Step 4: Add Pin Entries

For each identified pin, add an entry following this process:

```python
# For each pin:
1. Get pin_id from schematic (e.g., PA0)
2. Extract port letter (e.g., P → A)
3. Look up LQFP176 pin number from datasheet
4. Determine alternate_function (module that uses this pin)
5. Set direction based on protocol role
6. Assign protocol type
7. Find voltage level from schematic
8. Determine pull configuration
9. Write clear description
10. Link to external connector (if applicable)
11. Find matching SES requirement ID
```

**Example for one UART entry:**

```json
{
  "pin_id": "PA2",
  "pin_number": 25,
  "port": "A",
  "alternate_function": "UART2_TX",
  "direction": "output",
  "signal_name": "ENGINE_POWER_ON_OFF_PIN",
  "protocol": "UART",
  "voltage_level": "3.3V",
  "pull_configuration": "none",
  "description": "UART2 Transmitter - sends engine power control signal to external system",
  "connected_to": "DATA_CONNECTOR_PIN_7",
  "external_requirements": "AEME-SYS-0008"
}
```

### Step 5: Validate and Iterate

Run validation script after adding pins:

```bash
python validate_hsi.py HSI.json
```

Fix any errors reported:
- Duplicate pin IDs
- Invalid voltage levels
- Protocol inconsistencies
- Pin number out of range

---

## Protocol Examples

### 1. UART Protocol (Serial Communication)

**What it is:**
- Async serial communication (one at a time, not simultaneous)
- Used for: External control signals, status reports, configuration
- Speed: Up to 115200 baud (or higher)
- Distance: Short range (< 10 meters typically)

**Pin Configuration:**

```json
[
  {
    "pin_id": "PA2",
    "pin_number": 25,
    "port": "A",
    "alternate_function": "UART2_TX",
    "direction": "output",
    "signal_name": "ENGINE_POWER_ON_OFF_PIN",
    "protocol": "UART",
    "voltage_level": "3.3V",
    "pull_configuration": "none",
    "description": "UART2 Transmitter - sends power control commands (active high, 3.3V)"
  },
  {
    "pin_id": "PA3",
    "pin_number": 26,
    "port": "A",
    "alternate_function": "UART2_RX",
    "direction": "input",
    "signal_name": "ENGINE_STATUS_FEEDBACK",
    "protocol": "UART",
    "voltage_level": "3.3V",
    "pull_configuration": "pull-up",
    "description": "UART2 Receiver - receives engine status acknowledgments"
  }
]
```

**When to use UART:**
- ✓ Simple command/response with external systems
- ✓ Low bandwidth requirements
- ✗ Not suitable for multiple simultaneous devices

---

### 2. SPI Protocol (High-Speed Serial Bus)

**What it is:**
- Synchronous full-duplex communication
- Used for: Fast sensors, memory chips, displays
- Speed: 1-100+ Mbps
- Distance: Short range (PCB level)

**Pin Configuration:**

```json
[
  {
    "pin_id": "PB5",
    "pin_number": 89,
    "port": "B",
    "alternate_function": "SPI1_MOSI",
    "direction": "output",
    "signal_name": "SPI_DATA_OUT",
    "protocol": "SPI",
    "voltage_level": "3.3V",
    "pull_configuration": "none",
    "description": "SPI Master Out Slave In - data from STM32 to sensors"
  },
  {
    "pin_id": "PB4",
    "pin_number": 88,
    "port": "B",
    "alternate_function": "SPI1_MISO",
    "direction": "input",
    "signal_name": "SPI_DATA_IN",
    "protocol": "SPI",
    "voltage_level": "3.3V",
    "pull_configuration": "pull-up",
    "description": "SPI Master In Slave Out - data from sensors to STM32"
  },
  {
    "pin_id": "PB3",
    "pin_number": 87,
    "port": "B",
    "alternate_function": "SPI1_SCK",
    "direction": "output",
    "signal_name": "SPI_CLOCK",
    "protocol": "SPI",
    "voltage_level": "3.3V",
    "pull_configuration": "none",
    "description": "SPI Serial Clock - synchronizes MOSI/MISO data transfer"
  },
  {
    "pin_id": "PE4",
    "pin_number": 41,
    "port": "E",
    "alternate_function": "GPIO",
    "direction": "output",
    "signal_name": "SPI_CS_SENSOR1",
    "protocol": "GPIO",
    "voltage_level": "3.3V",
    "pull_configuration": "pull-up",
    "description": "SPI Chip Select for Sensor 1 - active low (pulled low to enable sensor)"
  }
]
```

**Why this structure:**
- MOSI/MISO/SCK are shared by all SPI devices
- Each device gets its own Chip Select (CS) pin
- Pull-up on MISO protects against contention
- CS pins use GPIO for flexible multi-device support

**When to use SPI:**
- ✓ High speed sensor data (IMU, pressure sensors)
- ✓ Multiple sensors (daisy-chain or individual CS)
- ✗ Not suitable for long distances (signal degradation)

---

### 3. I2C Protocol (Multi-Master Bus)

**What it is:**
- Synchronous open-drain bus
- Used for: Temperature sensors, EEPROMs, power management ICs
- Speed: 100 kHz or 400 kHz (standard or fast)
- Distance: ~1 meter on PCB

**Pin Configuration:**

```json
[
  {
    "pin_id": "PB6",
    "pin_number": 90,
    "port": "B",
    "alternate_function": "I2C1_SCL",
    "direction": "open_drain",
    "signal_name": "I2C_CLOCK",
    "protocol": "I2C",
    "voltage_level": "3.3V",
    "pull_configuration": "external-pullup",
    "description": "I2C Serial Clock Line - open-drain with external 4.7k pull-up to VCC"
  },
  {
    "pin_id": "PB7",
    "pin_number": 91,
    "port": "B",
    "alternate_function": "I2C1_SDA",
    "direction": "open_drain",
    "signal_name": "I2C_DATA",
    "protocol": "I2C",
    "voltage_level": "3.3V",
    "pull_configuration": "external-pullup",
    "description": "I2C Serial Data Line - open-drain with external 4.7k pull-up to VCC. Multiple devices can pull this line low simultaneously."
  }
]
```

**Key characteristics:**
- Always `open_drain` direction (pulls to ground, released by pull-up)
- Always `external-pullup` (resistors on PCB, typically 4.7k)
- Single I2C bus can support 127+ devices
- Each device has unique 7-bit address

**When to use I2C:**
- ✓ Multiple sensors on same bus (temp, humidity, pressure)
- ✓ Moderate speed (100-400 kHz)
- ✓ Simpler wiring (only 2 lines for any number of devices)
- ✗ Not suitable for high-speed data streams

---

### 4. ADC Protocol (Analog Input)

**What it is:**
- Analog-to-Digital Converter
- Used for: Sensor inputs (temperature, pressure, current)
- Resolution: 12-bit (4096 levels) typical
- Sample rate: < 1 MHz typical

**Pin Configuration:**

```json
[
  {
    "pin_id": "PC0",
    "pin_number": 3,
    "port": "C",
    "alternate_function": "ADC123_IN10",
    "direction": "input",
    "signal_name": "ANALOG_INPUT_1",
    "protocol": "ADC",
    "voltage_level": "0V-24V (via resistive divider to 0V-3.3V)",
    "pull_configuration": "none",
    "description": "Analog input for first sensor measurement. External circuit converts 0-24V industrial signal to 0-3.3V via resistive divider (R1=20k, R2=4.7k). Measures engine temperature."
  },
  {
    "pin_id": "PC1",
    "pin_number": 4,
    "port": "C",
    "alternate_function": "ADC123_IN11",
    "direction": "input",
    "signal_name": "ANALOG_INPUT_2",
    "protocol": "ADC",
    "voltage_level": "0V-24V (via resistive divider to 0V-3.3V)",
    "pull_configuration": "none",
    "description": "Analog input for second sensor measurement (pressure). Same divider circuit as ANALOG_INPUT_1."
  }
]
```

**Conversion formula (example):**
```
Raw_ADC = ADC_Value (0-4095)
Voltage = (Raw_ADC / 4095) * 3.3V
Scaled = Voltage * ((R1 + R2) / R2)  // Back to 0-24V
Temperature = (Scaled - 0) * 100     // Application specific
```

**When to use ADC:**
- ✓ Sensor inputs (continuous measurement)
- ✓ Voltage monitoring
- ✗ Not suitable for digital signals
- ✗ Slow compared to UART/SPI (1000x slower)

---

### 5. GPIO Protocol (Simple Digital I/O)

**What it is:**
- Simple digital input or output
- Used for: LED control, button input, relay switching, simple on/off signals
- Speed: Microsecond level
- Power: Typical 20mA per pin

**Output GPIO (LED Control):**

```json
[
  {
    "pin_id": "PD12",
    "pin_number": 67,
    "port": "D",
    "alternate_function": "GPIO",
    "direction": "output",
    "signal_name": "HMI_LED_RED",
    "protocol": "GPIO",
    "voltage_level": "3.3V",
    "pull_configuration": "none",
    "description": "Red LED control line. High (3.3V) = LED on, Low (0V) = LED off. Current limit via 470Ω resistor to anode."
  }
]
```

**Input GPIO (Button/Signal Detection):**

```json
[
  {
    "pin_id": "PA4",
    "pin_number": 14,
    "port": "A",
    "alternate_function": "GPIO",
    "direction": "input",
    "signal_name": "ERROR_DETECTION_SENSOR",
    "protocol": "GPIO",
    "voltage_level": "3.3V",
    "pull_configuration": "pull-down",
    "description": "External error signal input. High (3.3V) indicates error condition. Pull-down prevents floating when not connected."
  }
]
```

**When to use GPIO:**
- ✓ Simple on/off control (LEDs, relays)
- ✓ Simple digital inputs (buttons, level detection)
- ✓ Highly flexible, no special protocol
- ✗ Inefficient for complex data exchange
- ✗ Only 1 bit per pin

---

## Running Validation

### Prerequisites:
```bash
# Python 3.6+
python --version
# Python 3.x.x
```

### Running the Validation Script:

```bash
# From the project directory
python validate_hsi.py HSI.json

# Or with full path
python /path/to/validate_hsi.py /path/to/HSI.json
```

### Example Output (All Pass):

```
======================================================================
HSI.json SANITY CHECK
======================================================================
✓ JSON syntax valid

✅ ALL CHECKS PASSED!
----------------------------------------------------------------------

Total pins configured: 17
Errors: 0
Warnings: 0
======================================================================
```

### Example Output (With Errors):

```
======================================================================
HSI.json SANITY CHECK
======================================================================
✓ JSON syntax valid

❌ ERRORS FOUND:
----------------------------------------------------------------------
1. Pin PA0: Invalid protocol 'USART'. Must be one of: ADC, CAN, GPIO, I2C, SPI, UART, USB, Ethernet
2. Pin PB5 and PA0: pin_number 25 assigned twice
3. Pin duplicate signal name 'LED_RED' at pin PD13

⚠️  WARNINGS:
----------------------------------------------------------------------
1. Pin PC0: Uncommon voltage level '5V'. Common values: 0V-3.3V, 0V-5V, ...

Total pins configured: 17
Errors: 3
Warnings: 1
======================================================================
```

### What the Validator Checks:

1. ✅ **JSON Syntax**: Valid JSON format
2. ✅ **Required Fields**: All mandatory fields present
3. ✅ **Protocol Validity**: Protocol in approved list
4. ✅ **Direction Validity**: Direction values correct
5. ✅ **Voltage Levels**: Voltage values reasonable
6. ✅ **Pull Configuration**: Pull values valid
7. ✅ **STM32 Pin Validity**: Pin numbers within range
8. ✅ **Duplicate Detection**: No duplicate pin IDs or numbers
9. ✅ **Pin ID Format**: Format matches P[A-I][0-9]
10. ✅ **Signal Names**: No duplicate signal names
11. ✅ **Protocol Consistency**: I2C uses open_drain, etc.

---

## Common Mistakes

### ❌ Mistake 1: Wrong Pin Number

```json
{
  "pin_id": "PA0",
  "pin_number": 1000,  // INVALID - STM32F407 only has 176 pins!
  "port": "A",
  ...
}
```

**Fix:**
```json
{
  "pin_id": "PA0",
  "pin_number": 23,  // Check STM32F407 datasheet pinout table
  "port": "A",
  ...
}
```

### ❌ Mistake 2: Mismatched pin_id and Port

```json
{
  "pin_id": "PA5",  // Says port A, pin 5
  "port": "B",      // But port is B!
  ...
}
```

**Fix:**
```json
{
  "pin_id": "PB5",  // Must match
  "port": "B",
  ...
}
```

### ❌ Mistake 3: Wrong Direction for I2C

```json
{
  "signal_name": "I2C_CLOCK",
  "protocol": "I2C",
  "direction": "output",  // WRONG - I2C is open-drain!
  ...
}
```

**Fix:**
```json
{
  "signal_name": "I2C_CLOCK",
  "protocol": "I2C",
  "direction": "open_drain",  // Correct!
  "pull_configuration": "external-pullup",
  ...
}
```

### ❌ Mistake 4: Duplicate Pin Usage

```json
[
  {
    "pin_id": "PA5",
    "signal_name": "LED_RED",
    ...
  },
  {
    "pin_id": "PA5",  // SAME PIN!
    "signal_name": "BUTTON_INPUT",
    ...
  }
]
```

**Fix:**
```json
[
  {
    "pin_id": "PA5",
    "signal_name": "LED_RED",
    ...
  },
  {
    "pin_id": "PA6",  // Different pin
    "signal_name": "BUTTON_INPUT",
    ...
  }
]
```

### ❌ Mistake 5: Invalid Voltage Level

```json
{
  "voltage_level": "12V",  // STM32F407 is 3.3V logic!
  ...
}
```

**Fix:**
```json
{
  "voltage_level": "3.3V",
  // OR with external conversion:
  "voltage_level": "0V-24V (via resistive divider to 0V-3.3V)",
  ...
}
```

### ❌ Mistake 6: Missing Pull-up for UART RX

```json
{
  "signal_name": "UART_RX",
  "direction": "input",
  "pull_configuration": "none",  // RISKY - line may float
  ...
}
```

**Better:**
```json
{
  "signal_name": "UART_RX",
  "direction": "input",
  "pull_configuration": "pull-up",  // Idle state is high
  ...
}
```

### ❌ Mistake 7: Missing External Requirement Link

```json
{
  "pin_id": "PA0",
  "signal_name": "STANDBY_PIN",
  "external_requirements": "",  // Empty - no traceability!
  ...
}
```

**Fix:**
```json
{
  "pin_id": "PA0",
  "signal_name": "STANDBY_PIN",
  "external_requirements": "AEME-SYS-0007",  // Links to requirement
  ...
}
```

---

## Quick Reference Checklist

Use this checklist when creating HSI.json:

- [ ] All pins from hardware schematic included
- [ ] pin_id format correct (PA0, PB15, etc.)
- [ ] pin_number matches LQFP176 package pinout
- [ ] port matches first letter of pin_id
- [ ] direction field filled correctly
- [ ] signal_name descriptive and unique
- [ ] protocol is valid for pin usage
- [ ] voltage_level matches electrical spec
- [ ] pull_configuration set appropriately
- [ ] description clear and actionable
- [ ] connected_to shows external connection (or "Internal")
- [ ] external_requirements linked to SES requirement ID
- [ ] Run validation script returns no errors
- [ ] Reviewed by hardware team
- [ ] Shared with firmware development team

---

## Next Steps

1. **Modify HSI.json** with your specific STM32F407 pin configuration
2. **Run Validation**: `python validate_hsi.py HSI.json`
3. **Fix Errors**: Address any validation errors
4. **Review**: Have hardware engineer verify pin assignments
5. **Use in Firmware**: Reference when writing GPIO configuration code
6. **Document**: Keep this file in version control

---

## Additional Resources

- **STM32F407 Datasheet**: Pin Configuration and Electrical Specifications
- **Hardware Schematic**: Shows physical pin connections
- **SES.json**: System engineering specifications this HSI implements
- **Device Initialization Files**: HAL_GPIO_Init(), HAL_UART_Init(), etc.

