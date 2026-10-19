"""
Módulo de processamento avançado e feature engineering.
"""
import pandas as pd
import numpy as np
from src.config import FAIXA_TEMPO_ORDEM, PORTE_ORDEM, MES_ORDEM


def add_cohort_features(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona features de cohort analysis."""
    df = df.copy()
    
    # Mês de ativação (cohort)
    df["MES_ATIVACAO"] = df["DT_ATIVACAO"].dt.to_period("M")
    df["MES_BAIXA"] = df["DT_BAIXA"].dt.to_period("M")
    
    # Período relativo (meses entre ativação e baixa)
    df["MES_RELATIVO"] = (df["MES_BAIXA"] - df["MES_ATIVACAO"]).apply(lambda x: x.n if pd.notna(x) else None)
    
    # Tamanho do cohort (clientes ativados no mesmo mês)
    cohort_sizes = df.groupby("MES_ATIVACAO")["CODCLI"].nunique().reset_index()
    cohort_sizes.columns = ["MES_ATIVACAO", "COHORT_SIZE"]
    df = df.merge(cohort_sizes, on="MES_ATIVACAO", how="left")
    
    # Taxa de churn do cohort até aquele mês
    cohort_churn = df.groupby(["MES_ATIVACAO", "MES_RELATIVO"])["CODCLI"].nunique().reset_index()
    cohort_churn.columns = ["MES_ATIVACAO", "MES_RELATIVO", "CHURN_COUNT"]
    cohort_churn = cohort_churn.merge(cohort_sizes, on="MES_ATIVACAO")
    cohort_churn["CHURN_RATE"] = cohort_churn["CHURN_COUNT"] / cohort_churn["COHORT_SIZE"]
    
    df = df.merge(cohort_churn[["MES_ATIVACAO", "MES_RELATIVO", "CHURN_RATE"]], 
                  on=["MES_ATIVACAO", "MES_RELATIVO"], how="left")
    
    return df


def add_rfm_features(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona features estilo RFM (Recency, Frequency, Monetary proxy)."""
    df = df.copy()
    
    # Recency: dias desde a baixa até a data máxima do dataset
    max_date = df["DT_BAIXA"].max()
    df["RECENCY_DIAS"] = (max_date - df["DT_BAIXA"]).dt.days
    
    # Frequency proxy: número de linhas por cliente (múltiplos chips/linhas)
    freq = df.groupby("CODCLI").size().reset_index(name="FREQUENCY_LINHAS")
    df = df.merge(freq, on="CODCLI", how="left")
    
    # Monetary proxy: RV = SIM indica receita perdida
    df["MONETARY_FLAG"] = df["RV"].astype(str).str.upper().map({"SIM": 1, "NÃO": 0, "NAO": 0}).fillna(0).astype(int)
    
    # Segmentação RFM simples
    df["R_SCORE"] = pd.qcut(df["RECENCY_DIAS"].rank(method="first"), 4, labels=[4,3,2,1], duplicates="drop")
    df["F_SCORE"] = pd.qcut(df["FREQUENCY_LINHAS"].rank(method="first"), 4, labels=[1,2,3,4], duplicates="drop")
    df["M_SCORE"] = df["MONETARY_FLAG"]  # 0 ou 1
    
    df["RFM_SEGMENT"] = df["R_SCORE"].astype(str) + df["F_SCORE"].astype(str) + df["M_SCORE"].astype(str)
    
    return df


def add_dealer_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona métricas de performance por dealer/diretor/gerente."""
    df = df.copy()
    
    # Total churn por dealer
    dealer_stats = df.groupby("DEALER").agg(
        DEALER_CHURN_TOTAL=("CODCLI", "count"),
        DEALER_VOLUNTARIO=("DESCLASSIFICACAOBAIXA", lambda x: (x == "VOLUNTÁRIO").sum()),
        DEALER_INVOLUNTARIO=("DESCLASSIFICACAOBAIXA", lambda x: (x == "INVOLUNTÁRIO").sum()),
        DEALER_RV_SIM=("RV", lambda x: (x.astype(str).str.upper() == "SIM").sum()),
        DEALER_TEMPO_MEDIO=("TEMPO_VIDA_DIAS", "mean"),
    ).reset_index()
    
    dealer_stats["DEALER_PCT_VOLUNTARIO"] = dealer_stats["DEALER_VOLUNTARIO"] / dealer_stats["DEALER_CHURN_TOTAL"]
    dealer_stats["DEALER_PCT_RV"] = dealer_stats["DEALER_RV_SIM"] / dealer_stats["DEALER_CHURN_TOTAL"]
    
    df = df.merge(dealer_stats, on="DEALER", how="left")
    
    # Ranking do dealer (percentil)
    df["DEALER_RANK_PCTL"] = df["DEALER_CHURN_TOTAL"].rank(pct=True)
    
    return df


def prepare_filter_options(df: pd.DataFrame) -> dict:
    """Prepara opções para filtros do dashboard."""
    options = {}
    
    # Meses ordenados
    meses = df["MES_ANO"].dropna().unique()
    mes_ordem_map = {k: v for v, k in enumerate(sorted(meses, key=lambda x: MES_ORDEM.get(x, 99)))}
    options["MES_ANO"] = sorted(meses, key=lambda x: mes_ordem_map.get(x, 99))
    
    # UFs ordenadas
    options["UF"] = sorted(df["UF"].dropna().unique())
    
    # Regiões
    options["REGIAO"] = sorted(df["REGIAO"].dropna().unique())
    
    # Dealers
    options["DEALER"] = sorted(df["DEALER"].dropna().unique())
    
    # Diretores
    options["DIRETOR"] = sorted(df["DIRETOR"].dropna().unique())
    
    # Gerentes
    options["GERENTE_DIVISAO"] = sorted(df["GERENTE_DIVISAO"].dropna().unique())
    
    # Planos
    options["PLANO"] = sorted(df["PLANO"].dropna().unique())
    
    # Categorias de plano
    options["PLANO_CATEGORIA"] = sorted(df["PLANO_CATEGORIA"].dropna().unique())
    
    # Desclassificação
    options["DESCLASSIFICACAOBAIXA"] = sorted(df["DESCLASSIFICACAOBAIXA"].dropna().unique())
    
    # Motivos (top 20 + "Outros")
    motivos = df["MOTIVO_BAIXA"].value_counts()
    top_motivos = motivos.head(20).index.tolist()
    options["MOTIVO_BAIXA"] = top_motivos + (["Outros"] if len(motivos) > 20 else [])
    
    # RV
    options["RV"] = sorted(df["RV"].dropna().unique())
    
    # Portes
    options["PORTE"] = [p for p in PORTE_ORDEM if p in df["PORTE"].dropna().unique()]
    
    # Categorias
    options["CATEGORIA"] = sorted(df["CATEGORIA"].dropna().unique())
    
    # Faixas de tempo
    options["FAIXA_TEMPO"] = [f for f in FAIXA_TEMPO_ORDEM if f in df["FAIXA_TEMPO"].dropna().unique()]
    
    return options


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Aplica filtros ao DataFrame."""
    df = df.copy()
    
    for col, values in filters.items():
        if values and col in df.columns:
            if isinstance(values, list):
                df = df[df[col].isin(values)]
            else:
                df = df[df[col] == values]
    
    return df


def get_kpis(df: pd.DataFrame) -> dict:
    """Calcula KPIs principais."""
    total = len(df)
    voluntario = (df["DESCLASSIFICACAOBAIXA"] == "VOLUNTÁRIO").sum()
    involuntario = (df["DESCLASSIFICACAOBAIXA"] == "INVOLUNTÁRIO").sum()
    rv_sim = (df["RV"].astype(str).str.upper() == "SIM").sum()
    tempo_medio = df["TEMPO_VIDA_DIAS"].mean()
    
    # Churn por mês
    churn_mensal = df.groupby("MES_ANO").size().sort_index()
    mom_change = None
    if len(churn_mensal) >= 2:
        mom_change = (churn_mensal.iloc[-1] - churn_mensal.iloc[-2]) / churn_mensal.iloc[-2] * 100
    
    return {
        "total_churn": int(total),
        "voluntario": int(voluntario),
        "involuntario": int(involuntario),
        "pct_voluntario": round(voluntario / total * 100, 1) if total > 0 else 0,
        "pct_involuntario": round(involuntario / total * 100, 1) if total > 0 else 0,
        "rv_sim": int(rv_sim),
        "pct_rv": round(rv_sim / total * 100, 1) if total > 0 else 0,
        "tempo_medio_dias": round(tempo_medio, 1) if pd.notna(tempo_medio) else 0,
        "churn_mensal": churn_mensal.to_dict(),
        "mom_change_pct": round(mom_change, 1) if mom_change is not None else None,
    }


if __name__ == "__main__":
    from data_loader import load_unified
    df = load_unified()
    df = add_cohort_features(df)
    df = add_dealer_performance(df)
    print("KPIs:", get_kpis(df))
    print("\nOpções de filtro:", {k: len(v) for k, v in prepare_filter_options(df).items()})