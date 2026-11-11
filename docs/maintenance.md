# Collection maintenance

Every focused repository must include useful original implementation, reproducible examples and meaningful tests. Follow [original work and attribution](../ORIGINAL_WORK.md). Keep upstream copyright and license scope intact when adapting external code; do not rebrand linked resources as authored implementations.

Standalone original bundles live in `originals/` and are distributed to their focused homes. Run `python3 scripts/check_originals.py` before generation/publication, then run the tests from each generated repository to verify its standalone packaging.

## Curation standard

Prefer a small useful improvement over catalog growth. For each candidate, identify a task it improves, a gap it fills, prerequisites, license scope, and a way to evaluate it. Correct moved sources and lifecycle notes before adding a redundant alternative.

Use primary repositories and vendor/project documentation. Record immutable revisions and file identities. Read the actual license scope rather than inheriting a badge. Preserve the distinction between complete entry review, entry excerpt, README overview and observed execution.

Do not copy upstream bundles, claim benchmark gains from marketing, or manufacture activity when nothing merits a change. Original summaries, fixtures and guides should explain how to make a concrete decision.

## Updating related repositories

The hub catalog is the research register. Focused repositories retain stable entry IDs and source revisions. All 160 skill entries have exactly one focused subject home; related tools can appear in multiple collections.

The portable generator creates reviewable focused outputs:

```bash
python3 scripts/build_collections.py --output-root ../generated-collections
python3 scripts/arsenal.py check
```

Generate into a separate directory, review differences against each repository's latest main, and preserve intentional manual edits. The generator writes complete collection files; it is not a merge tool. Verify each resulting catalog before publishing.

## Evidence before publication

1. Read current remote heads and affected files.
2. Update the catalog, focused selections and counts consistently.
3. Regenerate pages and run the relevant local checks.
4. Publish with expected-head checks; reconcile concurrent work instead of forcing a ref.
5. Compare published file identities and report the observed validation scope.

An upstream tool being listed does not imply it was installed or tested. Hosted CI status and local checks are separate evidence. Keep credentials and private logs out of catalog records and fixtures.

## Original tools and fixture evidence

Privacy Guard is original repository code with a bounded email/JSON-field masking policy. Its synthetic fixtures, unit tests and CLI checks are separate from upstream catalog review labels.

```bash
python3 scripts/check_privacy_fixtures.py --check-report examples/privacy-guard-results.json
python3 -m unittest discover -s tests -v
```

After changing the guard or its fixtures, regenerate the recorded result and review it before publication:

```bash
python3 scripts/check_privacy_fixtures.py --write-report examples/privacy-guard-results.json
```

The report contains fixture IDs, outcomes, and source/fixture hashes; it excludes raw input and transformed payloads. A passing synthetic report establishes only the documented policy on those cases. It does not establish universal PII coverage, upstream Presidio behavior, or safe handling of untested formats.
