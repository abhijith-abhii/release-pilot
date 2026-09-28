# Release Pilot — learning guide

## What it does

Assemble a release review from local changes. The intended user is small engineering teams. Browser controls → validated Flask API → project analysis/workflow → results and export.

## Run and demonstrate

Follow the README installation block, then: Run the passing scenario and inspect tool observations. Run the failing scenario and see drafting stop. Select local-llm after downloading the model to generate an explicitly labeled summary, then repeat to see cached-run reuse.

## Important files

- `app.py` — local HTTP interface and request/error handling.
- `core.py` — project-specific logic.
- `tests/` — regression and correctness checks.
- `reports/` — recorded outputs and verification evidence.

## Three engineering decisions

1. Use a policy-constrained state machine to select inspection, test and drafting tools.
2. Run only an allowlisted unittest command against bundled workspaces, with a timeout and bounded output.
3. Cache runs by content, version and engine; optional local model synthesis stays inside an unsent review draft.

## Five interview questions

1. **What tools can the agent use?** It inspects an allowlisted local fixture workspace and runs its unit tests. The workflow can assemble a review draft but cannot send, push, tag or deploy a release.

2. **What prevents a failing release from being drafted?** The test result is a mandatory gate. A failing fixture produces a blocked review rather than a success summary.

3. **Why cache by content hash?** The cache is tied to workspace content and workflow identity, so repeated requests for unchanged inputs can reuse evidence without accidentally treating changed code as already checked.

4. **What did the local model evaluation reveal?** One generated summary introduced unsupported words. A lexical support check now withholds such prose and falls back to verified change bullets, while keeping the raw output in the audit evidence.

5. **Is that guard a semantic truth guarantee?** No. Vocabulary overlap is only a conservative filter. Human review remains required, and the deterministic tool results—not fluent model wording—control the workflow outcome.

## Independent exercise

Add a license-presence inspection tool and ensure its failure blocks draft creation.

Write down the expected behavior before editing. Add a meaningful regression check, run the existing suite, and describe what changed in your own words.

## Contribution and resume guidance

The implementation was developed with substantial AI assistance under Abhijith Viswanathan's direction. The verified contribution is the working artifact and the learning work actually completed, not invented employment or adoption.

Suggested factual bullet after personally validating the demo:

- Built a bounded release-review agent that runs local tests, blocks failing changes and audits generated summaries; added a fallback after observing unsupported model wording.

Use [VERIFICATION.md](VERIFICATION.md) to add only measured numbers. Do not claim production traffic, users, savings, upstream acceptance or cloud deployment without corresponding evidence.
