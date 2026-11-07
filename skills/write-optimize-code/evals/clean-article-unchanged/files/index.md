---
title: "How Do I Find Large Files on macOS?"
date: 2026-11-01
draft: true
---

List the ten largest files under your home directory:

```bash
du -ah ~ 2>/dev/null | sort -rh | head -n 10
```

To limit the search to files over 1 GB, use `find` with `-size`:

```bash
find ~ -type f -size +1G 2>/dev/null
```
