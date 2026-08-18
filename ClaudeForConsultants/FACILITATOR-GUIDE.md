<img width="150" src="https://github.com/BuckWoody/presentations/blob/master/graphics/logo.png?raw=true"> 

# Workshop: Claude for Technical Consultants

## Facilitator Guide

For whoever is teaching this workshop. Not distributed to students by default.

## Before class

- Confirm every registered student has completed [00 - Pre-Requisites](modules/00%20-%20Pre-Requisites.md),  send a reminder 48 hours out and again the morning of, specifically calling out the Projects/Artifacts/web-search checks in steps 2–5. The single most common cause of lost class time is discovering a feature toggle problem live in Module 01 instead of the day before.
- Have your own Claude.ai session open and logged in before students arrive, on the plan tier you expect most students to have, so any screen-share matches what they're seeing.
- Decide in advance how you want to handle students on a mix of plans (some Pro, some Team/Enterprise),  Module 06 is where this becomes relevant; it's worth a one-line acknowledgment early ("some of you have different data-handling terms than others,  Module 06 is where we get specific about that").

## Timing table

This mirrors the table in the root README. Timings are guidelines, not a contract,  flex by a few minutes per module before you start worrying about the schedule. If you're running behind, the safest place to trim is exercise discussion/comparison time, not the lecture content itself,  the modules were written assuming every lecture minute is already load-bearing.

| Segment | Suggested time | Running total |
|---|---|---|
| Welcome, agenda, prerequisite spot-check | 5 min | 0:05 |
| Module 01 (lecture + exercise) | 15 min | 0:20 |
| Module 02 (lecture + exercise) | 20 min | 0:40 |
| Module 03 (lecture + exercise) | 23 min | 1:03 |
| Module 04 (lecture + exercise) | 23 min | 1:26 |
| Module 05 (lecture + exercise) | 18 min | 1:44 |
| Module 06 (lecture + exercise) | 18 min | 2:02 |
| Module 07 (recap + discussion) | 10 min | 2:12 |

That totals slightly over 2 hours (2:12) by design,  it gives you a small buffer to absorb the Module 01 setup-troubleshooting risk above without the whole day sliding. If everything runs clean, you'll finish a few minutes early, which is a much better problem to have than running over.

## Room setup

- Projector/screen-share for your own session, so students can see what a real Project, Artifact, and search citation look like before doing it themselves in Module 01's exercise.
- If in-person: no specific hardware requirements beyond what pre-requisites already cover,  this is intentionally a bring-your-own-laptop, browser-only lab.
- If virtual: confirm your platform allows students to have both a video/chat window and their own browser tab visible at once,  the exercises assume they're working hands-on in parallel with your lecture, not only afterward.

## Common pitfalls, by module

- **Module 01:** the most common failure is a student on the Free plan who wasn't caught by the pre-requisites check. Have a backup plan (a shared demo account, or pairing them with a neighbor) rather than pausing the whole room to fix billing live.
- **Module 02:** students sometimes write an "engineered" prompt that's longer but not actually more specific,  it repeats the vague question with more words instead of adding real context/constraints. Worth circulating during the exercise to catch this pattern early, since Module 03's exercise depends on the skill actually landing.
- **Module 03:** watch for students skipping the custom-instructions step in the Project setup,  it's easy to go straight to asking the design question. If they skip it, the exercise still "works," but they miss the actual point (a Project's persistent context), so it's worth a mid-exercise nudge if you see it happening.
- **Module 04:** the exercise is built so that a shallow read produces a plausible-but-incomplete answer (naming only the lock/blocking symptom, missing the two underlying mechanisms). This is intentional,  it's the "first-plausible-answer trap" from the lecture, made concrete. Don't rescue students out of it too quickly; let a few of them hit it and self-correct using the follow-up-question prompt in step 4, then discuss it as a group.
- **Module 05:** the most common miss is producing two drafts that are actually the same register with a different word count, rather than genuinely different for their audience. Cold-read a volunteer's executive summary out loud,  if it still contains a wait-type name or a DMV reference, that's the teaching moment.
- **Module 06:** item 4 in the classification exercise (the contract clause) is deliberately the trap item,  see the answer key's note on why. Expect some students to answer "safe" because the *data itself* isn't sensitive; that's the exact misconception the exercise is built to surface.

## Facilitation notes from the underlying instructional design

A few principles this workshop's structure leans on, if you want to preserve them when you adapt this material:

- Every module opens with a **retrieval check**,  a quick, low-stakes recall question about the *previous* module before introducing new content. This is a deliberate spaced-retrieval technique, not filler; don't skip it under time pressure, since it's cheap (30–60 seconds) and it's doing real cognitive work.
- Every exercise is designed to produce **an early, visible win before the harder judgment call**,  for example, Module 01's tour before Module 02's actual skill-building. If you shorten a module, protect this shape rather than cutting straight to the hardest part.
- The running Contoso Retail scenario is a deliberate choice to reduce **context-switching cost**,  students spend their limited cognitive effort on the AI-usage skill being taught, not on re-orienting to a new fictional company every module. If you adapt this workshop to your own industry, keep one scenario running end to end rather than a fresh example per module.
