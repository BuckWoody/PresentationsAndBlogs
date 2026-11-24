<img width="150" style="float: right; margin: 0px 15px 15px 0px;" src="../graphics/logo.png">

# Workshop: Data Literacy

#### <i>Course Design Notes (for instructors and maintainers)</i>

<p style="border-bottom: 1px solid lightgrey;"></p>

These notes record how the modernized workshop is built and why. Keep this folder out of the learners' copy.

## Time budget (360 minutes, breaks extra)

| Module | Total | Lecture | Activities | Checkpoint |
|---|---:|---:|---:|---:|
| 00 Start Here | 10 | 5 | 5 | 0 |
| 01 Data Basics | 30 | 16 | 12 | 2 |
| 02 Find and Trust Data | 40 | 18 | 19 | 3 |
| 03 Work with Data | 40 | 17 | 20 | 3 |
| 04 See What Happened | 50 | 26 | 22 | 2 |
| 05 The Skeptic's Toolkit | 35 | 16 | 15 | 4 |
| 06 Find Out Why | 45 | 22 | 21 | 2 |
| 07 Look Ahead | 45 | 22 | 21 | 2 |
| 08 Decide What to Do | 45 | 22 | 21 | 2 |
| 09 Explain, Act, Learn | 20 | 8 | 11 | 1 |
| **Total** | **360** | **172** | **167** | **21** |

**Cadence.** Lecture blocks run from 3 to 10 minutes, and an activity follows each one, so exercises arrive roughly every 8 to 10 minutes of lecture. That's more often than the 15 to 20 minutes in the original brief, and it comes out at about half lecture and half activity. If you prefer longer talks, merge the two lecture blocks in a module (for example, 4.1 and 4.2) and let the activities run longer, which lowers the number of activities from about 23 to about 12. The module text doesn't need to change much, because the "Starting here?" boxes and activities are already separable.

## How the five goals were met

| Goal | Where it lives |
|---|---|
| 1. A linear, building path | Modules run alphabet (01, 02), tools (03), describe (04), doubt (05), diagnose (06), predict (07), decide (08), explain (09). Statistics is taught just in time (spread in 04, sampling variation in 06) instead of being a prerequisite. Each module opens with a "Starting here?" box and ships the case data in the state it needs. |
| 2. Frequent, cohesive exercises | One company (Lantern Peak), one dataset, and a single question (where should $150,000 go?). Each activity's output feeds the next (the messy files in 02 and 03 become the clean files in 04, the claims in 05 are tested in 06 and 07, and the evidence is scored in 08 and written up in 09). |
| 3. Vendor-neutral | Tools are described by kind (spreadsheet, query language, notebook, BI tool, AI assistant). SQLite is the one named database, because it's free, local, and a single file. No product-specific steps remain. |
| 4. Descriptive, diagnostic, predictive, prescriptive | 04, 06, 07, and 08, in that order, with the four kinds introduced in 00. |
| 5. Biases | Module 05 is a full module placed after learners have computed and charted things. Every module also ends with a skeptic's checkpoint tied to its stage. The approach is practice with feedback, which the research supports better than lists of names. |

## From the earlier version to this one

| Earlier version | Now |
|---|---|
| 00 Pre-requisites (Khan Academy links, Windows, Excel) | 00 Start Here: a 10-minute orientation and warm-up, with no installs |
| 01 Find Authoritative Data (defining data, types, sources, verification) | 01 Data Basics and 02 Find and Trust Data |
| 02 Work with Data Tools (Excel, SQL, R, Python, Power BI, text formats, databases) | 03 Work with Data (kinds of tools, formats, cleaning, combining), plus 04 for visualization |
| 03 Analyze Data in Context (context, skepticism, biases, fallacies) | 05 The Skeptic's Toolkit, and the context ideas folded into 04 and 06 |
| 04 Use Data for Intelligent Decisions (OODA, problem, alternatives, explain, post-mortem) | 08 Decide What to Do and 09 Explain, Act, Learn, with the predictive material in 07 |
| 21 activities, about 15 of them links to external tutorials | 23 activities that all run on the Lantern Peak data, plus optional extensions |

**What was kept:** the literacy analogy, the who/what/why questions, the car story, the data skeptic stance, the clothing color exercise, the post-mortem, and the Activity, Steps, Further Study, and Next Steps layout.

## Corrections to the earlier version

- The OODA loop grew out of John Boyd's study of air combat as a US Air Force fighter pilot, not out of ground-soldier casualty rates. It's also often reduced to "the faster loop wins." Module 08 corrects both points.
- "RDBS" should have been RDBMS. The fixed-width example looked the same as the delimited example because the spacing was lost. `{name : "Buck Woody"}` isn't valid JSON (the key needs quotation marks), and JSON isn't new.
- "Cognitive bias is a logical error" blurred two different things. Module 05 separates cognitive biases, logical fallacies, and data traps.
- Several external links had moved or died. Links in the modules were rewritten, and where possible they point to stable sources.

## Before publishing

- **Run the checks.** `tools/predeploy_check.py` covers style, references, the workbench tests, and the data rebuild. `tools/check_links.py` tests every web link. The step-by-step list is in `deployment-checklist.md`, and the results of the link check done while building this version are in `link-check.md` (including three links only you can confirm).
- **Answers are in two places.** The `facilitator` folder and the collapsed "Instructor notes" in every module both hold answers. For a public repository, run `python3 tools/make_learner_edition.py OUTPUT_FOLDER` to produce a copy without either, and keep this full version private.
- **Icons.** The Activity, Steps, and Further Study icons are hotlinked from the `microsoft/sqlworkshops` repository. `tools/localize_icons.py --download` copies them into your repository and rewrites every link.
- **Scenario assumptions in Module 08** (the low, base, and high cases for each option, and the probabilities) are invented for teaching. The inputs that come from the data are labeled as such.
- **Adventure Works** is an invented extract, labeled as such. It isn't the Microsoft sample database.
- **Synthetic data.** Lantern Peak is fictional. The effects planted in it (the mix shift, the loyalty selection, the survey non-response, the churn base rate) are described in `answer_key_numbers.md`.
- **Old module addresses.** Five small "this module has moved" pages keep the earlier filenames working.

## Rebuilding and testing

- `case-data/build_case_data.py` rebuilds the database, the CSV files, the data dictionary, and `answer_key_numbers.md`. It's seeded, and it checks that the Module 03 cleaning recipe ties out to the finance report to the cent for all 36 months (it stops with an error if it doesn't). The committed files were built with numpy 2.5.4. numpy doesn't promise the same random numbers across versions, so the modules' numbers belong to the committed files, and the script warns if your version differs.
- `case-data/make_images.py` rebuilds the chart images in `modules/images` (needs matplotlib).
- `case-data/adventure-works/build_aw_extract.py` rebuilds the Adventure Works extract and `aw_answer_key.md`.
- `tools/data-workbench/test_workbench.py` runs 23 checks against the browser tool.
- `tools/predeploy_check.py` runs all of the offline checks above in one go.
