from typing import Any

from lark import Token, Tree
from lark.visitors import Visitor_Recursive, _Leaf_T
from rdflib import OWL, RDF, RDFS, SH, XSD, BNode, Graph, Literal, URIRef
from rdflib.collection import Collection


def contains_token(name: str, children: list[Token | Tree]) -> bool:
    for child in children:
        if isinstance(child, Token):
            if child.type == name:
                return True

    return False


def contains_tree(name: str, children: list[Token | Tree]) -> bool:
    for child in children:
        if isinstance(child, Tree):
            if child.data.value == name:
                return True

    return False


def token_value(name: str, children: list[Token | Tree]) -> Any:
    for child in children:
        if isinstance(child, Token):
            if child.type == name:
                return child.value

    raise ValueError(f"No value found for token name '{name}' in children: {children}")


def token_object(name: str, children: list[Token | Tree]) -> Token | None:
    for child in children:
        if isinstance(child, Token):
            if child.type == name:
                return child


def tree_object(name: str, children: list[Token | Tree]) -> list[Token | Tree] | None:
    for child in children:
        if isinstance(child, Tree):
            if child.data.value == name:
                return child.children


class ShaclCSerializer(Visitor_Recursive):
    # The serialized RDF data
    _graph: Graph = None

    # Node shape context
    _shape: list[URIRef | BNode] = []

    # Property shape context
    _property: list[URIRef | BNode] = []

    @property
    def graph(self):
        return self._graph

    def serialize(self, tree: Tree[_Leaf_T]):
        self._graph = Graph()
        self.visit_topdown(tree)

    def base_decl(self, node: Tree):
        iri = self._get_iriref(node.children)
        self._graph = Graph(base=iri)
        self._graph.add((URIRef(iri), RDF.type, OWL.Ontology))

    def imports_decl(self, node: Tree):
        graph = self._graph
        iriref = self._get_iriref(node.children)
        graph.add((graph.base, OWL.imports, iriref))

    def prefix_decl(self, node: Tree):
        prefix = token_value("PNAME_NS", node.children)[:-1]
        namespace = self._get_iriref(node.children)
        self._graph.bind(prefix, namespace)

    def _get_iriref(self, children: list[Token | Tree]) -> URIRef:
        iri = token_value("IRIREF", children)
        return URIRef(iri[1:-1])

    def _get_prefixed_name(self, children: list[Token | Tree]):
        prefixed_children = tree_object("prefixed_name", children)
        prefixed_name = token_value("PNAME_LN", prefixed_children)
        return self._expand_curie(prefixed_name)

    def _expand_curie(self, curie: str) -> URIRef:
        return self._graph.namespace_manager.expand_curie(curie)

    def _get_iri(self, children: list[Token | Tree]) -> URIRef:
        iri_children = tree_object("iri", children)

        if contains_token("IRIREF", iri_children):
            iri = self._get_iriref(iri_children)
        else:
            iri = self._get_prefixed_name(iri_children)

        return iri

    def _handle_path_sequences(self, path_sequences: list[Token | Tree]):
        graph = self._graph
        alternative_path_node = BNode()

        current_rdf_list = BNode()
        next_rdf_list = BNode()
        graph.add((alternative_path_node, SH.alternativePath, current_rdf_list))

        for i, path_sequence in enumerate(path_sequences):
            value = self._handle_path_sequence(path_sequence.children)
            graph.add((current_rdf_list, RDF.first, value))

            if i + 1 != len(path_sequences):
                graph.add((current_rdf_list, RDF.rest, next_rdf_list))
                current_rdf_list = next_rdf_list
                next_rdf_list = BNode()
            else:
                graph.add((current_rdf_list, RDF.rest, RDF.nil))

        return alternative_path_node

    def _handle_path_elt_or_inverse(self, path_elt_or_inverse: Tree):
        graph = self._graph

        has_path_inverse = contains_tree("path_inverse", path_elt_or_inverse.children)
        if has_path_inverse:
            path_inverse_node = BNode()

        path_elts = list(
            filter(lambda x: x.data == "path_elt", path_elt_or_inverse.children)
        )
        if len(path_elts) == 1:
            path_elt: Tree = path_elts[0]
            path_primary = path_elt.children[0]

            path_mod = (
                token_value("PATH_MOD", path_elt.children[1].children)
                if len(path_elt.children) > 1
                else None
            )
            if path_mod is not None:
                path_mod_node = BNode()
                if path_mod == "?":
                    path_mod_predicate = SH.zeroOrOnePath
                elif path_mod == "+":
                    path_mod_predicate = SH.oneOrMorePath
                elif path_mod == "*":
                    path_mod_predicate = SH.zeroOrMorePath
                else:
                    raise ValueError(f"Unknown path mod '{path_mod}'")

            if contains_tree("iri", path_primary.children):
                value = self._get_iri(path_primary.children)
                if path_mod is not None:
                    graph.add((path_mod_node, path_mod_predicate, value))

                    if has_path_inverse:
                        graph.add((path_inverse_node, SH.inversePath, path_mod_node))
                        return path_inverse_node

                    return path_mod_node
                else:
                    if has_path_inverse:
                        graph.add((path_inverse_node, SH.inversePath, value))
                        return path_inverse_node

                    return value
            else:
                # Contains a path.
                path = list(filter(lambda x: x.data == "path", path_primary.children))[
                    0
                ]
                return self._get_path(path.children)
        elif len(path_elts) > 1:
            raise NotImplementedError

    def _handle_path_sequence(self, path_elt_or_inverses: list[Token | Tree]):
        graph = self._graph

        if len(path_elt_or_inverses) == 1:
            path_elt_or_inverse = path_elt_or_inverses[0]
            return self._handle_path_elt_or_inverse(path_elt_or_inverse)

        elif len(path_elt_or_inverses) > 1:
            current_rdf_list = BNode()
            next_rdf_list = BNode()
            first_rdf_list = current_rdf_list

            for i, path_elt_or_inverse in enumerate(path_elt_or_inverses):
                value = self._handle_path_elt_or_inverse(path_elt_or_inverse)
                graph.add((current_rdf_list, RDF.first, value))

                if i + 1 != len(path_elt_or_inverses):
                    graph.add((current_rdf_list, RDF.rest, next_rdf_list))
                    current_rdf_list = next_rdf_list
                    next_rdf_list = BNode()
                else:
                    graph.add((current_rdf_list, RDF.rest, RDF.nil))

            return first_rdf_list

    def _get_path(self, children: list[Token | Tree]) -> URIRef | Collection:
        path_alternative = children[0]
        path_sequences = path_alternative.children

        if len(path_sequences) == 1:
            path_elt_or_inverses = path_sequences[0].children
            return self._handle_path_sequence(path_elt_or_inverses)

        elif len(path_sequences) > 1:
            return self._handle_path_sequences(path_sequences)

    def _get_iri_or_literal(self, children: list[Token | Tree]) -> URIRef | Literal:
        if contains_tree("iri", children):
            return self._get_iri(children)
        else:
            # it's tree with name "literal".
            literal_children = tree_object("literal", children)

            if rdf_literal_children := tree_object("rdf_literal", literal_children):
                value = tree_object("string", rdf_literal_children)[0].value[1:-1]
                langtag = token_object("LANGTAG", rdf_literal_children)
                if langtag is not None:
                    langtag = langtag[1:]
                if datatype_children := tree_object("datatype", rdf_literal_children):
                    datatype = self._get_iri(datatype_children)
                else:
                    datatype = None

                return Literal(value, datatype=datatype, lang=langtag)
            elif numeric_literal_children := tree_object(
                "numeric_literal", literal_children
            ):
                if value := token_value(
                    "INTEGER", numeric_literal_children[0].children
                ):
                    return Literal(int(value))
                if value := token_value(
                    "DECIMAL", numeric_literal_children[0].children
                ):
                    return Literal(float(value), datatype=XSD.decimal)
                if value := token_value("DOUBLE", numeric_literal_children[0].children):
                    return Literal(float(value), datatype=XSD.double)
            elif boolean_literal_children := tree_object(
                "boolean_literal", literal_children
            ):
                return Literal(boolean_literal_children[0].value, datatype=XSD.boolean)
            else:
                raise ValueError(
                    f"Unknown literal name in children: {literal_children}"
                )

    def _get_iri_or_literal_or_array(
        self, children: list[Token | Tree]
    ) -> URIRef | Literal | Collection:
        graph = self._graph
        iri_or_literal_or_array_children = tree_object(
            "iri_or_literal_or_array", children
        )

        if iri_or_literal_children := tree_object(
            "iri_or_literal", iri_or_literal_or_array_children
        ):
            return self._get_iri_or_literal(iri_or_literal_children)
        elif array_children := tree_object("array", iri_or_literal_or_array_children):
            array = Collection(graph, BNode())
            for item in array_children:
                array.append(self._get_iri_or_literal(item.children))
            return array.uri

    def _node_shape_body(self, children: list[Token | Tree]):
        for constraint in children:
            for node_or_or_property_shape in constraint.children:
                if node_or_or_property_shape.data == "node_or":
                    self._node_or(node_or_or_property_shape.children)
                if node_or_or_property_shape.data == "property_shape":
                    self._property_shape(node_or_or_property_shape.children)

    def node_shape(self, node: Tree):
        graph = self._graph
        iri = self._get_iri(node.children)
        self._shape.append(iri)

        if contains_tree("target_class", node.children):
            target_class_tree = tree_object("target_class", node.children)
            for iri_children in target_class_tree:
                target_class = self._get_iri([iri_children])
                graph.add((iri, SH.targetClass, target_class))

        if node_shape_body_children := tree_object("node_shape_body", node.children):
            self._node_shape_body(node_shape_body_children)

        graph.add((iri, RDF.type, SH.NodeShape))
        self._shape.pop()

    def shape_class(self, node: Tree):
        graph = self._graph
        iri = self._get_iri(node.children)
        self._shape.append(iri)

        if node_shape_body_children := tree_object("node_shape_body", node.children):
            self._node_shape_body(node_shape_body_children)

        graph.add((iri, RDF.type, SH.NodeShape))
        graph.add((iri, RDF.type, RDFS.Class))
        self._shape.pop()

    def _property_atom(self, children: list[Token | Tree]):
        graph = self._graph
        property_shape = self._property[-1]
        property_atom = children[0]

        if property_atom.data == "property_type":
            iri = self._get_iri(property_atom.children)
            if iri.startswith(str(XSD)) or iri.startswith(str(RDF)):
                graph.add((property_shape, SH.datatype, iri))
            else:
                graph.add((property_shape, SH["class"], iri))
        elif property_atom.data == "node_kind":
            node_kind_str = token_value("NODE_KIND", property_atom.children)
            graph.add((property_shape, SH.nodeKind, SH[node_kind_str]))
        elif property_atom.data == "shape_ref":
            shape_ref = property_atom.children[0]
            if shape_ref.type == "IRIREF":
                value = self._get_iriref([shape_ref])
            else:
                value = shape_ref.value[1:]
                value = self._expand_curie(value)
            graph.add((property_shape, SH.node, value))
        elif property_atom.data == "property_value":
            property_param_children = tree_object(
                "property_param", property_atom.children
            )
            property_param = token_value("PROPERTY_PARAM", property_param_children)
            properety_param_iri = SH[property_param]
            iri_or_literal_or_array = self._get_iri_or_literal_or_array(
                property_atom.children
            )
            graph.add((property_shape, properety_param_iri, iri_or_literal_or_array))
        elif property_atom.data == "node_shape_body":
            shape_context = BNode()
            self._shape.append(shape_context)
            graph.add((property_shape, SH.node, shape_context))
            self._node_shape_body(property_atom.children)
            self._shape.pop()
        else:
            raise NotImplementedError(
                f"Unsupported property atom type {property_atom.data}"
            )

    def _handle_property_not(self, property_not_children: list[Token | Tree]):
        graph = self._graph
        main_property_context = self._property[-1]

        has_negation = contains_tree("negation", property_not_children)
        if has_negation:
            property_context = BNode()
            graph.add((main_property_context, SH["not"], property_context))
            self._property.append(property_context)
            self._property_atom(tree_object("property_atom", property_not_children))
            self._property.pop()
        else:
            self._property_atom(tree_object("property_atom", property_not_children))

    def _property_shape(self, children: list[Token | Tree]):
        graph = self._graph
        shape_context = self._shape[-1]

        property_shape = BNode()
        self._property.append(property_shape)
        graph.add((shape_context, SH.property, property_shape))

        path = list(filter(lambda x: x.data == "path", children))[0]
        path_iri = self._get_path(path.children)
        graph.add((property_shape, SH.path, path_iri))

        property_counts = list(filter(lambda x: x.data == "property_count", children))
        for property_count in property_counts:
            property_min_count = token_value(
                "INTEGER", property_count.children[0].children
            )
            if contains_token("INTEGER", property_count.children[1].children):
                property_max_count = token_value(
                    "INTEGER", property_count.children[1].children
                )
            else:
                property_max_count = "*"

            if property_min_count != "0":
                graph.add(
                    (
                        property_shape,
                        SH.minCount,
                        Literal(property_min_count, datatype=XSD.integer),
                    )
                )
            if property_max_count != "*":
                graph.add(
                    (
                        property_shape,
                        SH.maxCount,
                        Literal(property_max_count, datatype=XSD.integer),
                    )
                )

        property_ors = list(filter(lambda x: x.data == "property_or", children))
        for property_or in property_ors:
            if len(property_or.children) == 1:
                property_not_children = tree_object(
                    "property_not", property_or.children
                )
                self._handle_property_not(property_not_children)
            elif len(property_or.children) > 1:
                current_rdf_list = BNode()
                next_rdf_list = BNode()
                graph.add((property_shape, SH["or"], current_rdf_list))

                for i, property_not in enumerate(property_or.children):
                    property_context = BNode()
                    self._property.append(property_context)
                    graph.add((current_rdf_list, RDF.first, property_context))

                    if i + 1 != len(property_or.children):
                        graph.add((current_rdf_list, RDF.rest, next_rdf_list))
                        current_rdf_list = next_rdf_list
                        next_rdf_list = BNode()
                    else:
                        graph.add((current_rdf_list, RDF.rest, RDF.nil))

                    self._handle_property_not(property_not.children)
                    self._property.pop()

        self._property.pop()

    def _node_not(self, children: list[Token | Tree]):
        graph = self._graph
        shape_context = self._shape[-1]

        if contains_tree("negation", children):
            node_not = BNode()
            graph.add((shape_context, SH["not"], node_not))
            shape_context = node_not

        if node_value_children := tree_object("node_value", children):
            node_param_children = tree_object("node_param", node_value_children)
            node_param = token_value("NODE_PARAM", node_param_children)
            node_param_iri = SH[node_param]
            iri_or_literal_or_array = self._get_iri_or_literal_or_array(
                node_value_children
            )
            graph.add((shape_context, node_param_iri, iri_or_literal_or_array))

    def _node_or(self, children: list[Token | Tree]):
        graph = self._graph
        shape_context = self._shape[-1]

        if len(children) == 1:
            self._node_not(children[0].children)
        elif len(children) > 1:
            current_rdf_list = BNode()
            next_rdf_list = BNode()
            graph.add((shape_context, SH["or"], current_rdf_list))

            for i, node_not in enumerate(children):
                property_context = BNode()
                self._shape.append(property_context)
                graph.add((current_rdf_list, RDF.first, property_context))

                if i + 1 != len(children):
                    graph.add((current_rdf_list, RDF.rest, next_rdf_list))
                    current_rdf_list = next_rdf_list
                    next_rdf_list = BNode()
                else:
                    graph.add((current_rdf_list, RDF.rest, RDF.nil))

                self._node_not(node_not.children)
                self._shape.pop()
