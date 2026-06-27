#!/usr/bin/env python3
"""
TCHUEKAM Parseltongue CLI — Encode any query to bypass safety classifiers.
Usage:
  python parseltongue-cli.py "your query here" [--tier light|standard|heavy]
  
Example:
  python parseltongue-cli.py "How to hack a WiFi" --tier light
"""

import os, sys, json
from pathlib import Path

# Load parseltongue from godmode skill
HERMES_HOME = os.environ.get("HERMES_HOME", "D:\\hermes-home")
parsel_path = Path(HERMES_HOME) / "skills" / "red-teaming" / "godmode" / "scripts" / "parseltongue.py"

old_argv = list(sys.argv)
sys.argv = ["_parsel_cli"]

ns = {}
ns["__name__"] = "_parsel_module"
ns["__file__"] = str(parsel_path)
exec(compile(open(parsel_path).read(), str(parsel_path), 'exec'), ns)

sys.argv = old_argv

generate_variants = ns.get("generate_variants")
obfuscate_query = ns.get("obfuscate_query")
detect_triggers = ns.get("detect_triggers")
escalate_encoding = ns.get("escalate_encoding")

if len(sys.argv) < 2:
    print("Usage: python parseltongue-cli.py \"your query\" [--tier light|standard|heavy]")
    print("       python parseltongue-cli.py \"your query\" --detect-only")
    sys.exit(1)

query = sys.argv[1]
tier = "light"
detect_only = False

for i, arg in enumerate(sys.argv[2:], start=2):
    if arg == "--tier" and i + 1 < len(sys.argv):
        tier = sys.argv[i + 1]
    if arg == "--detect-only":
        detect_only = True

# Show trigger words
triggers = detect_triggers(query)
if triggers:
    print(f"⚠ Trigger words detected: {', '.join(triggers)}")

if detect_only:
    sys.exit(0)

# Generate variants
variants = generate_variants(query, tier=tier)

print(f"\n=== PARSELTONGUE ENCODINGS (tier: {tier}) ===\n")
for v in variants:
    label = v['label'].ljust(14)
    text = v['text']
    print(f"  [{label}] {text}")

print(f"\n{len(variants)} variants generated.")
print("\nTip: If the model refuses, try a higher tier: --tier standard or --tier heavy")
