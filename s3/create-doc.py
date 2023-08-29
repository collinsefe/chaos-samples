import json
import os
from unittest.mock import MagicMock, patch

import pytest
from botocore.exceptions import ClientError
from chaoslib.exceptions import FailedActivity

from chaosaws import aws_client
from chaosaws.s3.actions import delete_object, toggle_versioning

data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def read_configs(filename: str) -> dict:
    config = os.path.join(data_path, filename)
    with open(config, "r") as fh:
        return json.loads(fh.read())


def mock_client_error(*args, **kwargs) -> ClientError:
    return ClientError(
        operation_name=kwargs["op"],
        error_response={
            "Error": {"Code": kwargs["Code"], "Message": kwargs["Message"]}
        },
    )


@patch("chaosaws.s3.actions.aws_client", autospec=True)
def test_delete_object_true(test_client: aws_client):
    client = MagicMock()
    test_client.return_value = client
    client.list_buckets.return_value = read_configs("list_buckets_1.json")
    client.get_object.return_value = read_configs("get_object_1.json")
    client.delete_object.return_value = {}

    delete_object(bucket_name="chaos-test-bucket-001", 
object_key="chaos-folder/image.png")

    client.delete_object.assert_called_with(
        Bucket="chaos-test-bucket-001", Key="chaos-folder/image.png"
    )

