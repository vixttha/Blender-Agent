# Security

This project reads third-party 3D formats and may launch Blender. **Treat externally supplied models and BLEND projects as untrusted.** The path rules are safeguards, not OS isolation.

## Defensive controls

- Inputs and outputs are restricted to a configured, resolved workspace root.
- A source file can never be its own output path; existing outputs are not overwritten unless the CLI explicitly opts in.
- Publication without overwrite uses atomic hard-link creation: concurrent writes cannot silently clobber the same destination.
- The output parent and temporary path are revalidated before publication. Untrusted processes must not concurrently mutate workspace paths or symlinks; use separate OS-level sandboxes for hostile multi-tenant execution.
- Blender runs a fixed worker under background/factory startup with auto-execution disabled; tools do not accept arbitrary generated scripts.
- Blender work has a bounded timeout (default 180 seconds, maximum 900), captured log budget (256 KiB), source cap (512 MiB), and output cap (512 MiB). Detailed STL/OBJ inspection is limited to 128 MiB.
- Input parsers reject non-finite coordinates and invalid OBJ vertex references; these checks do not validate entire geometry.

## Residual risks

Operating system process memory, Blender add-ons and importer vulnerabilities, hostile directory rename races, and source mutations during import are not comprehensively sandboxed. Never run this process with elevated privileges or on a shared hostile workspace. Untrusted workloads should use a true OS/container boundary. No network service is provided.

## Responsible reporting

Use GitHub private vulnerability reporting if the repository enables it. If unavailable, request a private channel without posting exploit material in a public issue.

The v0.0.2 candidate is pre-alpha and carries no established security-support commitment.
