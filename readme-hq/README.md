# README HQ operating guide

This BART workspace adapts the [standalone v0.0.6 guide](https://github.com/vixttha/README-HQ/blob/f50e3749dab90ddfe35894284d1660097a1fb1a8/README-GUIDE.md). The [adoption record](workspace/v0.0.6/README.md) identifies the source and what this branch applies.

## Write for the first useful action

Lead with what Blender-Agent Refinement Toolkit does and what readers can try today. For the CLI route, show the minimum install, a reproducible sample, and a recognizable result. Follow with the optional MCP route, Blender requirements, common failures, and the maintainer paths. Use the full product name and call the agent BART. Keep the installed command names and configuration keys as implemented.

Back up claims with the package manifest, the relevant documentation, and public runner evidence. Put the tested release and its limits beside the command. Treat the published release and current development checkpoint as separate facts. Use [the upstream audit guide](https://github.com/vixttha/README-HQ/blob/f50e3749dab90ddfe35894284d1660097a1fb1a8/audits/README.md) to check scope and [the technique catalog](https://github.com/vixttha/README-HQ/blob/f50e3749dab90ddfe35894284d1660097a1fb1a8/techniques/README.md) when selecting changes.

## Draft, verify, archive, and publish

1. Resolve the full application commit and record the proposed homepage version in a new [draft workspace](../workspace/README.md). Record the intended reader, acceptance checks, and any open issues the draft touches.
2. Use one descriptive heading hierarchy, short entry points, and alternative text for meaningful images. Check rendered navigation and relative assets in the destination tree. Verify the documented commands and outcomes on standard public runners. Record the source SHA, platforms, workflow, and actual checkout. Record unsupported hosts and checks that were unavailable.
3. Keep draft and published status visible. On approval, preserve the exact page and associated assets, note the source commit and evidence, and add the version to the [homepage history](../versions/README.md).
4. Publish only through a separate scoped PR to `main` with owner approval. Verify the destination page and CI. Keep `readme-hq` as the permanent documentation branch and `graphify-hq` as the independent evidence branch.

[Template versions](versions/README.md) · [Branch validation](../.github/workflows/readme-hq.yml) · [Graphify integration](../graphify/README.md)
