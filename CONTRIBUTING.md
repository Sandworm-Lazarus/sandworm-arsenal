# Contributing

Useful additions solve a concrete task and have inspectable sources. A smaller, well-described collection is welcome.

1. Read the entry and its required supporting files. Do not execute a new package just to add a link.
2. Record the canonical repository, full commit, entry path, blob SHA, purpose, dependencies, and license evidence in `catalog/arsenal.json`.
3. Describe what you inspected. Keep source review separate from runtime evaluation. Do not label an entry tested without a reproducible report, environment, inputs, and outcome.
4. Explain why it adds value or replaces an existing entry. Identify forks and platform-specific requirements.
5. Regenerate the catalog and source pages, then run the local checks:

```bash
python3 scripts/arsenal.py render
python3 scripts/arsenal.py check
python3 -m unittest discover -s tests -v
```

Schema v2 represents read-only research. Use `entry-reviewed` with `read: true` for an entry-file review, or `entry-overview` with `read: false` for frontmatter and an opening excerpt. Neither covers every bundled file automatically. Record the exact scope in notes. A future runtime-tested entry needs a schema extension and an evaluation report; do not simply flip `runtime_tested` to `true`.

Keep third-party skill bodies and executable bundles out of this curated repository. Link to them at a reviewed revision. Original summaries and playbooks should be concise and useful in Thai or English.

For corrections, include the affected entry, a pinned source link, and the evidence that changes the conclusion. Never include credentials, private logs, or customer data in an issue or pull request.
