# README HQ validation fixtures

The README HQ unit tests create ephemeral copies of approved documentation files and modify them to verify failure behavior. They exercise archive drift, missing files, broken links, and accidental credential-like text. No downloaded assets, private files, personal paths, or external network access are required.

This directory contains documentation only; the actual fixtures are created in temporary directories by `tests/test_readme_hq.py`.
