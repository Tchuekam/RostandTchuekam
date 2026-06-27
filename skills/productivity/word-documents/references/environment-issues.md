# Known Environment Issues

## Python "SRE module mismatch" Error

When running `pip install`, `uv pip install`, or any Python import, you may encounter:

```
AssertionError: SRE module mismatch
```

This occurs when the Python interpreter version doesn't match its stdlib (e.g. Python 3.12 executable tries to load 3.11 stdlib modules from a cached uv environment).

### Workarounds

**1. Use Node.js instead of Python** for document creation (the `docx` npm module works fine).

**2. Pin the Python environment explicitly:**

```bash
# Use the full path to the exact Python executable
/c/Users/CLINIC/AppData/Local/Programs/Python/Python312/python.exe

# Sometimes uv's cached environment is the mismatch source
# Try installing via the system Python directly:
/c/Users/CLINIC/AppData/Local/Programs/Python/Python312/python.exe -m pip install "markitdown[pptx]"
```

**3. Install packages via npm** when Node.js equivalents exist (faster, no env conflicts).
