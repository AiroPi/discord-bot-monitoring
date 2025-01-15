import tomllib
from pathlib import Path

CONFIG_PATH = Path("config.toml")

monitor_ids: set[int]

if not CONFIG_PATH.exists() or not CONFIG_PATH.is_file():
    monitor_ids = set()
else:
    with CONFIG_PATH.open("rb") as f:
        _config = tomllib.load(f)
    monitor_ids = set(_config["monitor_ids"])
