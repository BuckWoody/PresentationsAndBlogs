<img width="150" src="https://github.com/BuckWoody/presentations/blob/master/graphics/logo.png?raw=true"> 

# Workshop: Claude for Technical Consultants

## 04 - Troubleshooting and Optimization Workflows

### Retrieval check

From Module 03: name one habit that keeps a Claude-assisted design comparison honest. *(Ask for trade-offs and the strongest counter-argument, not just a winner; feed it the customer's real constraints.)* Troubleshooting has its own version of the same discipline.

### The first-plausible-answer trap

Given a pile of symptoms, Claude,  like a human under time pressure,  will readily produce *a* plausible root cause. The risk isn't that it's dumb; it's that it's fluent enough that a plausible-sounding first answer doesn't feel like it needs a second opinion. Good troubleshooting, with or without AI, means resisting that pull. The fix is structural, not a matter of trying harder: **explicitly ask for multiple ranked hypotheses with their falsification criteria**, not a single diagnosis.

A prompt shape that works well:

> *"Given this evidence, list the three most likely root causes, ranked by probability. For each one, state (a) what in the evidence supports it, (b) what additional evidence would confirm it, and (c) what would rule it out. Don't collapse to a single answer,  I want to investigate in parallel."*

This does two things: it forces Claude to show its reasoning against the actual evidence (making it easier for you to spot a reach), and it gives you a concrete next step for each hypothesis instead of one untested guess.

### Claude as a second pair of eyes, not the instrument

Claude cannot query a live system, run a trace, or see anything you don't paste in. Every conclusion it offers is only as good as the evidence you gave it,  and it doesn't know what you *didn't* give it unless you tell it. Two habits that keep this grounded:

- **Tell it what you don't have**, not just what you do. "I don't have a live trace of blocking chains, only this point-in-time wait-stats snapshot" changes how much weight Claude should (and, if prompted well, will) put on any single conclusion.
- **Never apply a suggested fix to a live customer system without independently understanding why it should work.** If Claude's explanation doesn't make sense to you once you think it through, that's a signal to dig further,  not to trust the model over your own judgment, and not to dismiss it without checking either.

### Reading this incident's evidence with fresh eyes

Before the exercise, notice the shape of what's in `sample-data/`: an error log full of tempdb autogrow events and a lock timeout, a wait-stats snapshot dominated by `PAGELATCH_EX` and `LCK_M_X`, and a DBA's own note about a stored procedure that creates temp tables on every checkout and a table with an ever-increasing identity clustering key. None of that is an accident,  it's a deliberately constructed, internally consistent incident so that the exercise rewards actually reading the evidence, the same way a real incident would.

## Hands-On Exercise: Diagnose the Flash-Sale Slowdown

**Goal:** Produce a ranked, evidence-linked root-cause analysis for the Contoso checkout slowdown, inside the same Project you built in Module 03.

1. Still inside the `Contoso Retail Engagement` Project, start a new chat.
2. Upload (or paste the contents of) [`sample-data/sql-server-error-log-excerpt.txt`](../sample-data/sql-server-error-log-excerpt.txt) and [`sample-data/wait-stats-sample.txt`](../sample-data/wait-stats-sample.txt).
3. Write a prompt using the ranked-hypothesis shape from the lecture. Be specific: mention that this happened during a flash sale (~3x normal load), and that CPU and disk queue length were reported as unremarkable by the customer's DBA.
4. Read the response and check it against the evidence yourself:
   - Does the ranking make sense given that `PAGELATCH_EX` (not `PAGEIOLATCH_SH`) dominates the wait stats,  meaning this points toward in-memory contention (hot pages, tempdb allocation contention), not disk I/O?
   - Did it connect the temp-table-per-checkout detail and the ever-increasing identity clustering key to *why* those specific waits would show up under 3x concurrent load, or did it just restate the symptoms back at you?
   - Ask a follow-up if needed: *"Be more specific about the mechanism,  why would an ever-increasing identity clustering key cause PAGELATCH_EX contention specifically, and why would this get dramatically worse at 3x concurrency rather than scaling smoothly?"*
5. Ask for a short-term remediation plan appropriate for "three weeks until the next sale" (per the customer's actual email, which you'll use in Module 05),  versus a longer-term structural fix. This distinction (band-aid vs. real fix) is something you should expect to prompt for explicitly; it won't always volunteer it.
6. Compare your output against [`answer-key/04-troubleshooting-rca-example.md`](../answer-key/04-troubleshooting-rca-example.md). The answer key names the two intertwined root causes this scenario was built around,  check whether your own session found both, and whether it correctly separated the quick mitigation from the real fix.

**Checkpoint:** You should now be able to explain, in your own words and without re-reading the answer key, *why* an ever-increasing identity key and a temp-table-heavy stored procedure would both produce exactly this wait-stats signature under a traffic spike. If you can't yet, that's the thing to nail down before Module 05,  you're about to have to explain it to someone else.

## Next Steps

Continue to [*05 - Communicating Answers to Customers*](05%20-%20Communicating%20Answers%20to%20Customers.md).
