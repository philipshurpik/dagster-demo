from dagster import Definitions, load_assets_from_modules
from dagster_duckdb import build_duckdb_io_manager
from dagster_duckdb_pandas import DuckDBPandasTypeHandler

from . import assets
from .sensors import client_sensor, clients_job

duckdb_io_manager = build_duckdb_io_manager([DuckDBPandasTypeHandler()])

defs = Definitions(
    assets=load_assets_from_modules([assets]),
    jobs=[clients_job],
    sensors=[client_sensor],
    resources={"clients_db": duckdb_io_manager.configured({"database": "clients.duckdb"})},
)
