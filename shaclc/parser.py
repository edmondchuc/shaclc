from pathlib import Path

from lark import Lark

grammar_path = Path(__file__).parent / "grammar.lark"

with open(grammar_path, "r", encoding="utf-8") as file:
    grammar = file.read()
    shaclc_parser = Lark(grammar, start="shacl_doc")
