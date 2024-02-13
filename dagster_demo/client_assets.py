from dagster import AssetExecutionContext, asset

from .partitions import clients_partitions_def


@asset(partitions_def=clients_partitions_def)
def clients_init(context: AssetExecutionContext):
    print("************** Asset context **************")
    print(context)
    print("************ Asset context end ************")
