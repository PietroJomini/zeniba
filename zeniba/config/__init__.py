import tomli
from pathlib import Path

config_file = Path(__file__).parent / "config.toml"
config = tomli.loads(config_file.read_text())
