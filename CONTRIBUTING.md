# Contributing

Contributions should be focused, testable and safe for users of different AI harnesses.

- Work on a feature branch with a reviewable PR and exact-candidate public CI evidence.
- Document scope, supported formats, limitations and observable acceptance criteria.
- Reuse the same underlying Python implementation for CLI, MCP and future integrations.
- Add safety regressions for non-overwrite publication, simultaneous writers, symlinks, bad geometry and resource limits.
- Run real Blender integration for changed Blender operations; Python mocks alone are insufficient.
- Test the MCP server using an actual client session if MCP adapters change.
- Never commit real user asset data, identity information, secrets, proprietary fixtures or dynamically generated code without review.

Python checks:

~~~sh
python -m pip install -e .
python -m compileall -q src
python -m unittest discover -s tests -p "test_*.py" -v
~~~

MCP checks:

~~~sh
python -m pip install -e ".[mcp]"
python tests/test_mcp_smoke.py
~~~

Public CI is the verification source. A passing PR test does not waive a final review or release decision.
