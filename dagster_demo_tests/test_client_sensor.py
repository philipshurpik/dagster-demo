import json
import os
from unittest.mock import MagicMock, patch

from dagster import DagsterInstance, SkipReason, build_sensor_context

from dagster_demo.sensors import client_sensor


def test_client_sensor_no_new_clients():
    old_environ = dict(os.environ)
    os.environ.update({"GITHUB_USER_NAME": "username", "GITHUB_ACCESS_TOKEN": "token"})
    try:
        instance = DagsterInstance.ephemeral()
        with patch("requests.get") as mock:
            mock.return_value = MagicMock(ok=True, content=json.dumps([]))
            assert client_sensor(build_sensor_context(instance=instance)) == SkipReason(
                "No new clients"
            )
    finally:
        os.environ.clear()
        os.environ.update(old_environ)


def test_client_sensor_new_client():
    old_environ = dict(os.environ)
    os.environ.update({"GITHUB_USER_NAME": "username", "GITHUB_ACCESS_TOKEN": "token"})
    try:
        instance = DagsterInstance.ephemeral()
        with patch("requests.get") as mock:
            mock.return_value = MagicMock(ok=True, content=json.dumps([{"tag_name": "1.1.0"}]))
            result = client_sensor(build_sensor_context(instance=instance))
            assert len(result.run_requests) == 1
            assert result.run_requests[0].partition_key == "1.1.0"
            assert len(result.dynamic_partitions_requests) == 1
            assert result.dynamic_partitions_requests[0].partition_keys == ["1.1.0"]

    finally:
        os.environ.clear()
        os.environ.update(old_environ)


def test_client_sensor_new_client_with_cursor():
    old_environ = dict(os.environ)
    os.environ.update({"GITHUB_USER_NAME": "username", "GITHUB_ACCESS_TOKEN": "token"})
    try:
        instance = DagsterInstance.ephemeral()
        with patch("requests.get") as mock:
            mock.return_value = MagicMock(
                ok=True, content=json.dumps([{"tag_name": "1.1.0"}, {"tag_name": "1.2.0"}])
            )
            result = client_sensor(build_sensor_context(instance=instance, cursor="1.1.0"))
            assert len(result.run_requests) == 1
            assert result.run_requests[0].partition_key == "1.2.0"
            assert len(result.dynamic_partitions_requests) == 1
            assert result.dynamic_partitions_requests[0].partition_keys == ["1.2.0"]
            assert result.cursor == "1.2.0"

    finally:
        os.environ.clear()
        os.environ.update(old_environ)
