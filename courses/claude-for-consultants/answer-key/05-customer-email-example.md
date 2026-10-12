# Answer Key: Technical Email to Contoso's DBA (Module 05)

*Worked example,  check your own draft for the same qualities (mechanism actually explained, mitigation vs. structural fix separated, no invented specifics) rather than matching this wording.*

---

**Subject: RCA,  Saturday's checkout slowdown, plus what we're recommending before the next sale**

Hi [DBA name],

Here's what we found from the error log and wait-stats snapshot you sent over.

**What happened:** two related things compounded during the traffic spike. First, `dbo.Orders` clusters on an ever-increasing identity value, so every insert lands on the same last page,  under normal load that's invisible, but at roughly 3x concurrent checkout volume, sessions started queuing for that same page, which is what shows up as the `PAGELATCH_EX` waits dominating your snapshot (38.6% of total wait time). Second, `usp_CompleteCheckout` creates two temp tables on every execution, and at the same elevated concurrency this drove the tempdb autogrow events you saw repeating through the error log,  tempdb allocation contention on top of the Orders hot page. The lock timeouts and blocking you saw on Orders/OrderStatus look like a downstream symptom of both of the above holding transactions open longer, rather than a separate root cause.

**Before the next sale (three weeks out), we'd recommend:**
1. Add tempdb data files (a config change, no code or schema risk) to reduce the allocation contention we saw in the log.
2. We'd like to review whether the two temp tables in `usp_CompleteCheckout` can be lightened or restructured,  we'll follow up separately once we've looked at the procedure itself, since this needs testing before it touches production.

**Structural, not urgent-for-three-weeks:** the real fix for the Orders hot-page pattern is a clustering-key or partitioning change, which is a real project with trade-offs to walk through together,  not something to rush in before Saturday's sale. We'll bring options to our next working session.

One more thing we noticed while in here, unrelated to Saturday: your RTO/RPO target is informal and untested. Worth a conversation on its own.

Happy to walk through any of this live if that's easier than email.

[Your name]
