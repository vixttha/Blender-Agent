# v0.0.3 verification

- **Instructions HQ baseline** was [`388ddccdf6d84d302ce66392942873ab6c4347aa`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/commit/388ddccdf6d84d302ce66392942873ab6c4347aa). The [baseline archive job](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/actions/runs/44478687786/job/135405353651) verified the v0.0.2 archive and Graphify MCP.
- **Engineering baseline** was [`3e7f9e02e61739825b56bcafecebbd0221cc9657`](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/commit/3e7f9e02e61739825b56bcafecebbd0221cc9657). The [application CI run](https://github.com/vixttha/Blender-Agent-Refinement-Toolkit/actions/runs/44478268534) applies to that `main` commit.
- **Candidate archive and Graphify** receipts are produced by the [Instructions Archive workflow](../.github/workflows/instructions-archive.yml) and recorded on the candidate PR. Use the exact PR head, base and tested checkout from that receipt. The Graphify run reports its tool version, source files, graph checksum and MCP read-back. The committed graph snapshot follows the Instructions HQ push through the existing [Graphify archive process](../graphify/README.md).
- **Active ChatGPT Project settings and fresh-chat behavior** are pending. Follow the [setup guide](README.md) and record both results privately.
- **Maintainer acceptance** is pending.
