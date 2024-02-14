# Dagster Dynamic Partitions Demo

This example demonstrates how to use dynamically partitioned assets

File `demo_interface.py` is interface for creating jsons and putting them in directory.

A sensor polls folder for new jsons. 
When it finds one, it adds it to the set of partitions and runs the pipeline on it - i.e. requests a materialization of the partition corresponding to that item in each of the assets.

## Getting started

Install the project into your Python environment. By using the --editable flag, pip will install your Python package in ["editable mode"](https://pip.pypa.io/en/latest/topics/local-project-installs/#editable-installs) so that, as you develop, local code changes will automatically apply.

```bash
pip install -e ".[dev]"
```

Then, start the Dagster web server:

```bash
dagster dev
```

Open http://localhost:3000 with your browser to see the project.

### Dagster Debug 

You can debug your dagster assets and sensors via PyCharm or VSCode

Details on setup here:
https://github.com/dagster-io/dagster/discussions/10946

To run debug in PyCharm - select `debug_dagster.py` in files and select `Debug 'debugger_dagster'`