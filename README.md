# py-config-resolver

Reusable configuration resolution and YAML/JSON parsing utilities extracted from
the `mcv` (advanced-templating) project.

## Library

```python
from config_resolver import parse_data, read_config, merge_dicts

data = parse_data("cv.data.yaml")          # path or inline YAML/JSON string
config = read_config(data.get("config"), {"output": "cv.pdf"})
```

## CLI

```bash
# Print the merged configuration discovered from /etc/mcv, ~/.config/mcv,
# the current directory and its ancestors.
config-resolver show

# Apply CLI overrides on top of the discovered configuration.
config-resolver show --set output=cv.pdf --set template=/cv/v2/main.tex

# Parse an inline value or a file.
config-resolver parse '{"name": "Ada"}'
config-resolver parse cv.data.yaml

# Merge several files (later files win).
config-resolver merge base.yaml local.yaml
```
