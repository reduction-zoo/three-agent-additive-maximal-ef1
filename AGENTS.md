# Research instructions

Read the [fixed question](campaigns/three-agent-additive-maximal-ef1/question.md), [prior state](campaigns/three-agent-additive-maximal-ef1/state.md) and [preparation notes](campaigns/three-agent-additive-maximal-ef1/work/preparation.md). The fixed [test corpus](campaigns/three-agent-additive-maximal-ef1/work/cases.json) and [verifier](campaigns/three-agent-additive-maximal-ef1/work/check.py) are the starting evidence; the preparation notes state their coverage and any pending checks.

Run `uv sync --locked`, then `uv run --locked python campaigns/three-agent-additive-maximal-ef1/work/check.py --self-test` before relying on that evidence. Follow the current user's AutoResearch pipeline. Scope and budgets in the state describe earlier work and do not limit a new campaign. Preserve prior evidence, commit new work incrementally and make only evidence-backed claims.
