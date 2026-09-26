# Independent Set → Three-agent additive maximal EF1 allocation

Independent research campaign for the [fixed question](campaigns/three-agent-additive-maximal-ef1/question.md). [State](campaigns/three-agent-additive-maximal-ef1/state.md) records the current evidence and next action.

The initial commit fixes the question and setup. [Prepare evidence](campaigns/three-agent-additive-maximal-ef1/work/preparation.md), [contract](campaigns/three-agent-additive-maximal-ef1/work/contract.md), and [fixed corpus](campaigns/three-agent-additive-maximal-ef1/work/cases.json) are committed. The target-negative coverage limit is documented; no solution is claimed. Run the campaign from this repository and follow `AGENTS.md`.

Reproduce: `uv sync --locked`, then `uv run --locked python campaigns/three-agent-additive-maximal-ef1/work/check.py --self-test`.
