# Flask-Oxide: Workspace Instructions for AI Agents

## Action Guidelines for AI Agents
- Always check that your edits maintain consistency with the rest of the file and project.
- Always edit in a contextually appropriate location within the file, considering the logical flow and structure.
- Before and after editing, investigate whether there are related or affected sections/files, and synchronize or update them as needed to maintain consistency across the project.
- Do not make changes that conflict with established conventions or documentation.
- If unsure, consult maintainers as needed.

### Dependency Management and User Consent
- Never edit dependency management files (e.g., pyproject.toml, requirements.txt) or add/remove packages (e.g., via uv add/uv remove) without explicit user permission.
- Do not use pip install, uv pip, or similar commands for temporary or unmanaged installs unless the user specifically requests it.
- Always explain and confirm with the user before making any changes to project dependencies or environment configuration.

## Overview
This repository provides "Flask-Oxide," an extension that enables seamless integration and development of Rust modules in Flask applications with a developer experience equivalent to native Python. For project goals, priorities, and features, see [FEATURES.md](./FEATURES.md). For a general overview, see [README.md](./README.md).

## Development Environment
- Python 3.14 or higher
- Dependency management: [uv](https://astral.sh/uv/) + `pyproject.toml`
- Rust build/integration: planned for future updates

## Setup Instructions
1. **Dev Container Recommended**: Use the configuration in `.devcontainer/`
2. **Install dependencies**:
   ```sh
   # This runs automatically in the devcontainer, but for manual setup:
   wget -qO- https://astral.sh/uv/install.sh | sh
   uv sync && uv pip install -e .
   ```
3. **Virtual environment**: `~/.venv` is automatically activated

## Build & Test
- No Rust/Python implementation or test code is present at this time
- When adding implementations or changing requirements, update this file and [FEATURES.md](./FEATURES.md) accordingly

## Documentation
- [FEATURES.md](./FEATURES.md): Requirements and development specifications (project goals, features, priorities)
- [STRUCTURE.md](./STRUCTURE.md): Directory structure plan and roles of each directory
- [README.md](./README.md): Project overview
- [DESIGN.md](./flask_oxide/DESIGN.md): Design concepts and architectural decisions
- [CODING_STYLE.md](./CODING_STYLE.md): Coding conventions

## Coding Style
- All code generation, review, and edits (by humans or AI agents) must strictly follow the rules in [CODING_STYLE.md](./CODING_STYLE.md).
- When editing code, always check for consistency with this style and update related sections/files as needed.

## Notes
- Details on Rust integration and Flask extension will be added in the future
- Development rules and coding conventions are not yet defined
- For directory structure and file placement, see [STRUCTURE.md](./STRUCTURE.md)

## Project Language Policy
- All source code, comments, and documentation must be written in **English**.
- Communication between developers may be conducted in Japanese, but all deliverables must be in English only.

---

> **Link, don't embed**: For detailed explanations and guides, refer to README and other documentation. Only link here.
