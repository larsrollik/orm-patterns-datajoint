import logging
from pathlib import Path

import datajoint as dj


def prepare_schema_name(file):
    return Path(file).name.replace(".py", "")


def get_global_schema_prefix():
    return "EXAMPLE_GLOBAL_PREFIX"


def get_datajoint_schema(
    schema_prefix=None,
    schema_name=None,
    linking_module=None,
):
    """
    Check available schemas with:
        available_schemas = dj.list_schemas()

    """
    if schema_prefix is None:
        schema_prefix = get_global_schema_prefix()

    schema = dj.Schema(
        schema_name="__".join([schema_prefix, schema_name]),
        create_schema=True,
        create_tables=True,
        add_objects=(
            linking_module.__dict__
            if hasattr(linking_module, "__dict__")
            else None
        ),
    )
    logging.info(f"Schema: {schema}")
    return schema
