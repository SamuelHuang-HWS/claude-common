# Gemini Adapter Status

Status: research_note

Gemini CLI adapter support is intentionally not production-ready in Phase 4 v1.

Current assumptions:

- Gemini customization is expected to be extension-oriented rather than a direct one-file-per-agent mapping.
- A future adapter may map Sisyphus role contracts to extension assets such as `agents/`, `skills/`, `commands/`, `hooks/`, and `policies/`.
- Until local behavior is verified, Gemini adapter files must not be used for production Sisyphus gates.

Phase 4 v1 rule:

> Claude Code is the concrete adapter target; Codex is an experimental skeleton; Gemini remains documented research until validated.
