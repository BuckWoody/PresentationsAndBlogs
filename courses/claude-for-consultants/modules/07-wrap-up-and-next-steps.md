<img width="150" src="https://github.com/BuckWoody/presentations/blob/master/graphics/logo.png?raw=true"> 

# Workshop: Claude for Technical Consultants

## 07 - Wrap-Up and Next Steps

## Recap (retrieval practice,  try to answer before looking back)

1. What's the one rule from Module 01 that every other module builds on?
2. Name the four parts of a well-engineered technical prompt (Module 02).
3. What's a Project actually buying you over a one-off chat (Module 03)?
4. Why ask for ranked hypotheses instead of a single root cause (Module 04)?
5. Name one thing to check for before a customer-facing draft goes out (Module 05)?
6. What are the three separate questions behind "is it okay to paste this in?" (Module 06)?

*(Answers: 1,  Claude drafts, you decide. 2,  context, task, format, constraints. 3,  persistent custom instructions and reference files scoped to one engagement, so you're not re-pasting facts every time. 4,  a single confident answer doesn't feel like it needs a second look, even when it's wrong; ranked hypotheses with falsification criteria give you something to actually investigate. 5,  overpromising, invented specifics, or tone drift for the intended audience. 6,  is the data itself sensitive, does your contract with the customer allow it, and what does your specific plan's data agreement actually do with it.)*

## Where this goes next

Everything today ran in a browser tab, on purpose,  that's the right scope for a 2-hour introduction. Real consulting work sometimes outgrows it. Briefly, in order of how much additional setup they need:

- **Claude Code**,  an agentic command-line tool for delegating multi-step technical work (for example, having Claude work through a larger log file, write a small analysis script, or draft a batch of similar customer reports). Needs installation and, typically, an eligible subscription or API access.
- **The Claude API**,  for building Claude into your own tools or automations (a ticket-triage assistant, a report generator wired into your practice's own systems). Priced per token, requires a developer account and API key, and needs someone thinking about security the way Module 06 did, but for a system instead of a chat.
- **MCP (Model Context Protocol) connectors**,  let Claude read from and act on live systems (a ticketing system, a customer's telemetry, a knowledge base) instead of you pasting content in by hand. This is also where the prompt-injection risk from Module 06 gets sharper, since Claude is now touching live systems rather than just producing text for you to review,  the human-in-the-loop discipline from this workshop matters even more, not less, once this is in play.

None of these are "better" in the abstract,  they're the right next step only once a specific, recurring task in your own work outgrows a browser tab. If that happens, treat it as its own project with its own setup and its own review of Module 06's questions, not an afternoon add-on.

## Closing discussion prompt

As a group: what's one recurring task in your own consulting work,  not Contoso's,  where you can already picture using a Project the way Module 03 did? Naming a specific, real use case before you leave the room is the single best predictor of whether this actually gets used next week instead of being a one-time exercise.

## Keep going

- [`REFERENCES.md`](../REFERENCES.md),  curated references for every topic in this workshop, for whenever you want to go deeper than a 2-hour lab allows
- [`FACILITATOR-GUIDE.md`](../FACILITATOR-GUIDE.md),  if you're the one teaching this material to someone else next

Thank you for taking this workshop.
