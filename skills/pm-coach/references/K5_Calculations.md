# K5 — Calculations & Quantitative Methods

A drill-and-teach reference for every calculation the PMP exam can test.
Original synthesis — not a copy of any copyrighted text, and not real exam
questions. Use it alongside K3 (the EVM table in K3 §5 is a summary; this file
is the full treatment).

> **How to use this file.** Every formula below comes with *when it applies*
> and at least one fully worked, step-by-step numeric example. An AI agent can
> teach from any section directly; a candidate can cover the worked answer and
> re-derive it. Calculation questions are a small share of the exam (~5–10
> items) but they are *free points* once drilled — never lost to judgment.

---

## 1. Earned Value Management (EVM)

EVM compares what you **planned**, what you **earned**, and what you **spent**,
all in the same currency, at the same point in time.

### 1.1 The three base measurements and BAC

| Term | Name | Plain meaning |
|---|---|---|
| **PV** | Planned Value | Budgeted cost of the work *scheduled* by now |
| **EV** | Earned Value | Budgeted cost of the work *actually completed* (BAC × % complete) |
| **AC** | Actual Cost | What you *actually spent* to do that completed work |
| **BAC** | Budget at Completion | Total approved budget for the whole project |

Key idea: **EV is always valued at budgeted rates**, never at actual rates.
EV = BAC × (% of work complete).

### 1.2 Variances and indices

| Metric | Formula | Interpretation |
|---|---|---|
| Cost Variance | **CV = EV − AC** | > 0 under budget; < 0 over budget |
| Schedule Variance | **SV = EV − PV** | > 0 ahead of schedule; < 0 behind |
| Cost Performance Index | **CPI = EV / AC** | > 1 under budget; < 1 over budget |
| Schedule Performance Index | **SPI = EV / PV** | > 1 ahead; < 1 behind |

Memory aids: variances are **subtraction** (EV minus something), indices are
**division** (EV over something). **EV always comes first.** A negative variance
or an index below 1.0 is *bad*.

### 1.3 The running scenario

We carry one scenario through every EVM formula.

> **Scenario.** A project has **BAC = $200,000** and a planned duration of
> 10 months. At the end of **month 5**:
> - The schedule said 50% of the work should be done → **PV = $100,000**.
> - Actually 40% of the work is done → **EV = 0.40 × 200,000 = $80,000**.
> - The team has spent **AC = $90,000**.

**Variances and indices:**

- CV = EV − AC = 80,000 − 90,000 = **−$10,000** → over budget.
- SV = EV − PV = 80,000 − 100,000 = **−$20,000** → behind schedule.
- CPI = EV / AC = 80,000 / 90,000 = **0.889** → getting $0.89 of value per $1.
- SPI = EV / PV = 80,000 / 100,000 = **0.80** → working at 80% of planned pace.

This project is **over budget and behind schedule** — the worst quadrant.

### 1.4 Percent complete

**Percent complete = EV / BAC = 80,000 / 200,000 = 40%.**
Do not confuse it with *percent spent* (AC / BAC = 45%) or *percent of schedule
elapsed* (5/10 = 50%).

### 1.5 The four EAC variants — pick the right one

**EAC (Estimate at Completion)** = forecast of total cost when the project
finishes. There are four formulas; the exam tells you which by describing the
*nature of the variance*. Choosing the right one is the most-tested EVM skill.

| # | Formula | Use when… |
|---|---|---|
| 1 | EAC = **BAC / CPI** | Current cost variance is **typical** and will continue at the same rate |
| 2 | EAC = **AC + (BAC − EV)** | Current variance is **atypical / one-off**; remaining work runs to plan |
| 3 | EAC = **AC + [(BAC − EV) / (CPI × SPI)]** | **Both** cost and schedule pressure will affect the remaining work |
| 4 | EAC = **AC + bottom-up ETC** | The **original estimate is flawed**; re-estimate the rest from scratch |

**Worked, all four (same scenario):**

**Variant 1 — variance is typical:**
EAC = BAC / CPI = 200,000 / 0.889 = **$225,000**.
(Equivalently 200,000 / (80,000/90,000) = 200,000 × 90,000/80,000 = 225,000.)

**Variant 2 — variance was a one-off:**
EAC = AC + (BAC − EV) = 90,000 + (200,000 − 80,000) = 90,000 + 120,000 =
**$210,000**. The $120,000 of remaining work is assumed to run at budget.

**Variant 3 — cost and schedule both bite:**
EAC = AC + [(BAC − EV) / (CPI × SPI)]
= 90,000 + [120,000 / (0.889 × 0.80)]
= 90,000 + [120,000 / 0.711]
= 90,000 + 168,776 = **$258,776**.
Highest forecast — both indices are below 1, so they compound.

**Variant 4 — re-estimate the remainder:**
Suppose the team does a bottom-up re-estimate of the remaining work and gets
**ETC = $140,000**. Then EAC = AC + ETC = 90,000 + 140,000 = **$230,000**.

### 1.6 ETC, VAC

**ETC (Estimate to Complete)** = forecast cost of the *remaining* work.
General relation: **ETC = EAC − AC.**
Using Variant 1's EAC: ETC = 225,000 − 90,000 = **$135,000**.

**VAC (Variance at Completion)** = **BAC − EAC** = how far off budget you will
finish.
Using Variant 1: VAC = 200,000 − 225,000 = **−$25,000** → expect to overrun by
$25,000. Negative VAC = bad, consistent with negative CV.

### 1.7 TCPI — To-Complete Performance Index

TCPI is the cost efficiency you must *achieve from now on* to hit a target. It
is **(work remaining) / (money remaining)**.

| Target | Formula |
|---|---|
| Finish at the original budget (BAC) | TCPI = **(BAC − EV) / (BAC − AC)** |
| Finish at the new forecast (EAC) | TCPI = **(BAC − EV) / (EAC − AC)** |

**TCPI to BAC:**
TCPI = (200,000 − 80,000) / (200,000 − 90,000) = 120,000 / 110,000 = **1.09**.
You must run at 109% efficiency to still finish on the original budget — harder
than your current 0.889, so the original budget is now very tight.

**TCPI to EAC** (using Variant 1 EAC = 225,000):
TCPI = (200,000 − 80,000) / (225,000 − 90,000) = 120,000 / 135,000 = **0.889**.
It equals the CPI — by construction, because EAC = BAC/CPI assumes you keep
performing at exactly CPI. That is a useful sanity check.

**Reading TCPI:** > 1 means you must improve; < 1 means you have slack.

---

## 2. Three-Point Estimating / PERT

Single-point estimates ignore uncertainty. Three-point estimating uses an
**Optimistic (O)**, **Most Likely (M)**, and **Pessimistic (P)** value.

| Method | Expected value (E) formula |
|---|---|
| **Triangular** (simple average) | E = (O + M + P) / 3 |
| **Beta / PERT** (weighted) | E = (O + 4M + P) / 6 |

PERT weights the most-likely value 4×, so it pulls the estimate toward M.

**Standard deviation** of an activity: **σ = (P − O) / 6**.
**Variance** = σ².

### 2.1 Worked example — one activity

> Activity "Build API": O = 8 days, M = 12 days, P = 28 days.

- Triangular E = (8 + 12 + 28) / 3 = 48 / 3 = **16 days**.
- PERT E = (8 + 4×12 + 28) / 6 = (8 + 48 + 28) / 6 = 84 / 6 = **14 days**.
- σ = (P − O) / 6 = (28 − 8) / 6 = 20 / 6 = **3.33 days**.
- Variance = σ² = 3.33² = **11.1 days²**.

### 2.2 The empirical rule (confidence ranges)

For a roughly normal distribution, the PERT estimate ± multiples of σ give
confidence ranges:

| Range | Confidence | This activity (E = 14, σ = 3.33) |
|---|---|---|
| E ± 1σ | ~68% | 10.67 to 17.33 days |
| E ± 2σ | ~95% | 7.33 to 20.67 days |
| E ± 3σ | ~99.7% | 4.0 to 24.0 days |

So there is about a **95% chance** the activity finishes between 7.3 and
20.7 days. To combine activities along a path, **sum the variances**, then take
the square root for the path's σ (never add standard deviations directly).

---

## 3. Critical Path Method (CPM)

The **critical path** is the **longest** path of dependent activities through
the network. Its length is the **shortest possible project duration**.
Activities on it have **zero total float** — any slip delays the project.

### 3.1 Forward and backward pass

- **Forward pass** (left → right): computes **Early Start (ES)** and **Early
  Finish (EF)**. EF = ES + Duration − 1 (using whole-day convention). The next
  activity's ES = highest predecessor EF + 1.
- **Backward pass** (right → left): computes **Late Start (LS)** and **Late
  Finish (LF)**, starting from the project end.
- **Total Float (TF)** = LS − ES = LF − EF. Slack before the *project* slips.
- **Free Float (FF)** = (ES of next activity) − EF − 1. Slack before the *next
  activity* slips.

### 3.2 Worked network

> Activities and durations (days), with dependencies:
> - A (3) → B (4) → D (5) → End
> - A (3) → C (2) → D (5) → End

**Identify the paths:**
- Path 1: A → B → D = 3 + 4 + 5 = **12 days**
- Path 2: A → C → D = 3 + 2 + 5 = **10 days**

The **critical path is A → B → D = 12 days**. Project duration = 12 days.

**Float of C:** Path through C is 10 days; the project allows 12. C sits on a
path that is 2 days shorter, so:

- Total Float of C = 12 − 10 = **2 days**.
- B has Total Float = 0 (on the critical path), and so do A and D.

**Free float of C:** C must finish before D starts. If A ends day 3, C's
ES = day 4, EF = day 5. D's ES is driven by B (B finishes day 7), so D
starts day 8. Free float of C = (D's ES) − (C's EF) − 1 = 8 − 5 − 1 =
**2 days**. Here free float equals total float because C is the only
non-critical activity on its path.

### 3.3 Near-critical paths

A **near-critical path** is one whose length is close to the critical path
(here, Path 2 at 10 days is within 2 days of 12). It carries little float, so a
small slip can make it the new critical path. Monitor near-critical paths
almost as closely as the critical path.

---

## 4. Risk Quantification

### 4.1 Expected Monetary Value (EMV)

**EMV = Probability × Impact.** Threats are negative, opportunities positive.
Sum the EMVs of all risks for a total expected impact (the basis for
contingency reserve).

| Risk | Probability | Impact | EMV |
|---|---|---|---|
| Vendor delay (threat) | 30% | −$40,000 | −$12,000 |
| Scope rework (threat) | 50% | −$20,000 | −$10,000 |
| Early supplier discount (opportunity) | 20% | +$15,000 | +$3,000 |
| **Total EMV** | | | **−$19,000** |

Expected total impact = **−$19,000**, a reasonable contingency reserve figure.

### 4.2 Decision tree (worked)

> Choice: build a custom tool or buy an off-the-shelf one.
> - **Build:** costs $50,000. 60% chance it works fully (value $120,000);
>   40% chance it needs rework (value $70,000).
> - **Buy:** costs $30,000. 80% chance it fits (value $90,000); 20% chance it
>   needs add-ons (value $60,000).

EMV of each path = Σ (probability × outcome value), then subtract the
decision cost.

**Build branch:**
Expected value = 0.60 × 120,000 + 0.40 × 70,000 = 72,000 + 28,000 = 100,000.
Net EMV = 100,000 − 50,000 = **$50,000**.

**Buy branch:**
Expected value = 0.80 × 90,000 + 0.20 × 60,000 = 72,000 + 12,000 = 84,000.
Net EMV = 84,000 − 30,000 = **$54,000**.

**Decision: Buy** — its net EMV ($54,000) is higher.

### 4.3 Contingency reserve vs. management reserve

| | Contingency reserve | Management reserve |
|---|---|---|
| Covers | **Known** risks ("known-unknowns") | **Unknown** risks ("unknown-unknowns") |
| Sized by | Risk analysis (e.g., total EMV) | A policy %; engineering judgment |
| Part of cost baseline? | **Yes** | **No** (part of total project budget) |
| Spend it via | PM's authority | Requires management approval / change |

Cost baseline = work estimates + contingency reserve.
Total project budget = cost baseline + management reserve.

---

## 5. Procurement Math

### 5.1 Contract types recap

| Type | Who carries cost risk | Notes |
|---|---|---|
| **Fixed Price (FFP)** | Seller | Price locked; best when scope is clear |
| **Fixed Price Incentive Fee (FPIF)** | Shared, up to a ceiling | Has a PTA — see below |
| **Cost Plus Fixed Fee (CPFF)** | Buyer | Fee is a flat amount |
| **Cost Plus Incentive Fee (CPIF)** | Buyer (with share ratio) | Fee varies with performance |
| **Cost Plus Award Fee (CPAF)** | Buyer | Fee is subjective, buyer-judged |
| **Time & Materials (T&M)** | Buyer | Hybrid; good for staff augmentation |

### 5.2 Incentive fee / share ratio

In incentive contracts a **share ratio** (buyer : seller) splits the difference
between **target cost** and **actual cost**.

> CPIF: target cost $100,000, target fee $10,000, share ratio **80/20**
> (buyer/seller). Actual cost comes in at **$90,000**.

- Underrun = target cost − actual cost = 100,000 − 90,000 = $10,000.
- Seller's share of the underrun = 20% × 10,000 = $2,000 → seller's bonus.
- Final fee = target fee + share = 10,000 + 2,000 = **$12,000**.
- Total price to buyer = actual cost + final fee = 90,000 + 12,000 =
  **$102,000**.

(If costs *overran*, the share ratio splits the overrun and the seller's fee is
*reduced* by its share.)

### 5.3 Point of Total Assumption (PTA)

For an **FPIF** contract the PTA is the cost level above which the **seller
absorbs 100%** of every additional dollar — even though there is still a
ceiling price.

**PTA = Target Cost + [(Ceiling Price − Target Price) / Buyer's share ratio]**

> FPIF: Target cost $100,000, target fee $15,000 → **Target price $115,000**.
> Ceiling price $130,000. Share ratio **70/30** (buyer/seller), so buyer's
> share = 0.70.

PTA = 100,000 + [(130,000 − 115,000) / 0.70]
= 100,000 + [15,000 / 0.70]
= 100,000 + 21,429 = **$121,429**.

Interpretation: while actual cost stays below $121,429 the buyer and seller
share overruns 70/30. Once cost exceeds **$121,429**, the seller pays every
extra dollar, because the buyer's contribution has hit the ceiling price.

---

## 6. Communication Channels

The number of two-way communication links among **n** people:

**Channels = n(n − 1) / 2**

> A team has **6** people. Channels = 6 × 5 / 2 = **15**.

**The "added people" delta** — a classic trap. The question often gives a
team size, then *adds* members and asks for the *increase*.

> The 6-person team grows to **10** people. How many channels were *added*?

- New: 10 × 9 / 2 = **45**.
- Old: 6 × 5 / 2 = **15**.
- **Added channels = 45 − 15 = 30.**

Read carefully: "how many channels now" wants 45; "how many *new/added*" wants
30. If a question says "the project manager plus the team," count the PM in n.

---

## 7. Financial Selection Metrics

These help **choose between projects or options**. Decision rules:

| Metric | Better when | Decision rule |
|---|---|---|
| **NPV** (Net Present Value) | Higher | Pick highest NPV; reject NPV < 0 |
| **IRR** (Internal Rate of Return) | Higher | Pick highest IRR |
| **BCR** (Benefit-Cost Ratio) | Higher | Pick highest; BCR > 1 is viable |
| **Payback Period** | Shorter | Pick the shortest |
| **Depreciation** | n/a | Accounting allocation of asset cost |

**Definitions:**

- **NPV** — today's value of all future cash inflows minus outflows, discounted
  for the time value of money. A positive NPV adds value.
- **IRR** — the discount rate at which NPV = 0; the project's intrinsic
  percentage return.
- **BCR** — total benefits ÷ total costs. A ratio (cost-to-benefit, the inverse,
  is *lower-is-better* — read which one is given).
- **Payback period** — time for cumulative inflows to recover the initial
  investment. Ignores the time value of money and anything after payback.
- **Depreciation** — spreading a capital asset's cost over its useful life.
  **Straight-line:** equal amount each year = (Cost − Salvage) / Life.
  **Accelerated** (e.g., double-declining balance, sum-of-years'-digits): more
  expense in early years.

### 7.1 Worked selection example

> Three projects, choose one:

| Project | NPV | IRR | Payback |
|---|---|---|---|
| Alpha | $90,000 | 14% | 3 years |
| Beta | $120,000 | 11% | 4 years |
| Gamma | $120,000 | 18% | 2 years |

- By **NPV**: Beta and Gamma tie at $120,000 — higher is better, both beat
  Alpha.
- By **IRR**: Gamma (18%) wins.
- By **Payback**: Gamma (2 years) is shortest — best.

**Choose Gamma** — it ties on NPV and wins on IRR and payback. When metrics
*conflict*, the exam generally favors **NPV** as the primary measure because it
reflects absolute value added; use IRR/payback as tie-breakers.

### 7.2 Straight-line depreciation example

> Equipment costs $50,000, salvage value $5,000, useful life 5 years.

Annual depreciation = (50,000 − 5,000) / 5 = 45,000 / 5 = **$9,000 per year**.
Book value after year 2 = 50,000 − 2 × 9,000 = **$32,000**.

---

## 8. Exam Tips for Calculation Questions

- **Watch units and time periods.** Mixing months with weeks, or dollars with
  thousands, is the #1 careless error. Convert everything first.
- **Cumulative vs. current period.** EVM values are usually *cumulative to
  date*. If a question gives "this month's" PV/EV/AC, do not blend them with
  cumulative figures.
- **EV always comes first** in every variance and index. If you write AC − EV
  you have flipped the sign.
- **Sign convention:** negative variance = bad; index < 1 = bad; positive VAC =
  under budget. TCPI > 1 means you must work harder.
- **EAC — read the story, not just the numbers.** "Variance will continue" →
  BAC/CPI. "One-time event" → AC + (BAC − EV). "Both schedule and cost" →
  the CPI×SPI formula. "Original estimate was wrong" → AC + new ETC.
- **PERT weights M by 4**, divides by 6; triangular is a plain ÷3. Standard
  deviation is always (P − O) / 6.
- **Channels:** decide whether the question wants the *total* or the *added*
  count, and whether the PM is included in n.
- **Critical path = longest path; float on it = 0.** If asked for project
  duration, sum the longest path.
- **Decision trees / EMV:** subtract the *cost of the decision* from the
  expected value before comparing branches.
- **Don't over-round mid-calculation.** Keep 3–4 significant figures and round
  only the final answer; CPI especially compounds rounding error in EAC.
- **PTA:** the denominator is the **buyer's** share ratio, not the seller's.
- When metrics conflict in a selection question, **higher NPV** is the safest
  default; **shorter payback** and **higher IRR/BCR** are also "better."

---

## 9. Cross-References

- K1 — PMBOK 7 principles and performance domains (the "why").
- K2 — artifacts: where the cost baseline, schedule, and risk register live.
- K3 — exam logistics and the EVM summary table (§5).
- K4 — coaching on reasoning traps, including calculation carelessness.
