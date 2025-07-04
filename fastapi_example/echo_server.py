from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="EchoServer", stateless_http=True)

@mcp.tool(description="Ecoa a entrada do usuário.")
def echo(texto: str) -> str:
    """Ecoa a entrada do usuário.

    Args:
        texto (str): O texto a ser ecoado.

    Returns:
        str: O texto ecoado.
    """
    return f"Echo: {texto}"
