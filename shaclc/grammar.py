grammar = r"""
shacl_doc: directive* (node_shape | shape_class)*

directive: base_decl | imports_decl | prefix_decl
base_decl: KW_BASE IRIREF
imports_decl: KW_IMPORTS IRIREF
prefix_decl: KW_PREFIX PNAME_NS IRIREF

node_shape: KW_SHAPE iri target_class? node_shape_body
shape_class: KW_SHAPE_CLASS iri node_shape_body
node_shape_body: "{" constraint* "}"
target_class: "->" iri+

constraint: ( node_or+ | property_shape ) "."
node_or: node_not ( "|" node_not ) *
node_not: negation? node_value
node_value: node_param "=" iri_or_literal_or_array

property_shape: path ( property_count | property_or )*
property_or: property_not ( "|" property_not)*
property_not: negation? property_atom
property_atom: property_type | node_kind | shape_ref | property_value | node_shape_body
property_count: "[" property_min_count ".." property_max_count "]"
property_min_count: INTEGER
property_max_count: (INTEGER | "*")
property_type: iri
node_kind: NODE_KIND
NODE_KIND: "BlankNode" | "IRI" | "Literal" | "BlankNodeOrIRI" | "BlankNodeOrLiteral" | "IRIOrLiteral"
shape_ref: ATPNAME_LN | ATPNAME_NS | "@" IRIREF
property_value: property_param "=" iri_or_literal_or_array
negation: "!"

path: path_alternative
path_alternative: path_sequence ( "|" path_sequence )*
path_sequence: path_elt_or_inverse ( "/" path_elt_or_inverse )*
path_elt: path_primary path_mod?
path_elt_or_inverse: path_elt | path_inverse path_elt
path_inverse: "^"
path_mod: PATH_MOD
PATH_MOD: "?" | "*" | "+"
path_primary: iri | "(" path ")"

iri_or_literal_or_array: iri_or_literal | array
iri_or_literal: iri | literal

iri: IRIREF | prefixed_name
prefixed_name: PNAME_LN | PNAME_NS

literal: rdf_literal | numeric_literal | boolean_literal
boolean_literal: KW_TRUE | KW_FALSE
numeric_literal: numeric_literal_unsigned | numeric_literal_positive | numeric_literal_negative
numeric_literal_unsigned: INTEGER | DECIMAL | DOUBLE
numeric_literal_positive: INTEGER_POSITIVE | DECIMAL_POSITIVE | DOUBLE_POSITIVE
numeric_literal_negative: INTEGER_NEGATIVE | DECIMAL_NEGATIVE | DOUBLE_NEGATIVE
rdf_literal: string ( LANGTAG | "^^" datatype )?
datatype: iri
string: STRING_LITERAL1 | STRING_LITERAL2 | STRING_LITERAL_LONG1 | STRING_LITERAL_LONG2 | ESCAPED_STRING

array: "[" iri_or_literal* "]"

node_param: NODE_PARAM
NODE_PARAM: "targetNode"
            | "targetObjectsOf"
            | "targetSubjectsOf"
            | "deactivated"
            | "severity"
            | "message"
            | "class"
            | "datatype"
            | "nodeKind"
            | "minExclusive"
            | "maxExclusive"
            | "maxInclusive"
            | "minLength"
            | "maxLength"
            | "pattern"
            | "flags"
            | "languageIn"
            | "equals"
            | "disjoint"
            | "closed"
            | "ignoredProperties"
            | "hasValue"
            | "in"

property_param: PROPERTY_PARAM
PROPERTY_PARAM: "deactivated"
                | "severity"
                | "message"
                | "class"
                | "datatype"
                | "nodeKind"
                | "minExclusive"
                | "minInclusive"
                | "maxExclusive"
                | "maxInclusive"
                | "minLength"
                | "maxLength"
                | "pattern"
                | "flags"
                | "languageIn"
                | "uniqueLang"
                | "equals"
                | "disjoint"
                | "lessThan"
                | "lessThanOrEquals"
                | "qualifiedValueShape"
                | "qualifiedMinCount"
                | "qualifiedMaxCount"
                | "qualifiedValueShapesDisjoint"
                | "closed"
                | "ignoredProperties"
                | "hasValue"
                | "in"

############
# Keywords #
############

KW_BASE: "BASE"i
KW_IMPORTS: "IMPORTS"i
KW_PREFIX: "PREFIX"i

KW_SHAPE_CLASS: "shapeClass"
KW_SHAPE: "shape"

KW_TRUE: "true"
KW_FALSE: "false"

#############
# Terminals #
#############

PASS: /[ \t\n]/+
COMMENT: "#" /[^\n]/*

IRIREF: "<" (/[^<>"{}|^`\\\x00-\x20]/)* ">"
PNAME_NS: PN_PREFIX? ":"
PNAME_LN: PNAME_NS PN_LOCAL
ATPNAME_NS: "@" PN_PREFIX? ":"
ATPNAME_LN: "@" PNAME_NS PN_LOCAL
LANGTAG: "@" /[a-zA-Z]/+ ("-" /[a-zA-Z0-9]/+)*
INTEGER: /[0-9]/+
DECIMAL: /[0-9]/* "." /[0-9]/+
DOUBLE: /[0-9]/+ "." /[0-9]/* EXPONENT | "." (/[0-9]/)+ EXPONENT | (/[0-9]/+) EXPONENT
INTEGER_POSITIVE: "+" INTEGER
DECIMAL_POSITIVE: "+" DECIMAL
DOUBLE_POSITIVE: "+" DOUBLE
INTEGER_NEGATIVE: "-" INTEGER
DECIMAL_NEGATIVE: "-" DECIMAL
DOUBLE_NEGATIVE: "-" DOUBLE
EXPONENT: /[eE]/ /[+-]/? /[0-9]/+
STRING_LITERAL1: "'" ( (/[^\u0027\\u005C\u000A\u000D]/) | ECHAR | UCHAR )* "'"
STRING_LITERAL2: "\"" ( (/[^\u0022\\u005C\u000A\u000D]/) | ECHAR | UCHAR )* "\""
STRING_LITERAL_LONG1: "'''" ( ( "'" | "'" )? ( /[^'\\]/ | ECHAR | UCHAR ) )* "'''"
STRING_LITERAL_LONG2: "\"\"\"" ( ( "\"" | "\"" )? ( /[^"\\]/ | ECHAR | UCHAR ) )* "\"\"\""
UCHAR: "\\u" HEX HEX HEX HEX | "\\U" HEX HEX HEX HEX HEX HEX HEX HEX
ECHAR: "\\" /[tbnrf\"']/
WS: "\u0020" | "\u0009" | "\u000D" | "\u000A"
PN_CHARS_BASE: /[A-Z]/ | /[a-z]/
                | /[\u00C0-\u00D6]/ 
                | /[\u00D8-\u00F6]/ 
                | /[\u00F8-\u02FF]/ 
                | /[\u0370-\u037D]/ 
                | /[\u037F-\u1FFF]/ 
                | /[\u200C-\u200D]/ 
                | /[\u2070-\u218F]/ 
                | /[\u2C00-\u2FEF]/ 
                | /[\u3001-\uD7FF]/
                | /[\uF900-\uFDCF]/
                | /[\uFDF0-\uFFFD]/
PN_CHARS_U: PN_CHARS_BASE | "_"
PN_CHARS: PN_CHARS_U | "-" | /[0-9]/ | "\u00B7" | /[\u0300-\u036F]/ | /[\u203F-\u2040]/
PN_PREFIX: PN_CHARS_BASE ((PN_CHARS|".")* PN_CHARS)?
PN_LOCAL: (PN_CHARS_U | ":" | /[0-9]/ | PLX ) ((PN_CHARS | "." | ":" | PLX)* (PN_CHARS | ":" | PLX) )?
PLX: PERCENT | PN_LOCAL_ESC
PERCENT: "%" HEX HEX
HEX: /[0-9]/ | /[A-F]/ | /[a-f]/
PN_LOCAL_ESC: "\\" ( "_" | "~" | "." | "-" | "!" | "$" | "&" | "'" | "(" | ")" | "*" | "+" | "," | ";" | "=" | "/" | "?" | "#" | "@" | "%" )

%ignore PASS | COMMENT
%import common.ESCAPED_STRING
"""
