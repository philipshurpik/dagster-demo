from dagster import Definitions, load_assets_from_modules

from . import assets
from .sensors import client_sensor, clients_job


defs = Definitions(
    assets=load_assets_from_modules([assets]),
    jobs=[clients_job],
    sensors=[client_sensor],
)
