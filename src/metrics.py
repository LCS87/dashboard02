"""
Módulo de cálculo de métricas e KPIs para o dashboard.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from src.config import FAIXA_TEMPO_ORDEM, PORTE_ORDEM, MES_ORDEM


def calculate_overall_kpis(df: pd.DataFrame) -> Dict:
    """KPIs gerais do dataset - versão expandida com métricas de qualidade."""
    total = len(df)
    if total == 0:
        return {k: 0 for k in ["total", "voluntario", "involuntario", "rv_sim", 
                                "pct_voluntario", "pct_involuntario", "pct_rv", 
                                "tempo_medio", "tempo_mediano",
                                "pct_precoce_90", "pct_precoce_30",
                                "concentracao_top5_dealers", "concentracao_top3_motivos",
                                "gap_media_mediana"]}
    
    voluntario = int((df["DESCLASSIFICACAOBAIXA"] == "VOLUNTÁRIO").sum())
    involuntario = int((df["DESCLASSIFICACAOBAIXA"] == "INVOLUNTÁRIO").sum())
    rv_sim = int((df["RV"].astype(str).str.upper() == "SIM").sum())
    
    # Churn precoce (<= 90 dias e <= 30 dias)
    precoce_90 = int((df["TEMPO_VIDA_DIAS"] <= 90).sum())
    precoce_30 = int((df["TEMPO_VIDA_DIAS"] <= 30).sum())
    
    # Concentração: share do top 5 dealers / top 3 motivos
    top5_dealers = df.groupby("DEALER")["CODCLI"].count().nlargest(5).sum()
    top3_motivos = df.groupby("MOTIVO_BAIXA")["CODCLI"].count().nlargest(3).sum()
    
    tempo_medio = df["TEMPO_VIDA_DIAS"].mean()
    tempo_mediano = df["TEMPO_VIDA_DIAS"].median()
    gap_media_mediana = round(tempo_medio - tempo_mediano, 1) if pd.notna(tempo_medio) else 0
    
    return {
        "total": int(total),
        "voluntario": voluntario,
        "involuntario": involuntario,
        "rv_sim": rv_sim,
        "pct_voluntario": round(voluntario / total * 100, 1),
        "pct_involuntario": round(involuntario / total * 100, 1),
        "pct_rv": round(rv_sim / total * 100, 1),
        "tempo_medio": round(tempo_medio, 1) if pd.notna(tempo_medio) else 0,
        "tempo_mediano": round(tempo_mediano, 1) if pd.notna(tempo_mediano) else 0,
        "pct_precoce_90": round(precoce_90 / total * 100, 1),
        "pct_precoce_30": round(precoce_30 / total * 100, 1),
        "concentracao_top5_dealers": round(top5_dealers / total * 100, 1),
        "concentracao_top3_motivos": round(top3_motivos / total * 100, 1),
        "gap_media_mediana": gap_media_mediana,
    }


def calculate_monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Tendência mensal de churn."""
    trend = df.groupby("MES_ANO").agg(
        TOTAL=("CODCLI", "count"),
        VOLUNTARIO=("DESCLASSIFICACAOBAIXA", lambda x: (x == "VOLUNTÁRIO").sum()),
        INVOLUNTARIO=("DESCLASSIFICACAOBAIXA", lambda x: (x == "INVOLUNTÁRIO").sum()),
        RV_SIM=("RV", lambda x: (x.astype(str).str.upper() == "SIM").sum()),
        TEMPO_MEDIO=("TEMPO_VIDA_DIAS", "mean"),
    ).reset_index()
    
    # Ordena por mês
    trend["MES_ORDEM"] = trend["MES_ANO"].map(MES_ORDEM).fillna(99)
    trend = trend.sort_values("MES_ORDEM").drop(columns="MES_ORDEM")
    
    # MoM change
    trend["MOM_CHANGE_PCT"] = trend["TOTAL"].pct_change() * 100
    trend["MOM_CHANGE_PCT"] = trend["MOM_CHANGE_PCT"].round(1)
    
    return trend


def calculate_churn_by_dimension(df: pd.DataFrame, dim: str, top_n: int = 15) -> pd.DataFrame:
    """Churn agrupado por uma dimensão (UF, PLANO, DEALER, etc)."""
    if dim not in df.columns:
        return pd.DataFrame()
    
    grouped = df.groupby(dim).agg(
        TOTAL=("CODCLI", "count"),
        VOLUNTARIO=("DESCLASSIFICACAOBAIXA", lambda x: (x == "VOLUNTÁRIO").sum()),
        INVOLUNTARIO=("DESCLASSIFICACAOBAIXA", lambda x: (x == "INVOLUNTÁRIO").sum()),
        RV_SIM=("RV", lambda x: (x.astype(str).str.upper() == "SIM").sum()),
        TEMPO_MEDIO=("TEMPO_VIDA_DIAS", "mean"),
    ).reset_index()
    
    grouped["PCT_VOLUNTARIO"] = (grouped["VOLUNTARIO"] / grouped["TOTAL"] * 100).round(1)
    grouped["PCT_RV"] = (grouped["RV_SIM"] / grouped["TOTAL"] * 100).round(1)
    grouped["TEMPO_MEDIO"] = grouped["TEMPO_MEDIO"].round(1)
    
    grouped = grouped.sort_values("TOTAL", ascending=False).head(top_n)
    return grouped


def calculate_motivo_breakdown(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """Breakdown por motivo de baixa."""
    motivo = df.groupby("MOTIVO_BAIXA").agg(
        TOTAL=("CODCLI", "count"),
        VOLUNTARIO=("DESCLASSIFICACAOBAIXA", lambda x: (x == "VOLUNTÁRIO").sum()),
        INVOLUNTARIO=("DESCLASSIFICACAOBAIXA", lambda x: (x == "INVOLUNTÁRIO").sum()),
        RV_SIM=("RV", lambda x: (x.astype(str).str.upper() == "SIM").sum()),
    ).reset_index()
    
    motivo["PCT_TOTAL"] = (motivo["TOTAL"] / motivo["TOTAL"].sum() * 100).round(1)
    motivo = motivo.sort_values("TOTAL", ascending=False).head(top_n)
    return motivo


def calculate_plano_motivo_heatmap(df: pd.DataFrame) -> pd.DataFrame:
    """Matriz Plano x Motivo para heatmap."""
    pivot = pd.crosstab(df["PLANO"], df["MOTIVO_BAIXA"], values=df["CODCLI"], aggfunc="count", margins=False)
    pivot = pivot.fillna(0).astype(int)
    
    # Ordena planos por total
    plano_totals = df.groupby("PLANO")["CODCLI"].count().sort_values(ascending=False)
    pivot = pivot.reindex(plano_totals.index)
    
    # Ordena motivos por total
    motivo_totals = df.groupby("MOTIVO_BAIXA")["CODCLI"].count().sort_values(ascending=False)
    pivot = pivot[motivo_totals.index]
    
    return pivot


def calculate_uf_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Métricas por UF com região."""
    uf = df.groupby(["REGIAO", "UF"]).agg(
        TOTAL=("CODCLI", "count"),
        VOLUNTARIO=("DESCLASSIFICACAOBAIXA", lambda x: (x == "VOLUNTÁRIO").sum()),
        INVOLUNTARIO=("DESCLASSIFICACAOBAIXA", lambda x: (x == "INVOLUNTÁRIO").sum()),
        RV_SIM=("RV", lambda x: (x.astype(str).str.upper() == "SIM").sum()),
        TEMPO_MEDIO=("TEMPO_VIDA_DIAS", "mean"),
    ).reset_index()
    
    uf["PCT_VOLUNTARIO"] = (uf["VOLUNTARIO"] / uf["TOTAL"] * 100).round(1)
    uf["PCT_RV"] = (uf["RV_SIM"] / uf["TOTAL"] * 100).round(1)
    uf["TEMPO_MEDIO"] = uf["TEMPO_MEDIO"].round(1)
    uf = uf.sort_values("TOTAL", ascending=False)
    return uf


def calculate_dealer_ranking(df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """Ranking de dealers por volume de churn."""
    dealer = df.groupby(["DEALER", "DIRETOR", "GERENTE_DIVISAO"]).agg(
        TOTAL=("CODCLI", "count"),
        VOLUNTARIO=("DESCLASSIFICACAOBAIXA", lambda x: (x == "VOLUNTÁRIO").sum()),
        INVOLUNTARIO=("DESCLASSIFICACAOBAIXA", lambda x: (x == "INVOLUNTÁRIO").sum()),
        RV_SIM=("RV", lambda x: (x.astype(str).str.upper() == "SIM").sum()),
        TEMPO_MEDIO=("TEMPO_VIDA_DIAS", "mean"),
        TOP_MOTIVO=("MOTIVO_BAIXA", lambda x: x.mode().iloc[0] if not x.mode().empty else ""),
    ).reset_index()
    
    dealer["PCT_VOLUNTARIO"] = (dealer["VOLUNTARIO"] / dealer["TOTAL"] * 100).round(1)
    dealer["PCT_RV"] = (dealer["RV_SIM"] / dealer["TOTAL"] * 100).round(1)
    dealer["TEMPO_MEDIO"] = dealer["TEMPO_MEDIO"].round(1)
    dealer = dealer.sort_values("TOTAL", ascending=False).head(top_n)
    return dealer


def calculate_cohort_retention(df: pd.DataFrame) -> pd.DataFrame:
    """Matriz de retenção/cohort: contagem de churn por mês de ativação vs mês relativo."""
    # Prepara cohorts
    df_cohort = df.copy()
    df_cohort["MES_ATIVACAO"] = df_cohort["DT_ATIVACAO"].dt.to_period("M")
    df_cohort["MES_BAIXA"] = df_cohort["DT_BAIXA"].dt.to_period("M")
    df_cohort["MES_RELATIVO"] = (df_cohort["MES_BAIXA"] - df_cohort["MES_ATIVACAO"]).apply(lambda x: x.n if pd.notna(x) else None)
    
    # Tamanho do cohort (base de clientes ativos no mês de ativação)
    # Como não temos base total, usamos churn acumulado como proxy
    cohort_churn = df_cohort.groupby(["MES_ATIVACAO", "MES_RELATIVO"]).size().reset_index(name="CHURN_COUNT")
    
    # Pivot
    pivot = cohort_churn.pivot(index="MES_ATIVACAO", columns="MES_RELATIVO", values="CHURN_COUNT")
    pivot = pivot.fillna(0).astype(int)
    
    # Converte index/columns para string
    pivot.index = pivot.index.astype(str)
    pivot.columns = [f"M+{c}" for c in pivot.columns]
    
    return pivot


def calculate_cohort_rate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Matriz de cohort com TAXA de churn (%).
    Como não temos base ativa total, calcula taxa relativa ao tamanho do cohort (churn M+0).
    """
    df_cohort = df.copy()
    df_cohort["MES_ATIVACAO"] = df_cohort["DT_ATIVACAO"].dt.to_period("M")
    df_cohort["MES_BAIXA"] = df_cohort["DT_BAIXA"].dt.to_period("M")
    df_cohort["MES_RELATIVO"] = (df_cohort["MES_BAIXA"] - df_cohort["MES_ATIVACAO"]).apply(lambda x: x.n if pd.notna(x) else None)
    
    # Contagem por cohort e mês relativo
    cohort_counts = df_cohort.groupby(["MES_ATIVACAO", "MES_RELATIVO"]).size().reset_index(name="CHURN_COUNT")
    
    # Tamanho do cohort = churn no M+0 (primeiro mês)
    cohort_sizes = cohort_counts[cohort_counts["MES_RELATIVO"] == 0][["MES_ATIVACAO", "CHURN_COUNT"]].copy()
    cohort_sizes.columns = ["MES_ATIVACAO", "COHORT_SIZE"]
    
    # Merge para calcular taxa
    cohort_rate = cohort_counts.merge(cohort_sizes, on="MES_ATIVACAO", how="left")
    cohort_rate["CHURN_RATE"] = (cohort_rate["CHURN_COUNT"] / cohort_rate["COHORT_SIZE"] * 100).round(1)
    
    # Pivot da taxa
    pivot_rate = cohort_rate.pivot(index="MES_ATIVACAO", columns="MES_RELATIVO", values="CHURN_RATE")
    pivot_rate = pivot_rate.fillna(0).round(1)
    
    # Converte index/columns para string
    pivot_rate.index = pivot_rate.index.astype(str)
    pivot_rate.columns = [f"M+{c}" for c in pivot_rate.columns]
    
    return pivot_rate


def calculate_cohort_combined(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Retorna tanto contagem quanto taxa do cohort."""
    counts = calculate_cohort_retention(df)
    rates = calculate_cohort_rate(df)
    return counts, rates


def calculate_faixa_tempo_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Distribuição por faixa de tempo de vida."""
    faixa = df.groupby("FAIXA_TEMPO").agg(
        TOTAL=("CODCLI", "count"),
        VOLUNTARIO=("DESCLASSIFICACAOBAIXA", lambda x: (x == "VOLUNTÁRIO").sum()),
        INVOLUNTARIO=("DESCLASSIFICACAOBAIXA", lambda x: (x == "INVOLUNTÁRIO").sum()),
    ).reset_index()
    
    # Ordena pela ordem definida
    faixa["ORDEM"] = faixa["FAIXA_TEMPO"].map({v: i for i, v in enumerate(FAIXA_TEMPO_ORDEM)})
    faixa = faixa.sort_values("ORDEM").drop(columns="ORDEM")
    
    faixa["PCT_TOTAL"] = (faixa["TOTAL"] / faixa["TOTAL"].sum() * 100).round(1)
    return faixa


def calculate_porte_categoria_cross(df: pd.DataFrame) -> pd.DataFrame:
    """Cross-tab Porte x Categoria."""
    cross = pd.crosstab(df["PORTE"], df["CATEGORIA"], values=df["CODCLI"], aggfunc="count", margins=True, margins_name="TOTAL")
    cross = cross.fillna(0).astype(int)
    
    # Reordena portse
    porte_order = [p for p in PORTE_ORDEM if p in cross.index]
    if "TOTAL" in cross.index:
        porte_order.append("TOTAL")
    cross = cross.reindex(porte_order)
    
    return cross


def calculate_top_clientes_churn(df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """Top clientes com mais churn (múltiplas linhas)."""
    top = df.groupby(["CODCLI", "CLIENTE", "UF", "DEALER"]).agg(
        QTD_LINHAS=("NM_TELEFONE", "nunique"),
        TOTAL_CHURN=("CODCLI", "count"),
        PLANOS=("PLANO", lambda x: ", ".join(x.unique()[:3])),
        MOTIVOS=("MOTIVO_BAIXA", lambda x: ", ".join(x.unique()[:3])),
        PRIMEIRA_BAIXA=("DT_BAIXA", "min"),
        ULTIMA_BAIXA=("DT_BAIXA", "max"),
    ).reset_index()
    
    top = top.sort_values("TOTAL_CHURN", ascending=False).head(top_n)
    return top


if __name__ == "__main__":
    from data_loader import load_unified
    df = load_unified()
    
    print("KPIs Gerais:", calculate_overall_kpis(df))
    print("\nTendência Mensal:")
    print(calculate_monthly_trend(df))
    print("\nTop 10 UFs:")
    print(calculate_churn_by_dimension(df, "UF", 10))
    print("\nTop 10 Motivos:")
    print(calculate_motivo_breakdown(df, 10))
    print("\nTop 10 Dealers:")
    print(calculate_dealer_ranking(df, 10))
    print("\nDistribuição Faixa Tempo:")
    print(calculate_faixa_tempo_distribution(df))