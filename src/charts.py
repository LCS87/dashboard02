"""
Módulo de gráficos Plotly para o dashboard - usando tema Floresta & Cobre.
Versão 2.0 - Otimizada para legibilidade, contraste e formatação pt-BR.

Notas de formatação:
- ``layout.separators = ",."`` (plotly.js: charAt(0)=decimal, charAt(1)=milhar)
  aplica o locale pt-BR em ticks, hover, texttemplate e labels de pie/treemap.
- Eixos numéricos usam ``tickformat=",.0f"`` (agrupamento de milhar + 0 decimais).
- Rotulos de valor em barras usam ``texttemplate="%{text:,.0f}"`` via locale pt-BR.
"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Optional, List, Dict
from src.config import FAIXA_TEMPO_ORDEM, PORTE_ORDEM, UF_REGIAO
from src.theme import get_theme_colors, get_plotly_template

PT_BR = ",."  # separadores pt-BR: decimal "," e milhar "."


def get_colors():
    """Retorna cores do tema ativo."""
    return get_theme_colors()


def get_template():
    """Retorna template Plotly do tema ativo."""
    import streamlit as st
    mode = st.session_state.get("theme_mode", "light")
    return get_plotly_template(mode)["layout"]


def format_number_br(value, decimals=0):
    """Formata número no padrão brasileiro: 1.234 ou 1.234,56"""
    if pd.isna(value):
        return "0"
    if decimals == 0:
        return f"{int(round(float(value))):,}".replace(",", ".")
    formatted = f"{float(value):,.{decimals}f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")


def format_pct_br(value):
    """Formata percentual no padrão brasileiro: 12,3%"""
    if pd.isna(value):
        return "0%"
    return f"{float(value):.1f}".replace(".", ",") + "%"


def _max_label_len(series: pd.Series) -> int:
    """Maior tamanho de rótulo de categoria (seguro para vazio/NaN)."""
    mx = series.astype(str).str.len().max()
    return int(mx) if pd.notna(mx) else 0


def apply_layout(fig: go.Figure, title: str = "", height: int = 500,
                 show_legend: bool = True, legend_orientation: str = "h",
                 margin: dict = None) -> go.Figure:
    """Aplica layout padrão aos gráficos usando tema ativo - versão melhorada."""
    colors = get_colors()
    template = get_template()

    if margin is None:
        margin = dict(l=70, r=60, t=80, b=70)

    # Text color from theme - contraste WCAG AA
    text_color = colors.tokens["text"]
    muted_color = colors.tokens["muted"] if "muted" in colors.tokens else colors.tokens["text"]

    fig.update_layout(
        title=dict(
            text=title,
            x=0.02,
            y=0.98,
            font=dict(size=22, color=text_color, family="Inter, sans-serif")
        ),
        template=template.get("template", "plotly_white"),
        separators=PT_BR,
        height=height,
        margin=margin,
        showlegend=show_legend,
        legend=dict(
            orientation=legend_orientation,
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor=colors.tokens["surface"],
            bordercolor=colors.tokens["border"],
            borderwidth=1,
            font=dict(color=text_color, size=14),
        ),
        hovermode="closest",
        hoverlabel=dict(
            bgcolor=colors.tokens["surface"],
            bordercolor=colors.tokens["border"],
            font=dict(color=text_color, size=15)
        ),
        paper_bgcolor=template.get("paper_bgcolor", colors.tokens["surface"]),
        plot_bgcolor=template.get("plot_bgcolor", colors.tokens["surface"]),
        font=dict(color=text_color, size=14, family="Inter, sans-serif"),
        xaxis=dict(
            showgrid=True,
            gridcolor=template.get("xaxis", {}).get("gridcolor", colors.tokens["border"]),
            gridwidth=1,
            linecolor=template.get("xaxis", {}).get("linecolor", colors.tokens["border"]),
            tickfont=dict(color=text_color, size=14),
            title=dict(font=dict(color=muted_color, size=15)),
            zerolinecolor=template.get("xaxis", {}).get("zerolinecolor", colors.tokens["border"]),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=template.get("yaxis", {}).get("gridcolor", colors.tokens["border"]),
            gridwidth=1,
            linecolor=template.get("yaxis", {}).get("linecolor", colors.tokens["border"]),
            tickfont=dict(color=text_color, size=14),
            title=dict(font=dict(color=muted_color, size=15)),
            zerolinecolor=template.get("yaxis", {}).get("zerolinecolor", colors.tokens["border"]),
            tickformat=",.0f",
        ),
    )
    return fig


def kpi_card(value, label: str, delta=None,
             delta_color: str = "normal") -> go.Figure:
    """Cria um card KPI estilo indicator."""
    colors = get_colors()
    template = get_template()

    num_value = value if isinstance(value, (int, float)) and pd.notna(value) else 0
    delta_cfg = None
    if isinstance(delta, (int, float)) and pd.notna(delta):
        delta_cfg = {
            "reference": float(delta),
            "relative": False,
            "valueformat": ".1f",
            "increasing": {"color": colors.involuntario},
            "decreasing": {"color": colors.voluntario},
        }

    fig = go.Figure(go.Indicator(
        mode="number+delta" if delta_cfg else "number",
        value=num_value,
        delta=delta_cfg,
        number={"font": {"size": 42, "color": colors.tokens["text"]}, "valueformat": ",.0f"},
        title={"text": label, "font": {"size": 15, "color": colors.tokens["muted"]}},
        domain={"x": [0, 1], "y": [0, 1]},
    ))
    fig.update_layout(height=140, margin=dict(l=15, r=15, t=15, b=15),
                      separators=PT_BR,
                      paper_bgcolor=template.get("paper_bgcolor", colors.tokens["bg"]))
    return fig


def line_churn_trend(df: pd.DataFrame, title: str = "Evolução Mensal do Churn") -> go.Figure:
    """Gráfico de linha: churn total, voluntário, involuntário por mês."""
    colors = get_colors()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["MES_ANO"], y=df["TOTAL"],
        mode="lines+markers", name="Total",
        line=dict(color=colors.primary, width=4),
        marker=dict(size=12, symbol="circle", line=dict(width=2, color=colors.tokens["surface"])),
        hovertemplate="<b>%{x}</b><br>Total: %{y:,.0f}<extra></extra>",
        customdata=df["MES_ANO"].astype(str).tolist(),
    ))

    fig.add_trace(go.Scatter(
        x=df["MES_ANO"], y=df["VOLUNTARIO"],
        mode="lines+markers", name="Voluntário",
        line=dict(color=colors.voluntario, width=3, dash="dash"),
        marker=dict(size=10, symbol="diamond", line=dict(width=2, color=colors.tokens["surface"])),
        hovertemplate="<b>%{x}</b><br>Voluntário: %{y:,.0f}<extra></extra>",
        customdata=df["MES_ANO"].astype(str).tolist(),
    ))

    fig.add_trace(go.Scatter(
        x=df["MES_ANO"], y=df["INVOLUNTARIO"],
        mode="lines+markers", name="Involuntário",
        line=dict(color=colors.involuntario, width=3, dash="dot"),
        marker=dict(size=10, symbol="square", line=dict(width=2, color=colors.tokens["surface"])),
        hovertemplate="<b>%{x}</b><br>Involuntário: %{y:,.0f}<extra></extra>",
        customdata=df["MES_ANO"].astype(str).tolist(),
    ))

    fig = apply_layout(fig, title, height=520, margin=dict(l=70, r=60, t=80, b=70))
    fig.update_layout(
        hovermode="x unified",
        yaxis_title="Quantidade de Churns",
        xaxis_title="Mês/Ano",
        xaxis=dict(tickangle=0),
        yaxis=dict(rangemode="tozero", tickformat=",.0f"),
    )
    return fig


def bar_churn_by_dim(df: pd.DataFrame, dim: str, title: str = "",
                     color_col: str = None, horizontal: bool = True) -> go.Figure:
    """Gráfico de barras: churn por dimensão - legibilidade melhorada."""
    colors = get_colors()

    # Formatos pt-BR no hover (vírgula decimal)
    hover_formats = {}
    for col in ["PCT_VOLUNTARIO", "PCT_RV", "PCT_TOTAL", "TEMPO_MEDIO"]:
        if col in df.columns:
            hover_formats[col] = ":.1f"
    if "RV_SIM" in df.columns:
        hover_formats["RV_SIM"] = ":.0f"

    # Cor uniforme (sem colorbar redundante) quando não há dimensão de cor
    marker_cfg = dict(line=dict(width=1, color=colors.tokens["border"]))
    if not color_col:
        marker_cfg["color"] = colors.primary

    if horizontal:
        fig = px.bar(
            df, y=dim, x="TOTAL",
            color=color_col,
            color_discrete_sequence=colors.color_sequence if color_col else None,
            orientation="h",
            text="TOTAL",
            hover_data=hover_formats if hover_formats else None,
        )
        fig.update_traces(
            textposition="outside",
            texttemplate="%{text:,.0f}",
            textfont=dict(size=15, color=colors.tokens["text"], family="Inter"),
            marker=marker_cfg,
        )
        fig.update_yaxes(
            categoryorder="total ascending",
            tickfont=dict(size=14),
        )
        fig.update_xaxes(tickformat=",.0f")
        # Margem esquerda dinâmica: rótulos de categoria longos (Dealer, Motivo...)
        left = min(420, max(80, _max_label_len(df[dim]) * 8 + 30))
        margin = dict(l=left, r=90, t=80, b=70)
    else:
        fig = px.bar(
            df, x=dim, y="TOTAL",
            color=color_col,
            color_discrete_sequence=colors.color_sequence if color_col else None,
            text="TOTAL",
            hover_data=hover_formats if hover_formats else None,
        )
        fig.update_traces(
            textposition="outside",
            texttemplate="%{text:,.0f}",
            textfont=dict(size=15, color=colors.tokens["text"], family="Inter"),
            marker=marker_cfg,
        )
        fig.update_xaxes(tickangle=-45, tickfont=dict(size=13))
        fig.update_yaxes(tickformat=",.0f")
        margin = dict(l=70, r=60, t=80, b=110)

    # Dynamic height: base + 35px por barra
    bar_height = max(500, len(df) * 35 + 150)
    return apply_layout(fig, title or f"Churn por {dim}", height=bar_height, margin=margin)


def donut_voluntario_involuntario(df: pd.DataFrame, title: str = "Voluntário vs Involuntário") -> go.Figure:
    """Donut chart: voluntário vs involuntário - tamanho aumentado."""
    colors = get_colors()
    template = get_template()

    counts = df["DESCLASSIFICACAOBAIXA"].value_counts()
    total = counts.sum()

    # Percentuais em pt-BR já embutidos no rótulo
    percentages = [f"{v / total * 100:.1f}%".replace(".", ",") for v in counts.values]
    labels_with_pct = [f"{label}<br>({pct})" for label, pct in zip(counts.index, percentages)]

    fig = go.Figure(go.Pie(
        labels=labels_with_pct,
        values=counts.values,
        customdata=list(counts.index),  # rótulos crus p/ clique (label exibido tem <br>/%)
        hole=0.55,
        marker=dict(
            colors=[colors.voluntario, colors.involuntario],
            line=dict(color=colors.tokens["surface"], width=4)
        ),
        textinfo="label+percent",
        textposition="outside",
        textfont=dict(size=15, color=colors.tokens["text"], family="Inter"),
        hovertemplate="<b>%{label}</b><br>Quantidade: %{value:,.0f}<br>%{percent}<extra></extra>",
        pull=[0.03, 0.03],
    ))

    fig.update_layout(
        separators=PT_BR,
        title=dict(text=title, x=0.02, y=0.98, font=dict(size=22, color=colors.tokens["text"], family="Inter")),
        height=500,
        margin=dict(l=70, r=70, t=80, b=90),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=14, color=colors.tokens["text"]),
            bgcolor=colors.tokens["surface"],
            bordercolor=colors.tokens["border"],
            borderwidth=1,
        ),
        paper_bgcolor=template.get("paper_bgcolor", colors.tokens["surface"]),
        annotations=[dict(
            text=f"<b>Total</b><br>{format_number_br(total)}",
            x=0.5, y=0.5,
            font=dict(size=18, color=colors.tokens["text"]),
            showarrow=False
        )]
    )
    return fig


def bar_motivo_breakdown(df: pd.DataFrame, title: str = "Top Motivos de Churn") -> go.Figure:
    """Barras horizontais: motivos de churn - contraste melhorado."""
    colors = get_colors()

    hover_formats = {}
    if "PCT_TOTAL" in df.columns:
        hover_formats["PCT_TOTAL"] = ":.1f"
    if "RV_SIM" in df.columns:
        hover_formats["RV_SIM"] = ":.0f"

    has_desclass = "DESCLASSIFICACAOBAIXA" in df.columns

    fig = px.bar(
        df, y="MOTIVO_BAIXA", x="TOTAL",
        color="DESCLASSIFICACAOBAIXA" if has_desclass else None,
        color_discrete_map={"VOLUNTÁRIO": colors.voluntario, "INVOLUNTÁRIO": colors.involuntario} if has_desclass else None,
        orientation="h",
        text="TOTAL",
        hover_data=hover_formats if hover_formats else None,
    )
    fig.update_traces(
        textposition="outside",
        texttemplate="%{text:,.0f}",
        textfont=dict(size=15, color=colors.tokens["text"], family="Inter"),
        marker=dict(line=dict(width=1, color=colors.tokens["border"])),
    )
    fig.update_yaxes(
        categoryorder="total ascending",
        tickfont=dict(size=14),
    )
    fig.update_xaxes(tickformat=",.0f")
    # Motivos têm labels longos -> margem esquerda dinâmica
    left = min(460, max(110, _max_label_len(df["MOTIVO_BAIXA"]) * 8 + 30))
    margin = dict(l=left, r=90, t=80, b=70)
    return apply_layout(fig, title, height=max(560, len(df) * 34 + 150), margin=margin)


def heatmap_plano_motivo(pivot: pd.DataFrame, title: str = "Plano vs Motivo de Churn") -> go.Figure:
    """Heatmap: Plano x Motivo - tamanho e legibilidade aumentados."""
    colors = get_colors()
    template = get_template()

    # Limita para top 15 planos e top 10 motivos para legibilidade
    pivot_plot = pivot.iloc[:15, :10]

    # Texto das células já formatado em pt-BR (100% determinístico)
    text_values = [[format_number_br(v) for v in row] for row in pivot_plot.values]

    fig = go.Figure(go.Heatmap(
        z=pivot_plot.values,
        x=pivot_plot.columns,
        y=pivot_plot.index,
        colorscale=colors.sequences["sequential_volume"],
        hoverongaps=False,
        hovertemplate="<b>Plano:</b> %{y}<br><b>Motivo:</b> %{x}<br><b>Churn:</b> %{z:,.0f}<extra></extra>",
        colorbar=dict(
            title=dict(text="Qtd Churn", font=dict(size=14, color=colors.tokens["text"])),
            tickfont=dict(color=colors.tokens["muted"], size=13),
        ),
        text=text_values,
        texttemplate="%{text}",
        textfont=dict(size=13, color="#1F2D26"),
    ))

    left = min(420, max(130, _max_label_len(pivot_plot.index) * 8 + 30))
    fig.update_layout(
        separators=PT_BR,
        title=dict(text=title, x=0.02, y=0.98, font=dict(size=22, color=colors.tokens["text"], family="Inter")),
        height=640,
        margin=dict(l=left, r=70, t=80, b=110),
        xaxis=dict(
            tickangle=-45,
            side="bottom",
            tickfont=dict(color=colors.tokens["text"], size=14),
        ),
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(color=colors.tokens["text"], size=14),
        ),
        paper_bgcolor=template.get("paper_bgcolor", colors.tokens["surface"]),
        plot_bgcolor=template.get("plot_bgcolor", colors.tokens["surface"]),
    )
    return fig


def treemap_motivo_hierarchy(df: pd.DataFrame, title: str = "Hierarquia de Motivos") -> go.Figure:
    """Treemap: Desclassificação -> Motivo - tamanho aumentado."""
    colors = get_colors()
    template = get_template()

    # Agrupa
    tree_data = df.groupby(["DESCLASSIFICACAOBAIXA", "MOTIVO_BAIXA"]).size().reset_index(name="COUNT")

    fig = px.treemap(
        tree_data,
        path=["DESCLASSIFICACAOBAIXA", "MOTIVO_BAIXA"],
        values="COUNT",
        color="DESCLASSIFICACAOBAIXA",
        color_discrete_map={"VOLUNTÁRIO": colors.voluntario, "INVOLUNTÁRIO": colors.involuntario},
        hover_data=["COUNT"],
    )

    fig.update_traces(
        textinfo="label+value+percent parent",
        textfont_size=17,
        textfont_color=colors.tokens["text"],
        marker=dict(line=dict(width=2, color=colors.tokens["surface"]), cornerradius=6),
        hovertemplate="<b>%{label}</b><br>Qtd: %{value:,.0f}<br>%{percentParent:.1%}<extra></extra>",
    )

    fig.update_layout(
        separators=PT_BR,
        title=dict(text=title, x=0.02, y=0.98, font=dict(size=22, color=colors.tokens["text"], family="Inter")),
        height=560,
        margin=dict(l=20, r=20, t=80, b=20),
        paper_bgcolor=template.get("paper_bgcolor", colors.tokens["surface"]),
    )
    return fig


def scatter_tempo_vida_rv(df: pd.DataFrame, title: str = "Tempo de Vida vs RV") -> go.Figure:
    """Scatter: tempo de vida vs RV, colorido por desclassificação."""
    colors = get_colors()

    fig = px.scatter(
        df, x="TEMPO_VIDA_DIAS", y="RV",
        color="DESCLASSIFICACAOBAIXA",
        color_discrete_map={"VOLUNTÁRIO": colors.voluntario, "INVOLUNTÁRIO": colors.involuntario},
        hover_data=["CLIENTE", "PLANO", "MOTIVO_BAIXA", "UF", "DEALER"],
        opacity=0.65,
        color_discrete_sequence=colors.color_sequence,
    )

    fig = apply_layout(fig, title, height=520)
    fig.update_layout(
        xaxis_title="Tempo de Vida (dias)",
        yaxis_title="RV (SIM=1, NÃO=0)",
        xaxis=dict(tickformat=",.0f"),
        yaxis=dict(dtick=1, tickvals=[0, 1], ticktext=["Não", "Sim"]),
    )
    return fig


def box_tempo_by_categoria(df: pd.DataFrame, title: str = "Tempo de Vida por Categoria") -> go.Figure:
    """Box plot: tempo de vida por categoria de churn."""
    colors = get_colors()

    fig = px.box(
        df, x="CATEGORIA", y="TEMPO_VIDA_DIAS",
        color="DESCLASSIFICACAOBAIXA",
        color_discrete_map={"VOLUNTÁRIO": colors.voluntario, "INVOLUNTÁRIO": colors.involuntario},
        points="outliers",
    )

    fig = apply_layout(fig, title, height=520)
    fig.update_layout(
        xaxis_title="Categoria",
        yaxis_title="Tempo de Vida (dias)",
        yaxis=dict(tickformat=",.0f"),
    )
    return fig


def bar_faixa_tempo(df: pd.DataFrame, title: str = "Distribuição por Faixa de Tempo") -> go.Figure:
    """Barras: distribuição por faixa de tempo."""
    colors = get_colors()

    # Ordena pela ordem definida
    df_plot = df.copy()
    df_plot["ORDEM"] = df_plot["FAIXA_TEMPO"].map({v: i for i, v in enumerate(FAIXA_TEMPO_ORDEM)})
    df_plot = df_plot.sort_values("ORDEM")

    fig = px.bar(
        df_plot, x="FAIXA_TEMPO", y="TOTAL",
        color="DESCLASSIFICACAOBAIXA" if "DESCLASSIFICACAOBAIXA" in df_plot.columns else None,
        color_discrete_map={"VOLUNTÁRIO": colors.voluntario, "INVOLUNTÁRIO": colors.involuntario},
        text="TOTAL",
        barmode="group",
    )
    fig.update_traces(
        textposition="outside",
        texttemplate="%{text:,.0f}",
        textfont=dict(size=15, color=colors.tokens["text"], family="Inter"),
        marker=dict(line=dict(width=1, color=colors.tokens["border"])),
    )
    fig.update_xaxes(tickfont=dict(size=14))
    fig.update_yaxes(tickformat=",.0f")
    return apply_layout(fig, title, height=520)


def bar_porte_categoria_stacked(cross: pd.DataFrame, title: str = "Porte x Categoria") -> go.Figure:
    """Barra empilhada: Porte x Categoria - contraste melhorado."""
    colors = get_colors()

    # Remove linha TOTAL se existir
    plot_data = cross.drop(index="TOTAL", errors="ignore")

    fig = go.Figure()
    for i, cat in enumerate(plot_data.columns):
        fig.add_trace(go.Bar(
            name=cat,
            x=plot_data.index,
            y=plot_data[cat],
            marker_color=colors.color_sequence[i % len(colors.color_sequence)],
            marker_line=dict(width=1, color=colors.tokens["surface"]),
            hovertemplate=f"<b>Porte:</b> %{{x}}<br><b>{cat}:</b> %{{y:,.0f}}<extra></extra>",
        ))

    fig.update_layout(
        barmode="stack",
        separators=PT_BR,
        title=dict(text=title, x=0.02, y=0.98, font=dict(size=22, color=colors.tokens["text"], family="Inter")),
        height=500,
        margin=dict(l=70, r=60, t=80, b=70),
        xaxis_title="Porte",
        yaxis_title="Quantidade",
        xaxis=dict(tickfont=dict(size=14)),
        yaxis=dict(tickformat=",.0f", tickfont=dict(size=14)),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=14, color=colors.tokens["text"]),
            bgcolor=colors.tokens["surface"],
            bordercolor=colors.tokens["border"],
            borderwidth=1,
        ),
        paper_bgcolor=colors.tokens["surface"],
        plot_bgcolor=colors.tokens["surface"],
    )
    return fig


def table_dealer_ranking(df: pd.DataFrame, title: str = "Ranking de Dealers") -> go.Figure:
    """Tabela interativa: ranking de dealers - fontes maiores."""
    colors = get_colors()
    template = get_template()

    # Prepara dados para exibição
    display_df = df[["DEALER", "DIRETOR", "GERENTE_DIVISAO", "TOTAL", "VOLUNTARIO", "INVOLUNTARIO",
                      "PCT_VOLUNTARIO", "PCT_RV", "TEMPO_MEDIO", "TOP_MOTIVO"]].copy()

    display_df.columns = ["Dealer", "Diretor", "Gerente", "Total", "Voluntário", "Involuntário",
                           "% Voluntário", "% RV", "Tempo Médio (dias)", "Top Motivo"]

    # Formata números em pt-BR
    for col in ["Total", "Voluntário", "Involuntário"]:
        display_df[col] = display_df[col].apply(lambda x: format_number_br(x))
    for col in ["% Voluntário", "% RV"]:
        display_df[col] = display_df[col].apply(lambda x: format_pct_br(x))
    display_df["Tempo Médio (dias)"] = display_df["Tempo Médio (dias)"].apply(
        lambda x: f"{float(x):.1f}".replace(".", ",") if pd.notna(x) else "-")

    fig = go.Figure(go.Table(
        header=dict(
            values=list(display_df.columns),
            fill_color=colors.primary,
            font=dict(color="white", size=14, family="Inter"),
            align="left",
            height=42,
        ),
        cells=dict(
            values=[display_df[c] for c in display_df.columns],
            fill_color=[[colors.tokens["surface"], colors.tokens["hover"]] * (len(display_df) // 2 + 1)][:len(display_df)],
            font=dict(color=colors.tokens["text"], size=13, family="Inter"),
            align="left",
            height=36,
            line_color=colors.tokens["border"],
        ),
    ))

    fig.update_layout(
        separators=PT_BR,
        title=dict(text=title, x=0.02, y=0.98, font=dict(size=22, color=colors.tokens["text"], family="Inter")),
        height=max(300, min(700, len(display_df) * 42 + 160)),
        margin=dict(l=20, r=20, t=80, b=20),
        paper_bgcolor=template.get("paper_bgcolor", colors.tokens["surface"]),
    )
    return fig


def cohort_heatmap(cohort_pivot: pd.DataFrame, title: str = "Cohort Analysis - Taxa de Churn por Mês de Ativação",
                   show_rate: bool = True) -> go.Figure:
    """Heatmap de cohort analysis - tamanho aumentado."""
    colors = get_colors()
    template = get_template()

    # % com vírgula decimal no padrão pt-BR (locale plotly) ou contagem inteira
    texttemplate = "%{z:.1%}" if show_rate else "%{z:,.0f}"
    text_values = [
        [format_pct_br(v * 100) if show_rate else format_number_br(v) for v in row]
        for row in cohort_pivot.values
    ]

    fig = go.Figure(go.Heatmap(
        z=cohort_pivot.values,
        x=cohort_pivot.columns,
        y=cohort_pivot.index,
        colorscale=colors.sequences["sequential_risk"],
        hoverongaps=False,
        hovertemplate="<b>Cohort:</b> %{y}<br><b>Mês Relativo:</b> %{x}<br><b>Churn:</b> %{z:,.2f}<extra></extra>",
        colorbar=dict(
            title=dict(
                text="Taxa de Churn" if show_rate else "Qtd Churn",
                font=dict(size=14, color=colors.tokens["text"]),
            ),
            tickfont=dict(color=colors.tokens["muted"], size=13),
            **({"tickformat": ".0%"} if show_rate else {}),
        ),
        text=text_values,
        texttemplate="%{text}",
        textfont=dict(size=13, color="#1F2D26"),
    ))

    left = min(300, max(100, _max_label_len(cohort_pivot.index) * 8 + 30))
    fig.update_layout(
        separators=PT_BR,
        title=dict(text=title, x=0.02, y=0.98, font=dict(size=22, color=colors.tokens["text"], family="Inter")),
        height=520,
        margin=dict(l=left, r=70, t=80, b=80),
        xaxis=dict(side="bottom", tickfont=dict(color=colors.tokens["text"], size=14)),
        yaxis=dict(autorange="reversed", tickfont=dict(color=colors.tokens["text"], size=14)),
        paper_bgcolor=template.get("paper_bgcolor", colors.tokens["surface"]),
        plot_bgcolor=template.get("plot_bgcolor", colors.tokens["surface"]),
    )
    return fig


def map_uf_churn(df: pd.DataFrame, title: str = "Churn por UF") -> go.Figure:
    """Mapa do Brasil por UF (choropleth)."""
    colors = get_colors()
    template = get_template()

    # Dados por UF
    uf_data = df.groupby("UF").size().reset_index(name="TOTAL")

    fig = px.choropleth(
        uf_data,
        locations="UF",
        geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
        color="TOTAL",
        color_continuous_scale=colors.sequences["sequential_volume"],
        scope="south america",
        hover_name="UF",
        hover_data={"TOTAL": ":.0f"},
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False,
        showcoastlines=True,
        coastlinecolor=colors.tokens["border"],
        bgcolor=colors.tokens["surface"],
    )

    fig.update_layout(
        separators=PT_BR,
        title=dict(text=title, x=0.02, y=0.98, font=dict(size=22, color=colors.tokens["text"], family="Inter")),
        height=580,
        margin=dict(l=20, r=20, t=80, b=20),
        paper_bgcolor=template.get("paper_bgcolor", colors.tokens["surface"]),
        coloraxis_colorbar=dict(
            title=dict(text="Churn", font=dict(size=14, color=colors.tokens["text"])),
            tickfont=dict(color=colors.tokens["muted"], size=13),
        ),
    )
    return fig


def bar_comparativo_mensal(df: pd.DataFrame, dim: str, title: str = "") -> go.Figure:
    """Barras agrupadas: comparativo mensal por dimensão."""
    colors = get_colors()

    # Pivot: mês x dimensão
    pivot = df.groupby(["MES_ANO", dim]).size().reset_index(name="COUNT")
    pivot_pivot = pivot.pivot(index=dim, columns="MES_ANO", values="COUNT").fillna(0)

    fig = go.Figure()
    for i, mes in enumerate(pivot_pivot.columns):
        fig.add_trace(go.Bar(
            name=mes,
            x=pivot_pivot.index,
            y=pivot_pivot[mes],
            marker_color=colors.color_sequence[i % len(colors.color_sequence)],
            marker_line=dict(width=1, color=colors.tokens["surface"]),
            hovertemplate=f"<b>{mes}</b><br>%{{x}}: %{{y:,.0f}}<extra></extra>",
        ))

    fig = apply_layout(
        fig, title or f"Comparativo Mensal por {dim}", height=520,
        margin=dict(l=70, r=60, t=80, b=110),
    )
    fig.update_layout(
        barmode="group",
        xaxis=dict(tickangle=-45, tickfont=dict(size=13)),
        yaxis=dict(tickformat=",.0f", title="Quantidade"),
    )
    return fig


def funnel_churn(df: pd.DataFrame, title: str = "Composição do Churn") -> go.Figure:
    """Barra empilhada horizontal: Total -> Vol/Invol -> RV dentro de cada."""
    colors = get_colors()
    template = get_template()

    total = len(df)
    vol = int((df["DESCLASSIFICACAOBAIXA"] == "VOLUNTÁRIO").sum())
    invol = int((df["DESCLASSIFICACAOBAIXA"] == "INVOLUNTÁRIO").sum())

    # RV dentro de cada tipo
    vol_rv_sim = int(((df["DESCLASSIFICACAOBAIXA"] == "VOLUNTÁRIO") & (df["RV"].astype(str).str.upper() == "SIM")).sum())
    vol_rv_nao = vol - vol_rv_sim
    invol_rv_sim = int(((df["DESCLASSIFICACAOBAIXA"] == "INVOLUNTÁRIO") & (df["RV"].astype(str).str.upper() == "SIM")).sum())
    invol_rv_nao = invol - invol_rv_sim

    fig = go.Figure()

    # Total como barra de fundo
    fig.add_trace(go.Bar(
        name="Total",
        y=["Churn"],
        x=[total],
        orientation="h",
        marker_color=colors.tokens["border"],
        opacity=0.3,
        hovertemplate="Total: %{x:,.0f}<extra></extra>",
    ))

    # Voluntário
    fig.add_trace(go.Bar(
        name="Voluntário",
        y=["Churn"],
        x=[vol],
        orientation="h",
        marker_color=colors.voluntario,
        hovertemplate="Voluntário: %{x:,.0f}<extra></extra>",
    ))

    # Involuntário
    fig.add_trace(go.Bar(
        name="Involuntário",
        y=["Churn"],
        x=[invol],
        orientation="h",
        marker_color=colors.involuntario,
        hovertemplate="Involuntário: %{x:,.0f}<extra></extra>",
    ))

    # RV dentro de Voluntário (overlay)
    fig.add_trace(go.Bar(
        name="Voluntário + RV=SIM",
        y=["Churn"],
        x=[vol_rv_sim],
        orientation="h",
        marker_color=colors.primary,
        opacity=0.8,
        hovertemplate="Voluntário + RV=SIM: %{x:,.0f}<extra></extra>",
    ))

    fig.add_trace(go.Bar(
        name="Voluntário + RV=NÃO",
        y=["Churn"],
        x=[vol_rv_nao],
        orientation="h",
        marker_color=colors.voluntario,
        opacity=0.5,
        hovertemplate="Voluntário + RV=NÃO: %{x:,.0f}<extra></extra>",
    ))

    # RV dentro de Involuntário
    fig.add_trace(go.Bar(
        name="Involuntário + RV=SIM",
        y=["Churn"],
        x=[invol_rv_sim],
        orientation="h",
        marker_color=colors.warning,
        opacity=0.8,
        hovertemplate="Involuntário + RV=SIM: %{x:,.0f}<extra></extra>",
    ))

    fig.add_trace(go.Bar(
        name="Involuntário + RV=NÃO",
        y=["Churn"],
        x=[invol_rv_nao],
        orientation="h",
        marker_color=colors.involuntario,
        opacity=0.5,
        hovertemplate="Involuntário + RV=NÃO: %{x:,.0f}<extra></extra>",
    ))

    fig.update_layout(
        barmode="overlay",
        separators=PT_BR,
        title=dict(text=title, x=0.02, y=0.98, font=dict(size=22, color=colors.tokens["text"], family="Inter")),
        height=300,
        margin=dict(l=40, r=40, t=80, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=14, color=colors.tokens["text"]),
            bgcolor=colors.tokens["surface"],
            bordercolor=colors.tokens["border"],
            borderwidth=1,
        ),
        paper_bgcolor=template.get("paper_bgcolor", colors.tokens["surface"]),
        plot_bgcolor=template.get("plot_bgcolor", colors.tokens["surface"]),
        xaxis=dict(
            showgrid=True,
            gridcolor=colors.tokens["border"],
            tickformat=",.0f",
            title="Quantidade",
        ),
        yaxis=dict(showticklabels=False),
    )
    return fig


def stacked_bar_composition(df: pd.DataFrame, title: str = "Composição Voluntário/Involuntário por RV") -> go.Figure:
    """Barra 100% stacked: composição RV dentro de Vol/Invol."""
    colors = get_colors()

    # Calcula composição
    vol = df[df["DESCLASSIFICACAOBAIXA"] == "VOLUNTÁRIO"]
    invol = df[df["DESCLASSIFICACAOBAIXA"] == "INVOLUNTÁRIO"]

    vol_rv_sim = (vol["RV"].astype(str).str.upper() == "SIM").sum()
    vol_rv_nao = len(vol) - vol_rv_sim
    invol_rv_sim = (invol["RV"].astype(str).str.upper() == "SIM").sum()
    invol_rv_nao = len(invol) - invol_rv_sim

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="Voluntário - RV=SIM",
        x=["Voluntário"],
        y=[vol_rv_sim],
        marker_color=colors.primary,
        marker_line=dict(width=1, color=colors.tokens["surface"]),
        hovertemplate="Voluntário + RV=SIM: %{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="Voluntário - RV=NÃO",
        x=["Voluntário"],
        y=[vol_rv_nao],
        marker_color=colors.voluntario,
        opacity=0.7,
        marker_line=dict(width=1, color=colors.tokens["surface"]),
        hovertemplate="Voluntário + RV=NÃO: %{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="Involuntário - RV=SIM",
        x=["Involuntário"],
        y=[invol_rv_sim],
        marker_color=colors.warning,
        marker_line=dict(width=1, color=colors.tokens["surface"]),
        hovertemplate="Involuntário + RV=SIM: %{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="Involuntário - RV=NÃO",
        x=["Involuntário"],
        y=[invol_rv_nao],
        marker_color=colors.involuntario,
        opacity=0.7,
        marker_line=dict(width=1, color=colors.tokens["surface"]),
        hovertemplate="Involuntário + RV=NÃO: %{y:,.0f}<extra></extra>",
    ))

    fig.update_layout(
        barmode="stack",
        separators=PT_BR,
        title=dict(text=title, x=0.02, y=0.98, font=dict(size=22, color=colors.tokens["text"], family="Inter")),
        height=500,
        margin=dict(l=70, r=60, t=80, b=70),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=14, color=colors.tokens["text"]),
            bgcolor=colors.tokens["surface"],
            bordercolor=colors.tokens["border"],
            borderwidth=1,
        ),
        paper_bgcolor=colors.tokens["surface"],
        plot_bgcolor=colors.tokens["surface"],
        yaxis_title="Quantidade",
        yaxis=dict(tickformat=",.0f"),
        xaxis=dict(tickfont=dict(size=14)),
    )
    return fig


if __name__ == "__main__":
    from data_loader import load_unified
    from metrics import calculate_monthly_trend, calculate_motivo_breakdown

    df = load_unified()

    # Teste rápido
    trend = calculate_monthly_trend(df)
    print("Trend:", trend)

    fig = line_churn_trend(trend)
    fig.show()
