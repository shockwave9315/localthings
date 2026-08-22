# AGENTS.md

This fork uses AI coding agents as normal implementation and review tools.

For pull requests targeting `shockwave9315/localthings`, automated review must
focus on functional correctness and follow the fork-local review policy in
`CONTRIBUTING.md`.

Do not raise findings solely about commit author/committer identity, AI or tool
attribution, co-author trailers, commit provenance, or whether AI produced any
part of a change. Do not raise style-only findings about comments or docstrings
unless they cause CI/lint/type failures, materially obscure correctness, or
create a real maintenance risk.

Prioritize code behavior: correctness, regressions, entity/state lifecycle,
Home Assistant API usage, restore/statistics continuity, concurrency, error
handling, security/data-loss risk, and whether tests actually cover the bug.

When preparing a patch for another repository, follow that target repository's
rules separately; fork-local review policy is not meant to be exported
upstream.
