# Activation Workflow

The TCHUEKAM agent uses a strict pre-launch gatekeeper sequence:

1. **Hardware Fingerprinting**: `bootstrap.py` utilizes `wmi` to query the motherboard's serial number. This acts as the unique device identifier.
2. **Telemetry Pinging**: Before contacting the license server, the binary performs an asynchronous `posthog.capture` event. This allows tracking of every attempt to launch the agent.
3. **License Validation**:
   - The binary sends the unique fingerprint to the Supabase `licenses` table.
   - It checks the `is_active` column.
   - **Fail-Fast**: If `is_active` is not `True`, the process `sys.exit(1)` immediately, preventing the `hermes` agent process from ever initializing.
4. **Hermes Handover**: Upon successful validation, the bootstrap process spawns the `hermes` agent as a sub-process, passing through any necessary environmental context.
