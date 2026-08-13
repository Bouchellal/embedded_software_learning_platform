# V Cycle and Requirement Engineering Training

## Welcome to the Industry

Hello there, and welcome to our Nameless Company. It is a pleasure to have young minds joining us.

In the industry, when we develop an industrial equipment, we do not start by immediately opening SolidWorks, creating a PCB, or writing the first line of embedded code. In reality, a very large part of our work is spent on planning, documenting, and designing. In many projects, about 80% of the effort goes into preparation, structure, and organization, while only about 20% is spent on the technical work that students often imagine is the main activity.

That means that working on a CAD file, a PCB layout, or a blinking LED embedded program is only a part of the story. The real challenge is to make sure the system is well defined before we build it.

If we do the opposite, if we jump directly into implementation without proper planning, we are very likely to create bad-quality software and hardware, and we will spend much more time fixing problems later, literal **debt**. In engineering, this is a guaranteed path to delays, rework, and costly mistakes.

## A First Important Lesson

Before we write code or design hardware, we must ask:

- What exactly must the system do?
- What are the constraints?
- What could go wrong?
- How will we verify that the solution is correct?

This is where requirement engineering becomes essential. Good requirements are the foundation of good engineering.

## Agile vs V Cycle

Now let us talk about two very different ways of working.

### Agile

Agile is mainly used in pure software development. It is a flexible approach where teams can iterate quickly, learn from feedback, and change direction relatively fast. An iteration can take **1 to 3 days**. If a software team realizes that a feature should be redesigned, they can often adjust the **next morning** or next iteration without too much trouble.

This is why Agile works very well for software-only products.

### V Cycle

The V Cycle, on the other hand, is a more structured and disciplined approach. It is especially important when the product is not only software, but also includes hardware, PCB design, mechanical parts, and embedded systems.

Why is this important?

Because in these systems, changing a PCB or redesigning a mechanical part is not as simple as changing a few lines of code. A PCB redesign may require new components, new layouts, more testing, and more validation. A mechanical modification can delay the whole project. That is why we need a method that forces us to think carefully before manufacturing or implementation begins.

In other words:

- Agile is often better for fast-moving software projects.
- The V Cycle is often better for systems where hardware and software are tightly connected and changes are expensive.

## What is the V Cycle?

The V Cycle is a model that shows the relationship between development and verification.

It is called a V because the activities on the left side of the model move from general to more detailed design, and the activities on the right side verify and validate the solution.

![V-cycle](../../.images/03_guided_avionic_project/v_cycle.jpg)

### Left Side of the V: Development Phases

1. Specification
   - Understand the needs.
   - Define the requirements clearly.

2. High-Level Design
   - Define the overall architecture.
   - Decide how the system will be organized.

3. Low-Level Design
   - Define detailed components and internal behavior.
   - Specify how each part will work.

4. Implementation
   - Build the actual software and hardware.
   - Create the code, PCB, and mechanical realization.

### Right Side of the V: Integration, Verification and Validation

After implementation, we move to the verification and validation phase of the V Cycle. This is where we confirm that the product is correct, safe, and aligned with the initial requirements.

1. Integration
   - We combine the different parts of the system together.
   - We check that software, hardware, and interfaces work correctly as a whole.

2. Verification
   - We verify that each element and each subsystem behaves as expected.
   - This includes checking requirements, reviewing design choices, and performing tests.

3. Validation
   - We validate that the final product really satisfies the user's and customer's needs.
   - This is the step where we ask: "Did we build the right system?"

In some engineering teams, a unit test is also added between the implementation phase and the integration phase. A unit test is a small test that checks one specific function, module, or component in isolation. For example, in software, we can test a function that calculates a temperature threshold to ensure it returns the correct value for different inputs. It helps detect errors early, before the full system is assembled.

For now, we do not use unit testing in this training, because our focus is first on understanding the overall V Cycle and the importance of requirements, design, and integration.

The goal is to confirm that the final product satisfies the original requirements and is ready for real use.

## Why the V Cycle Matters

The V Cycle matters because it helps us avoid expensive mistakes. It gives us a structured way to move from requirements to a final verified product.

It also reminds us that verification should not happen only at the end. In a good engineering process, we think about testing and validation from the beginning.

## How Long Does One V Cycle Take?

The time required for one V Cycle depends on the complexity of the system.

For a small subsystem, one V Cycle may take a short time. For a larger embedded product, it may take weeks or even months. In many industrial projects, teams may complete one V Cycle, then refine the design and start another one. In some cases, a project may require two or even three V Cycles before the product is mature enough for production.

This is normal.

The important point is that each cycle helps improve quality, reduce risk, and make the final product more reliable.

## Final Reflection

Before we continue, think about this:

- What is more expensive: discovering a mistake early or discovering it late?
- Why is planning important in embedded systems?
- Why can a small change in hardware cause a large delay in a project?

The answer is simple: good engineering is not only about building something. It is about building the right thing, in the right way, and with enough confidence that it will work.

That is the real purpose of requirement engineering and the V Cycle.

## Understanding Systems, Subsystems, and Units

In engineering, we often talk about systems, subsystems, and units. For us, an equipment is considered a system.

A system is a complete product that performs a function. It is made of different parts that work together to achieve one goal.

A system of systems is a larger set of connected systems that interact with each other. For example, in an aircraft or industrial machine, one subsystem may control power, another may manage communication, and another may handle sensing or actuation.

A subsystem is a smaller part of the overall system. It has its own role, but it also depends on the rest of the system to work correctly.

A unit is an even smaller element, such as a specific electronic component, a software module, or a mechanical part.

For our purpose, an equipment is considered a system because it contains several domains working together:

- Hardware, such as PCBs, connectors, harnesses, sensors, and power circuits
- Mechanical parts, such as the case, brackets, screws, covers, and mounting structures
- Software, such as firmware, binaries, configuration files, embedded control logic, communication routines, and user interfaces

![System and units](../../.images/03_guided_avionic_project/system_and_unit.jpg)

These three domains are not independent. They must work together correctly.

## Interfaces Between Domains

A very important idea in engineering is that interfaces exist between the different parts of the system. If these interfaces are not well defined, the system can fail even if each part seems correct on its own.

### Hardware-Software Interface

The hardware-software interface defines how the software interacts with the hardware. This is essential in embedded systems.

Examples of hardware-software interfaces include:

1. The pins used on the microcontroller or processor
2. The GPIO configuration and signal direction
3. The communication protocols, such as SPI, I2C, UART, or CAN
4. The voltage levels used by the electronic components
5. The clock frequency and timing requirements
6. The interrupt lines and event triggers
7. The analog input ranges and sampling rates
8. The power supply constraints and current limits
9. The reset and startup behavior of the hardware
10. The sensor and actuator connection mapping

### Mechanical-Hardware Interface

The mechanical-hardware interface defines how the hardware is physically mounted and connected to the mechanical structure.

Examples of mechanical-hardware interfaces include:

1. The locations where screws and fasteners are placed
2. The way the PCB is fixed inside the case
3. The grounding path to the metallic case
4. The placement and attachment of connectors and LEDs
5. The clearance between components and the enclosure
6. The routing of cables and harnesses
7. The vibration and shock constraints of the assembly
8. The thermal contact between components and the mechanical frame
9. The positioning of antennas, displays, or switches
10. The mechanical protection of sensitive electronic parts

Understanding these interfaces is essential because a good system is not only made of good parts. It is made of parts that fit together correctly at the level of function, structure, and communication.


# Full V Cycle of the System and Units with inputs and output documents

Here is the full V Cycle for the system an units, the X-axis represents the time axis.

As you can see, the system V cycle is the first to starts. Then comes in parallel the hardware and mechanical's V cycles. Last comes the software's cycle.

Yet, all engineer have to collaborate on early technical question that overlaps between system level, hardware, mechanical and software too.

![Full V Cycle Simple](../../.images/03_guided_avionic_project/Full-V-Cycle-No-Traceability-No-Inter-Unit.svg)

## List of documents

First, let us explain the documents that are on the left side of each V cycle. These are the documents used for planning and designing before implementation begins.

<details>
  <summary>System documents</summary>

  ### System Documentation Cycle

  #### Client Requirements
  - Scope: capture what the customer wants the system to do, the business goals, constraints, and success criteria.
  - Common traps:
    - Writing implementation details instead of needs.
    - Leaving requirements vague or unmeasurable.
    - Missing non-functional rules such as safety, reliability, or maintainability.
  - Good tips:
    - Use simple, user-focused language.
    - Make each requirement testable and measurable.
    - Separate must-have items from optional or future ideas.

  #### System Specification
  - Scope: translate client requirements into a structured description of the system, its interfaces, and its expected behavior.
  - Common traps:
    - Mixing high-level system goals with low-level design decisions.
    - Omitting important interfaces between hardware, software, and mechanics.
    - Not tracking which requirement each specification line supports.
  - Good tips:
    - Keep the specification organized by system functions and interfaces.
    - Include clear acceptance criteria for each part.
    - Review the specification with hardware, software, and mechanical stakeholders.

  #### Functional Diagram
  - Scope: show the system’s main functions and how they connect, without describing the exact components or implementation.
  - Common traps:
    - Turning the diagram into a wiring or hardware layout.
    - Using too many detailed elements that hide the big picture.
    - Not showing the data or signal flow clearly.
  - Good tips:
    - Focus on functions and data paths rather than physical parts.
    - Use consistent symbols and labels.
    - Keep it readable for non-specialists.

  #### Use Case Diagram
  - Scope: describe how users or external systems interact with the system, and what the system must do in each scenario.
  - Common traps:
    - Missing important actors or use cases.
    - Writing use cases as internal design steps instead of user goals.
    - Forgetting error cases, maintenance, or abnormal situations.
  - Good tips:
    - Start with the main user goals and add secondary interactions later.
    - Label each use case with a concise action phrase.
    - Link use cases back to requirements when possible.

  #### State Diagram
  - Scope: define the system or subsystem states and the transitions that occur based on events, inputs, or conditions.
  - Common traps:
    - Creating too many states for the same behavior.
    - Ignoring what happens on invalid or unexpected inputs.
    - Mixing state transitions with implementation details.
  - Good tips:
    - Keep states meaningful and distinct.
    - Show both normal and error transitions.
    - Use it for behavior that depends on mode, sequence, or lifecycle.

  #### Sequence Diagram
  - Scope: describe the order of interactions between system elements over time for a specific scenario.
  - Common traps:
    - Drawing a sequence diagram for every small detail instead of the important flows.
    - Including implementation details like exact function names or variable values.
    - Forgetting to show timing constraints or delays when they matter.
  - Good tips:
    - Use sequence diagrams for complex protocols, startup flows, or use case execution.
    - Keep each diagram focused on one scenario.
    - Label messages with the type of data or command being exchanged.

  #### Block Diagram
  - Scope: show the main physical or logical blocks of the system and their major connections.
  - Common traps:
    - Confusing block diagrams with detailed circuit diagrams.
    - Drawing too many blocks so the diagram becomes cluttered.
    - Not identifying the boundaries between hardware, software, and mechanics.
  - Good tips:
    - Use block diagrams to communicate the architecture at a glance.
    - Clearly separate blocks by domain or subsystem.
    - Add labels for the main interfaces and signals.

</details>

<details>
  <summary>Hardware documents</summary>

  #### Hardware Specification
  - Scope: define the hardware requirements for the system, including electrical performance, power, sensors, actuators, and physical form factors.
  - Common traps:
    - Describing how the hardware should be built instead of what it must achieve.
    - Omitting the electrical environment, EMI/EMC, and thermal constraints.
    - Not linking hardware requirements back to system-level requirements.
  - Good tips:
    - Include clear values for voltage, current, frequency, and signal levels.
    - Specify interfaces, connector types, and physical dimensions.
    - Keep it technology-agnostic until the design phase.

  #### Hardware Mechanical Interface Specification
  - Scope: define how the electronic hardware fits into the mechanical design, including mounting, enclosure clearances, and structural constraints.
  - Common traps:
    - Leaving mechanical mounting and fastener details undefined.
    - Assuming the PCB can fit anywhere inside the case without verifying sizes.
    - Forgetting to define grounding, shielding, and thermal paths.
  - Good tips:
    - Specify connector locations, mounting hole positions, and board envelope.
    - Define required clearance to moving parts or thermal elements.
    - Describe mechanical loads, vibration, and sealing requirements if relevant.

  #### Hardware Software Interface Specification
  - Scope: define the exact connection between the hardware and the firmware/software, including pins, signals, protocols, and timing.
  - Common traps:
    - Using generic labels like "signal 1" instead of real names.
    - Leaving timing or voltage levels unspecified.
    - Not identifying which subsystem owns each interface.
  - Good tips:
    - List pin assignments, communication buses, and expected signal behavior.
    - Include timing diagrams or protocol notes for critical interfaces.
    - Keep the document up to date with both the hardware and firmware teams.

  #### Block Diagram
  - Scope: show the main physical hardware blocks and their interconnections, without going into detailed component-level design.
  - Common traps:
    - Treating the block diagram as a schematic or routing guide.
    - Including too many low-level components that make the diagram noisy.
    - Not showing how major blocks connect to power and external interfaces.
  - Good tips:
    - Use it to communicate the overall hardware architecture.
    - Keep blocks at the level of boards, power converters, sensors, and interfaces.
    - Label major connections clearly, such as power, data, and ground.

  #### Schematics
  - Scope: provide the detailed electrical design of the hardware, showing components, nets, and connections.
  - Common traps:
    - Creating schematics with unclear net names or missing references.
    - Not verifying the schematic against the actual PCB layout.
    - Leaving power rails, decoupling, or protection components undocumented.
  - Good tips:
    - Use readable annotation and standardized symbols.
    - Verify that schematics match the selected components and footprints.
    - Include important notes on power sequencing and startup behavior.

  #### PCB Routing
  - Scope: document the routing rules and layout decisions for the printed circuit board, including trace widths, clearances, and layer usage.
  - Common traps:
    - Treating PCB routing as a purely graphical exercise without documented rules.
    - Ignoring signal integrity, return paths, and high-speed routing constraints.
    - Not documenting the purpose of specific trace layouts such as differential pairs.
  - Good tips:
    - Define stack-up, impedance needs, and layer assignments.
    - Document special routing requirements for sensitive or high-current nets.
    - Review the routed board with electrical and mechanical teams before finalizing.

</details>

<details>
  <summary>Software documents</summary>

  #### Software Specification
  - Scope: define the software requirements and behavior, based on the system specification and hardware-software interfaces.
  - Common traps:
    - Writing software design details instead of requirements.
    - Not accounting for hardware constraints such as pin usage, timing, and resource limits.
    - Leaving out error handling, startup, and shutdown behavior.
  - Good tips:
    - Make the software requirements clear, measurable, and linked to the system needs.
    - Include required interfaces, inputs/outputs, and expected responses.
    - Review the spec with hardware and system engineers to ensure consistency.

  #### State Diagram
  - Scope: describe the software states and transitions for modules or control flows that depend on modes or events.
  - Common traps:
    - Using state diagrams for simple linear code where they add no value.
    - Ignoring unexpected events or failure modes in the state transitions.
    - Mixing states with implementation details like specific functions.
  - Good tips:
    - Use state diagrams for mode-based logic, startup/shutdown sequences, or communication state machines.
    - Include both normal and error transitions.
    - Keep state names meaningful and avoid overcomplicating the diagram.

  #### Flowchart Diagram
  - Scope: show the step-by-step logic of a process or algorithm, including decisions, loops, and actions.
  - Common traps:
    - Drawing flowcharts for every tiny function instead of key algorithms.
    - Making the chart too detailed, which hurts readability.
    - Using inconsistent symbols or unclear labels.
  - Good tips:
    - Use flowcharts for important algorithmic flows, initialization, and control loops.
    - Keep diagrams focused and easy to follow.
    - Annotate decisions with clear conditions.

  #### Component Diagram
  - Scope: show the main software modules, their relationships, and the dependencies between them.
  - Common traps:
    - Drawing a diagram with too many tiny modules that look like a code-level class map.
    - Leaving dependencies vague or implicit.
    - Not showing which components map to hardware interfaces or system functions.
  - Good tips:
    - Group components by functional area.
    - Show data flow or interface direction when useful.
    - Use it to explain architecture, not code structure.

  #### Sequence Diagram
  - Scope: illustrate the runtime interaction between software components, hardware interfaces, and external actors for a given scenario.
  - Common traps:
    - Showing only internal code calls instead of meaningful system interactions.
    - Making the sequence too long and hard to read.
    - Not specifying the context or scenario clearly.
  - Good tips:
    - Use sequence diagrams for startup, communication exchanges, and critical event handling.
    - Keep each diagram limited to a single use case or flow.
    - Label messages with the type of data or action.

  #### Class Diagram
  - Scope: define the main software classes or structures, their attributes, and their relationships in object-oriented or component-based designs.
  - Common traps:
    - Using a class diagram as a literal map of every source file.
    - Including unnecessary implementation details.
    - Not updating the diagram as the design evolves.
  - Good tips:
    - Use class diagrams to describe the software design at a higher level.
    - Focus on important entities, interfaces, and relationships.
    - Keep it aligned with the software specification and component model.

</details>

<details>
  <summary>Mechanical documents</summary>

  #### Mechanical Specification
  - Scope: define the mechanical requirements for the system, including assemblies, enclosures, load-bearing structures, and environmental constraints.
  - Common traps:
    - Writing the design before the mechanical requirements are fully understood.
    - Ignoring thermal management, vibration, or manufacturability issues.
    - Leaving mechanical tolerances and fit requirements vague.
  - Good tips:
    - Describe the mechanical functions and the conditions the design must endure.
    - Capture required dimensions, materials, and surface finishes.
    - Include maintenance and access requirements when relevant.

  #### Hardware Mechanical Interface Specification
  - Scope: define how the mechanical parts interface with the electronic hardware, including mounting, enclosure penetration, and grounding.
  - Common traps:
    - Assuming the hardware will automatically fit the mechanical case.
    - Not specifying how connectors and cables are supported or sealed.
    - Forgetting the mechanical consequences of thermal expansion or assembly forces.
  - Good tips:
    - Document PCB mount positions, connector cutouts, and assembly sequences.
    - Specify where the mechanical design must support or protect hardware elements.
    - Define grounding points, EMI shielding, and vibration mounting details.

  #### Mechanical Design Specification
  - Scope: describe the mechanical design itself, including parts, materials, finishes, and assembly requirements.
  - Common traps:
    - Mixing CAD model detail with the high-level specification.
    - Omitting the bill of materials or part sourcing constraints.
    - Failing to capture the required mechanical performance.
  - Good tips:
    - Keep the specification focused on functional and manufacturing needs.
    - Reference the bill of materials for parts and materials.
    - Note any special assembly or inspection requirements.

  #### Block Diagram
  - Scope: show the main mechanical subsystems and their relationships in a high-level design view.
  - Common traps:
    - Confusing mechanical block diagrams with detailed CAD drawings.
    - Showing every small bracket or fastener instead of major assemblies.
    - Leaving the relationship to hardware and software unclear.
  - Good tips:
    - Use it to explain the mechanical architecture and assembly flow.
    - Keep blocks at the level of enclosures, frames, modules, and major interfaces.
    - Identify which blocks interact with hardware or software components.

  #### Bill of Materials
  - Scope: list all mechanical parts, fasteners, materials, and purchased items required for the design.
  - Common traps:
    - Including incomplete or inconsistent part numbers.
    - Forgetting to list quantities, material grades, or supplier details.
    - Not linking parts to their function or assembly location.
  - Good tips:
    - Use a clear table with part, description, quantity, and source.
    - Include reference designators or assembly locations.
    - Keep the BOM updated as the design evolves.

  #### Parts (CAD models)
  - Scope: capture the detailed geometry of mechanical parts, usually in CAD file formats like SLDPRT.
  - Common traps:
    - Keeping CAD models undocumented or without part metadata.
    - Using overly generic parts when the design needs custom geometry.
    - Not verifying the model against interface and assembly requirements.
  - Good tips:
    - Keep CAD models organized with clear names and version control.
    - Include notes on critical dimensions and fit tolerances.
    - Share models with hardware and assembly teams for integration review.

  #### Assembly (CAD assembly)
  - Scope: define how mechanical parts fit together and how the overall product is assembled.
  - Common traps:
    - Treating assembly models as perfect instead of checking for real-world manufacturing and assembly issues.
    - Not documenting assembly order, fasteners, or required tools.
    - Ignoring serviceability and access for maintenance.
  - Good tips:
    - Use assembly CAD to validate fit, clearance, and part interactions.
    - Document the assembly sequence and critical join points.
    - Review the model with manufacturing and test engineers to catch problems early.

</details>

