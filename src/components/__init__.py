"""
Componentes reutilizáveis para Dashboard Premium.
"""
import streamlit as st
import pandas as pd
from typing import List, Dict, Any
from src.theme import get_theme


def kpi_card(label: str, value: str, delta: str = None, 
             delta_color: str = "normal", help_text: str = None) -> None:
    """Renderiza um card KPI estilizado."""
    theme = get_theme()
    
    delta_html = ""
    if delta:
        color = theme.danger if delta_color == "inverse" else theme.success
        delta_html = f'<div style="color: {color}; font-size: 0.875rem; font-weight: 600; margin-top: 0.25rem;">{delta}</div>'
    
    help_html = f'<div style="font-size: 0.75rem; color: {theme.muted}; margin-top: 0.5rem;">{help_text}</div>' if help_text else ""
    
    st.markdown(f"""
    <div style="
        background: {theme.surface};
        border: 1px solid {theme.border};
        border-radius: 12px;
        padding: 1.5rem;
        transition: all 0.25s ease;
        box-shadow: 0 1px 2px rgba(26, 40, 32, 0.06);
    ">
        <div style="font-size: 0.875rem; font-weight: 500; color: {theme.muted}; text-transform: uppercase; letter-spacing: 0.05em;">{label}</div>
        <div style="font-size: 2.5rem; font-weight: 700; color: {theme.text}; margin: 0.5rem 0;">{value}</div>
        {delta_html}
        {help_html}
    </div>
    """, unsafe_allow_html=True)


def metric_row(metrics: List[Dict[str, Any]], cols: int = 4) -> None:
    """Renderiza uma linha de métricas KPI."""
    columns = st.columns(cols)
    for i, m in enumerate(metrics):
        with columns[i % cols]:
            kpi_card(
                label=m["label"],
                value=m["value"],
                delta=m.get("delta"),
                delta_color=m.get("delta_color", "normal"),
                help_text=m.get("help")
            )


def info_banner(message: str, type: str = "info", 
                action: str = None, dismissible: bool = True) -> None:
    """Renderiza banner de informação/alerta estilizado."""
    theme = get_theme()
    
    type_config = {
        "info": {"bg": theme.premium_tokens.get('info_light', '#DCE8EC'), 
                 "border": theme.premium_tokens.get('info', '#5C8A9F'),
                 "icon": "ℹ️"},
        "success": {"bg": theme.premium_tokens.get('success_light', '#D4E9DF'), 
                    "border": theme.premium_tokens.get('success', '#3D7A5F'),
                    "icon": "✅"},
        "warning": {"bg": theme.premium_tokens.get('warning_light', '#F5EDCC'), 
                    "border": theme.premium_tokens.get('warning', '#D4A017'),
                    "icon": "⚠️"},
        "error": {"bg": theme.premium_tokens.get('error_light', '#F5DCD8'), 
                  "border": theme.premium_tokens.get('error', '#C45C4A'),
                  "icon": "🚨"},
    }
    
    config = type_config.get(type, type_config["info"])
    
    dismiss_btn = ""
    if dismissible:
        dismiss_btn = '<button onclick="this.parentElement.style.display=\'none\'" style="background:none;border:none;font-size:1.2rem;cursor:pointer;color:inherit;">✕</button>'
    
    st.markdown(f"""
    <div style="
        background: {config['bg']};
        border-left: 4px solid {config['border']};
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        animation: slideDown 300ms ease;
    ">
        <span style="font-size: 1.25rem;">{config['icon']}</span>
        <div style="flex: 1;">
            <strong>{message}</strong>
        </div>
        {dismiss_btn}
    </div>
    <style>
    @keyframes slideDown {{
        from {{ opacity: 0; transform: translateY(-10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    </style>
    """, unsafe_allow_html=True)


def chart_container(fig, title: str = "", height: int = 400) -> None:
    """Wrapper para gráfico com container estilizado."""
    theme = get_theme()
    
    if title:
        st.markdown(f"""
        <h3 style="color: {theme.text}; font-weight: 600; margin-bottom: 0.5rem;">{title}</h3>
        """, unsafe_allow_html=True)
    
    st.plotly_chart(fig, width="stretch", config={'displayModeBar': False})


def filter_panel(filters: Dict[str, List], key_prefix: str = "") -> Dict[str, List]:
    """Painel de filtros colapsável."""
    from src.data_processor import prepare_filter_options
    from src.utils import get_theme
    
    theme = get_theme()
    
    with st.expander("🔍 Filtros", expanded=True):
        # O filter_sidebar do utils.py já renderiza os filtros
        # Aqui apenas chamamos a versão original
        from src.utils import filter_sidebar
        return filter_panel_original(key_prefix)


def download_section(df: pd.DataFrame, filename: str = "dados.csv", 
                     label: str = "📥 Baixar CSV") -> None:
    """Seção de download com botão estilizado."""
    theme = get_theme()
    
    csv = df.to_csv(index=False, sep=";", encoding="utf-8-sig")
    
    st.download_button(
        label=label,
        data=csv.encode("utf-8-sig"),
        file_name=filename,
        mime="text/csv",
        width="stretch"
    )


def empty_state(message: str = "Nenhum dado encontrado", icon: str = "📭") -> None:
    """Estado vazio amigável."""
    theme = get_theme()
    
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 3rem 1rem;
        color: {theme.muted};
    ">
        <div style="font-size: 3rem; margin-bottom: 1rem;">{icon}</div>
        <div style="font-size: 1.125rem; font-weight: 500;">{message}</div>
    </div>
    """, unsafe_allow_html=True)


def section_header(title: str, subtitle: str = "", icon: str = "") -> None:
    """Header de seção estilizado."""
    theme = get_theme()
    
    icon_html = f"<span style='margin-right: 0.5rem;'>{icon}</span>" if icon else ""
    
    st.markdown(f"""
    <div style="margin-bottom: 1rem;">
        <h2 style="
            color: {theme.text};
            font-weight: 600;
            font-size: 1.5rem;
            margin: 0;
            display: flex;
            align-items: center;
        ">{icon_html}{title}</h2>
        {f'<p style="color: {theme.muted}; margin: 0.25rem 0 0 0; font-size: 1rem;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def responsive_columns(ratios: List[int]) -> List:
    """Cria colunas responsivas."""
    return st.columns(ratios)


def period_caption(periods: List[str]) -> None:
    """Legenda do período filtrado."""
    theme = get_theme()
    
    if periods:
        periodo_str = " → ".join(periods)
        st.markdown(f"""
        <div style="
            color: {theme.muted};
            font-size: 0.875rem;
            padding: 0.5rem 0;
            border-bottom: 1px solid {theme.border};
            margin-bottom: 1rem;
        ">
            📅 Período: {periodo_str}
        </div>
        """, unsafe_allow_html=True)


# Função original de filter_sidebar para compatibilidade
def filter_panel_original(key_prefix: str = "") -> Dict[str, List]:
    from src.utils import filter_sidebar
    from src.data_loader import load_unified
    
    # Precisamos carregar dados para obter opções
    # Isso será chamado no contexto onde df já está disponível
    pass