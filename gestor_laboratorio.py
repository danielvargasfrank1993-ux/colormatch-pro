# =====================================================================
# gestor_laboratorio.py — Gestão de Fórmulas e Bases (ColorMatch Pro)
# =====================================================================

from dados_fabrica import CORES, PRODUTOS


def atualizar_titanio_produto(id_produto, novas_gramas_titanio):
    """Atualiza a quantidade base de Titânio (TiO2) por caixa/balde de um produto."""
    if id_produto not in PRODUTOS:
        raise ValueError(f"Produto '{id_produto}' não encontrado.")

    PRODUTOS[id_produto]["titanio_g"] = float(novas_gramas_titanio)


def atualizar_multiplicadores(id_produto, novo_fator_amarelo, novo_fator_outros):
    """Ajusta os fatores de escala de pigmentação para um produto específico."""
    if id_produto not in PRODUTOS:
        raise ValueError(f"Produto '{id_produto}' não encontrado.")

    PRODUTOS[id_produto]["fator_amarelo"] = float(novo_fator_amarelo)
    PRODUTOS[id_produto]["fator_outros"] = float(novo_fator_outros)


def cadastrar_nova_cor(id_cor, nome_cor, dicionario_pigmentos):
    """Cadastra ou atualiza uma cor na biblioteca com suas dosagens base por kg (1.0x)."""
    CORES[id_cor] = {"nome": nome_cor, "pigmentos": dicionario_pigmentos}