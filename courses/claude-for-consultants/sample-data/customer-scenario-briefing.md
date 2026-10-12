# Customer Scenario Briefing: Contoso Retail

*Fictitious customer. Used as a consistent thread through Modules 03–06.*

## Who they are

Contoso Retail is a mid-size retail chain (60 stores, one central e-commerce site) running its order and inventory system on SQL Server. They've engaged your consulting organization for two things: (1) advice on whether and how to modernize their database platform, and (2) help diagnosing a recurring performance problem during high-traffic sales events.

## Current environment

- SQL Server 2019, Standard Edition
- Single on-premises physical server: 4 vCPU, 32 GB RAM, 500 GB local SSD storage
- One primary database (`ContosoOrders`, ~180 GB) plus a smaller reporting database
- No high-availability configuration today,  nightly full backup, log backups every 15 minutes
- IT team: one full-time DBA (part-time on SQL Server specifically), a small infrastructure team, no dedicated cloud team yet
- Compliance: standard retail PCI-DSS scope for payment data (payment data itself is tokenized by their payment processor and does **not** live in `ContosoOrders`)

## Business constraints

- Budget-conscious,  leadership wants a cost-effective modernization path, not necessarily the most feature-rich one
- Low tolerance for a "big bang" cutover,  prefers an incremental path if one exists
- RTO/RPO target for the order database: RTO 1 hour, RPO 15 minutes (informal today; not yet tested)
- Flash-sale events (roughly monthly) roughly triple normal transaction volume for 2–4 hours

## The two threads you'll work

1. **Solution design (Module 03):** Contoso's IT Director has asked for a comparison of modernization paths,  stay on-premises, move to an Azure VM, or move to a managed platform-as-a-service option,  with a recommendation and clearly stated trade-offs, given the constraints above.
2. **Troubleshooting (Module 04):** During the most recent flash sale, checkout transactions slowed dramatically for about 90 minutes. The DBA pulled an error log excerpt and a wait-statistics snapshot from during the event (see `sql-server-error-log-excerpt.txt` and `wait-stats-sample.txt`) and sent them to you along with the original complaint email (`customer-email-original-complaint.txt`).

Everything after this point in the workshop treats these two threads as real client work,  the exercises ask you to actually produce the design comparison and the root-cause analysis, using Claude, from this briefing and the files alongside it.
