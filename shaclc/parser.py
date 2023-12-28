from lark import Lark

from shaclc.grammar import grammar

shaclc_parser = Lark(grammar, start="shacl_doc")
