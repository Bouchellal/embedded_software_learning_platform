# Embedded Software Learning Platform

## TL;DR

We, Polytechnique Algiers alumni, built a hardware platform inspired from real life On-board Avionic Product development process and delivered multiple examples in ENP Algiers.

We provide here in this Github repository:
  - [ ] Links to learn prerequisites embedded software concepts,
  - [ ] Links to learn development processes,
  - [ ] A guided project inspired from real-world development process of an Avionic Product,
  - [ ] A guideline on how to manage the life cycle of a product, with this platform as an example.
  - [ ] Documentation of the hardware platform:
    - [ ] Design Documents.
    - [ ] Maintenance and Auto-Test of the platform.
    - [ ] Traceability of each individual platform.

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
                                │  Pi 4 B 1GB │││          │││ MPU Nucleo │││
                                │             │││          │││   G071RB   │││
                                │             │││   GPIO   │││            │││
                                │             │◄┼──────────┼┤│            │││
                                │  Tester SW  │││   GPIO   │││ TESTED SW  │││
                                │             │├┼──────────┼►│            │├┼────┐
                                │┌─┐          │├┼─┐        │││            │├┼─┐  │
                                ││ │          └┘│ │        │└┘            └┘│ │  │
                                └└┬┘────────────┘ │        └────────────────┘ │  │
                 Eth to User      │               │                           │  │
      ◄───────────────────────────┘               │                  ┌────────┘  │
                                                  │I2C               │ I2C       │ SPI
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

The technical skills we will guide students through are:

  - UML / SysML:
    - [x] How to design and document software/system with diagrams.

  - Version control:
    - [x] Master git workflow,
    - [x] Master git precommit.

  - Basic C code:
    - [x] Structures,
    - [x] Compilation,
    - [x] Memory layout (code, data, heap, and stack),
    - [x] Coding with linters and standards,
    - [x] Coding critical software.

  - Basic Python:
    - [x] Object-oriented programming,
    - [x] Coding with linters and standards.

  - Robot Framework:
    - [x] Automated testing,
    - [x] Write your own test steps library for embedded system.

  - Embedded Systems:
    - [x] Configuring and reading registers,
    - [x] Understanding PinMux-ing and manually applying it.

  - Linux:
    - [x] Understanding file system,
    - [x] Learning basic Linux commands,
    - [x] Writing shell & bash scripts,
    - [x] Understanding environment and sourcing,
    - [x] Bootloader, Device Tree, Kernel, rootFS.
