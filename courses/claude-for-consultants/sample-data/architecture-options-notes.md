# Contoso Retail,  Raw Notes for Modernization Comparison

*Unedited notes from the discovery call with Contoso's IT Director. Use these as the raw input for the Module 03 exercise,  part of the exercise is noticing what's missing or ambiguous, not just what's stated.*

- Current: SQL Server 2019 Standard Edition, single on-prem box, 4 vCPU / 32GB RAM / 500GB local SSD
- Primary DB `ContosoOrders` ~180GB, growing maybe 15%/year
- No HA/DR today. Backups: nightly full + log backups every 15 min, copied to a NAS on-site only (no offsite copy,  IT Director flagged this as "something we know we should fix")
- One part-time DBA, small infra team, no cloud team
- Budget-conscious,  leadership explicitly said "don't bring us the fanciest option, bring us the sensible one"
- Wants to avoid a "big bang" cutover if there's an incremental path
- Informal RTO 1 hour / RPO 15 min for the order database,  "informal" because it's never actually been tested
- Flash sales ~monthly, ~3x normal transaction volume for 2-4 hours, this is the direct trigger for the Module 04 incident
- PCI scope: payment data is tokenized by a third-party processor before it ever reaches `ContosoOrders`,  the DB itself is not expected to be in full PCI cardholder-data scope, but confirm this isn't something to just take at face value
- IT Director's actual question: "Should we move this to Azure, and if so, to what,  and can you tell me in something I can put in front of my VP without a computer science degree?"
- Nothing has been decided yet. No target date. No specific budget number was given,  only "cost-effective."
