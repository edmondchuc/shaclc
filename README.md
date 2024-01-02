# Python SHACL Compact Syntax Parser

A Python SHACL Compact Syntax parser and serializer based on the specification at https://w3c.github.io/shacl/shacl-compact-syntax/.

All tests defined in [github.com/w3c/data-shapes/shacl-compact-syntax/tests](https://github.com/w3c/data-shapes/tree/gh-pages/shacl-compact-syntax/tests) are passing.

## Browser playground

Play around with the implementation in your browser at https://edmondchuc.github.io/shaclc/.

## Quickstart

Installation.

```shell
pip install shaclc
```

Usage.

```python
from shaclc import shaclc_to_graph

shaclc_str = """
BASE <http://example.com/ns>

IMPORTS <http://example.com/person-ontology>

PREFIX ex: <http://example.com/ns#>

shape ex:PersonShape -> ex:Person {
	ex:ssn xsd:string [0..1] pattern="^\\d{3}-\\d{2}-\\d{4}$" .
}
"""

graph = shaclc_to_graph(shaclc_str)

graph.print(format="longturtle")
```

Output.

```
BASE <http://example.com/ns>
PREFIX ex: <http://example.com/ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX sh: <http://www.w3.org/ns/shacl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

<>
    a owl:Ontology ;
    owl:imports <http://example.com/person-ontology> ;
.

<#PersonShape>
    a sh:NodeShape ;
    sh:property
        [
            sh:datatype xsd:string ;
            sh:maxCount 1 ;
            sh:path <#ssn> ;
            sh:pattern "^\\d{3}-\\d{2}-\\d{4}$" ;
        ] ;
    sh:targetClass <#Person> ;
.
```
