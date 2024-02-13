from dagster import AssetSelection, define_asset_job

from .partitions import clients_partitions_def

clients_job = define_asset_job(
    "clients_job", AssetSelection.groups("clients"), partitions_def=clients_partitions_def
)
