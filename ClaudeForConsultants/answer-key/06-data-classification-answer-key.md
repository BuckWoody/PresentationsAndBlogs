# Answer Key: Data Classification and Redaction (Module 06)

## Classification

| # | Item | Classification | Which question drove it |
|---|---|---|---|
| 1 | Error log with real hostname/instance/IP | **Sanitize first** | Data sensitivity,  hostnames and internal IPs are the kind of infrastructure detail worth stripping as routine practice, independent of any specific contract clause |
| 2 | Wait-stats snapshot alone (no names/hosts) | **Safe to paste as-is** | None of the three raise a flag,  no PII, no identifying infrastructure, and it's the kind of generic performance data most engagements don't restrict |
| 3 | Priya's email (real name, title, company) | **Sanitize, or get sign-off depending on your contract** | Primarily contract terms,  email correspondence with a named individual is exactly the kind of thing an NDA or services agreement may restrict sharing with third parties; data sensitivity (a real name) reinforces the same conclusion |
| 4 | The services-agreement confidentiality clause itself | **Don't paste without legal/contract sign-off** | Contract terms, explicitly and directly,  the clause itself says not to disclose "system logs and configuration data" to third parties without consent; pasting *that clause* (or anything it covers) into a third-party tool without checking your engagement's specific terms is the exact scenario it's written to prevent |
| 5 | Generic T-SQL syntax question | **Safe to paste as-is** | None of the three apply,  there's no customer data in the question at all |
| 6 | Full `architecture-options-notes.md` contents | **Sanitize/limit, or confirm your plan and contract cover it** | A mix of data sensitivity (business/budget detail, though no PII/credentials) and contract terms (engagement-specific information),  softer than item 3 (no named individual), but still not "generic," so the same check applies before treating it as automatically fine |

## Why item 4 is the one people get wrong

It's tempting to answer these purely on the technical sensitivity axis,  "is there PII or a secret in it?" Item 4 has neither. What it has is a contract clause that makes the disclosure question answerable independent of the data's technical sensitivity: **the client's agreement says not to share this category of information with third parties without consent, full stop.** A third-party AI tool is a third party. This is exactly why Module 06's lecture separated "is the data sensitive" from "does your contract allow it" as two different questions,  a clean answer on one doesn't resolve the other.

## Worked redaction example (item 1)

**Before (illustrative "real" version, not what you were given in `sample-data/`):**

```
Contoso Retail,  SQL Server ERRORLOG excerpt
Instance: CONTOSO-PROD-DB01\SQL2019 (10.42.18.117)
...
2026-05-09 14:03:15.77 spid52 Time out occurred while waiting for buffer latch...
```

**After redaction,  every diagnostic detail preserved, every identifying detail removed:**

```
Contoso Retail,  SQL Server ERRORLOG excerpt
Instance: [REDACTED-INSTANCE-NAME] ([REDACTED-IP])
...
2026-05-09 14:03:15.77 spid52 Time out occurred while waiting for buffer latch...
```

Notice what *didn't* change: timestamps, spid numbers, wait types, message text, page IDs, database IDs,  everything that actually matters for diagnosis. A good redaction is judged by whether someone could still do the troubleshooting from it, not by how much got blacked out.
