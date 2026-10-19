"""
Módulo de carregamento e unificação dos dados de churn.
"""
import pandas as pd
import json
from pathlib import Path
from typing import List, Optional
from src.config import (
    DATA_RAW_DIR, UNIFIED_PARQUET, SCHEMA_JSON,
    CSV_ENCODING, CSV_SEP, COLUNAS_MENSAIS, COLUNAS_CONSOLIDADO,
    COLUNAS_FINAIS, UF_REGIAO, PLANO_CATEGORIA, MES_ORDEM,
    DATE_COLUMNS, NUMERIC_COLUMNS
)
from src.anonymizer import DataAnonymizer


def _normalize_column_name(col: str) -> str:
    """Normaliza nome da coluna: strip, upper, substitui espaços/caracteres especiais."""
    col = col.strip().upper()
    col = col.replace("ÃƒÂŠ", "E").replace("ÃƒÂ", "A").replace("ÃƒÂ“", "O")
    col = col.replace("ÃƒÂ§", "C").replace("ÃƒÂ³", "O").replace("ÃƒÂ¡", "A")
    col = col.replace("ÃƒÂ©", "E").replace("ÃƒÂ­", "I").replace("ÃƒÂº", "U")
    return col


def _parse_date_mixed(series: pd.Series) -> pd.Series:
    """Parse de datas com múltiplos formatos."""
    # Tenta formatos comuns - usa o primeiro que produz datas válidas
    formats = [
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d/%m/%y",
        "%m/%Y",      # 06/2026
        "%m/%y",      # 06/26
    ]
    
    for fmt in formats:
        try:
            result = pd.to_datetime(series, format=fmt, errors="coerce")
            # Verifica se pelo menos uma data foi parseada com sucesso
            if result.notna().any():
                return result
        except Exception:
            continue
    
    # Fallback: infer com dayfirst=True
    return pd.to_datetime(series, errors="coerce", dayfirst=True)


def _extract_mes_ano(dt_ref: pd.Series, dt_baixa: pd.Series) -> pd.Series:
    """Extrai mês/ano no formato 'MMM/YY' (ex: abr/26)."""
    # Prioriza DT_REFERENCIA, senão usa DT_BAIXA
    ref = dt_ref.fillna(dt_baixa)
    # strftime %b retorna abreviação em inglês (Jan, Feb, Mar, Apr, May, Jun...)
    # Mapeia para português
    mes_map = {
        "jan": "jan", "feb": "fev", "mar": "mar", "apr": "abr",
        "may": "mai", "jun": "jun", "jul": "jul", "aug": "ago",
        "sep": "set", "oct": "out", "nov": "nov", "dec": "dez"
    }
    return ref.dt.strftime("%b/%y").str.lower().replace(mes_map, regex=True)


def _calculate_dias_ativo(dt_ativacao: pd.Series, dt_baixa: pd.Series) -> pd.Series:
    """Calcula dias entre ativação e baixa."""
    return (dt_baixa - dt_ativacao).dt.days


def _classify_faixa_tempo(dias: pd.Series) -> pd.Series:
    """Classifica dias ativos em faixas."""
    bins = [0, 30, 60, 90, 180, 365, float("inf")]
    labels = ["0-30d", "31-60d", "61-90d", "91-180d", "181-365d", ">1 ano"]
    return pd.cut(dias, bins=bins, labels=labels, right=True)


def _extract_plano_categoria(plano: pd.Series) -> pd.Series:
    """Extrai categoria do plano baseado no nome."""
    def _map_plano(p):
        if pd.isna(p):
            return "Outros"
        p_upper = str(p).upper()
        for key, cat in PLANO_CATEGORIA.items():
            if key in p_upper:
                return cat
        return "Outros"
    return plano.apply(_map_plano)


def load_monthly_csv(filepath: Path) -> pd.DataFrame:
    """Carrega um CSV mensal (junho, maio) com encoding latin-1."""
    df = pd.read_csv(
        filepath,
        sep=CSV_SEP,
        encoding=CSV_ENCODING,
        dtype=str,  # Lê tudo como string primeiro
        keep_default_na=False,
        na_values=["", "NA", "N/A", "null", "NULL", "None"]
    )
    # Normaliza nomes das colunas
    df.columns = [_normalize_column_name(c) for c in df.columns]
    return df


def load_consolidated_csv(filepath: Path) -> pd.DataFrame:
    """Carrega o CSV consolidado (abril-maio-junho)."""
    df = pd.read_csv(
        filepath,
        sep=CSV_SEP,
        encoding=CSV_ENCODING,
        dtype=str,
        keep_default_na=False,
        na_values=["", "NA", "N/A", "null", "NULL", "None"]
    )
    df.columns = [_normalize_column_name(c) for c in df.columns]
    return df


def process_monthly_df(df: pd.DataFrame) -> pd.DataFrame:
    """Processa DataFrame mensal: tipos, datas, features."""
    df = df.copy()
    
    # Renomeia colunas para padrão unificado
    rename_map = {
        "DEALEAR": "DEALER",
        "CD_DEALER": "CD_DEALER",
        "NOMEDIRETOR": "DIRETOR",
        "NOMEGERENTEDIVISAO": "GERENTE_DIVISAO",
        "CODCLI": "CODCLI",
        "CNPJ_CLIENTE": "CNPJ_CLIENTE",
        "CLIENTE": "CLIENTE",
        "UF": "UF",
        "DDD": "DDD",
        "MATERIAL": "MATERIAL",
        "NM_TELEFONE": "NM_TELEFONE",
        "DT_BAIXA": "DT_BAIXA",
        "DT_ATIVACAO": "DT_ATIVACAO",
        "PLANO": "PLANO",
        "DESCLASSIFICACAOBAIXA": "DESCLASSIFICACAOBAIXA",
        "MOTIVO_BAIXA": "MOTIVO_BAIXA",
        "RV": "RV",
        "DT_REFERENCIA": "DT_REFERENCIA",
    }
    df = df.rename(columns=rename_map)
    
    # Converte datas
    for col in ["DT_BAIXA", "DT_ATIVACAO", "DT_REFERENCIA"]:
        if col in df.columns:
            df[col] = _parse_date_mixed(df[col])
    
    # Converte numéricos
    for col in ["CODCLI", "DDD"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    
    # Features derivadas
    df["MES_ANO"] = _extract_mes_ano(df.get("DT_REFERENCIA"), df["DT_BAIXA"])
    df["DIAS_ATIVO"] = _calculate_dias_ativo(df["DT_ATIVACAO"], df["DT_BAIXA"])
    df["FAIXA_TEMPO"] = _classify_faixa_tempo(df["DIAS_ATIVO"])
    df["PLANO_CATEGORIA"] = _extract_plano_categoria(df["PLANO"])
    df["REGIAO"] = df["UF"].map(UF_REGIAO).fillna("Outros")
    df["TEMPO_VIDA_DIAS"] = df["DIAS_ATIVO"]
    
    # Campos que não existem no mensal - preenche com NaN
    for col in ["PORTE", "CATEGORIA"]:
        if col not in df.columns:
            df[col] = pd.NA
    
    return df


def process_consolidated_df(df: pd.DataFrame) -> pd.DataFrame:
    """Processa DataFrame consolidado: tipos, datas, features."""
    df = df.copy()
    
    rename_map = {
        "CODCLI": "CODCLI",
        "CLIENTE": "CLIENTE",
        "UF": "UF",
        "DDD": "DDD",
        "DT_BAIXA": "DT_BAIXA",
        "DT_ATIVACAO": "DT_ATIVACAO",
        "PLANO": "PLANO",
        "DESCLASSIFICACAOBAIXA": "DESCLASSIFICACAOBAIXA",
        "MOTIVO_BAIXA": "MOTIVO_BAIXA",
        "RV": "RV",
        "MÊS/ANO": "MES_ANO_CONS",
        "DIAS": "DIAS_ATIVO",
        "PORTE": "PORTE",
        "CATEGORIA": "CATEGORIA",
        "FAIXA": "FAIXA_TEMPO",
    }
    df = df.rename(columns=rename_map)
    
    # Converte datas
    for col in ["DT_BAIXA", "DT_ATIVACAO"]:
        if col in df.columns:
            df[col] = _parse_date_mixed(df[col])
    
    # Converte numéricos
    for col in ["CODCLI", "DDD", "DIAS_ATIVO"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    
    # MES_ANO do consolidado já vem formatado
    if "MES_ANO_CONS" in df.columns:
        df["MES_ANO"] = df["MES_ANO_CONS"].str.lower().str.replace("maio", "mai").str.replace("junho", "jun").str.replace("abril", "abr")
    
    # Features derivadas
    df["FAIXA_TEMPO"] = df.get("FAIXA_TEMPO", _classify_faixa_tempo(df["DIAS_ATIVO"]))
    df["PLANO_CATEGORIA"] = _extract_plano_categoria(df["PLANO"])
    df["REGIAO"] = df["UF"].map(UF_REGIAO).fillna("Outros")
    df["TEMPO_VIDA_DIAS"] = df["DIAS_ATIVO"]
    
    # Campos de hierarquia não existem no consolidado
    for col in ["DEALER", "CD_DEALER", "DIRETOR", "GERENTE_DIVISAO", "DT_REFERENCIA", "CNPJ_CLIENTE", "MATERIAL", "NM_TELEFONE"]:
        if col not in df.columns:
            df[col] = pd.NA
    
    return df


def merge_datasets(monthly_dfs: List[pd.DataFrame], consolidated_df: pd.DataFrame) -> pd.DataFrame:
    """
    Une datasets mensais com consolidado.
    Estratégia: usa consolidado como base (tem mais campos analíticos),
    enriquece com dados de hierarquia dos mensais via CODCLI + DT_BAIXA + NM_TELEFONE.
    """
    # Combina todos os mensais
    if monthly_dfs:
        df_monthly = pd.concat(monthly_dfs, ignore_index=True)
    else:
        df_monthly = pd.DataFrame()
    
    # Normaliza MES_ANO nos mensais (pode vir como 'may/26')
    if not df_monthly.empty and "MES_ANO" in df_monthly.columns:
        df_monthly["MES_ANO"] = df_monthly["MES_ANO"].str.lower().replace({"may": "mai"})
    
    # Se não tem consolidado, retorna apenas mensais processados
    if consolidated_df.empty:
        return df_monthly
    
    # Normaliza MES_ANO no consolidado (pode vir como 'may/26')
    if "MES_ANO" in consolidated_df.columns:
        consolidated_df["MES_ANO"] = consolidated_df["MES_ANO"].str.lower().replace({"may": "mai"})
    
    # Cria chave de junção
    def make_key(df):
        return (
            df["CODCLI"].astype(str) + "|" +
            df["DT_BAIXA"].dt.strftime("%Y-%m-%d").fillna("") + "|" +
            df.get("NM_TELEFONE", pd.Series("", index=df.index)).astype(str)
        )
    
    df_monthly["_KEY"] = make_key(df_monthly)
    consolidated_df["_KEY"] = make_key(consolidated_df)
    
    # Campos de hierarquia para trazer do mensal
    hierarquia_cols = ["DEALER", "CD_DEALER", "DIRETOR", "GERENTE_DIVISAO", "DT_REFERENCIA", "CNPJ_CLIENTE", "MATERIAL", "NM_TELEFONE"]
    
    # Merge: left join do consolidado com mensal
    df_merged = consolidated_df.merge(
        df_monthly[["_KEY"] + hierarquia_cols].drop_duplicates(subset="_KEY"),
        on="_KEY",
        how="left",
        suffixes=("", "_MENSAL")
    )
    
    # Remove chave temporária
    df_merged = df_merged.drop(columns=["_KEY"])
    
    # Remove coluna duplicada MES_ANO_CONS se existir
    if "MES_ANO_CONS" in df_merged.columns:
        df_merged = df_merged.drop(columns=["MES_ANO_CONS"])
    
    # Adiciona registros mensais que NÃO estão no consolidado (novos meses)
    if not df_monthly.empty:
        keys_consolidado = set(consolidated_df["_KEY"].unique())
        df_novos = df_monthly[~df_monthly["_KEY"].isin(keys_consolidado)].copy()
        if not df_novos.empty:
            df_novos = df_novos.drop(columns=["_KEY"])
            # Garante mesmas colunas
            for col in df_merged.columns:
                if col not in df_novos.columns:
                    df_novos[col] = pd.NA
            # Reordena colunas dos novos para match
            df_novos = df_novos[df_merged.columns]
            df_merged = pd.concat([df_merged, df_novos], ignore_index=True)
    
    return df_merged


def load_and_process_all() -> pd.DataFrame:
    """Pipeline completo: carrega, processa, une e salva dataset unificado."""
    print("[INFO] Carregando CSVs mensais...")
    # Usa nomes exatos para evitar capturar o consolidado
    monthly_files = [
        DATA_RAW_DIR / "Relatorio_Info_B2B_Churn_junho.csv",
        DATA_RAW_DIR / "RelatorioInfoB2B_Churn_maio.csv",
    ]
    monthly_files = [f for f in monthly_files if f.exists()]
    monthly_dfs = []
    for f in monthly_files:
        print(f"  - {f.name}")
        df = load_monthly_csv(f)
        df = process_monthly_df(df)
        monthly_dfs.append(df)
    
    print("[INFO] Carregando CSV consolidado...")
    consolidated_file = DATA_RAW_DIR / "RelatorioInfoB2B_Churn_abril-maio-junho.csv"
    if consolidated_file.exists():
        df_cons = load_consolidated_csv(consolidated_file)
        df_cons = process_consolidated_df(df_cons)
    else:
        df_cons = pd.DataFrame()
    
    print("[INFO] Unificando datasets...")
    df_unified = merge_datasets(monthly_dfs, df_cons)
    
    # Ordena colunas finais - usa colunas que existem
    priority_cols = [
        "CODCLI", "CLIENTE", "UF", "DDD", "DT_BAIXA", "DT_ATIVACAO",
        "PLANO", "DESCLASSIFICACAOBAIXA", "MOTIVO_BAIXA", "RV",
        "DT_REFERENCIA", "MES_ANO", "DIAS_ATIVO", "PORTE", "CATEGORIA", "FAIXA_TEMPO",
        "DEALER", "CD_DEALER", "DIRETOR", "GERENTE_DIVISAO",
        "REGIAO", "PLANO_CATEGORIA", "TEMPO_VIDA_DIAS"
    ]
    existing_priority = [c for c in priority_cols if c in df_unified.columns]
    other_cols = [c for c in df_unified.columns if c not in existing_priority and not c.endswith("_MENSAL")]
    df_unified = df_unified[existing_priority + other_cols]
    
    # Salva parquet
    print(f"[INFO] Salvando em {UNIFIED_PARQUET}")
    df_unified.to_parquet(UNIFIED_PARQUET, index=False)
    
    # Salva schema
    schema = {col: str(df_unified[col].dtype) for col in df_unified.columns}
    with open(SCHEMA_JSON, "w", encoding="utf-8") as f:
        json.dump(schema, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Dataset unificado: {len(df_unified)} linhas, {len(df_unified.columns)} colunas")
    return df_unified


def load_unified(anonymize: bool = True) -> pd.DataFrame:
    """Carrega dataset unificado do parquet (cache-friendly).
    
    Args:
        anonymize: Se True, aplica anonimização aos dados sensíveis.
    """
    if UNIFIED_PARQUET.exists():
        df = pd.read_parquet(UNIFIED_PARQUET)
    else:
        df = load_and_process_all()
    
    if anonymize:
        anonymizer = DataAnonymizer(seed=42)
        df = anonymizer.anonymize_dataframe(df)
    
    return df


def incremental_update(new_csv_path: Path) -> pd.DataFrame:
    """Adiciona novo CSV mensal ao dataset unificado existente."""
    print(f"[INFO] Atualização incremental: {new_csv_path.name}")
    df_new = load_monthly_csv(new_csv_path)
    df_new = process_monthly_df(df_new)
    
    df_existing = load_unified()
    
    # Chave para deduplicação
    def make_key(df):
        return (
            df["CODCLI"].astype(str) + "|" +
            df["DT_BAIXA"].dt.strftime("%Y-%m-%d").fillna("") + "|" +
            df.get("NM_TELEFONE", pd.Series("", index=df.index)).astype(str)
        )
    
    df_new["_KEY"] = make_key(df_new)
    df_existing["_KEY"] = make_key(df_existing)
    
    # Remove duplicados (mantém existente)
    keys_existing = set(df_existing["_KEY"].unique())
    df_new_unique = df_new[~df_new["_KEY"].isin(keys_existing)].drop(columns=["_KEY"])
    df_existing = df_existing.drop(columns=["_KEY"])
    
    if not df_new_unique.empty:
        df_updated = pd.concat([df_existing, df_new_unique], ignore_index=True)
        df_updated.to_parquet(UNIFIED_PARQUET, index=False)
        print(f"[OK] Adicionados {len(df_new_unique)} novos registros. Total: {len(df_updated)}")
    else:
        df_updated = df_existing
        print("[INFO] Nenhum registro novo (todos duplicados).")
    
    return df_updated


if __name__ == "__main__":
    # Teste rápido
    df = load_and_process_all()
    print(df.head())
    print("\nColunas:", df.columns.tolist())
    print("\nDtypes:\n", df.dtypes)
    print("\nMeses únicos:", sorted(df["MES_ANO"].dropna().unique()))
    print("\nUFs únicas:", sorted(df["UF"].dropna().unique()))
    print("\nDesclassificação:", df["DESCLASSIFICACAOBAIXA"].value_counts())
    print("\nMotivos top 10:", df["MOTIVO_BAIXA"].value_counts().head(10))