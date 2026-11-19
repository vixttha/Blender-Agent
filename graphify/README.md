# Code Stack Template Graphify HQ

| Version | Actual files | Graphify | Provenance |
| --- | --- | --- | --- |
| v0.0.1 | [Template](../v0.0.1/) | [Map](v0.0.1/graph.json) | [Receipt](v0.0.1/receipt.json) |
| v0.0.2 | [Template](../v0.0.2/) | [Map](v0.0.2/graph.json) | [Receipt](v0.0.2/receipt.json) |

Use [the comparison](../VERSION_HISTORY.md) for the differences between versions. The maps are kept beside the kits so copying a version folder installs just the template. This archive uses the [Blender-Agent Graphify HQ](https://github.com/vixttha/Blender-Agent/tree/graphify-hq) pattern and indexes Code Stack itself.

## Use a version map through MCP

Choose the graph for the version you need. A Graphify MCP host can run its stdio server with that graph file as its argument:

    python -m graphify.serve graphify/v0.0.2/graph.json

Useful read-only lookups:

- `graph_stats` gives counts for the loaded version.
- `get_node` with `document:v0.0.2/AUDIT.md` locates the audit guide.
- `get_node` with `symbol:v0.0.2/tools/audit.py:inventory` locates the Python inventory function.

Each map includes tracked kit files, Markdown headings and relative links, and Python definitions and imports. This is a static navigation map. The Graphify job tests MCP in Actions. Using the same graph in a chat requires a connected Graphify host.

## Maintain the archive on public runners

The [catalog](catalog.json) pins each version folder to the commit that contains its files. The workflow checks the tracked folder against that commit, rebuilds with the pinned [Graphify HQ tools](https://github.com/vixttha/Blender-Agent/tree/5526238af9b510092db336d01b26a42c1ef82548/tools/graphify), and queries Graphify MCP for counts, files and Python symbols. Each receipt records the Git blobs, Graphify version, and the graph hash.

When files are missing or differ, the job emits bounded `CODE_STACK_GRAPH_EXPORT` records after MCP verification. Review and commit the emitted files to the candidate branch, then require a passing rebuild before merging. Use the version PR to determine approval. Receipts record source provenance independently of PR state.
