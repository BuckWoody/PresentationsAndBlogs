<img width="150" style="float: right; margin: 0px 15px 15px 0px;" src="../graphics/logo.png">

# Workshop: Data Literacy

#### <i>Deployment Checklist</i>

<p style="border-bottom: 1px solid lightgrey;"></p>

A step-by-step list for moving this version into your GitHub repository (`courses/data-literacy`). The commands assume you're in your local clone of the repository.

## Before you change anything

1. **Preserve the earlier version.** Tag the current state so you can return to it:
   ```
   git tag data-literacy-v1
   git push origin data-literacy-v1
   ```
2. **Work on a branch,** so nothing reaches the public site until you merge:
   ```
   git checkout -b data-literacy-v2
   ```

## Put the new files in place

3. Delete the old contents of `courses/data-literacy`, then copy in the contents of this package (the `README.md`, `modules`, `case-data`, `tools`, `facilitator`, `graphics`, and the two dot-files `.gitignore` and `.gitattributes`). Make sure the dot-files come across, because some file managers hide them.
4. The old `.vscode/tasks.json` isn't carried over on purpose. It only opened a search engine.
5. **The old module filenames still work.** Five small "this module has moved" pages in `modules/` keep old links alive (`00-pre-requisites`, `01-find-authoritative-data`, `02-work-with-data-tools`, `03-analyze-data-in-context`, and `04-use-data-for-intelligent-decisions`). They matter if you've shared those addresses in posts, slides, or emails. Delete them when you're confident nobody uses them.

## Run the checks

6. Install what the checks use (optional, but they skip what's missing):
   ```
   pip install flask numpy
   ```
7. Run the full offline check. You should see `4 passed, 0 failed`:
   ```
   python3 tools/predeploy_check.py
   ```
8. Run the web link check. Treat every **MOVED** and **FAILED** line as a broken link, and open any **BLOCKED** link in a browser:
   ```
   python3 tools/check_links.py
   ```
   Also look at the "Could not be verified" section of `facilitator/link-check.md`, which lists three links only you can confirm.
9. *(Optional)* Remove the dependence on Microsoft's icon repository, then run step 7 again:
   ```
   python3 tools/localize_icons.py --download
   ```

## Decisions to make

10. **Answer keys.** Answers live in two places: the `facilitator` folder, and the collapsed "Instructor notes" block at the end of every module. A public repository shows both to everyone. Keep this full version private, and publish a learner edition instead:
    ```
    python3 tools/make_learner_edition.py ../data-literacy-learner
    ```
    It copies everything learners need, leaves out the answer keys, the instructor notes and the maintenance scripts, and checks that every link still works. (The "Check yourself" and "Reveal the answers" blocks inside activities stay, because they give learners feedback on their own work.) If you'd rather publish everything, nothing breaks, and learners who peek will only spoil the exercises.
11. **License.** Decide how others may reuse the text and the data. The data is fictional and free of any real person's information, so a permissive license suits it. Add a `LICENSE` file at the repository root.
12. **Regenerating the data.** The modules quote numbers from the committed data files. Don't rebuild the data unless you mean to re-check those numbers, and expect a warning if your numpy version differs from the one the files were built with (2.5.4). The check in step 7 only compares a rebuild when the versions match.

## Look at it on GitHub before you announce it

13. Push the branch and open a few pages in the browser. Check that tables render, that the collapsed "Instructor notes" blocks open, that the logo and the module icons appear, and that the "Next Steps" links go to the right module. Open `modules/01-data-basics.md` and `modules/08-decide-what-to-do.md` at minimum, because they use the most formatting.
14. Merge the branch when you're satisfied.

## If something goes wrong

15. Roll back by checking out the tag from step 1, or by reverting the merge. Nothing here changes anything outside the `courses/data-literacy` folder.
