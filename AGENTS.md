# Agent instructions

This repository documents a design. It contains no build step, no test suite, and
no deployed service. Keep it that way.

## Conventions

- **Prose style.** Active voice. One instruction per sentence. Define a term the
  first time it appears. Prefer a concrete number over an adjective.
- **Cross-references** are relative paths from the file that mentions them. Every
  link must resolve — check before committing.
- **No unverified numbers.** A figure is either measured here, or attributed to its
  source with a link. Do not present an author-reported result as a benchmark.
- **Headings are short and literal.** An em dash is allowed only as a separator
  between a label and its expansion (`L2 — Owner`), never to join two clauses.

## What this repository must not become

- **Not a framework.** `reference/` exists to be copied, not installed. Do not add
  packaging, a version number, or a release process to it.
- **Not a vendor pitch.** Nothing here may require a specific product. Provider
  mentions are evidence, not recommendations.
- **Not a benchmark claim.** No performance claim without a linked source and a
  statement of what was actually measured.

## Evidence discipline

This matters more here than in most repositories, because the design is justified by
published results and those results are easy to misreport.

When citing a finding:

1. Link the primary source, not a summary of it.
2. State what was measured, on what task class, with what models.
3. If it is an experience report rather than a controlled study, say so.
4. If a result cuts against this design, include it. The tradeoffs document is
   required to carry the counter-evidence.

A paraphrase is not a citation. If you have not read the source, do not cite it.

## Diagrams

Rendered from `diagrams/render_animations.py`. Edit the source and re-run rather than
editing an image. Caption arrays and layout functions are independent — update both
together, or the diagram will label the wrong stage.

## Editing rules

Each pattern file follows the same shape: Problem, Solution, Invariants, Checks,
Failure if omitted. Keep that order. The invariants are the content; if you change
one, check whether the corresponding document in `docs/` makes the same claim, and
change both.
