from rdflib import Graph

from shaclc.parser import shaclc_parser
from shaclc.serializer import ShaclCSerializer


def shaclc_to_graph(shaclc: str) -> Graph:
    """Parse the shaclc string and return a Graph object."""
    tree = shaclc_parser.parse(shaclc)
    shaclc_serializer = ShaclCSerializer()
    shaclc_serializer.serialize(tree)
    return shaclc_serializer.graph
