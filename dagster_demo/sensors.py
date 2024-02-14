import os

from dagster import RunRequest, SensorEvaluationContext, SensorResult, sensor, SkipReason
from .partitions import clients_partitions_def
from .jobs import clients_job


CLIENTS_DIR = 'data/clients_meta'


@sensor(job=clients_job, minimum_interval_seconds=5)
def client_sensor(context: SensorEvaluationContext):
    clients = os.listdir(CLIENTS_DIR)
    new_clients = [c for c in clients if not clients_partitions_def.has_partition_key(c, dynamic_partitions_store=context.instance)]

    if len(new_clients) == 0:
        return SkipReason("No new clients")

    return SensorResult(
        run_requests=[
            RunRequest(partition_key=client_name) for client_name in new_clients
        ],
        dynamic_partitions_requests=[
            clients_partitions_def.build_add_request(new_clients)
        ],
    )
