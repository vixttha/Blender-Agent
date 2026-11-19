# Release approval

The repository owner's manual workflow dispatch records approval for one final tag, one full commit SHA, and one successful application CI push run. Select the default branch at the approved commit and supply the three values in the dispatch. The package's version at that commit must match the tag.

The **Verify release approval** workflow runs with read-only permissions on a standard public GitHub runner. It verifies the owner identity, the default branch head, and every job in the exact application CI run. Running it directly verifies the release decision without publishing.

A later publishing workflow must use a manual dispatch with the same three inputs and call `.github/workflows/release-approval.yml`. Set the publisher job to depend on the verification job with `needs`, and use only the verified `release_tag` and `release_sha` outputs. Give `contents: write` only to the publishing job. Immediately before publishing, confirm the default branch still points to the verified SHA and the requested tag is unused.

The standard CI unit tests exercise invalid owner, ref, SHA, version, CI run, and job results. Those tests use synthetic inputs and create no releases.
