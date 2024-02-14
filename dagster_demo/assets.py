import os

from dagster import AssetExecutionContext, asset
from pandas import DataFrame

from .partitions import clients_partitions_def
from .sensors import CLIENTS_DIR
from .utils import read_json


@asset(partitions_def=clients_partitions_def, io_manager_key="clients_db", metadata={"partition_expr": "file_name"})
def clients_meta_load(context: AssetExecutionContext) -> DataFrame:
    """Loader New Client Request Data from sensors"""
    file_name = context.partition_key
    company_data = read_json(os.path.join(CLIENTS_DIR, file_name))
    competitors = company_data.get('competitors') or []
    print("load competitors", competitors)
    rows = [
        {
            "file_name": file_name,
            "company_name": company_data.get('company_name'),
            "competitor_name": competitor,
        } for competitor in competitors
    ]
    return DataFrame(rows)


@asset(partitions_def=clients_partitions_def)
def competitor_analysis(clients_meta_load: DataFrame) -> None:
    """Search data for each competitor"""
    company_name = clients_meta_load.iloc[0]["company_name"]
    print("************************************* Company name: ", company_name)
    for i in range(len(clients_meta_load)):
        competitor_name = clients_meta_load.iloc[i]["competitor_name"]
        print("Competitor name: ", competitor_name)
    print("*************************************")
