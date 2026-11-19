# Release approval

The repository owner's manual workflow dispatch records approval for one final tag, one full commit SHA, and one successful application CI push run. Select the default branch at the approved commit and supply the three values in the dispatch. The package's version at that commit must match the tag.

The **Verify release approval** workflow runs with read-only permissions on a standard public GitHub runner. It verifies the owner identity, the default branch head, and every job in the exact application CI run. Running it directly verifies the release decision without publishing.

In **Prepare or publish a Blender-Agent pre-release**, use the same three inputs and leave **Publish the verified pre-release** unchecked for a live verification run. Once the read-only run passes and you approve the exact release, dispatch it again with publication checked. The publisher uses the verifier's tag and SHA, confirms the default-branch head again, and creates a new tag at the exact SHA before publishing the GitHub pre-release. The publishing job alone receives `contents: write`. An existing tag causes tag creation to fail. If tagging succeeds and publication fails, inspect the tag and failed run before authorizing recovery.

The standard CI unit tests exercise invalid owner, ref, SHA, version, CI run, and job results with synthetic inputs. The public pull-request check also feeds the authentic GitHub event to the verifier and requires a rejection. To exercise a positive owner dispatch, GitHub requires the workflow on the default branch.
