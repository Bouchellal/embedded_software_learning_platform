# 1. First Meeting with the System Architect

In your first meeting with Djamal, the System Architect, you will discuss the requirements of the project and the overall architecture of the software solution. Djamal will provide you with an overview of the project and explain how your role as an Embedded Software Engineer fits into the larger picture.

## 1.1 Overview of the Process

The development process will follow a V cycle on System level, and on each Unit level.

![System and Unit definition](../../.images/03_guided_avionic_project/system_and_unit.jpg)

- The System level will focus on the overall architecture and design of the software solution, ensuring that it meets the client's requirements and is scalable for future enhancements.
- The Software Unit level will focus on the development of the embedded software solution that interfaces with the hardware components and collects data in real-time.
- The Hardware Unit level will focus on the design and implementation of the hardware components of the solution, including the sensors, electrical interfaces, power management.
- The Mechanical Unit level will focus on the design and implementation of the mechanical components of the solution, including the housing and mounting of the hardware components.

The System level and the 3 Units, all will follow a similar V-cycle: 

![System and Unit definition](../../.images/03_guided_avionic_project/v_cycle.jpg)

The V-Cycle is a model that emphasizes a direct relationship between every development phase and its corresponding testing phase.

- The Left Side (Downward): Decomposition and definition. You break high-level system needs down into low-level software code.
- The Bottom (The Vertex): The actual implementation (coding).
- The Right Side (Upward): Integration and verification. You prove that what you built matches what you defined on the left side.

Why use it? It ensures Traceability. If a test fails on the right side, you know exactly which requirement on the left side was misunderstood or implemented incorrectly

Each phase of the V-cycle will involve specific activities and deliverables, such as requirements gathering, design, implementation, testing, and validation. The process will be iterative, with feedback loops to ensure that the solution meets the client's requirements and is of high quality.

Each **V-cycle** will need its own inputs and will provide its own outputs.

Each **phase of the V-cycle** will need its own inputs and will provide its own outputs.

For example, here is the V-Cycle for the System level with its inputs and outputs **for the downward phases**:

![System level V-cycle](../../.images/03_guided_avionic_project/system-v_cycle.jpg)

# 2. Tasks for you!

**For the next couple of tasks you do not need the hardware platform.**

Task 0: Set up the project folder on your own computer. [Go to task 0](./_task_0.md)

Task 1: Review the System Requirements written by Djamal (the System Architect). [Go to task 1](./_task_1.md)

Task 2: Create a python project to automate the requirement management and traceability. [Go to task 2](./_task_2.md)

Task 3: Help the System engineer draw the System Diagrams. [Go to task 3](./_task_3.md)

