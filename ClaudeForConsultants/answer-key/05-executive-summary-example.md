# Answer Key: Executive Summary for Priya's VP (Module 05)

*Worked example,  check yours for zero jargon and a clear "what's being done" close, not for matching wording.*

---

**Subject: Saturday's checkout slowdown,  what happened and what we're doing**

- **What happened:** During Saturday's flash sale, order volume roughly tripled for about two hours, and the database briefly couldn't keep up,  that's what caused the slow checkouts and errored carts.
- **Why:** Two specific technical bottlenecks in how the system handles a surge of simultaneous orders, which we've identified precisely from the system's own logs.
- **Before the next sale:** We're making a low-risk configuration change this week that directly addresses one of the two bottlenecks, and reviewing a targeted code change for the second.
- **The complete fix:** requires a larger structural change to how order data is stored,  this is a real project, not a quick patch, and we'll bring options and trade-offs to your team rather than rushing it before the next sale.
- **One related item we noticed:** your backup/recovery targets have never actually been tested. Not connected to Saturday, but worth a short conversation soon.

Happy to walk your team through the technical detail separately if useful,  this version is meant to be the two-minute read.
