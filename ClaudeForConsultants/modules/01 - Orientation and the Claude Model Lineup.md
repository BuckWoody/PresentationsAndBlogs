<img width="150" src="https://github.com/BuckWoody/presentations/blob/master/graphics/logo.png?raw=true"> 

# Workshop: Claude for Technical Consultants

## 01 - Orientation and the Claude Model Lineup

### Why this matters to your job specifically

You already know how to design solutions, troubleshoot systems, and write up findings for customers,  that's your job today, without AI. What changes with Claude in the loop is *where your time goes*: less time on research-and-drafting mechanics, more time on the judgment calls that are actually why the customer hired a consultant instead of reading documentation themselves. This workshop is built around that reallocation, using one thread,  a fictitious customer, **Contoso Retail**,  from solution design through troubleshooting to the final customer email.

The one rule that sits underneath everything today: **Claude drafts, you decide.** Nothing you produce with Claude in this lab goes to a customer without your review. That's not a disclaimer,  it's the actual skill being taught.

### The current Claude model family

As of this workshop, Anthropic organizes Claude into a small set of tiers, each suited to a different kind of work:

| Tier | What it's for | Where you'll notice it |
|---|---|---|
| **Claude Haiku 4.5** | Fastest and cheapest; near-frontier intelligence for high-volume or latency-sensitive work | Rarely something you pick directly in Claude.ai,  matters more when building automation later |
| **Claude Sonnet 5** | The default, balanced model,  frontier-level intelligence for coding, agents, and everyday enterprise work | **This is what you'll use for almost everything today** |
| **Claude Opus 5** | The flagship for complex agentic coding and the hardest enterprise reasoning tasks | You must get approval to use this model. Costs are tracked. |
| **Claude Fable 5 / Claude Mythos 5** | The most capable tier, positioned for long-running agentic work; Mythos shares Fable's capability without some safety classifiers and is limited-release | You must get approval to use this model. Costs are tracked. |

Two things worth knowing as a consultant, not a model-spec collector:

1. **The default model on Claude.ai is almost always the right choice.** Don't spend engagement time picking a model unless you have a specific reason,  a genuinely hard, long, multi-step reasoning problem,  to reach for a heavier tier.
2. **Model names and pricing change on a timescale of months, not years.** If a customer asks you which model to use, or what something costs, the honest answer is "let me check the current docs with you",  treat [docs.claude.com](https://docs.claude.com) and [claude.com/pricing](https://claude.com/pricing) as the source of truth, not your memory of this information.

### The three Claude.ai features this workshop uses

- **Projects**,  a persistent workspace scoped to one engagement or customer, holding custom instructions and reference files that every conversation in that Project can see. Think of it as the equivalent of a well-organized engagement folder that Claude actually reads.
- **Artifacts**,  a separate panel where Claude renders substantial output (a document, a table, a diagram, a small app) so it's easy to view, edit, and hand off, instead of being buried in chat scroll.
- **Web search**,  lets Claude look up current information rather than relying only on what it learned during training, which matters a great deal for anything version-specific (a product feature, a pricing page, a compliance requirement).

We're deliberately *not* using Claude Code, the API, or MCP connectors today,  those are real, powerful tools, and Module 07 points you toward them, but they add setup overhead (API keys, command-line tooling, billing) that this 2-hour format doesn't have room for. Everything today runs in a browser tab.

### A word on accuracy

Claude is very good at producing fluent, confident-sounding technical text,  including fluent, confident-sounding text that is *wrong*. It can misremember an exact DMV column name, invent a plausible-but-nonexistent configuration setting, or state a deprecated behavior as current. This isn't a flaw specific to Claude; it's true of every current LLM. The skill this workshop teaches is treating Claude as a very fast, very well-read colleague whose specific factual claims you verify before they reach a customer,  not as an oracle.

## Hands-On Exercise: Workspace Tour

**Goal:** Get comfortable navigating the three features you'll use all day, before any exercise depends on you finding them under time pressure.

1. Open [claude.ai](https://claude.ai) and start a new chat.
2. Ask Claude: *"I'm a technical consultant working on a SQL Server performance question for a retail customer. In two sentences, what's the difference between when I should use a Project versus a one-off chat for this kind of work?"* Read the answer,  you'll test whether you agree with it by the end of the day.
3. Open **Projects** in the sidebar and create a new Project named `Orientation Test`. Add one line of custom instructions: `Answer like you're briefing a technical consultant,  be direct, flag uncertainty, and don't pad your answers.` This is a preview of what you'll do for real in Module 03.
4. Inside that Project, ask: *"Search the web and tell me today's date and one current Claude model name I haven't heard of yet."* Confirm it actually searches rather than answering purely from memory,  look for a visible citation or search indicator.
5. Ask: *"Create an Artifact: a markdown table comparing Claude Haiku 4.5, Sonnet 5, and Opus 5 on speed, cost, and 'best for.'"* Confirm it opens in a separate panel, not just inline text.
6. Delete the `Orientation Test` Project (or leave it,  it won't interfere with anything later) and move on.

**Checkpoint:** Before continuing, everyone in the room should be able to say where Projects, Artifacts, and web search live in the interface. If something didn't work, flag it now,  Module 03 assumes this all works.

## Next Steps

Continue to [*02 - Prompting for Technical Accuracy*](02%20-%20Prompting%20for%20Technical%20Accuracy.md).
