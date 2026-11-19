# Security

The project imports complex 3D formats. Treat all external models and Blender projects as untrusted.

Safeguards currently implemented:

- Workspace-restricted paths with symlink resolution.
- No in-place source-file modification.
- Outputs refuse to overwrite existing files unless an explicit CLI overwrite flag is provided.
- A fixed Blender worker; no model-provided script execution.
- Factory startup and disabled automatic script execution for background Blender runs.
- Timeouts and temporary output promotion only after basic success checks.

These controls do not eliminate Blender importer vulnerabilities or malicious content in untrusted projects. Keep permissions minimal, use an isolated execution environment for risky files, and verify generated outputs separately.

For vulnerability reports, use GitHub private vulnerability reporting if enabled. Do not publish exploitation steps or private information in a public issue.

v0.0.1 is pre-alpha and has no established security-support service-level commitment.
