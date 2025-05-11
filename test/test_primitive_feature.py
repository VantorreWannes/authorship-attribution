import os
import json
from typing import Any
from pytest import FixtureRequest, fixture
from authorship_attribution import PrimitiveFeature, Json


@fixture(
    params=[
        "hello world",
        "",
        0,
        None,
        {"key": "value"},
        [1, 2, 3],
    ]
)
def data(request: FixtureRequest) -> Any:
    return request.param


@fixture
def feature(data) -> PrimitiveFeature:
    return PrimitiveFeature(data)


@fixture
def json_data(data) -> Json:
    return json.dumps({"value": data}, indent=4)


@fixture
def write_path(tmpdir: str) -> str:
    read_path = os.path.join(tmpdir, "write_path.json")
    if os.path.exists(read_path):
        os.remove(read_path)
    return read_path


@fixture
def read_path(tmpdir: str, json_data: Json) -> str:
    read_path = os.path.join(tmpdir, "read_path.json")
    with open(read_path, "w") as file:
        file.write(json_data)
    return read_path


def test_value_data(feature: PrimitiveFeature, data: str):
    assert feature.value == data


def test_to_json(feature: PrimitiveFeature, json_data: Json):
    assert feature.to_json() == json_data


def test_from_json(json_data: Json, data: Any):
    assert PrimitiveFeature.from_json(json_data).value == data


def test_name():
    assert PrimitiveFeature.name() == "Primitive"


def test_file_name():
    assert PrimitiveFeature.file_name() == "Primitive.json"


def test_to_file(feature: PrimitiveFeature, write_path: str):
    feature.to_file(write_path)
    assert os.path.exists(write_path)


def test_from_file(read_path: str, data: Any):
    primitive_feature: PrimitiveFeature = PrimitiveFeature.from_file(read_path)
    assert primitive_feature.value == data
