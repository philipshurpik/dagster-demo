from dagster import Definitions, load_assets_from_modules
from dagster_duckdb import build_duckdb_io_manager
from dagster_duckdb_pandas import DuckDBPandasTypeHandler

from . import release_assets, client_assets
from .release_sensor import release_sensor
from .client_sensor import client_sensor, clients_job

duckdb_io_manager = build_duckdb_io_manager([DuckDBPandasTypeHandler()])

defs = Definitions(
    assets=load_assets_from_modules([release_assets, client_assets]),
    jobs=[clients_job],
    sensors=[client_sensor],
    resources={"warehouse": duckdb_io_manager.configured({"database": "releases.duckdb"})},
)
