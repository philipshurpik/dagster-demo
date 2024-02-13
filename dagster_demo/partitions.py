from dagster import DynamicPartitionsDefinition

clients_partitions_def = DynamicPartitionsDefinition(name="clients")
