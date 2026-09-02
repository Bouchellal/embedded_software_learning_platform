# Requirements Engineering — An Introduction for Engineers

> **Who is this for?** You've never written a formal requirement before, and you're about to work on a project where every requirement is tracked, reviewed, and tested. This lecture gives you the vocabulary and the reflexes you need before you write your first one.

**By the end of this lecture, you will be able to:**
- Explain what a requirement is (and isn't)
- Write a requirement that passes the SMART test
- Use "shall" and "shall not" correctly
- Understand why traceability matters and how it works
- Fill in a requirement's metadata (ID, parent, allocation, verification method...)
- Follow this project's JSON format and identifier conventions

---

## 1. What is a requirement, really?

Think of a requirement as **a contract between stakeholders and engineers**.

> It defines *what* the system must do, *what it must not do*, and *under which constraints* it operates.

What it is **not**:
- ❌ A design note
- ❌ A description of your code
- ❌ An implementation detail

A requirement states the **expected result**. It says nothing about *how* you get there — that choice stays with the engineering team.

**Analogy:** if you hired a contractor to build a bridge, you'd say "the bridge shall support 40 tonnes" — not "use steel beams spaced 2m apart." The first is a requirement. The second is a design decision.

---

## 2. Why does this matter so much in aerospace / embedded systems?

In safety-critical fields, a requirement is not just documentation — it's **evidence**. Standards like DO-178C exist because regulators (and your future self, six months from now) need to trust that:

| Principle | What it means |
|---|---|
| **Repeatability** | The engineering process is documented and can be reproduced |
| **Traceability** | Every requirement links to a need *and* a verification result |
| **Deterministic behavior** | The system behaves predictably, in normal *and* failure conditions |
| **Verification** | You can prove the software does what the requirement says — and nothing more |

> 🧠 **Key takeaway:** in safety-critical engineering, *code alone proves nothing*. Only code + traceable requirements + verification evidence proves the system is safe.

---

## 3. The SMART test

A requirement is only useful if it's **testable and unambiguous**. Run every requirement you write through the SMART checklist:

| Letter | Meaning | Ask yourself... |
|---|---|---|
| **S** | Specific | Does this target *one* clear behavior? |
| **M** | Measurable | Is there a number, threshold, or condition? |
| **A** | Achievable | Can this actually be built, given our constraints? |
| **R** | Relevant | Does this serve a real user or system need? |
| **T** | Testable | Can I verify this by test, analysis, inspection, or demonstration? |

### ❌ Bad requirement
> "The software should be fast and never crash."

| Problem | Why |
|---|---|
| "fast" | Not measurable |
| "never crash" | Too vague to verify |
| — | No verification method implied |

### ✅ Good requirement
> "The software shall process each sensor sample within 50 ms of the interrupt event."

- **Specific** → sensor data processing
- **Measurable** → 50 ms
- **Relevant** → supports real-time timing behavior
- **Testable** → processing time can be measured directly

---

## 4. What to describe — and what to leave out

| ✅ Describe | ❌ Don't describe |
|---|---|
| Required system behavior | Internal design decisions |
| Expected output or condition | Algorithms or implementation methods |
| Constraints, limits, performance | Specific coding style or hardware choices |
| Safety or operational conditions | Personal preferences or assumptions |

### Example: implementation leaking into a requirement

❌ **Too prescriptive:**
> "The software shall use a round-robin scheduler to process sensor data."

This tells the engineer *how* to build it — that's a design decision, not a requirement.

✅ **Behavior-based instead:**
> "The software shall process each sensor sample within 10 ms of arrival."

Same intent, but now the implementation is free. This version is:
- Easier to verify
- Less likely to lock in a design too early
- Reusable if the implementation changes later

---

## 5. The words that carry legal weight: modal verbs

In requirements, **word choice is not style — it's obligation.**

| Verb | Meaning | Use it for... |
|---|---|---|
| **shall** | Mandatory | Binding requirements |
| **shall not** | Prohibited | Constraints, forbidden states, safety barriers |
| ~~should~~ | Recommended, *not* binding | Avoid in formal requirements |
| ~~may~~ | Optional | Avoid in formal requirements |
| ~~will~~ | States a fact / future event | Avoid in formal requirements |

**Examples:**
- ✅ "The system **shall** disconnect the autopilot when the pilot applies 10 lbf to the yoke."
- ✅ "The system **shall not** deploy the thrust reversers while the aircraft is in flight mode."

> ⚠️ **Rule of thumb:** if a sentence in a requirements doc uses "should," "may," or "will," stop and ask whether it's actually binding. If yes — rewrite it with "shall."

---

## 6. Derived requirements

Sometimes, a requirement shows up *during design*, not because a customer asked for it, but because the engineer needs it to satisfy something else.

**Example:** while designing the timing logic, an engineer realizes a watchdog timer is needed. That watchdog requirement is *derived* — it wasn't in the original customer request.

**Rules for derived requirements:**
- They must be **justified**
- They must be **reviewed** by the safety or design authority
- They should be **linked to a rationale or parent requirement** whenever possible

> 🚩 A derived requirement with no parent and no rationale is a red flag — it may be introducing unreviewed risk into the system.

---

## 7. Traceability: the thread that holds everything together

Traceability means every requirement can be followed, end to end:

```
customer need
   └─ system requirement
        └─ subsystem requirement
             └─ software / hardware design
                  └─ implementation
                       └─ verification test
```

If **any link breaks**, the evidence is incomplete. A test case that can't be traced back to a requirement means: *we don't actually know what we validated.*

This is exactly why certification bodies care so much about it — traceability turns "we tested the software" into "we can prove exactly what we tested and why."

---

## 8. Single source of truth

Don't repeat the same value across multiple requirements — **define it once, then reference it.**

### ❌ Repetition-prone version
> Req 1: "collect data at 10 Hz"
> Req 2: "raise an error if data isn't processed within 10 Hz"

If the frequency ever changes, you now have two places to update — and it's easy to miss one.

### ✅ Single source of truth
> **Req 1:** "The system shall collect data from the sensors at a frequency of 10 Hz, defined as `DATA_COLLECTION_FREQUENCY`."
> **Req 2:** "The system shall raise an error if the collected data is not processed within `DATA_COLLECTION_FREQUENCY`."

One authoritative definition → consistent, maintainable, and less error-prone.

---

## 9. Anatomy of a requirement (the metadata)

A requirement is not just a sentence — it's a **structured data element**. In tools like DOORS, Jama, or a GitHub-based requirements database, every requirement carries metadata:

| Attribute | Definition | Why it matters |
|---|---|---|
| **Unique ID** | Permanent identifier (e.g. `SW-REQ-001`) | Enables traceability and version control |
| **Title** | Short descriptive name | Quick identification |
| **Text** | Full requirement statement | Defines the expected behavior |
| **Parent Link** | Higher-level requirement satisfied | Upward traceability |
| **Child Link** | Lower-level requirement/implementation fed | Downward traceability |
| **Allocation** | System / software / hardware / mechanical | Ownership and responsibility |
| **Verification Method** | Test / analysis / inspection / demonstration | How compliance will be proven |
| **Variant** | Current / future / obsolete / variant-specific | Tracks product version state |

---

## 10. This project's format

In this project, every requirement is a JSON object in a list, following this schema:

```json
[
  {
    "identifier": "AEME-CR-0001",
    "title": "Maximum size for the equipment",
    "text": "The equipment shall not exceed maximum size of 40 cm x 40 cm x 20 cm (length x width x height).",
    "verification_method": "Test",
    "parent": "",
    "allocation": "System",
    "variant": "current"
  },
  {
    "identifier": "AEME-CR-0002",
    "title": "Example requirement",
    "text": "The system shall ...",
    "verification_method": "Analysis",
    "parent": "AEME-CR-0001",
    "allocation": "System",
    "variant": "current"
  }
]
```

**Fields, always in this order:**
`identifier` → `title` → `text` → `verification_method` → `parent` → `allocation` → `variant`

### Identifier conventions

The identifier tells you the document type at a glance:

| Specification Document | Identifier Format |
|---|---|
| Client Requirement | `AEME-CR-XXXX` |
| System Specification | `AEME-SYS-XXXX` |
| Software Unit Specification | `AEME-SW-XXXX` |
| Hardware Unit Specification | `AEME-HW-XXXX` |
| Mechanical Unit Specification | `AEME-MECH-XXXX` |
| Hardware Software Interface Specification | `AEME-HSI-XXXX` |

`XXXX` = a unique, incrementing number within that document type.

---

## 11. Before you submit a requirement: the 3-question check

Ask yourself, for every requirement you write:

1. **What** must the system do?
2. **Under what condition or constraint**?
3. **How** will we prove it's correct?

> If you can't answer all three clearly, it's not a requirement yet — go back and refine it.

---

## Quick reference cheat sheet

- Use **"shall"** for mandatory behavior, **"shall not"** for prohibitions. Avoid "should/may/will."
- Describe **behavior**, not **implementation**.
- Every value used more than once needs **one authoritative definition**.
- Every requirement needs: ID, title, text, verification method, parent, allocation, variant.
- Derived requirements need a **rationale** and a **review**.
- If it's not **SMART**, it's not done.