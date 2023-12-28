from pathlib import Path

import pytest
from rdflib import Graph
from rdflib.compare import isomorphic

from shaclc import shaclc_to_graph


def get_test_files():
    test_dir = Path(__file__).parent / "data/valid"
    files = list(test_dir.glob("*.shaclc"))
    for file in files:
        test_name = file.name.split(".shaclc")[0]
        yield file, test_dir / (test_name + ".ttl")


@pytest.mark.parametrize("shaclc_file, expected_file", get_test_files())
def test(shaclc_file: str, expected_file: str):
    with open(shaclc_file, "r", encoding="utf-8") as file:
        # Replace backslashes that are escaped.
        shaclc_str = file.read().replace("\\\\", "\\")
        graph = shaclc_to_graph(shaclc_str)
        expected_graph = Graph()
        expected_graph.parse(expected_file)

        assert isomorphic(graph, expected_graph), graph.serialize()
