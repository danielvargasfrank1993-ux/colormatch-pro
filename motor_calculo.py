# =====================================================================
# motor_calculo.py — Motor de Cálculo de Bateladas (ColorMatch Pro)
# =====================================================================

# Importa o banco de dados que validamos no PASSO 1
from dados_fabrica import CORES, PRODUTOS


def calcular_batelada(id_produto, id_cor, num_caixas):
    """Calcula a dosagem exata de titânio, cargas e pigmentos para uma batelada.

    :param id_produto: Chave do produto (ex: 'textura_rugosa')
    :param id_cor: Chave da cor (ex: 'camurca')
    :param num_caixas: Quantidade de caixas/baldes a serem produzidos
    :return: Dicionário estruturado com o resultado da dosagem
    """
    if id_produto not in PRODUTOS:
        raise ValueError(f"Produto '{id_produto}' não encontrado no sistema.")
    if id_cor not in CORES:
        raise ValueError(f"Cor '{id_cor}' não encontrada no sistema.")

    prod = PRODUTOS[id_produto]
    cor = CORES[id_cor]

    # 1. CÁLCULO DO TITÂNIO BASE TOTAL
    titanio_total_g = prod["titanio_g"] * num_caixas

    # 2. CÁLCULO DOS PIGMENTOS DA BATELADA
    pigmentos_calculados = {}
    for pigmento, gramas_base in cor["pigmentos"].items():
        # Aplica a regra de negócio:
        # Se for Amarelo Óxido (Y25), usa o fator_amarelo.
        # Para os demais pigmentos, usa o fator_outros.
        if pigmento == "Y25":
            fator = prod["fator_amarelo"]
        else:
            fator = prod["fator_outros"]

        # Fórmula: Gramas Base (1kg) x Fator da Base x Peso Unitário x Num de Caixas
        dosagem_g = gramas_base * fator * prod["peso_unitario"] * num_caixas
        pigmentos_calculados[pigmento] = round(dosagem_g, 3)

    # 3. MONTAGEM DA ESTRUTURA DE RESPOSTA
    resultado = {
        "produto": prod["nome"],
        "embalagem": prod["embalagem"],
        "cor": cor["nome"],
        "num_caixas": num_caixas,
        "titanio_total_g": titanio_total_g,
        "cargas_base": prod["cargas"],
        "pigmentos": pigmentos_calculados,
    }

    return resultado


def imprimir_ordem_producao(resultado):
    """Exibe no terminal a Ordem de Produção formatada para o chão de fábrica."""
    print("\n" + "=" * 55)
    print("        COLORMATCH PRO — ORDEM DE PRODUÇÃO")
    print("=" * 55)
    print(f"PRODUTO:  {resultado['produto']} ({resultado['embalagem']})")
    print(f"COR:      {resultado['cor']}")
    print(f"LOTE:     {resultado['num_caixas']} caixa(s)")
    print("-" * 55)

    print("📦 TITÂNIO E CARGAS BASE PARA A BATELADA:")
    tit_g = resultado["titanio_total_g"]
    if tit_g >= 1000:
        print(f"  • Titânio (TiO₂): {tit_g / 1000:.3f} kg")
    else:
        print(f"  • Titânio (TiO₂): {tit_g:.1f} g")

    for carga, qtd in resultado["cargas_base"].items():
        print(f"  • {carga}: {qtd}")

    print("-" * 55)
    print("🎨 PIGMENTOS DA BATELADA (BALANÇA):")
    for pig, qtd_g in resultado["pigmentos"].items():
        g_por_caixa = qtd_g / resultado["num_caixas"]
        if qtd_g >= 1000:
            print(
                f"  • Pigmento [{pig}]: {qtd_g / 1000:.3f} kg ({g_por_caixa:.2f} g/caixa)"
            )
        else:
            print(f"  • Pigmento [{pig}]: {qtd_g:.2f} g ({g_por_caixa:.2f} g/caixa)")
    print("=" * 55 + "\n")


# =====================================================================
# TESTE RÁPIDO DO PASSO 2
# =====================================================================
if __name__ == "__main__":
    # Testando 10 caixas de Textura Rugosa na cor Camurça
    res1 = calcular_batelada("textura_rugosa", "camurca", 10)
    imprimir_ordem_producao(res1)