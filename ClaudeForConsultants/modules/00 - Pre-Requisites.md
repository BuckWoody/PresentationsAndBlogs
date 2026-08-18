<img width="150" src="https://github.com/BuckWoody/presentations/blob/master/graphics/logo.png?raw=true"> 

# Workshop: Claude for Technical Consultants

## 00 - Pre-Requisites

**Complete this module before the workshop starts.** There is no dedicated setup time in the 2-hour class, the clock starts with Module 01.

## What you need

- A **web browser**,  Chrome, Edge, or Firefox, current version. No other software, no API key, and no local installation are required anywhere in this workshop.
- A **Claude.ai account on the Pro plan or higher** (Pro, Max, Team, or Enterprise). The Free plan does not reliably include Projects and has usage limits that will interrupt a hands-on lab.
  - IUse the company-provided Team or Enterprise seat,not a personal account. Module 06 explains why this matters for customer data.
  - If you need to sign up for Pro individually for this class: go to [claude.ai](https://claude.ai), create an account, and subscribe to Pro from the settings menu. Confirm current pricing at [claude.com/pricing](https://claude.com/pricing) before you do,  it's subject to change and this document won't be updated for every price change.
- An **internet connection** (this is a cloud service; there is no offline/local mode for Claude.ai).

## Account check

Log in at [claude.ai](https://claude.ai) and confirm each of the following. If any step fails, see **Troubleshooting** below.

1. **You can start a new chat and send a message.** Type "Hello" and confirm you get a response.
2. **You can create a Project.** In the left sidebar, look for **Projects** and select **Create project** (wording may vary slightly by plan/version). Name it anything for this test,  you'll create the real one in Module 03.
3. **You can attach a file to a Project.** Any small text file will do for this check.
4. **Web search is available.** Ask Claude a question about something you know changed recently (e.g., "what's today's date") and confirm it can search rather than just answering from memory. If you don't see any indication it searched, check your account's tool settings,  this is sometimes a toggle under **Settings → Feature Preview** or similar, and the exact location changes as Anthropic updates the product. If you can't find it, that's fine,  we'll troubleshoot together at the start of class.
5. **You can see Artifacts render.** Ask Claude: "Create a simple markdown table comparing three fruits." Confirm the output renders in a distinct panel rather than only inline in the chat. If it only appears inline, check the same feature settings as step 4.

## Download the sample data

Download or clone this repository so you have the [`sample-data/`](../sample-data) folder available. You'll upload files from it into a Claude Project during Module 03, and reference others during Modules 04–06. Nothing in `sample-data/` is real customer information,  it's a fictitious scenario (Contoso Retail) written for this class.

## Recommended pre-reading (optional, ~10 minutes)

These aren't required, but if you want a head start:

- [Claude Overview](https://claude.com),  what Claude is and the current product family
- [Prompt Engineering Overview](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview),  the ideas behind Module 02
- [Claude Help Center](https://support.claude.com),  how Projects and Artifacts work, in Anthropic's own words

## Troubleshooting

| Symptom | Likely cause | What to do |
|---|---|---|
| "Projects" isn't in your sidebar | You're on the Free plan, or the organization's admin has restricted it | Confirm your plan under **Settings → Billing**; if the org manages your seat, ask your Claude admin |
| Web search doesn't seem to run | Feature Preview / tool setting is off, or the org has disabled it at the admin level | Check **Settings**; if you're on a managed Team/Enterprise seat, ask your workspace admin |
| You don't have a Claude account at all and can't sign up | The organization may require SSO-based provisioning | Contact your Claude admin or IT,  don't create a personal Pro account that will hold customer data later; get provisioned properly |
| You're not sure which plan you're on |,  | **Settings → Billing** shows your current plan; when in doubt, ask before class rather than during it |

## Next Steps

Once every check above passes, continue to [*01 - Orientation and the Claude Model Lineup*](01%20-%20Orientation%20and%20the%20Claude%20Model%20Lineup.md).
