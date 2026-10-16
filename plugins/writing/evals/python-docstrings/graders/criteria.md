---
type: llm
focus: { source: file, path: src/geo.py }
weight: 2
---

PASS only if all of the following hold for the docstrings in src/geo.py:
1. Each of the six public functions (validate, distance_km, bearing, destination, format_dms, waypoints) has a Google-style docstring whose `Args:` section lists exactly the parameters in that function's signature, each with a description (a description may wrap onto continuation lines or run to two sentences; that is normal Google style).
2. Every function that returns a value has a `Returns:` section, except `waypoints`, which is a generator and uses `Yields:` instead. `validate` returns nothing and may omit `Returns:`.
3. `validate` and `format_dms` each list `ValueError` under `Raises:` with the condition that triggers it. No other function claims to raise.
4. The `Returns:` section of `destination` describes the tuple element by element: latitude first, then longitude, both in degrees.
5. Each summary line is a single sentence ending in a period, starts on the opening `"""` line, and says what the function does rather than restating its name or signature (for example "Compute the great-circle distance between two points." passes; "distance_km function." fails).
6. The module has a docstring that says what the module provides.
7. The function bodies and signatures are unchanged.
`_helper` is private and may stay undocumented. FAIL if any docstring names a parameter that does not exist, describes a return type the code does not produce, or uses "This function", "Function to", or "Returns the result" as a summary.
