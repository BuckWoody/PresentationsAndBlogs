# Answer Key: Contoso Modernization Comparison (Module 03)

*This is a worked example of the shape a strong output should have,  not a template to match word-for-word. Use it to check whether your own session's output reflected Contoso's actual constraints and stated uncertainty where it should, not to check for identical wording. Treat every specific figure below as illustrative, not verified current pricing,  that's the point of Module 02's verification habit.*

## Comparison

| | Stay on-premises (upgraded) | Infrastructure-as-a-Service (VM in the cloud) | Platform-as-a-Service (managed database) |
|---|---|---|---|
| **What changes** | New/upgraded hardware, same operational model | Same SQL Server, someone else's hardware | The platform vendor manages patching, backups, and HA |
| **Migration effort** | Lowest,  no platform change | Moderate,  lift-and-shift, minimal app changes | Higher,  some compatibility validation needed, but often still low for a mainstream workload |
| **Ongoing DBA burden** | Unchanged,  still on one part-time DBA | Slightly reduced (infra managed, DB administration still manual) | Substantially reduced,  patching, backup, and basic HA become the platform's job |
| **Cost shape** | Capital expense, predictable | Operating expense, scales with VM size | Operating expense, scales with tier/compute,  often the best fit for "cost-effective," but needs sizing to avoid over-provisioning |
| **HA/DR fit** | Requires you to build it,  currently absent | You still build it, but cloud infrastructure makes it easier | Often included or a configuration toggle, directly addressing the untested RTO/RPO target |
| **Incremental path?** | N/A,  no change | **Yes**,  closest to a non-"big-bang" first step | Possible, but typically means a real migration project, not a toggle |

## Recommendation

Given Contoso's explicit preference against a "big bang" cutover, its single part-time DBA, and its currently-untested RTO/RPO target, **an infrastructure-as-a-service move is the more defensible first step**, with a managed platform-as-a-service option flagged as the stronger *long-term* fit once the business is comfortable with a real migration project,  because it most directly reduces the operational burden on a single part-time DBA and typically makes hitting a real, *tested* RTO/RPO target easier than either alternative.

**The strongest argument against this recommendation:** an infrastructure-as-a-service move mostly relocates today's problems rather than solving them,  Contoso keeps the same patching, backup design, and single-DBA operational model, just on rented hardware. If the underlying goal is reducing operational burden rather than just avoiding capital expense, jumping straight to the managed platform option (accepting more migration effort now) may serve Contoso better than treating infrastructure-as-a-service as a stepping stone it never actually leaves.

## Flagged for verification before this goes to Contoso

- Exact current service tier names, pricing, and capability limits for each cloud option,  verify against current vendor documentation, not this document
- Whether Contoso's existing licensing carries any transfer benefit to a cloud option,  a licensing specialist question, not one Claude should be trusted on unverified
- The actual RTO/RPO Contoso's chosen option delivers, once selected,  needs a real test, not an assumption
