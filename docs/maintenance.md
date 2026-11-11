# Collection maintenance

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
