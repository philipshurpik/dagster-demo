from setuptools import find_packages, setup

setup(
    name="dagster_demo",
    packages=find_packages(exclude=["dagster_demo_tests"]),
    install_requires=[
        "dagster",
        "dagster-duckdb-pandas",
        "requests",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
