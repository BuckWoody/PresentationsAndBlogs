<img width="150" src="https://github.com/BuckWoody/presentations/blob/master/graphics/logo.png?raw=true"> 

# Workshop: Claude for Technical Consultants

## References

Here are some curated resources for going deeper on each module's topic. Anthropic's own products, policies, and pricing change often,  treat every Anthropic link below as the current source of truth over anything stated in this workshop's modules.

## Claude fundamentals (Modules 01–02)

- [Claude Overview](https://claude.com),  Anthropic's product family, current as of when you visit
- [Claude Platform Docs,  Intro to Claude](https://platform.claude.com/docs/en/intro),  the current model lineup, straight from Anthropic
- [Prompt Engineering Overview](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview),  the ideas behind Module 02, in more depth
- [Claude Help Center](https://support.claude.com),  Projects, Artifacts, web search, and every other Claude.ai feature, documented for end users

## Solution design and Projects (Module 03)

- [Claude Help Center](https://support.claude.com),  search for "Projects" for current setup and sharing behavior
- Your own organization's Azure/cloud platform documentation for whatever comparison you actually need,  this workshop deliberately didn't hardcode specific service names because they move faster than a training document should try to keep up with

## Troubleshooting the Contoso scenario, for real (Module 04)

These are the genuine, non-fictitious Microsoft Learn references behind the incident used in this workshop,  worth reading even if you never touch SQL Server day to day, because the reasoning pattern (latch contention → hot page → concurrency-driven, not I/O-driven) generalizes to plenty of other platforms:

- [Recommendations to reduce allocation contention in SQL Server tempdb database](https://learn.microsoft.com/en-us/troubleshoot/sql/database-engine/performance/recommendations-reduce-allocation-contention)
- [tempdb Database (SQL Server)](https://learn.microsoft.com/en-us/sql/relational-databases/databases/tempdb-database)
- [Diagnose and resolve latch contention on SQL Server](https://learn.microsoft.com/en-us/sql/relational-databases/diagnose-resolve-latch-contention),  see specifically the guidance on replacing a sequential index key with a non-sequential one, which is the exact mechanism behind this workshop's incident

## Customer communication (Module 05)

- [Prompt Engineering Overview](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview),  the "give an example of the output you want" technique is the single highest-leverage one for house-style customer communications

## Security, privacy, and cost (Module 06,  the section worth re-reading most often)

- [Anthropic Trust Center](https://trust.anthropic.com),  SOC 2, compliance artifacts, and the technical detail behind Anthropic's security posture
- [Claude Help Center,  data retention practices](https://support.claude.com),  search "data retention" for the current, plan-by-plan breakdown; this is exactly the kind of page that gets updated
- [Claude API / Platform pricing](https://platform.claude.com/docs/en/about-claude/pricing) and [claude.com/pricing](https://claude.com/pricing),  current token and subscription pricing
- [OWASP Top 10 for Agentic Applications (2026)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/),  the industry-standard risk taxonomy behind Module 06's prompt-injection discussion, useful reading before your organization connects Claude to any live system via MCP or agentic tooling

## Extending the workflow beyond Claude.ai (Module 07)

- [Claude Code Docs](https://code.claude.com/docs/en/overview),  the agentic command-line tool
- [Claude Platform Docs,  API Reference](https://platform.claude.com/docs/en/api/overview),  building with the Claude API
- [Model Context Protocol](https://claude.com/partners/mcp),  connecting Claude to live systems, and the OWASP reference above before you do
