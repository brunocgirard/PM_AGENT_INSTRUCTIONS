# K6 — Agile, Scrum & Hybrid Mechanics

A working reference to the mechanics of agile, Scrum, Kanban, and hybrid
delivery, written for a project manager studying for the PMP exam and running
hybrid projects. Original synthesis in original wording — not a copy of any
copyrighted text, and not real exam questions. Roughly half the PMP exam is
agile/hybrid; this file fills that gap. For predictive mechanics see K1; for
exam logistics see K3.

---

## 1. The Agile Mindset

"Agile" is not a single method. It is an umbrella term for approaches that
deliver value in short, repeated cycles, welcome change, and rely on feedback
instead of a fixed up-front plan. Scrum, Kanban, XP, and others are all agile.

### Empirical process control

Agile assumes you cannot fully predict the work. Instead of planning everything
first, you run small experiments and learn. This rests on three pillars:

- **Transparency** — work, progress, and problems are visible to everyone.
- **Inspection** — the team frequently checks the product and the process.
- **Adaptation** — when inspection shows drift, the team adjusts quickly.

This loop — do a small piece, look at it, adjust — is the heart of every agile
event and the reason agile suits high-uncertainty work.

### The four values (paraphrased)

The Agile Manifesto states four preferences. The items on the right still have
value; the items on the left have **more** value.

| Prefer this | Over this |
|---|---|
| People and their interactions | Processes and tools |
| Software (a working product) that works | Exhaustive documentation |
| Collaboration with the customer | Contract negotiation |
| Responding to change | Following a fixed plan |

### The twelve principles (paraphrased)

1. Satisfy the customer through early and continuous delivery of value.
2. Welcome changing requirements, even late, as a competitive advantage.
3. Deliver working product frequently, in weeks rather than months.
4. Business people and developers work together daily.
5. Build projects around motivated people; give them support and trust.
6. Favor face-to-face conversation as the richest way to communicate.
7. Working product is the primary measure of progress.
8. Sustain a constant, indefinitely repeatable pace; avoid burnout.
9. Pay continuous attention to technical excellence and good design.
10. Maximize the work *not* done — simplicity is essential.
11. The best designs and architectures emerge from self-organizing teams.
12. At regular intervals, the team reflects and tunes its own behavior.

---

## 2. The Scrum Framework

Scrum is the most-tested agile framework. It is lightweight: three
accountabilities, five events, three artifacts — and nothing more is required.

### The three accountabilities (roles)

| Accountability | What they own | Day-to-day work |
|---|---|---|
| **Product Owner** | Value and the Product Backlog | Orders the backlog, writes/refines items, sets priorities, decides what is built and when, talks to stakeholders, accepts or rejects work. One person, not a committee. |
| **Scrum Master** | The team's effectiveness and the process | Coaches Scrum, facilitates events, removes impediments, shields the team from disruption, coaches the organization. A servant leader, not a boss. |
| **Developers** | Building a usable Increment each Sprint | The people doing the work — design, build, test, integrate. Self-managing: they decide *how* to do the work and own the Sprint Backlog. |

The Scrum Master and Product Owner do **not** assign tasks; the Developers
pull their own work. There is no "project manager" role inside Scrum.

### The five events

The Sprint is a container; the other four happen inside it.

| Event | Timebox (1-month Sprint) | Purpose |
|---|---|---|
| **Sprint** | 1 month or less, fixed length | The container for all work; produces a usable Increment. |
| **Sprint Planning** | Up to 8 hours | Team agrees the Sprint Goal, selects backlog items, and plans the work. Answers *why, what, how*. |
| **Daily Scrum** | 15 minutes, every day | Developers re-plan the next 24 hours toward the Sprint Goal and surface blockers. |
| **Sprint Review** | Up to 4 hours | Team and stakeholders inspect the Increment, gather feedback, and adapt the Product Backlog. |
| **Sprint Retrospective** | Up to 3 hours | The team inspects *itself* — process, tools, relationships — and plans improvements. |

Shorter Sprints get proportionally shorter timeboxes. A Sprint is never
extended; if the goal becomes obsolete the Product Owner may cancel it.

### The three artifacts and their commitments

Each artifact carries a **commitment** that creates focus and measures progress.

| Artifact | What it is | Commitment |
|---|---|---|
| **Product Backlog** | The single ordered list of everything that might be needed in the product. | **Product Goal** — the longer-term objective the team is working toward. |
| **Sprint Backlog** | The Sprint Goal + items selected for the Sprint + the plan to deliver them. | **Sprint Goal** — the single objective for the Sprint. |
| **Increment** | A concrete, usable step toward the Product Goal; Sprints can produce more than one. | **Definition of Done** — the shared quality bar an item must meet to be "done". |

---

## 3. Kanban and Flow

Kanban is an agile method focused on **flow** — the smooth, steady movement of
work through a process. It does not prescribe roles, timeboxes, or sprints. You
overlay it on whatever process you already have and improve it gradually.

### Core practices

- **Visualize the work** — a board with columns for each stage (e.g. To Do,
  In Progress, Review, Done). Every work item is a card.
- **Limit Work in Progress (WIP)** — each column has a maximum number of cards.
  When a column is full, you cannot start new work; you must finish or help.
  WIP limits expose bottlenecks and stop multitasking.
- **Pull system** — work is *pulled* into the next stage only when there is
  capacity, rather than *pushed* in by a schedule.
- **Manage and improve flow** — measure flow and reduce delays continuously.

### Flow metrics

| Metric | Meaning |
|---|---|
| **Lead time** | Total time from a request being raised to it being delivered (customer's clock). |
| **Cycle time** | Time from work actually *starting* to it finishing (team's clock). |
| **Throughput** | Number of items completed per unit of time. |
| **WIP** | Number of items started but not finished. |

Little's Law links them: average cycle time ≈ WIP ÷ throughput. Lowering WIP
shortens cycle time. A **cumulative flow diagram (CFD)** stacks the count of
items in each stage over time; widening bands reveal bottlenecks, and the
horizontal gap between the top and bottom bands shows lead time.

### Kanban vs. Scrum

| Use Scrum when... | Use Kanban when... |
|---|---|
| Work fits into planned, goal-driven iterations. | Work arrives unpredictably (support, ops, maintenance). |
| You want a regular cadence of review and feedback. | Priorities change mid-stream and timeboxes feel artificial. |
| The team benefits from fixed roles and ceremonies. | You want to improve an existing process incrementally. |

Many teams blend the two ("Scrumban") — a Scrum cadence with WIP limits and a
flow board.

---

## 4. Backlog and Requirements

### User stories

A **user story** is a short, plain-language description of a need from the
user's point of view. A common format:

> *As a [type of user], I want [some capability], so that [some benefit].*

The story is a placeholder for a conversation, not a full specification. Detail
is added through discussion and **acceptance criteria** — testable conditions
that define when the story is satisfied.

### INVEST — qualities of a good story

| Letter | Quality |
|---|---|
| **I** | Independent — can be built without depending on other stories. |
| **N** | Negotiable — a starting point for conversation, not a contract. |
| **V** | Valuable — delivers value to a user or customer. |
| **E** | Estimable — the team can size it. |
| **S** | Small — fits comfortably inside one iteration. |
| **T** | Testable — has clear acceptance criteria. |

### Hierarchy of work

**Epic** (a large body of work, often spanning releases) → **Feature** (a
deliverable slice of functionality) → **User story** (a small, iteration-sized
item) → **Task** (a unit of work the Developers create to deliver a story).
Large items are split progressively as they near the top of the backlog.

### Definition of Ready vs. Definition of Done

- **Definition of Ready (DoR)** — the checklist a backlog item must meet
  *before* the team will commit to it (clear, estimated, has acceptance
  criteria, dependencies known). It is an entry gate into a Sprint.
- **Definition of Done (DoD)** — the quality bar an item must meet to be
  considered complete (coded, tested, integrated, documented). It is an exit
  gate. DoD is a Scrum commitment; DoR is an optional team agreement.

### Backlog refinement

**Refinement** (also called grooming) is the ongoing activity of adding detail,
estimates, and order to backlog items so the top of the backlog is always ready
to be worked. It is continuous, not a single event, and typically consumes a
small percentage of the team's capacity.

### Prioritization techniques

| Technique | How it works |
|---|---|
| **MoSCoW** | Sort items into Must have, Should have, Could have, Won't have (this time). |
| **WSJF** (Weighted Shortest Job First) | Score = Cost of Delay ÷ Job Size; do the highest score first. |
| **Value-based / value vs. effort** | Plot items by business value against effort; pick high value, low effort first. |
| **Kano model** | Classify features as basic, performance, or delighters to balance the backlog. |

---

## 5. Agile Estimation and Metrics

### Relative sizing and story points

Agile teams estimate **relatively** — comparing items to each other — rather
than in absolute hours. A **story point** is a unit of relative size that
blends effort, complexity, and uncertainty. Teams often use a Fibonacci-like
scale (1, 2, 3, 5, 8, 13) because larger items carry more uncertainty.

### Planning poker

A consensus estimation technique: each Developer privately picks a card, all
reveal at once, and outliers explain their reasoning. The discussion — not the
number — is the real value. The team re-votes until it converges.

### Velocity and forecasting

**Velocity** is the number of story points (or items) a team completes per
iteration. Averaged over several iterations, it becomes a planning tool:

> Remaining points ÷ average velocity ≈ iterations remaining.

Velocity is a forecasting aid for *one team over time*. It must never be used
to compare teams or as a performance target — that corrupts the estimates.

### Burndown vs. burnup

| Chart | Shows | Reads as |
|---|---|---|
| **Burndown** | Work remaining over time, trending toward zero. | Are we on track to finish the Sprint/release? |
| **Burnup** | Work completed climbing toward a total scope line. | Same, but also makes *scope changes* visible (the line moves). |

### Release planning

A **release plan** forecasts which features will be ready by which dates,
across several iterations. It is built from the prioritized backlog, the team's
velocity, and the release goal — and is re-forecast every iteration as real
data arrives. Agile fixes time and cost, and flexes scope; predictive does the
reverse.

---

## 6. Agile Roles and Leadership

Agile leadership is **servant leadership** — the leader exists to serve the
team, not to direct it. The team's needs come first; authority is earned, not
assumed.

### What a servant leader actually does

- **Removes impediments** — clears blockers the team cannot resolve itself:
  access, dependencies, organizational friction, distractions.
- **Shields the team** — buffers them from interruptions and shifting demands
  so they can sustain focus and a steady pace.
- **Facilitates** — runs events so they are productive and timeboxed, draws out
  quiet voices, and helps the team reach its own decisions.
- **Coaches and mentors** — grows individuals' skills and the team's agile
  maturity; asks questions rather than giving answers.
- **Builds the environment** — creates psychological safety so people raise
  problems early, fosters trust, and promotes collaboration.
- **Connects the team to value** — keeps purpose, the customer, and outcomes
  visible.

### Self-organizing and self-managing teams

A **self-organizing** team decides *how* to do the work; a **self-managing**
team also decides *who* does it and *which* work to take. The leader sets the
goal and the boundaries, then steps back. The leader does not assign tasks,
does not micromanage, and does not solve problems the team can solve itself.
This is the single most common right-answer pattern on the PMP exam.

---

## 7. Scaling and Other Frameworks

Exam-level awareness only — recognize these by name and purpose.

| Framework / practice | What to know |
|---|---|
| **Scrum of Scrums** | A scaling technique: a representative from each team meets regularly to coordinate dependencies across teams. |
| **SAFe** (Scaled Agile Framework) | A heavyweight framework for coordinating many agile teams at enterprise scale; organizes work into Agile Release Trains and Program Increments. |
| **LeSS** (Large-Scale Scrum) | Scrum scaled up with minimal extra process — one Product Owner and one backlog across multiple teams. |
| **DSDM** | An agile project delivery framework that fixes time, cost, and quality and flexes features; uses MoSCoW prioritization and timeboxing. |
| **Crystal** | A family of methods (Crystal Clear, Crystal Orange...) tailored by team size and project criticality; emphasizes people and communication. |
| **XP** (Extreme Programming) | An engineering-focused agile method. Key practices: **pair programming** (two developers, one workstation), **test-driven development** (write the test first, then code), **continuous integration** (merge and test small changes constantly), refactoring, small releases, collective code ownership. |

---

## 8. Hybrid Delivery

A **hybrid** approach deliberately combines predictive and adaptive elements.
You tailor the mix to the work — using the right tool for each part rather than
forcing one method onto everything.

### Common hybrid patterns

| Pattern | Description | When it fits |
|---|---|---|
| **Predictive gates around agile delivery** | Formal initiation and closeout phases with milestone reviews; agile iterations in the middle for the build. | Governance or funding requires phase gates, but requirements will evolve. |
| **Agile build, predictive deployment** | Product is developed iteratively, then released through a planned, sequenced rollout. | The work is uncertain but deployment (training, regulation, logistics) is fixed. |
| **Parallel workstreams, different approaches** | Stable, well-understood components run predictively; novel or volatile components run agile. | A project mixes commodity work with innovation. |
| **Predictive front, agile finish** | Heavy up-front design where it is cheap to change, agile execution where feedback matters. | Architecture must be fixed early but features can emerge. |

### Deciding what goes where

Push a component toward **agile** when requirements are unclear or volatile,
feedback is valuable, and the customer can engage frequently. Push it toward
**predictive** when requirements are stable and well understood, the sequence
is fixed, compliance demands documentation, or change is genuinely expensive.
The deliverable type drives the approach (see K1 §3).

### Earned value and agile metrics together

In a hybrid project the two measurement systems coexist:

- Predictive workstreams report **earned value** — CV, SV, CPI, SPI, EAC (K3 §5).
- Agile workstreams report **velocity, burndown/burnup, throughput, and cycle
  time**.
- A blended option is **agile earned value**: treat completed story points as
  earned value, the release budget as BAC, and compute CPI/SPI from points and
  spend — giving executives one consistent set of indices.
- Roll both up into one dashboard so stakeholders see overall health without
  needing to understand each method.

---

## 9. Agile on the PMP Exam

### What the exam tests

The exam does not test whether you can recite the Scrum Guide. It tests
**judgment in scenarios** — recognizing an agile situation and choosing the
response a good servant leader and agile practitioner would make. Expect heavy
hybrid content.

### Answer patterns that tend to be correct

- **Let the team decide and self-organize** — the PM/Scrum Master facilitates,
  does not assign tasks or impose solutions.
- **Remove the impediment** rather than escalate, blame, or work around it.
- **Go to the source / talk to the person** — favor direct, face-to-face
  conversation over documents and email.
- **Use the backlog** — handle new scope by adding it to the backlog and
  re-prioritizing, not by invoking formal change control (that is predictive).
- **Inspect and adapt** — take the issue to the next appropriate event
  (Retrospective for process problems, Review for product feedback).
- **Deliver value early and get feedback** — prefer a small working increment
  over a long, complete one.
- **Protect a sustainable pace** — do not solve schedule pressure with overtime.

### Common traps

- Choosing the answer where the PM or Scrum Master assigns work or makes the
  team's decisions for them — almost always wrong.
- Adding scope mid-Sprint — the Sprint Backlog is the Developers' to protect;
  new work goes to the Product Backlog for a future Sprint.
- Applying a Change Control Board to an agile workstream — change is absorbed
  through re-prioritization, not a CCB.
- Treating velocity as a productivity target or a way to compare teams.
- Skipping the Retrospective or events "to save time" — never the right answer.
- Confusing the roles: the Product Owner owns *value and the backlog*; the
  Scrum Master owns *the process and the team's effectiveness*; the Developers
  own *how the work gets done*.
- Confusing Definition of Ready (entry) with Definition of Done (exit).

When a question is ambiguous, pick the option that empowers the team, increases
transparency, delivers value sooner, and gathers feedback. See K3 §6 for the
broader PMI mindset.
