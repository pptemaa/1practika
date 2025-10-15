import toml
import sys
import os

try:
    cfg = toml.load("config.toml")
except Exception as e:
    print(f"Ошибка загрузки: {e}", file=sys.stderr)
    sys.exit(1)

params = [
    ("package_name", str),
    ("repository_url", str),
    ("repo_mode", str),
    ("output_image", str),
    ("ascii_tree", (bool, str)),
    ("max_depth", int),
]

for k, t in params:
    if k not in cfg:
        print(f"Нет параметра: {k}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(cfg[k], t):
        print(f"Неверный тип у {k}", file=sys.stderr)
        sys.exit(1)

if cfg["repo_mode"] not in {"clone", "local", "none"}:
    print("repo_mode: допустимые значения — clone/local/none", file=sys.stderr)
    sys.exit(1)

if cfg["repo_mode"] == "local" and not os.path.exists(cfg["repository_url"]):
    print(f"Файл или каталог не найден: {cfg['repository_url']}", file=sys.stderr)
    sys.exit(1)

if cfg["max_depth"] < 0:
    print("max_depth < 0", file=sys.stderr)
    sys.exit(1)

for k, v in cfg.items():
    print(f"{k} = {v!r}")
