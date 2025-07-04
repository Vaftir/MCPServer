"""
MCP Calculator Server - Versão Simples
=====================================

Servidor MCP simples com funções matemáticas básicas implementadas 
como tools usando decoradores @mcp.tool().

ORDEM DE PRECEDÊNCIA DOS OPERADORES:
1. Parênteses (), Colchetes [], Chaves {}
2. Potência (**)
3. Multiplicação (*) e Divisão (/)
4. Soma (+) e Subtração (-)
"""


import math
from mcp.server.fastmcp import FastMCP

# Criar servidor MCP
mcp = FastMCP(name="MathServer", stateless_http=True)
# ============================================================================
# FUNÇÕES MATEMÁTICAS SIMPLES COM @mcp.tool()
# ============================================================================

@mcp.tool(description="Realiza a soma de dois números.")
def soma(a: float, b: float) -> float:
    """Realiza a soma de dois números."""
    return a + b

@mcp.tool(description="Realiza a subtração de dois números.")
def subtracao(a: float, b: float) -> float:
    """Realiza a subtração de dois números.

    Args:
        a (float): O minuendo.
        b (float): O subtraendo.

    Returns:
        float: O resultado da subtração.
    """
    return a - b

@mcp.tool(description="Realiza a multiplicação de dois números.")
def multiplicacao(a: float, b: float) -> float:
    """Realiza a multiplicação de dois números.

    Args:
        a (float): O primeiro fator.
        b (float): O segundo fator.

    Returns:
        float: O resultado da multiplicação.
    """
    return a * b

@mcp.tool(description="Realiza a divisão de dois números.")
def divisao(a: float, b: float) -> float:
    """Realiza a divisão de dois números.

    Args:
        a (float): O numerador.
        b (float): O denominador.

    Returns:
        float: O resultado da divisão.
    """
    if b == 0:
        raise ValueError("Divisão por zero não é permitida!")
    return a / b

@mcp.tool(description="Calcula a potência de um número")
def potencia(base: float, expoente: float) -> float:
    """Calcula a potência de um número.

    Args:
        base (float): A base da potência.
        expoente (float): O expoente da potência.

    Returns:
        float: O resultado da potência.
    """
    return math.pow(base, expoente)

@mcp.tool(description="Calcula a raiz quadrada de um número")
def raiz_quadrada(numero: float) -> float:
    """Calcula a raiz quadrada de um número.

    Args:
        numero (float): O número do qual calcular a raiz quadrada.

    Returns:
        float: A raiz quadrada do número.
    """
    if numero < 0:
        raise ValueError("Não é possível calcular a raiz quadrada de um número negativo.")
    return math.sqrt(numero)

@mcp.tool(description="Calcula a tangente de um ângulo em radianos")
def tangente(angulo: float) -> float:
    """Calcula a tangente de um ângulo em radianos.

    Args:
        angulo (float): O ângulo em radianos.

    Returns:
        float: A tangente do ângulo.
    """
    return math.tan(angulo)

@mcp.tool(description="retorna uma constante matemática")
def constante_pi(constante: str) -> float:
    """Retorna uma das contstantes dependendo do parâmetro.
    Se constante for "pi", retorna PI (3.1415...).
    Se constante for "e", retorna E (2.7182...).
    Se for "tau", retorna TAU (6.2831...).

    Args:
        constante (str): O nome da constante.

    Raises:
        ValueError: Se a constante não for reconhecida.

    Returns:
        float: O valor da constante.
    """
    if constante == "pi":
        return math.pi
    elif constante == "e":
        return math.e
    elif constante == "tau":    
        return math.tau
    else:
        raise ValueError("Constante desconhecida.")

   

@mcp.tool(description="Avalia uma expressão matemática.")
def avaliar_expressao(expressao: str) -> float:
    """Avalia uma expressão matemática seguindo a ordem de precedência.

    Args:
        expressao (str): A expressão matemática a ser avaliada.

    Raises:
        ValueError: Se a expressão contiver caracteres não permitidos.
        ValueError: Se ocorrer um erro ao avaliar a expressão.

    Returns:
        float: O resultado da avaliação da expressão.
    """
    try:
        # Validação básica de segurança
        caracteres_permitidos = set("0123456789+-*/().** ")
        if not all(c in caracteres_permitidos for c in expressao):
            raise ValueError("Expressão contém caracteres não permitidos")
        
        resultado = eval(expressao)
        return resultado
    except Exception as e:
        raise ValueError(f"Erro ao avaliar expressão: {str(e)}")

@mcp.tool(description="Explica a ordem de precedência dos operadores matemáticos.")
def explicar_precedencia() -> str:
    """Explica a ordem de precedência dos operadores matemáticos.

    Returns:
        str: A ordem de precedência dos operadores.
    """
    return """
ORDEM DE PRECEDÊNCIA DOS OPERADORES:

1. AGRUPADORES:
   • Parênteses ()  - sempre primeiro
   • Colchetes []   - depois dos parênteses  
   • Chaves {}      - por último

2. OPERADORES (maior → menor precedência):
   • Potência (**)
   • Multiplicação (*) e Divisão (/)
   • Soma (+) e Subtração (-)

EXEMPLOS:
• 2 + 3 * 4 = 14 (multiplicação primeiro)
• (2 + 3) * 4 = 20 (parênteses primeiro)
• 2 ** 3 * 4 = 32 (potência primeiro)
    """

