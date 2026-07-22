# =====================================================================
# dados_fabrica.py — Módulo de Dados da Fábrica (ColorMatch Pro)
# =====================================================================

# 1. BASES DE PRODUTOS, TITÂNIO, CARGAS E MULTIPLICADORES
PRODUTOS = {
    "cristal_italy": {
        "nome": "Cristal Italy",
        "embalagem": "Caixa 20 kg",
        "peso_unitario": 20.0,
        "titanio_g": 80.0,
        "cargas": {"Gel Ligante + Malha #20": "Q.S.P."},
        "fator_amarelo": 1.0,
        "fator_outros": 1.0,
    },
    "grafini": {
        "nome": "Grafini / Grafiato",
        "embalagem": "Caixa 20 kg",
        "peso_unitario": 20.0,
        "titanio_g": 52.0,
        "cargas": {"Calcita #325 (Fosqueante)": "Q.S.P."},
        "fator_amarelo": 1.0,
        "fator_outros": 1.0,
    },
    "selador_primer": {
        "nome": "Selador / Primer",
        "embalagem": "Caixa 18 L",
        "peso_unitario": 18.0,
        "titanio_g": 100.0,
        "cargas": {
            "Calcita #325": "3.500 kg",
            "Reflex HTM": "2.000 kg",
            "Carbonato #1000": "3.500 kg",
        },
        "fator_amarelo": 10.0,
        "fator_outros": 10.0,
    },
    "textura_rugosa": {
        "nome": "Textura Rugosa",
        "embalagem": "Caixa 20 kg",
        "peso_unitario": 20.0,
        "titanio_g": 181.0,
        "cargas": {"Calcita #325": "5.300 kg"},
        "fator_amarelo": 2.5,
        "fator_outros": 3.0,
    },
    "micro_revestimento": {
        "nome": "Micro Revestimento",
        "embalagem": "Caixa 18 L",
        "peso_unitario": 18.0,
        "titanio_g": 668.0,
        "cargas": {
            "Calcita #325": "3.900 kg",
            "Carbonato de Cálcio": "1.509 kg",
            "Carbonato #1000": "2.000 kg",
        },
        "fator_amarelo": 8.0,
        "fator_outros": 9.0,
    },
    "latex_premium": {
        "nome": "Tinta Látex Premium",
        "embalagem": "Caixa 18 L",
        "peso_unitario": 18.0,
        "titanio_g": 1500.0,
        "cargas": {
            "Carbonato #1000": "1.840 kg",
            "Carbonato de Cálcio": "2.500 kg",
            "Reflex HTM": "2.760 kg",
        },
        "fator_amarelo": 20.0,
        "fator_outros": 20.0,
    },
}

# 2. CATÁLOGO BASE DE CORES (Dosagem por 1 kg - Fator 1.0x)
CORES = {
    "elefante": {
        "nome": "Elefante",
        "pigmentos": {"Y25": 0.100, "CB": 0.070, "SH": 0.010},
    },
    "terracota": {
        "nome": "Terracota",
        "pigmentos": {"Y25": 5.000, "FGR": 0.500, "CB": 0.006},
    },
    "martin_pescador": {
        "nome": "Martin Pescador (Suvinil)",
        "pigmentos": {"Verde": 0.718, "SH": 0.541},
    },
    "amarelo_demarcacao": {
        "nome": "Amarelo Demarcação",
        "pigmentos": {"Y25": 4.000, "Amarelo Limpo": 7.000},
    },
    "camurca": {
        "nome": "Camurça",
        "pigmentos": {"Y25": 0.900, "930": 0.140, "CB": 0.040},
    },
    "areia": {
        "nome": "Areia",
        "pigmentos": {"Y25": 0.400, "930": 0.040, "CB": 0.010},
    },
    "gelo": {
        "nome": "Gelo",
        "pigmentos": {"Y25": 0.056, "SH": 0.0024, "CB": 0.007},
    },
}

# Validação simples ao executar o arquivo diretamente
if __name__ == "__main__":
    print(f"✅ Módulo de dados carregado com sucesso!")
    print(f"Total de produtos cadastrados: {len(PRODUTOS)}")
    print(f"Total de cores cadastradas: {len(CORES)}")