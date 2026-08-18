<img width="150" src="https://github.com/BuckWoody/presentations/blob/master/graphics/logo.png?raw=true"> 

# Workshop: Claude for Technical Consultants

## 03 - Solution Design Workflows

### Retrieval check

From Module 02: what are the four parts of a well-engineered technical prompt? *(Context, task, format, constraints.)* Today we scale that up from a single prompt to an entire engagement.

### From one-off chats to an engagement workspace

A one-off chat is fine for a quick question. Real consulting work is longer-lived than that,  you'll have the same customer facts relevant across a dozen conversations over days or weeks. Re-pasting the environment details every time is slow and error-prone (you *will* eventually paste the wrong version of a fact). This is exactly what a **Project** is for:

- **Custom instructions** set once,  the audience, the tone, standing constraints ("this customer is budget-conscious," "always flag anything that would need a maintenance window"),  and every conversation in the Project inherits them.
- **Uploaded reference files**,  the discovery notes, an architecture diagram description, a prior email thread,  become available to every conversation without re-pasting.
- Everything stays **scoped to that customer**, which also matters for the data-handling discussion in Module 06: a Project is a natural boundary for "what belongs to this engagement" versus "what doesn't."

### Using web search for solution design, responsibly

Solution design almost always means comparing options against current vendor capabilities,  and "current" is the operative word. Claude's training has a knowledge cutoff; product tiers, service limits, and feature availability all move faster than that. This is exactly when you want Claude to search rather than answer from memory,  ask it to, and look for the citations that show it did.

Two habits that keep this reliable:

- **Ask for trade-offs, not just a winner.** "Recommend one option" produces a shorter answer that's easier to be wrong about with no way for you to catch it. "Compare three options against these specific constraints, then recommend one and name the strongest objection to your own recommendation" produces something you can actually defend to a customer.
- **Feed it the customer's actual constraints, not a generic version of the problem.** A generic "should I move to Azure" question gets a generic answer full of hedges. Contoso's specific budget sensitivity, its informal RTO/RPO, and its one part-time DBA are what make a recommendation *theirs* instead of a rehash of a vendor's marketing page.

### Turning the output into something you can hand off

This is what **Artifacts** are for. When you ask for a document, a comparison table, or a diagram description, Claude renders it in its own panel,  easy to review, edit, export, or paste into your own deliverable template, instead of scraped out of a chat transcript. For a customer-facing design comparison, ask explicitly for it as a structured document (headers, a comparison table, a clearly separated recommendation section) so it becomes an Artifact rather than a wall of chat prose.

## Hands-On Exercise: Build the Modernization Comparison

**Goal:** Produce a first-draft solution-design Artifact for Contoso Retail's modernization question, using a Project as the engagement workspace.

1. Create a new Project named `Contoso Retail Engagement`.
2. Set custom instructions along these lines (adapt as you like):
   > *"You're assisting a technical consultant working with Contoso Retail, a budget-conscious mid-size retail customer. When asked for recommendations, always state trade-offs explicitly and flag your own uncertainty rather than sounding more confident than you are. This customer's audience for final documents ranges from a hands-on DBA to a non-technical VP,  ask which audience applies if it isn't obvious."*
3. Upload [`sample-data/customer-scenario-briefing.md`](../sample-data/customer-scenario-briefing.md) and [`sample-data/architecture-options-notes.md`](../sample-data/architecture-options-notes.md) to the Project.
4. In a new chat inside the Project, write a prompt that asks Claude to:
   - Search for current information on the realistic modernization paths available for a SQL Server 2019 workload (staying on-premises with upgrades, an infrastructure-as-a-service option, and a platform-as-a-service option)
   - Compare them specifically against Contoso's stated constraints (budget sensitivity, no big-bang preference, informal RTO/RPO, single part-time DBA)
   - Produce the comparison as a structured Artifact: a comparison table plus a short recommendation section
   - Explicitly name the strongest argument *against* whatever it recommends
5. Read the result critically:
   - Is anything stated with more precision or confidence than you'd be comfortable defending to Priya's VP? Circle it.
   - Did it use the specific Contoso constraints, or could you swap in any customer's name and the answer wouldn't change? If the latter, that's a sign to iterate the prompt with more specific constraints rather than accepting a generic answer.
   - Pick one specific claim (a service limit, a pricing figure, a named feature) and note what you'd check against official documentation before this goes in front of Contoso.
6. If time allows, iterate once: ask Claude to revise the Artifact assuming the customer's leadership explicitly rejects any option requiring a "big bang" cutover, and see how the recommendation shifts.

Compare your Artifact against [`answer-key/03-solution-comparison-example.md`](../answer-key/03-solution-comparison-example.md),  not to check for an exact match, but to see whether the shape (trade-offs stated, constraints reflected, uncertainty flagged) lines up.

**Checkpoint:** Keep this Project open,  Module 04 continues in it with the troubleshooting incident.

## Next Steps

Continue to [*04 - Troubleshooting and Optimization Workflows*](04%20-%20Troubleshooting%20and%20Optimization%20Workflows.md).
