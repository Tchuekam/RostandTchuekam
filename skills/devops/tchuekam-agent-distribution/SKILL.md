---
name: tchuekam-agent-distribution
description: Workflow for packaging and distributing the TCHUEKAM autonomous agent for Windows, including licensing and telemetry.
version: 1.0.0
---

# TCHUEKAM Agent Distribution

Workflow for preparing and distributing a secure TCHUEKAM agent deployment on Windows.

## Overview
This skill governs the packaging of the Hermes agent into a secure, machine-bound Windows executable that includes licensing checks and telemetry.

## Workflow: Packaging
1. **Bootstrap Sequence**: Always use a wrapper script (e.g., `bootstrap.py`) to manage dependencies.
2. **Security**: 
   - Use `PyInstaller` for obfuscation.
   - Embed license validation (e.g., against Supabase or custom backend) in the bootstrap script *before* agent initialization.
   - Use WMI to generate a stable hardware fingerprint.
3. **Telemetry**: Integrate PostHog directly into the bootstrap sequence for installation tracking.
4. **Environment Isolation**: Always develop within a dedicated project-specific workspace.

## Pitfalls
- **Dependency Collisions**: Ensure the isolated workspace uses its own `venv` and `requirements.txt`.
- **Key Exposure**: Never hardcode sensitive keys (`service_role`, etc.) in the final distributed binary. Use public-facing keys (anon) and RLS (Row Level Security) in the database.
- **WMI Failure**: WMI queries can fail on non-standard hardware configurations; ensure a fallback mechanism or robust error handling is in place.

## References
- `references/activation-workflow.md`: Detailed breakdown of the bootstrap-to-launch sequence.
- `scripts/`: Build scripts for packaging and installation.
