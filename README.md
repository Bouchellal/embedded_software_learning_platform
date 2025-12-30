# Embedded Software Learning Platform

## Introduction

This project is my attempt to create a learning platform and assemble a set of courses aimed at helping students at École Nationale Polytechnique (**ENP**) in Algiers fill gaps in the current academic curriculum.

The content is shaped by my four years of professional experience in aerospace embedded software engineering, as well as by one year of studies at a French university, where I was particularly inspired by lectures delivered by engineers from AIRBUS, Thales, and other industry leaders. Through this platform, I aim to build a strong bridge between academia and industry.

My long-term vision is for this project to grow beyond ENP Algiers by:

- organizing talks and conferences led by ENP alumni,

- fostering student-driven open-source projects,

- enabling alumni-guided projects that can serve as internship-like experiences for students,

- and eventually expanding and deploying these learning platforms and lectures beyond ENP Algiers.

Ultimately, the goal is to build a practical, industry-oriented learning ecosystem driven by students, alumni, and professionals.

## The added value of the platform

The added value of this project is to teach the **Development Process** to students.

This will cover:
  - V Cycle process:
    - Plan, Specification, Design, Implementation, Test, Validation.
    - Traceability management, Matrix of Compliances, Matrix of Coverages.
  - Continuous Integration / Continuous Deployment.
  - Test bench and automated tests.

From my experience, these concepts are the missing link in the ENP program for producing engineers ready to create products in Algeria.

## The platform hardware

                                ┌───────────────┐          ┌────────────────┐
                                │             ┌┐│   UART   │┌┐            ┌┐│
                                │  Raspberry  │◄┼──────────┼►│ STM32  ARM │││
                                │  Pi 3/4 B   │││          │││ MPU Nucleo │││
                                │             │││          │││            │││
                                │             │││   GPIO   │││            │││
                                │             │◄┼──────────┼┤│            │││
                                │  Tester SW  │││   GPIO   │││ TESTED SW  │││
                                │             │├┼──────────┼►│            │├┼───┐
                                │┌─┐          │├┼─┐        │││            │├┼─┐ │
                                ││ │          └┘│ │        │└┘            └┘│ │ │
                                └└┬┘────────────┘ │        └────────────────┘ │ │
                 Eth to User      │               │                           │ │
      ◄───────────────────────────┘         ┌─────┘            ┌──────────────┘ │I2C/SPI
                                            │I2C/SPI           │ I2C/SPI   ┌────┘
                                            │                  │           │
                                        ┌───┴───┐          ┌───┴───┐   ┌───┴───┐
                                        │       ├──────────►       │   │       │
                                        │  DAC  │          │  ADC  │   │ NVRAM │
                                        │       ├──────────►       │   │       │
                                        └───────┘          └───────┘   └───────┘

Hence, the hardware platform that we provide will **not be spectacular**. We intend to include:

- One Raspberry Pi (Model 3 or 4, Type B),
- One STM32 Nucleo board (no requirements for high performance or number of cores),
- One ADC,
- One DAC,
- One NVRAM.

At least one of these components should support I2C and SPI protocols.

## Technical skills to learn

We will not necessarily provide tutorials and lessons for every technical concept or skill we guide students through. Instead, we provide a set of links to the tutorials and lessons we recommend.

As software engineers, we are aware that using links to external videos and lessons carries the risk that links become deprecated or content is no longer available.
Thus, we **invite students** to inform us and **suggest** new links for better content.

<details>
<summary>The technical skills we will guide students through are:<summary>
  - UML / SysML:
    - [ ] How to design and document software with diagrams.

  - Version control:
    - [ ] Master git workflow.

  - Basic C code:
    - [ ] Structures,
    - [ ] Cross-compilation,
    - [ ] Memory layout (code, data, heap, and stack),
    - [ ] Coding with linters and standards,
    - [ ] Coding critical software.

  - Basic Python:
    - [ ] Object-oriented programming,
    - [ ] Coding with linters and standards.

  - Robot Framework:
    - [ ] Automated testing,
    - [ ] Write your own test steps library for embedded system.

  - Embedded Systems:
    - [ ] Reading data sheets,
    - [ ] Configuring and reading registers,
    - [ ] Understanding PinMux-ing and manually applying it.

  - Linux:
    - [ ] [ ] Understanding file system,
    - [ ] Learning basic Linux commands,
    - [ ] Writing shell & bash scripts,
    - [ ] Understanding environment and sourcing,
    - [ ] Bootloader, Device Tree, Kernel, rootFS.
<details>