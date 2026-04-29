# Sisyphus Skill Contracts

This directory contains machine-readable YAML contracts for active `proj-*` skills and `cross-review`.

## Structure

- `contract.schema.json`: JSON Schema subset used by health checks.
- `*.contract.yaml`: Individual skill contracts.

## Rules

- Do **not** copy detailed instructional text from `SKILL.md` into contracts.
- Contracts define only I/O, routing, boundaries, and validation-relevant metadata.
- `name` must match the filename and the actual skill directory name.
- `what` and `when` must be concise and useful for routing.
- `forbidden_actions` must describe role boundaries.
- Retired skills should be removed from active contracts after their skill directory is removed.
