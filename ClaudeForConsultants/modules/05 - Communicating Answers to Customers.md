<img width="150" src="https://github.com/BuckWoody/presentations/blob/master/graphics/logo.png?raw=true"> 

# Workshop: Claude for Technical Consultants
## 05 - Communicating Answers to Customers

### Retrieval check

From Module 04: what's the risk of asking for a single root cause instead of ranked hypotheses? *(You get one plausible-sounding answer with no visible alternative, and a fluent wrong answer doesn't feel like it needs a second look.)* The same fluency risk shows up again here, aimed at a different audience: a confident, well-written customer email is not the same thing as a *correct* one.

### One set of facts, two audiences

Look back at Priya's email from Module 04's scenario: she needs two different things from the same incident,  something she can act on with her DBA, and something she can say to her VP who "does not want to hear the word 'latch.'" This is one of the clearest wins for AI-assisted drafting: **the underlying facts don't change, but the register, depth, and vocabulary should shift completely** depending on who's reading.

Rather than writing both by hand, or writing one and awkwardly trimming it for the other audience, ask Claude for both explicitly, as separate drafts, with the audience named:

> *"Draft two things from the root-cause analysis above: (1) a technical email to the customer's DBA, including the specific mechanism and both the short-term mitigation and long-term fix; (2) a 5-bullet executive summary for a non-technical VP,  no jargon, no wait-type names, focused on impact and what's being done about it."*

### What to check before anything goes out

A fluent draft earns scrutiny in three specific places:

- **Overpromising.** Does the draft commit to a timeline, an SLA, or a guarantee ("this will fully resolve the issue") that you haven't actually verified you can back? Soften anything that reads as a promise you didn't intend to make.
- **Invented specifics.** Watch for numbers, dates, or names that sound plausible but that you didn't provide,  a draft can quietly "fill in" a detail that was never in the source material. If you can't point to where a fact came from, don't send it.
- **Tone drift.** An executive summary that's still full of technical hedging reads as evasive to a VP; a technical email that's been oversimplified reads as condescending to a DBA. Read each draft *as that specific reader* before approving it.

### The review checkpoint is not optional

This is the moment where "Claude drafts, you decide" from Module 01 becomes a literal, concrete step: **read every word of a customer-facing draft before it goes out, every time, with no exceptions for time pressure.** The entire value of this workflow depends on that discipline holding,  the moment it doesn't, you've handed judgment to a tool that has none of the accountability you do.

## Hands-On Exercise: Draft Two Audience-Tailored Communications

**Goal:** Turn Module 04's root-cause analysis into two real deliverables, then review both like you're about to hit send.

1. Still in the `Contoso Retail Engagement` Project, in the same chat (or a new one referencing your Module 04 findings), upload or paste [`sample-data/customer-email-original-complaint.txt`](../sample-data/customer-email-original-complaint.txt) so Claude can see exactly what Priya asked for and how she phrased it.
2. Ask for the technical DBA-facing email first. Require: the specific mechanism (in plain-enough language that a working DBA who isn't an internals expert can follow it), the short-term mitigation, and the longer-term structural fix.
3. Ask for the executive summary second, as a separate draft, explicitly barring jargon and wait-type names, framed around business impact and next steps.
4. **Review both as if you were about to send them:**
   - In the technical email: is the mechanism actually explained, or just asserted? Would Contoso's DBA be able to act on it?
   - In the executive summary: could Priya's VP read it in 30 seconds and understand what happened and what's being done, with zero SQL Server knowledge?
   - In either draft: circle anything that promises a specific timeline or outcome you (as the consultant) haven't actually committed to.
5. Make at least one real edit to each draft based on something you found in step 4,  even a small one. The point is practicing the review, not producing a perfect first draft.
6. Compare against [`answer-key/05-customer-email-example.md`](../answer-key/05-customer-email-example.md) and [`answer-key/05-executive-summary-example.md`](../answer-key/05-executive-summary-example.md).

**Checkpoint:** Could you defend every sentence in your final technical email if Contoso's DBA pushed back on it? If there's a sentence you couldn't defend, that's the one to cut or soften before this exercise counts as "done."

## Next Steps

Continue to [*06 - Security, Privacy, and Cost Awareness*](06%20-%20Security%2C%20Privacy%2C%20and%20Cost%20Awareness.md).
