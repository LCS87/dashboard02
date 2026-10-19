"""
Configurações centrais do dashboard B2B Churn.
"""
from pathlib import Path

# ============================================================
# Paths
# ============================================================
ROOT_DIR = Path(__file__).parent.parent  # dashboard02/
DATA_RAW_DIR = ROOT_DIR / "data" / "raw"
DATA_PROCESSED_DIR = ROOT_DIR / "data" / "processed"
DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

UNIFIED_PARQUET = DATA_PROCESSED_DIR / "churn_unificado.parquet"
SCHEMA_JSON = DATA_PROCESSED_DIR / "schema.json"

# ============================================================
# Mapeamentos e Constantes
# ============================================================

# UF -> Região
UF_REGIAO = {
    "AC": "Norte", "AP": "Norte", "AM": "Norte", "PA": "Norte", "RO": "Norte", "RR": "Norte", "TO": "Norte",
    "AL": "Nordeste", "BA": "Nordeste", "CE": "Nordeste", "MA": "Nordeste", "PB": "Nordeste",
    "PE": "Nordeste", "PI": "Nordeste", "RN": "Nordeste", "SE": "Nordeste",
    "DF": "Centro-Oeste", "GO": "Centro-Oeste", "MT": "Centro-Oeste", "MS": "Centro-Oeste",
    "ES": "Sudeste", "MG": "Sudeste", "RJ": "Sudeste", "SP": "Sudeste",
    "PR": "Sul", "RS": "Sul", "SC": "Sul",
}

# Planos -> Categoria de plano (para agrupamento)
PLANO_CATEGORIA = {
    "1GB": "Entrada", "6GB": "Entrada", "8GB": "Entrada",
    "10GB": "Intermediário", "12GB": "Intermediário", "15GB": "Intermediário", "20GB": "Intermediário",
    "30GB": "Avançado", "40GB": "Avançado", "50GB": "Avançado", "100GB": "Premium",
}

# Ordem dos meses para sorting
MES_ORDEM = {
    "abr/26": 1, "04/2026": 1, "abr/26": 1,
    "mai/26": 2, "05/2026": 2, "mai/26": 2,
    "jun/26": 3, "06/2026": 3, "jun/26": 3,
}

# Faixas de tempo (dias ativos)
FAIXA_TEMPO_ORDEM = [
    "0-30d", "31-60d", "61-90d", "91-180d", "181-365d", ">1 ano"
]

# Portes
PORTE_ORDEM = ["Pequeno", "Médio-Pequeno", "Médio", "Médio-Grande", "Grande"]

# Colunas esperadas nos CSVs mensais (junho, maio)
COLUNAS_MENSAIS = [
    "DEALEAR", "CD_DEALER", "NOMEDIRETOR", "NOMEGERENTEDIVISAO",
    "CODCLI", "CNPJ_CLIENTE", "CLIENTE", "UF", "DDD", "MATERIAL",
    "NM_TELEFONE", "DT_BAIXA", "DT_ATIVACAO", "PLANO",
    "DESCLASSIFICACAOBAIXA", "MOTIVO_BAIXA", "RV", "DT_REFERENCIA"
]

# Colunas do arquivo consolidado (abril-maio-junho)
COLUNAS_CONSOLIDADO = [
    "CODCLI", "CLIENTE", "UF", "DDD", "DT_BAIXA", "DT_ATIVACAO",
    "PLANO", "DESCLASSIFICACAOBAIXA", "MOTIVO_BAIXA", "RV",
    "Mês/Ano", "Dias", "Porte", "Categoria", "Faixa"
]

# Colunas finais unificadas
COLUNAS_FINAIS = [
    "CODCLI", "CLIENTE", "UF", "DDD", "DT_BAIXA", "DT_ATIVACAO",
    "PLANO", "DESCLASSIFICACAOBAIXA", "MOTIVO_BAIXA", "RV",
    "DT_REFERENCIA", "MES_ANO", "DIAS_ATIVO", "PORTE", "CATEGORIA", "FAIXA_TEMPO",
    "DEALER", "CD_DEALER", "DIRETOR", "GERENTE_DIVISAO",
    "REGIAO", "PLANO_CATEGORIA", "TEMPO_VIDA_DIAS"
]

# Configurações de encoding dos CSVs originais
CSV_ENCODING = "latin-1"
CSV_SEP = ";"

# Colunas de data
DATE_COLUMNS = ["DT_BAIXA", "DT_ATIVACAO", "DT_REFERENCIA"]

# Colunas numéricas
NUMERIC_COLUMNS = ["CODCLI", "DDD", "DIAS_ATIVO", "TEMPO_VIDA_DIAS"]

# Colunas categóricas para filtros
CATEGORICAL_FILTERS = [
    "UF", "REGIAO", "DEALER", "DIRETOR", "GERENTE_DIVISAO",
    "PLANO", "PLANO_CATEGORIA", "DESCLASSIFICACAOBAIXA",
    "MOTIVO_BAIXA", "RV", "PORTE", "CATEGORIA", "FAIXA_TEMPO", "MES_ANO"
]