# Contributing

Focused contributions are welcome.

- Describe a real user workflow, its assumptions and acceptance criteria.
- Use a feature branch and a reviewable pull request.
- Preserve CLI/MCP behavior through shared core functions.
- Add negative-path tests for paths, untrusted inputs, overwrites and Blender failures.
- Keep fixtures synthetic and small; do not commit proprietary models or private information.
- State which Blender version was actually tested. Python-only CI does not verify Blender integration.
- Keep all commands sandboxable; do not introduce an arbitrary Python or shell execution endpoint.

Local checks:

~~~sh
python -m pip install -e .
python -m compileall -q src
python -m unittest discover -s tests -v
~~~

Contributions must not disclose private identity information, tokens, non-public files or external proprietary assets.
