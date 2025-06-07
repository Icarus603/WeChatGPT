# Repository Guidelines

- Run `pytest -q` after making changes.
- Use `poetry` for dependency management. Ensure any new dependencies are added to `pyproject.toml`.
- Configuration such as API tokens should be stored in `config.yaml` which is ignored by git. Use `config_template.yaml` as the template.
- This project targets macOS; avoid Windows-specific libraries.
