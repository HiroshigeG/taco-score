#!/usr/bin/env python3
"""Inject data/history.json into index.html between the taco-data markers."""
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent
payload = json.dumps(json.loads((root / "data/history.json").read_text()),
                     ensure_ascii=False, separators=(",", ":"))
html = (root / "index.html").read_text()
new = re.sub(r'(<script type="application/json" id="taco-data">).*?(</script>)',
             lambda m: m.group(1) + payload + m.group(2), html, flags=re.S)
assert new != html or payload in html, "markers non trovati"
(root / "index.html").write_text(new)
print("embedded", len(payload), "bytes")
