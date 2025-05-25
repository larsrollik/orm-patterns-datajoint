from __future__ import annotations

import logging
from pathlib import Path

import datajoint as dj
import yaml

from orm_patterns_datajoint.config.model import AppConfig

_config: AppConfig | None = None
_config_path: Path | None = None


def resolve_path(path: str | Path) -> Path:
    return Path(path).expanduser().resolve(strict=False)


package_name = resolve_path(__file__).parent.parent.name


def get_package_config_filename() -> str:
    return f"{package_name}.config.yaml"


def get_default_config_paths() -> list[Path]:
    """Return a list of default search paths for the config file."""
    config_name = get_package_config_filename()
    return [
        Path.cwd() / config_name,
        Path(__file__).parent / config_name,
        Path.home() / config_name,
    ]


def find_existing_config_path() -> Path:
    """Return the first existing config file path from defaults."""
    for path in get_default_config_paths():
        if path.exists():
            return path
    raise FileNotFoundError(
        f"Could not find config file '{get_package_config_filename()}' "
        f"in: {[str(p.parent) for p in get_default_config_paths()]}"
    )


def write_default_config(
    path: Path | str | None = None,
    overwrite: bool = False,
    exist_ok: bool = False,
    home_fallback: bool = False,
) -> Path:
    """
    Write the default config to a given or first valid path.

    Args:
        path: Optional target path to write to.
        overwrite: Whether to overwrite if file exists.
        exist_ok: If True, do not raise error if file exists.
        home_fallback: If True, fallback to writing in user home dir.

    Returns:
        Path to the written config file.

    Raises:
        FileExistsError if file already exists and overwrite=False.
        FileNotFoundError if no valid directory to write to.
    """
    config_name = get_package_config_filename()
    target = None

    if path:
        path = resolve_path(path)
        target = path / config_name if path.is_dir() else path

    else:
        for p in get_default_config_paths():
            if p.parent.exists():
                target = p
                break

    if not target or home_fallback:
        target = Path.home() / config_name
        logging.info(f"Writing default config to user home directory: {target}")

    if not target:
        raise FileNotFoundError("No suitable location found for default config.")

    if target.exists() and not overwrite:
        if exist_ok:
            return target  # Exists, do nothing
        raise FileExistsError(f"Config already exists at {target}")
    # Else: overwrite

    # No file yet or overwriting
    default = AppConfig().as_original_dict()
    with Path(target).open("w") as f:
        yaml.safe_dump(default, f)
        logging.info(f"Wrote default config to: {target}")

    return target


def load_config(path: Path | str = "") -> AppConfig:
    """Load the config and cache both the config and path."""
    global _config, _config_path
    if _config is not None:
        return _config

    _config_path = resolve_path(path) if path else find_existing_config_path()
    with Path(_config_path).open("r") as f:
        yaml_cfg = yaml.safe_load(f) or {}

    _config = AppConfig(**yaml_cfg)
    return _config


def get_config() -> dict:
    """Return the currently loaded config as a dict with original keys."""
    if _config is None:
        raise RuntimeError("Call load_config() first.")
    return _config.as_original_dict()


def save_config() -> bool:
    """Write the current config back to the same file it was loaded from."""
    if _config is None or _config_path is None:
        raise RuntimeError("No config loaded; cannot save.")

    with Path(_config_path).open("w") as f:
        yaml.safe_dump(_config.as_original_dict(), f, sort_keys=False)
        logging.info(f"Saved current config to: {_config_path}")
    return True


def patch_datajoint_config(path: Path | str = "") -> None:
    """Load config and patch dj.config directly with matching keys."""

    config = load_config(path).as_original_dict()
    dj.config.update(config)
