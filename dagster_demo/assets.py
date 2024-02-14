import os

from dagster import AssetExecutionContext, asset, ResourceParam, MaterializeResult
from pandas import DataFrame

from .app.serper import Serper
from .partitions import clients_partitions_def
from .sensors import CLIENTS_DIR
from .utils import read_json


@asset(partitions_def=clients_partitions_def, io_manager_key="clients_db", metadata={"partition_expr": "file_name"})
def clients_meta(context: AssetExecutionContext) -> DataFrame:
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
def competitor_urls(clients_meta: DataFrame, search_api: ResourceParam[Serper]) -> DataFrame:
    """Search data for each competitor"""
    company_name = clients_meta.iloc[0]["company_name"]
    competitors = [clients_meta.iloc[i]["competitor_name"] for i in range(len(clients_meta))]
    print(company_name, "Competitors:", competitors)

    new_urls_df = search_api.get_new_search_results(company_name, competitors)
    new_urls_df['file_name'] = clients_meta.iloc[0]["file_name"]
    return new_urls_df


# here need to add scrapper
@asset(partitions_def=clients_partitions_def)
def competitor_scrapped(competitor_urls: DataFrame) -> MaterializeResult:
    """Scrap data for all new links"""
    if len(competitor_urls) == 0:
        return MaterializeResult(metadata={"Record Count": 0})
    company_name = competitor_urls.iloc[0]["company_name"]
    print("Company name", company_name, "New urls: ", len(competitor_urls))
    return MaterializeResult(
        metadata={
            "Record Count": len(competitor_urls),
            "Company name": company_name,
        }
    )
