from typing import Any

from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    # Flat dot-named config keys with field aliases
    add_hidden_timestamp: bool = Field(False, alias="add_hidden_timestamp")
    connection_charset: str = Field("", alias="connection.charset")
    connection_init_function: str | None = Field(None, alias="connection.init_function")
    database_host: str = Field("localhost", alias="database.host")
    database_password: str | None = Field(None, alias="database.password")
    database_port: int = Field(3306, alias="database.port")
    database_reconnect: bool = Field(True, alias="database.reconnect")
    database_use_tls: bool | None = Field(None, alias="database.use_tls")
    database_user: str | None = Field(None, alias="database.user")
    display_limit: int = Field(12, alias="display.limit")
    display_show_tuple_count: bool = Field(True, alias="display.show_tuple_count")
    display_width: int = Field(14, alias="display.width")
    enable_python_native_blobs: bool = Field(True, alias="enable_python_native_blobs")
    fetch_format: str = Field("array", alias="fetch_format")
    filepath_checksum_size_limit: int | None = Field(None, alias="filepath_checksum_size_limit")
    loglevel: str = Field("INFO", alias="loglevel")
    safemode: bool = Field(True, alias="safemode")

    # Add fields that are not directly datajoint package fields
    global_schema_prefix: str = Field("", alias="global_schema_prefix")

    class Config:
        populate_by_name = True  # Allow using field names or aliases for input
        extra = "forbid"  # Forbid unknown keys

    def as_original_dict(self) -> dict[str, Any]:
        """Return config using original dotted keys (as loaded from file)."""
        return_dict = {
            "add_hidden_timestamp": self.add_hidden_timestamp,
            "connection.charset": self.connection_charset,
            "connection.init_function": self.connection_init_function,
            "database.host": self.database_host,
            "database.password": self.database_password,
            "database.port": self.database_port,
            "database.reconnect": self.database_reconnect,
            "database.use_tls": self.database_use_tls,
            "database.user": self.database_user,
            "display.limit": self.display_limit,
            "display.show_tuple_count": self.display_show_tuple_count,
            "display.width": self.display_width,
            "enable_python_native_blobs": self.enable_python_native_blobs,
            "fetch_format": self.fetch_format,
            "filepath_checksum_size_limit": self.filepath_checksum_size_limit,
            "loglevel": self.loglevel,
            "safemode": self.safemode,
            # other fields
            "global_schema_prefix": self.global_schema_prefix,
        }
        return return_dict
