"""
Utilitários diversos para o dashboard.
"""
import streamlit as st
import pandas as pd
from typing import Any, Dict, List
from functools import wraps
import hashlib

# Import do tema
from src.theme import get_css, get_tokens, ThemeColors, get_theme_colors


def init_theme() -> None:
    """Inicializa tema no session_state e injeta CSS."""
    if "theme_mode" not in st.session_state:
        st.session_state["theme_mode"] = "light"
    
    # Injeta CSS do tema ativo
    st.markdown(get_css(st.session_state["theme_mode"]), unsafe_allow_html=True)


def theme_toggle_sidebar() -> None:
    """Renderiza toggle de tema na sidebar."""
    with st.sidebar:
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### 🎨 Tema")
        with col2:
            # Toggle visual
            current = st.session_state["theme_mode"]
            new_mode = "dark" if current == "light" else "light"
            label = "🌙" if current == "light" else "☀️"
            if st.button(label, key="theme_toggle", help=f"Alternar para modo {'escuro' if current == 'light' else 'claro'}", width="stretch"):
                st.session_state["theme_mode"] = new_mode
                st.rerun()


def get_theme() -> ThemeColors:
    """Retorna cores do tema ativo."""
    return get_theme_colors(st.session_state.get("theme_mode", "light"))


def format_number(num: float, decimals: int = 0) -> str:
    """Formata número com separador de milhares brasileiro."""
    if pd.isna(num):
        return "-"
    if decimals == 0:
        return f"{int(num):,}".replace(",", ".")
    return f"{num:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_pct(num: float, decimals: int = 1) -> str:
    """Formata porcentagem."""
    if pd.isna(num):
        return "-"
    return f"{num:.{decimals}f}%".replace(".", ",")


def format_date_br(date) -> str:
    """Formata data no padrão brasileiro DD/MM/YYYY."""
    if pd.isna(date):
        return "-"
    return pd.Timestamp(date).strftime("%d/%m/%Y")


def download_button(df: pd.DataFrame, filename: str, label: str = "📥 Baixar CSV") -> None:
    """Botão de download CSV."""
    csv = df.to_csv(index=False, sep=";", encoding="utf-8-sig")
    st.download_button(
        label=label,
        data=csv.encode("utf-8-sig"),
        file_name=filename,
        mime="text/csv",
        width="stretch",
    )


def filter_sidebar(df: pd.DataFrame, key_prefix: str = "") -> Dict[str, List]:
    """Renderiza sidebar com filtros e retorna dicionário de filtros selecionados."""
    from src.data_processor import prepare_filter_options
    
    options = prepare_filter_options(df)
    filters = {}
    
    with st.sidebar:
        st.markdown("### 🔍 Filtros")
        
        # Mês/Ano (multiselect)
        meses = options.get("MES_ANO", [])
        if meses:
            selected = st.multiselect(
                "📅 Mês/Ano",
                options=meses,
                default=meses,
                key=f"{key_prefix}_mes"
            )
            if selected:
                filters["MES_ANO"] = selected
        
        # UF
        ufs = options.get("UF", [])
        if ufs:
            selected = st.multiselect(
                "🗺️ UF",
                options=ufs,
                default=[],
                key=f"{key_prefix}_uf"
            )
            if selected:
                filters["UF"] = selected
        
        # Região
        regioes = options.get("REGIAO", [])
        if regioes:
            selected = st.multiselect(
                "🌎 Região",
                options=regioes,
                default=[],
                key=f"{key_prefix}_regiao"
            )
            if selected:
                filters["REGIAO"] = selected
        
        # Plano
        planos = options.get("PLANO", [])
        if planos:
            selected = st.multiselect(
                "📱 Plano",
                options=planos,
                default=[],
                key=f"{key_prefix}_plano"
            )
            if selected:
                filters["PLANO"] = selected
        
        # Desclassificação
        desclass = options.get("DESCLASSIFICACAOBAIXA", [])
        if desclass:
            selected = st.multiselect(
                "📋 Tipo de Churn",
                options=desclass,
                default=[],
                key=f"{key_prefix}_desclass"
            )
            if selected:
                filters["DESCLASSIFICACAOBAIXA"] = selected
        
        # RV
        rv_opts = options.get("RV", [])
        if rv_opts:
            selected = st.multiselect(
                "💰 RV",
                options=rv_opts,
                default=[],
                key=f"{key_prefix}_rv"
            )
            if selected:
                filters["RV"] = selected
        
        st.markdown("---")
        if st.button("🔄 Limpar Filtros", width="stretch"):
            st.rerun()
    
    return filters


@st.cache_data(ttl=3600, show_spinner="Carregando dados...")
def load_data_cached() -> pd.DataFrame:
    """Carrega dados com cache do Streamlit."""
    from src.data_loader import load_unified
    return load_unified()


def get_data_hash(df: pd.DataFrame) -> str:
    """Gera hash do DataFrame para cache invalidation."""
    return hashlib.md5(pd.util.hash_pandas_object(df, index=True).values).hexdigest()


def page_header(title: str, subtitle: str = "") -> None:
    """Header padrão das páginas — premium: título + eyebrow enxutos, alinhados."""
    sub = f'<p class="page-sub">{subtitle}</p>' if subtitle else ""
    st.markdown(
        f"""
        <div class="page-head">
            <h1>{title}</h1>
            {sub}
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_row(metrics: List[Dict[str, Any]], cols: int = 4) -> None:
    """Renderiza uma linha de métricas KPI."""
    columns = st.columns(cols)
    for i, m in enumerate(metrics):
        with columns[i % cols]:
            delta = m.get("delta")
            delta_color = m.get("delta_color", "normal")
            st.metric(
                label=m["label"],
                value=m["value"],
                delta=delta,
                delta_color=delta_color,
            )


def info_box(message: str, type: str = "info") -> None:
    """Caixa de informação colorida usando tokens do tema.
    
    Aceita **negrito** markdown e converte para <strong> (dentro de HTML
    o markdown nativo não é processado — os asteriscos apareceriam literais).
    """
    import re
    theme = get_theme()
    icons = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}
    
    # Mapeia tipos para tokens do tema
    border_map = {
        "info": theme.primary,
        "success": theme.voluntario,
        "warning": theme.warning,
        "error": theme.involuntario,
    }
    
    border_color = border_map.get(type, theme.primary)
    bg_color = theme.tokens["surface"]
    message = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", message)
    
    st.markdown(
        f"""
        <div class="st-info-box-{type}" style="
            background-color: {bg_color};
            border-left: 4px solid {border_color};
            padding: 12px 16px;
            border-radius: 4px;
            margin: 8px 0;
            color: {theme.tokens['text']};
        ">
            <strong>{icons.get(type, icons['info'])} {message}</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_state(message: str = "Nenhum dado encontrado com os filtros atuais.") -> None:
    """Estado vazio amigável."""
    theme = get_theme()
    st.markdown(
        f"""
        <div style="
            text-align: center;
            padding: 60px 20px;
            color: {theme.tokens['muted']};
        ">
            <div style="font-size: 48px; margin-bottom: 16px;">📭</div>
            <div style="font-size: 18px; font-weight: 500;">{message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Amostra padronizada das seções de exportação
EXPORT_SAMPLE_COLS = [
    "MES_ANO", "UF", "REGIAO", "PLANO", "DEALER", "DIRETOR", "GERENTE_DIVISAO",
    "DESCLASSIFICACAOBAIXA", "MOTIVO_BAIXA", "RV", "TEMPO_VIDA_DIAS",
]
EXPORT_RENAME = {
    "MES_ANO": "Mês/Ano", "UF": "UF", "REGIAO": "Região", "PLANO": "Plano",
    "DEALER": "Dealer", "DIRETOR": "Diretor", "GERENTE_DIVISAO": "Gerente Divisão",
    "DESCLASSIFICACAOBAIXA": "Classificação", "MOTIVO_BAIXA": "Motivo de Baixa",
    "RV": "RV", "TEMPO_VIDA_DIAS": "Tempo de Vida (dias)",
}


def export_section(df: pd.DataFrame, filename: str, title: str = "Exportação — Dados Completos",
                   extra_name: str = "", detail_df=None, detail_title: str = "",
                   sample_n: int = 100) -> None:
    """Seção de exportação SEMPRE visível: título + botão/legenda + amostra legível.

    Substitui os expanders colapsáveis que escondiam o botão de download
    e tabelas com colunas cruas (nomes técnicos truncados).
    """
    heading = f"### 📋 {title} — {extra_name}" if extra_name else f"### 📋 {title}"
    st.markdown(heading)

    col_dl, col_cap = st.columns([1, 3], vertical_alignment="center")
    with col_dl:
        download_button(df, filename, label="⬇️ Baixar CSV Completo")
    with col_cap:
        st.caption("CSV com todos os registros filtrados (';', UTF-8 com BOM).")

    sample_cols = [c for c in EXPORT_SAMPLE_COLS if c in df.columns]
    if sample_cols:
        st.markdown(f"**Amostra dos dados (primeiras {sample_n} linhas):**")
        sample = df.head(sample_n)[sample_cols].rename(
            columns={k: v for k, v in EXPORT_RENAME.items() if k in sample_cols}
        )
        dataframe_with_config(sample, height=330)

    if detail_df is not None and not detail_df.empty:
        st.markdown(f"**{detail_title or 'Detalhamento'}:**")
        detail_rename = {
            "MOTIVO_BAIXA": "Motivo de Baixa", "DESCLASSIFICACAOBAIXA": "Classificação",
            "TOTAL": "Total", "VOLUNTARIO": "Voluntário", "INVOLUNTARIO": "Involuntário",
            "RV_SIM": "RV = SIM", "PCT_TOTAL": "% do Total",
            "PCT_VOLUNTARIO": "% Voluntário", "PCT_RV": "% RV",
            "TEMPO_MEDIO": "Tempo Médio (dias)", "DEALER": "Dealer",
            "DIRETOR": "Diretor", "GERENTE_DIVISAO": "Gerente Divisão",
            "TOP_MOTIVO": "Top Motivo",
        }
        detail = detail_df.rename(columns={k: v for k, v in detail_rename.items() if k in detail_df.columns})
        dataframe_with_config(detail, height=380)


def clickable_chart(fig, key: str, hint: str = "",
                    priority=("customdata", "y", "x", "label")):
    """Gráfico clicável via on_select="rerun": retorna o valor do item selecionado.

    Interatividade cruzada: passe o retorno para apply_click_filter() para
    filtrar os painéis seguintes da aba. Clicar no mesmo item de novo limpa
    a seleção (retorna None).
    """
    ev = st.plotly_chart(fig, key=key, width="stretch", on_select="rerun")
    if hint:
        st.caption(hint)
    pts = getattr(getattr(ev, "selection", None), "points", None) or []
    if not pts:
        return None
    p = pts[0] if isinstance(pts[0], dict) else pts[0].__dict__
    for k in priority:
        v = p.get(k)
        if isinstance(v, (list, tuple)):
            v = v[0] if v else None
        if v not in (None, ""):
            return str(v)
    return None


def apply_click_filter(df: pd.DataFrame, dim, value) -> pd.DataFrame:
    """Aplica filtro vindo de um clique em gráfico (sem mutar o df de origem)."""
    if dim is None or value is None or df.empty or dim not in df.columns:
        return df
    mask = df[dim].astype(str) == str(value)
    return df[mask] if mask.any() else df


def dataframe_with_config(df: pd.DataFrame, height: int = 400) -> None:
    """Exibe DataFrame com configurações otimizadas."""
    st.dataframe(
        df,
        width="stretch",
        height=height,
        hide_index=True,
        column_config={
            col: st.column_config.Column(
                help=f"Coluna: {col}",
            ) for col in df.columns
        },
    )


# Mapeamento de meses para ordenação
MES_LABELS = {
    "abr/26": "Abr/2026",
    "mai/26": "Mai/2026", 
    "jun/26": "Jun/2026",
    "04/2026": "Abr/2026",
    "05/2026": "Mai/2026",
    "06/2026": "Jun/2026",
}

def format_mes_ano(mes: str) -> str:
    """Formata mês/ano para exibição."""
    return MES_LABELS.get(mes, mes)