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

1. **What problem does this project solve, and what is its unit of work?** Explain assemble a release review from local changes, identify small engineering teams as the audience, and trace one concrete example through the files above. Use the demonstration output rather than hypothetical impact.
2. **Why did you choose the first design decision?** Use a policy-constrained state machine to select inspection, test and drafting tools. Show the corresponding implementation and a test that would fail if that property were removed.
3. **How do you protect correctness when inputs or execution change?** Run only an allowlisted unittest command against bundled workspaces, with a timeout and bounded output. Explain the relevant invalid-input or edge-case test and distinguish a checked property from an untested assumption.
4. **How do you make results inspectable and reproducible?** Cache runs by content, version and engine; optional local model synthesis stays inside an unsent review draft. Point to actual outputs and recorded commands. Explain why a successful example is weaker evidence than a tested boundary or independently reconciled total.
5. **What would you improve before real deployment or real-data use?** Bundled example repositories only; it is not a general shell agent. Secret detection is illustrative, not comprehensive. The language model may write inaccurate summaries; test evidence and change manifests remain authoritative. No pushes, tags or external messages occur. Choose one limitation, describe the missing evidence, and propose a measurable acceptance check rather than promising production readiness.

## Independent exercise

Add a license-presence inspection tool and ensure its failure blocks draft creation.

Write down the expected behavior before editing. Add a meaningful regression check, run the existing suite, and describe what changed in your own words.

## Contribution and resume guidance

The implementation was developed with substantial AI assistance under Abhijith Viswanathan's direction. The verified contribution is the working artifact and the learning work actually completed, not invented employment or adoption.

Suggested factual bullet after personally validating the demo:

- Implemented and validated assemble a release review from local changes using Python · Flask, with tool-planning agent and documented correctness checks and limitations.

Use [VERIFICATION.md](VERIFICATION.md) to add only measured numbers. Do not claim production traffic, users, savings, upstream acceptance or cloud deployment without corresponding evidence.
