<img width="150" style="float: right; margin: 0px 15px 15px 0px;" src="../graphics/logo.png">

# Workshop: Data Literacy

#### <i>Link Check Report (November 24, 2026)</i>

<p style="border-bottom: 1px solid lightgrey;"></p>

This records how each external link was checked, and how far to trust the result. The checks were run from an environment that could fetch only some pages, so the report separates what was confirmed from what wasn't. To finish the job on your own machine in about a minute, run `python3 tools/check_links.py`.

**How to read the levels**

- **Fetched live** means the page was requested during the check and its content was read.
- **Found by search** means a search returned this exact address with content that matches what the module says. That shows the page existed and said this when it was indexed, and it is not a live test.
- **Not checked** means the link wasn't tested here. Most of these are long-lived reference sites, but only a live request can confirm them.

## Found broken, and fixed

| Link | What happened | Replaced with |
|---|---|---|
| NASA APPEL page about the Mars Climate Orbiter (Module 01) | **Fetched live: it redirects to APPEL's generic home page.** The article is gone, though the old address still "works," which is why a quick glance wouldn't catch it. | NASA JPL's announcement of the likely cause (fetched live, content confirmed), NASA's Mishap Investigation Board Phase I report (found by search), and an IEEE Spectrum article (found by search) |

## Confirmed

| Link | Used in | Level |
|---|---|---|
| jpl.nasa.gov/news/mars-climate-orbiter-team-finds-likely-cause-of-loss/ | Module 01 | Fetched live |
| llis.nasa.gov/llis_lib/pdf/1009464main1_0641-mr.pdf | Module 01 | Found by search |
| spectrum.ieee.org/why-the-mars-probe-went-off-course | Module 01 | Found by search |
| usgs.gov/data-management/data-dictionaries | Module 01 | Found by search (the address without "www" was returned; the module links the "www" form, which should resolve to the same page) |
| openaccess.city.ac.uk/id/eprint/12324 | Module 05 | Found by search |
| psychologicalscience.org/news/minds-business/debiasing-your-decisions.html | Module 05 | Found by search |
| criticalthinking.org/pages/defining-critical-thinking/766 | Module 05 | Found by search (exact address) |
| maxwell.af.mil/News/Display/Article/420819/ | Module 08 | Found by search |
| en.wikipedia.org/wiki/OODA_loop | Module 08 | Found by search |
| en.wikipedia.org/wiki/John_Boyd_(military_strategist) | Module 08 | Found by search |
| en.wikipedia.org/wiki/List_of_cognitive_biases | Module 05 | Found by search |

## Not checked here (long-lived sites, confirm with the script)

- Merriam-Webster: the entry for "data" (Module 01)
- Khan Academy: Math, and Statistics and probability (Modules 00, 01, 04, 06, 07, 09)
- data.gov (Module 02)
- sqlite.org, and the command-line shell page (Module 03)
- Wikipedia: Anscombe's quartet, List of fallacies, Simpson's paradox, Confounding, A/B testing, Expected value, Sensitivity analysis
- otexts.com/fpp3/ (Modules 07 and 09)
- The Cognitive Bias Codex image on Wikimedia (Module 05). This address was carried over from the earlier version of the workshop
- The Bootstrap stylesheet on jsDelivr, version 5.3.3 (the data workbench)

## Could not be verified: please click these once

| Link | Where | Why it couldn't be checked |
|---|---|---|
| dataliteracy.com | README (Related Workshops) | Carried over from the earlier version. Searches for it returned the Data Literacy Project and Qlik's program pages, and never this address. If it no longer serves what the README says, remove the line or point it at a site you trust |
| buckwoody.github.io/presentations/ai_ml_dl/ | Module 07 (Further Study) | Your own page, and it wasn't reachable by the tools used here |
| tinyurl.com/bw-sample | README, Module 00, and the Adventure Works README | A short link from your company profile document. A redirect can't be followed from here, so confirm it lands on the Adventure Works material you intend |
| The 11 icon images on github.com/microsoft/sqlworkshops | Every module | Not fetchable from here. They are the same images the earlier version used. To remove the dependency, run `python3 tools/localize_icons.py --download` |

## A note on the "moved" problem

The most useful thing this check found is that a dead page can look alive. The NASA address answered normally, and sent readers to an unrelated page. `tools/check_links.py` is built to catch exactly that: it reports **MOVED** when a link answers at a different address from the one you linked. Treat every MOVED line as a broken link until you've looked at it.
