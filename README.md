<div align="center">

# Blender-Agent · Code Stack

**Programming language architecture for Blender automation**

[Stack](STACK.md) · [Memory](STACK_MEMORY.md) · [Audit](AUDIT.md) · [Proposals](PROPOSALS.md) · [Registry](code-stack.json)

</div>

> [!TIP]
> **Starting with a new agent?** Give it this README URL and say **“Read Code Stack and work as Stack.”** It can load the [role](STACK.md) and [recorded project context](STACK_MEMORY.md) directly from Git.

```mermaid
flowchart LR
    CLI["Command line"] --> CORE["Python core"]
    MCP["MCP host"] --> CORE
    CORE -- "JSON job" --> WORKER["Blender Python worker"]
    WORKER --> RESULT["Asset and geometry report"]
```

## Where each language belongs

| Layer | Choice | Why it belongs |
| --- | --- | --- |
| **Core and host tooling** | Python | The CLI and MCP adapter share asset and job logic. The core declares no runtime dependencies, and MCP is optional. [Architecture](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/docs/ARCHITECTURE.md) · [Package](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/pyproject.toml) |
| **Inside Blender** | Python with `bpy` and `bmesh` | These Blender APIs are already used by the worker for scene and mesh operations. [Worker](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/src/blender_agent/blender_worker.py) · [Blender API](https://docs.blender.org/api/main/info_overview.html) |
| **Between processes** | JSON | The host writes explicit job data and the worker returns a geometry report. [Host](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/src/blender_agent/jobs.py) · [Worker](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/src/blender_agent/blender_worker.py) |
| **Build, checks and documentation** | TOML, YAML, embedded Bash and Markdown | Package configuration, free public-runner CI and human-readable project documentation. [Workflow](https://github.com/vixttha/Blender-Agent/blob/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b/.github/workflows/ci.yml) · [GitHub runner billing](https://docs.github.com/en/actions/concepts/billing-and-usage) |

## Where the stack can grow

| If we approve this work | Consider | Design review |
| --- | --- | --- |
| Browser asset preview | TypeScript with HTML/CSS | [CS-002](PROPOSALS.md#cs-002--browser-asset-viewer) |
| A demonstrated mesh-processing bottleneck | Rust for an isolated helper, or C++ for a specific geometry library | [CS-003](PROPOSALS.md#cs-003--measure-before-native-code) |
| Artist-editable parametric models | Python with Blender Geometry Nodes | [CS-004](PROPOSALS.md#cs-004--editable-procedural-modeling) |

## Evidence you can follow

| Record | What it tells you |
| --- | --- |
| [Foundation audit](AUDIT.md) | Exact application revision, observed stack, tested scope and open checks |
| [Technology registry](code-stack.json) | Status, role and primary evidence for every registered technology |
| [Code Stack Actions](https://github.com/vixttha/Blender-Agent/actions/workflows/code-stack.yml) | Run results for the branch's audit against the pinned application |
| [Portable template v0.0.1](https://github.com/vixttha/Blender-Agent/tree/042390d63e72dc3e1fbb0c87387ea9f8d42f1d6f/v0.0.1) | Copyable files for any Git project, with a validator and proposal format |

<details>
<summary>Documentation patterns we borrowed</summary>

- **VS Code** documents source organization by architectural layer. This hub maps technologies to Blender-Agent's execution boundaries. [VS Code source organization](https://github.com/microsoft/vscode/wiki/Source-Code-Organization)
- **Rust RFCs** put motivation, trade-offs and alternatives alongside each proposal. Our proposals add validation and rollback for the specific project. [Rust RFC template](https://github.com/rust-lang/rfcs/blob/master/0000-template.md)
- **CPython** uses its README to route users to documentation and practical next steps. The links above give humans and agents a short path to the files they need. [CPython README](https://github.com/python/cpython/blob/main/README.rst)

</details>

**Audited application:** [v0.0.2 candidate `2f621fbd`](https://github.com/vixttha/Blender-Agent/commit/2f621fbd5ad0e3e6a96bc9037a9d7cd28edda65b) · **Review:** [Foundation PR #1](https://github.com/vixttha/Blender-Agent/pull/1)
