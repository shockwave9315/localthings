# Contributing

See the README's [Contributing](README.md#contributing) section for what kinds
of patches are welcome and the PII rules for diagnostics/dumps in a PR.

## Fork-local automated review

For pull requests targeting `shockwave9315/localthings`, automated reviewers
should spend review budget on real code and behavior rather than provenance or
cosmetic policy checks.

- Do not raise findings about commit author/committer identity, AI/tool
  attribution, co-author trailers, commit provenance, or whether AI produced
  any part of the change.
- Do not raise style-only findings about comments, docstrings, wording, or
  formatting unless they cause CI/lint/type failures, materially obscure
  correctness, or create a concrete maintenance problem.
- Reserve P0/P1 for functional breakage, data loss/corruption, security issues,
  serious regressions, or changes that cannot work as intended.
- Prioritize correctness, regressions, Home Assistant API contracts,
  entity/state lifecycle, restore/statistics continuity, concurrency, error
  handling, and test coverage of the reported bug.
- When a change may later be sent upstream, keep the functional patch clean;
  the target repository's contribution and attribution rules can be applied
  separately before upstream submission.

## Commits

Fork-local commits may be authored or committed by a human, automation, or AI
tooling. Commit attribution is not a review signal in this fork.

Before sending a patch to another repository, rewrite or squash commit history
only if that target repository requires different attribution rules.

## Code comments

Comments should explain non-obvious behavior or evidence rather than restating
the code. Keep them concise when practical, but comment/docstring style alone
is not a review finding unless it affects correctness, CI, or maintainability.

## For AI coding agents

See `AGENTS.md`.
