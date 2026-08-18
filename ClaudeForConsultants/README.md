<img width="150" src="https://github.com/BuckWoody/presentations/blob/master/graphics/logo.png?raw=true"> 

# Workshop: Claude for Technical Consultants

## Solution Design, Troubleshooting, and Customer Communication

#### *A hands-on lab for Technical Consultants*

## About this Workshop

Welcome to this hands-on lab on using **Claude** (Anthropic's AI assistant) effectively in the day-to-day work of a Technical Consultant. In this workshop, you'll learn how to use Claude.ai,  specifically **Projects**, **Artifacts**, and **web search**,  to design customer solutions, troubleshoot and optimize customer systems, and turn technical findings into clear, audience-appropriate answers for customers.

The focus of this workshop is understanding **how to use an AI assistant as a force multiplier in consulting work without outsourcing your judgment to it**,  you stay the engineer of record; Claude accelerates research, drafting, and structured thinking.

You'll start with an orientation to the current Claude model lineup and the Claude.ai workspace, then move through a single running customer scenario,  a retail company called **Contoso Retail** running SQL Server,  that carries you through solution design, troubleshooting, and customer communication, before closing with the security, privacy, and cost considerations you need to raise with your own account team before using any AI tool on real customer data. There's a focus throughout on how to extrapolate what you learn here to other customer engagements, technologies, and consulting scenarios beyond SQL Server.

This README explains how the workshop is laid out, what you'll learn, and the tools you'll use. To get this lab onto your own machine, use the **Code → Download ZIP** button on the repo page, or clone it with `git clone`.

### Learning Objectives

In this workshop you'll learn to:

- Choose the right Claude model and Claude.ai feature (Projects, Artifacts, web search) for a given consulting task
- Write prompts that get accurate, usable technical output on the first or second try
- Set up a Claude Project as a persistent, contextualized workspace for a customer engagement
- Use Claude to research and compare solution options and produce a shareable design artifact
- Use Claude as a structured, hypothesis-driven troubleshooting partner,  without outsourcing verification
- Draft audience-appropriate customer communications (technical and executive) from the same underlying facts
- Classify customer data by sensitivity and know what's safe to put into an AI tool, what needs sanitizing, and what needs a different plan entirely
- Reason about the cost model of Claude.ai vs. the API, so you can speak sensibly with customers who ask about it

This workshop trains **Technical Consultants**,  the people who sit between a product and a customer's live environment, doing solution design, troubleshooting/optimization, and technical communication as their core job.

The concepts and skills taught in this workshop form the starting points for:

```
Technical Consultants and Solution Architects, to use AI assistance responsibly and effectively
across the full lifecycle of a customer engagement,  from initial design through
troubleshooting to the final customer-facing writeup.

Support Engineers and Premier/Unified Support delivery staff, who do similar
troubleshooting-and-communication work under time pressure.

Consulting practice leads and enablement teams, who need a template for how their
organization expects AI tools to be used on customer engagements.
```

## Business Applications of this Workshop

Consulting organizations run on billable hours and customer trust. Every hour a consultant spends re-deriving a well-known architecture trade-off, hunting through documentation for the right wait-type explanation, or wordsmithing a customer email is an hour not spent on the judgment calls that actually require a human expert. Used well, an AI assistant compresses the research-and-drafting time around those judgment calls; used badly, it produces confident-sounding technical claims that are wrong, or it ends up holding data it should never have seen.

Industry examples where this matters: a **retail** customer's checkout system slowing down during a flash sale, a **financial services** customer asking for a migration comparison under strict compliance constraints, a **healthcare** customer's reporting database needing a performance root-cause analysis that must be defensible in a written summary to their leadership. The pattern,  design, troubleshoot, communicate,  repeats across every industry a consulting practice serves.

## Technologies used in this Workshop

The solution includes the following tools. You aren't limited to these for your own work,  by the end of the workshop you'll understand how to extend this approach to Claude Code, the Claude API, and MCP connectors when a task outgrows the Claude.ai web experience.

| Technology | Description |
|---|---|
| A modern web browser (Chrome, Edge, or Firefox) | The only client software required,  everything runs at claude.ai |
| Claude.ai (Anthropic), Pro plan or higher | The AI assistant itself, plus the Projects and Artifacts features this lab depends on |
| Web search (built into Claude.ai) | Used for solution-design research against current vendor documentation |
| SQL Server sample scenario (Contoso Retail) | The running case study used for the hands-on exercises,  no SQL Server installation is required; all sample data is provided as text files |

## Before Taking this Workshop

You'll need a web browser and the ability to sign up for (or already hold) a **Claude Pro** account or higher. No local software installation, no API key, and no cloud subscription of your own beyond Claude.ai are required.

This workshop assumes you're already comfortable with:

- General IT/database troubleshooting concepts (reading a log file, interpreting a metrics table),  deep SQL Server expertise is *not* required; the scenario is written to be followable by any technical consultant
- Working in a modern web application (tabs, file upload, copy/paste)
- Your own organization's customer-data handling policy, or knowing who to ask about it

If you're new to Claude entirely, a few references are worth a skim before class:

- [Claude Overview,  Anthropic](https://claude.com)
- [Claude Help Center](https://support.claude.com)
- [Prompt Engineering Overview,  Anthropic](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview)

### Setup

**A full pre-requisites document is located here: [00 - Pre-Requisites](modules/00%20-%20Pre-Requisites.md).** Complete this before the workshop starts,  class time is scheduled tightly around a 2-hour format and there isn't room to do account setup live. *Use our company's Claude Team or Enterprise seat instead of a personal Pro account so your work stays inside our data agreement,  see Module 06 for why this matters. While this workshop uses a fictional company example for training, some of the details you use in the prompts and code may be sensitive.*

## Workshop Details

| | |
|---|---|
| **Primary Audience:** | Technical Consultants tasked with designing, troubleshooting, and communicating about customer solutions |
| **Secondary Audience:** | Solution Architects, Premier/Unified Support engineers, consulting practice leads |
| **Level:** | 200 (assumes general technical/consulting experience; no prior AI tool experience assumed) |
| **Type:** | In-person or virtual, instructor-led, hands-on lab |
| **Length:** | 2 hours |

## Workshop Modules

This is a modular workshop. Each module below is designed for **up to 15 minutes of lecture**, immediately followed by a **hands-on exercise**, so no single stretch of "watching a slide" runs longer than about a quarter of an hour. Suggested timings are guidelines,  we may flex them by a few minutes either way as the class needs.

| **Module** | **Topics** | **Suggested Timing** |
|---|---|---|
| [00 - Pre-Requisites](modules/00%20-%20Pre-Requisites.md) | Account setup, feature checks, sample data download,  **complete before class** | Self-paced, before class |
| [01 - Orientation and the Claude Model Lineup](modules/01%20-%20Orientation%20and%20the%20Claude%20Model%20Lineup.md) | What Claude is, current model lineup and when to use each, the Claude.ai workspace tour | Lecture 8 min + Exercise 7 min |
| [02 - Prompting for Technical Accuracy](modules/02%20-%20Prompting%20for%20Technical%20Accuracy.md) | Anatomy of a good technical prompt, context/task/format/constraints, verifying output | Lecture 10 min + Exercise 10 min |
| [03 - Solution Design Workflows](modules/03%20-%20Solution%20Design%20Workflows.md) | Projects as engagement workspaces, research with web search, producing a design Artifact | Lecture 10 min + Exercise 13 min |
| [04 - Troubleshooting and Optimization Workflows](modules/04%20-%20Troubleshooting%20and%20Optimization%20Workflows.md) | Hypothesis-driven troubleshooting with diagnostic data, avoiding the first-plausible-answer trap | Lecture 10 min + Exercise 13 min |
| [05 - Communicating Answers to Customers](modules/05%20-%20Communicating%20Answers%20to%20Customers.md) | Audience-tailored drafting, tone control, the human-review checkpoint before sending | Lecture 8 min + Exercise 10 min |
| [06 - Security, Privacy, and Cost Awareness](modules/06%20-%20Security%2C%20Privacy%2C%20and%20Cost%20Awareness.md) | Data classification, Pro vs. Team/Enterprise data handling, prompt injection awareness, cost model | Lecture 10 min + Exercise 8 min |
| [07 - Wrap-Up and Next Steps](modules/07%20-%20Wrap-Up%20and%20Next%20Steps.md) | Recap, extending the workflow with Claude Code/API/MCP, where to go deeper | Lecture 5 min + Discussion 5 min |

**Total in-class time: ~120 minutes (2 hours).**

Supporting materials:

- [`sample-data/`](sample-data) - The Contoso Retail scenario files used across Modules 03–06
- [`answer-key/`](answer-key) - Worked examples of what a strong exercise output looks like, for self-check or instructor use
- [`REFERENCES.md`](REFERENCES.md) - Curated references for going deeper on every topic in this workshop

## Next Steps

Next, continue to [*Pre-Requisites*](modules/00%20-%20Pre-Requisites.md).

## Legal Notices

**Contoso Retail** is a fictitious company used purely as a teaching scenario, in the same tradition as Microsoft's long-standing use of "Contoso" in its own training materials. No real customer data is used or required anywhere in this workshop.

This workshop discusses Anthropic's Claude products and refers to Anthropic's public documentation and pricing pages. It is not published by, reviewed by, or endorsed by Anthropic; product names, plan names, and pricing are Anthropic's and are subject to change,  always verify current details at [claude.com](https://claude.com) and [docs.claude.com](https://docs.claude.com).
