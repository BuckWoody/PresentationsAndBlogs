<img width="150" src="https://github.com/BuckWoody/presentations/blob/master/graphics/logo.png?raw=true"> 

# Workshop: Claude for Technical Consultants

## 02 - Prompting for Technical Accuracy

### Retrieval check

Before new material: from Module 01, what's the one rule underneath everything today? *(Claude drafts, you decide.)* Keep that in mind,  good prompting is what makes the "draft" worth reviewing quickly instead of rewriting from scratch.

### The anatomy of a prompt that gets useful technical output

A vague prompt gets a vague, generically-correct-but-useless answer. Compare:

> ❌ "Why is my SQL Server slow?"

> ✅ "A retail customer's SQL Server 2019 Standard Edition instance (4 vCPU, 32GB RAM) shows checkout-transaction slowdowns specifically during flash-sale traffic spikes. I'll paste error log and wait-stats excerpts below. Rank the three most likely root causes by probability, and for each, tell me exactly what additional evidence would confirm or rule it out. Assume I know SQL Server but don't assume I've already ruled anything out."

The second prompt works better for four reasons that generalize to almost any technical prompt you'll write today:

1. **Context**,  the specific environment, not a generic one. Model, edition, sizing, symptom, timing.
2. **Task**,  a precise verb ("rank... by probability"), not an open-ended one ("help me understand").
3. **Format**,  how you want the answer structured (ranked list, with confirming/ruling-out evidence per item), so you're not stuck reformatting a wall of prose before you can use it.
4. **Constraints**,  what to assume and what not to ("don't assume I've already ruled anything out"),  this single line does more to prevent Claude from jumping straight to its first guess than almost anything else you can add.

### Techniques worth having on hand

- **Give an example of what good output looks like**, especially for anything with a house style (a customer email format, an RCA template). Claude follows a shown pattern far more reliably than a described one.
- **Ask for the reasoning, not just the answer**, when the stakes are high: "before you give your recommendation, walk through the trade-offs you're weighing." This surfaces the assumptions you need to check.
- **Ask Claude to flag its own uncertainty.** A line like "if you're not confident about a specific number, name, or setting, say so explicitly instead of stating it plainly" measurably reduces the chance a wrong detail slides through unflagged,  though it doesn't eliminate the need for you to verify.
- **Iterate rather than starting over.** If the first answer is close, say what's wrong with it specifically ("the executive summary is still too technical,  cut the DMV names entirely") rather than re-describing the whole task from scratch.
- **Use a Project's custom instructions for anything you'd otherwise repeat every time**,  the audience, the tone, the standing constraints of an engagement. You'll do exactly this in Module 03.

### The other half of the skill: verifying

However good the prompt, verify anything that would be embarrassing or costly if wrong before it leaves your hands:

- **Version-specific claims** (an exact setting name, a DMV column, a feature's availability in a specific edition),  check against current official documentation.
- **Numbers presented with false precision**,  "this typically resolves 73% of cases like this" is a sentence pattern Claude can produce without a real source behind the number. If you can't trace where a specific figure came from, don't repeat it to a customer as fact.
- **Anything that sounds suspiciously definitive about a fast-moving product area**,  pricing, licensing terms, service limits,  these change often enough that "sounds right" isn't a substitute for checking the current source.

## Hands-On Exercise: Rewrite a Vague Prompt

**Goal:** Practice writing a prompt with context, task, format, and constraints,  and see the output difference for yourself.

1. Start a new chat (not inside a Project yet,  that's Module 03).
2. Open [`sample-data/architecture-options-notes.md`](../sample-data/architecture-options-notes.md) and skim the Contoso Retail environment facts,  you'll reuse this file for the rest of the day.
3. **Send the vague version first:** ask Claude *"Why is my SQL Server slow?"* with no other context. Read the answer,  notice how generic it has to be, because it has nothing to work with.
4. **Now send an engineered version.** Using the four-part structure from the lecture, write your own prompt that includes:
   - The specific Contoso environment facts from the notes file (paste the relevant lines)
   - A precise task ("rank the three most likely..." or similar,  your choice)
   - A requested output format
   - At least one explicit constraint (what to assume / not assume, or a request to flag uncertainty)
5. Compare the two answers side by side. In one sentence each, write down: what did the engineered prompt get you that the vague one didn't, and is there anything in the engineered answer you'd want to verify before repeating it to a customer?
6. **Optional stretch:** ask Claude to critique your own prompt,  *"What's one way you'd improve the prompt I just gave you, if I asked you again on a harder version of this problem?"*

**Checkpoint:** Compare your before/after with a neighbor if time allows. The point isn't that everyone's engineered prompt looks identical,  it's that everyone can point to *which specific addition* changed the answer's usefulness.

## Next Steps

Continue to [*03 - Solution Design Workflows*](03%20-%20Solution%20Design%20Workflows.md).
