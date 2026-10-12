# Answer Key: Flash-Sale Slowdown Root Cause (Module 04)

*This scenario was constructed around two intertwined root causes. A strong exercise output should surface both and explain the mechanism, not just restate the symptoms. This is a worked reference, not a substitute for your own session's reasoning.*

## Ranked hypotheses

### 1. Hot-page insert contention from the ever-increasing identity clustering key (primary driver)

**Supporting evidence:** `PAGELATCH_EX` is the single largest wait type (38.6% of total wait time), and the DBA's follow-up trace ties most of it to the last page of `dbo.Orders`' clustered index. `PAGEIOLATCH_SH`,  the disk-bound version of a similar wait,  is comparatively small, and CPU/disk queue length were both reported as unremarkable. That combination points at **in-memory latch contention on a single hot page**, not a disk bottleneck.

**Mechanism:** because `dbo.Orders` clusters on an ever-increasing `IDENTITY` value, every single insert targets the same last page of the same last extent. At normal traffic this rarely matters,  the latch is held so briefly it's invisible. At 3x concurrent checkout volume, many sessions queue up for the exact same page's latch simultaneously, and that queuing is what shows up as `PAGELATCH_EX` wait time. This is a classic "last-page insert hotspot" pattern, and it scales *non-linearly* with concurrency,  exactly matching a 3x traffic spike producing a dramatically disproportionate slowdown rather than a proportional one.

**Confirms:** wait-stats breakdown by page ID (already partially done,  the DBA's trace), or `sys.dm_os_waiting_tasks` captured live during a future event, showing many sessions queued on the same page ID.

**Rules out:** if a live capture instead showed contention spread across many different pages rather than concentrated on the last page, this wouldn't be the mechanism.

### 2. tempdb allocation contention from per-checkout temp tables (contributing, compounding factor)

**Supporting evidence:** repeated `tempdev` autogrow events throughout the window in the error log, and `PAGELATCH_EX` waits additionally correlating to tempdb's PFS/GAM/SGAM page ranges per the DBA's note,  plus the detail that `dbo.usp_CompleteCheckout` creates two local temp tables on every single execution.

**Mechanism:** creating and dropping temp tables at high frequency and high concurrency generates contention on tempdb's own metadata/allocation pages (a well-known tempdb scaling limitation, generally worse with fewer tempdb data files), and it's part of *why* tempdb kept growing during the event rather than settling at a stable size,  the sizing fix from "the last incident" addressed capacity, not the underlying allocation-contention pattern. This compounds the first issue: sessions already queued on the `Orders` hot page are additionally contending for tempdb resources on the same execution path.

**Confirms:** `sys.dm_db_file_space_usage` and tempdb-specific wait breakdowns captured live during a future event; a count of tempdb data files (the log mentions autogrow of a single file, `tempdev`,  one file is a common contributor to this exact pattern).

**Rules out:** if tempdb showed no unusual page contention and the temp tables turned out to be trivially small/short-lived even at 3x load, this would be a much smaller contributor than hypothesis 1.

### 3. Lock escalation/blocking on `dbo.Orders` / `dbo.OrderStatus` (largely a symptom, not an independent cause)

The `LCK_M_X` waits and the explicit "Lock request time out" message are real, but they're consistent with being **downstream of** hypotheses 1 and 2 rather than a third independent cause: sessions already stalled on page-latch and tempdb contention hold transactions open longer, which increases the surface area for ordinary write-write blocking on the same hot rows/pages. Worth stating this explicitly in your answer,  a strong RCA distinguishes a root cause from a downstream symptom of the other root causes.

## Remediation plan

**Short-term (before the next sale, ~3 weeks out):**
- Add additional tempdb data files (commonly recommended in multiples matching available cores, up to a practical limit) to reduce tempdb allocation-page contention,  a configuration change, not a code or schema change, so it's realistic in the timeframe.
- Review whether `#cartItems` / `#priceCalc` genuinely need to be temp tables on every execution, or could be replaced with table variables or restructured to reduce per-call allocation overhead, if a low-risk code change can be tested in time.

**Longer-term (structural fix):**
- Address the `dbo.Orders` hot-page pattern directly,  options to evaluate (each with real trade-offs, not a free win) include a different clustering key strategy (e.g., a key that spreads inserts, potentially at the cost of clustered range-scan performance elsewhere) or partitioning to spread the hot point across multiple pages. This is a schema-level change requiring careful testing and is not a three-week fix.
- Revisit the "informal, untested" RTO/RPO target from the scenario briefing while touching this system anyway,  a good consultant flags an adjacent risk they noticed, not just the one they were asked about.
