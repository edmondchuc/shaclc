from lark.exceptions import UnexpectedInput, UnexpectedToken, UnexpectedCharacters
from shaclc import shaclc_to_graph


def convert(shaclc_str: str) -> str:
    try:
        graph = shaclc_to_graph(shaclc_str)
        return graph.serialize(format="longturtle")
    except UnexpectedToken as err:
        return f"Unexpected token: {err}"
    except UnexpectedCharacters as err:
        return f"Unexpected character: {err}"
    except UnexpectedInput as err:
        return f"Unexpected input: {err}"
    except Exception as err:
        return err
