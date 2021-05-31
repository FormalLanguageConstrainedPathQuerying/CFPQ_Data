import pytest
import rdflib

import cfpq_data

g1 = cfpq_data.graph_from_dataset("foaf", verbose=False)
g2 = cfpq_data.graph_from_dataset("core", verbose=False)
g3 = cfpq_data.graph_from_text("1 A 2", verbose=False)


@pytest.mark.parametrize(
    "graph,query,expected_response",
    [
        (
            g1,
            "subClassOf",
            (
                "label",
                rdflib.term.URIRef("http://www.w3.org/2000/01/rdf-schema#subClassOf"),
            ),
        ),
        (
            g2,
            "type",
            (
                "label",
                rdflib.term.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
            ),
        ),
        (g3, "A", ("label", "A")),
        (g3, "B", None),
    ],
)
def test_find_label(graph, query, expected_response):
    assert cfpq_data.find_label(graph, query, verbose=False) == expected_response
