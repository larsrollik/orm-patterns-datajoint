import logging
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import datajoint as dj

from orm_patterns_datajoint.config.tools import (
    patch_datajoint_config,
    write_default_config,
)

try:
    __version__ = version(Path(__file__).parent.name)
except PackageNotFoundError:
    __version__ = "0.0.4"

__all__ = ["write_default_config", "patch_datajoint_config"]


def _prepare_schema_name(file):
    return Path(file).stem


def get_datajoint_schema(
    file, linking_module, default_global_schema_prefix: str = "GLOBAL_SCHEMA_PREFIX_DEFAULT"
):
    schema_prefix = dj.config.get("global_schema_prefix", default_global_schema_prefix)
    schema_name = _prepare_schema_name(file)
    full_schema_name = f"{schema_prefix}__{schema_name}"

    schema = dj.Schema(
        schema_name=full_schema_name,
        create_schema=True,
        create_tables=True,
        add_objects=(linking_module.__dict__ if hasattr(linking_module, "__dict__") else None),
    )
    logging.info(f"Schema: {full_schema_name}")
    return schema
