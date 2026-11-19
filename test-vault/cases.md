# Blender-Agent cases

| Case | Area | Priority | Suggested implementation | Expected outcome |
|---|---|---|---|---|
| DOCS-001 | Catalog | P0 | Python standard library | The validator accepts a well-formed catalog and exits successfully. |
| PYTHON-001 | Host runtime | P0 | CI unit and negative-path tests on Python 3.11 and 3.12, Linux and Windows | Package installs, source compiles, and unit and negative-path tests pass on each runtime. |
| MCP-001 | Installed MCP and Blender | P0 | Existing OBJ and MTL roundtrip in `tests/test_mcp_smoke.py` | The re-imported GLB assigns AuditRed with red RGBA; existing OBJ and MTL destinations and source bytes are preserved. |
| BLENDER-001 | Blender Python | P0 | Two-scene fixture and MCP conversion in `tests/test_mcp_smoke.py` | Pre-export geometry reports the active triangle only. The exported STL independently measures one triangle. |

The repository's CI runs these cases on standard public GitHub-hosted runners. Use the Python matrix job results for PYTHON-001. The installed-wheel Blender smoke jobs append the two Blender case verdicts, expected and observed values, exact checkout SHA, and run identity to their job summaries.

BLENDER-001 tracks [issue #55](https://github.com/vixttha/Blender-Agent/issues/55). The exact known file-wide count mismatch is reported as a failed case and a CI warning while the smoke job continues. Any other mismatch fails the smoke job. Remove that exception when issue #55 is repaired.
