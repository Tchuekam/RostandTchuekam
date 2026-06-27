"""Print the content of USER.md and its backup for review."""
path = "D:\\hermes-home\\memories\\USER.md"
bak = path + ".bak.1779820915"
print("=== USER.md ===")
try:
    print(open(path).read())
except Exception as e:
    print(f"Error: {e}")
print("=== Backup ===")
try:
    print(open(bak).read())
except Exception as e:
    print(f"Error: {e}")
