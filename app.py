"""
Dashboard B2B Churn - Aplicação Principal Streamlit.
Tema: Floresta & Cobre Premium (Light/Dark) com Sidebar Recolhível, Alertas, Comparação Temporal, Exportação PDF.
"""
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuração da página (DEVE SER A PRIMEIRA COISA)
st.set_page_config(
    page_title="Dashboard B2B Churn - Telecomunicações S/A",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Imports locais
from src.data_loader import load_unified, incremental_update
from src.data_processor import apply_filters, add_cohort_features, add_dealer_performance
from src.utils import (
    load_data_cached, filter_sidebar, page_header, metric_row, 
    info_box, empty_state, download_button, format_number, format_pct,
    init_theme, theme_toggle_sidebar, get_theme
)
from src.metrics import (
    calculate_overall_kpis, calculate_monthly_trend, calculate_churn_by_dimension,
    calculate_uf_metrics, calculate_motivo_breakdown, calculate_plano_motivo_heatmap,
    calculate_faixa_tempo_distribution, calculate_porte_categoria_cross,
    calculate_dealer_ranking, calculate_cohort_retention,
    calculate_top_clientes_churn
)
import plotly.graph_objects as go
from src.charts import (
    line_churn_trend, donut_voluntario_involuntario, bar_churn_by_dim,
    map_uf_churn, funnel_churn, stacked_bar_composition,
    treemap_motivo_hierarchy, heatmap_plano_motivo, box_tempo_by_categoria,
    bar_faixa_tempo, bar_porte_categoria_stacked, table_dealer_ranking,
    cohort_heatmap, bar_comparativo_mensal, scatter_tempo_vida_rv,
    bar_motivo_breakdown, stacked_bar_composition
)

# Novos módulos premium
from src.sidebar_manager import SidebarManager
from src.alerts import AlertSystem
from src.comparator import TemporalComparator
from src.export_pdf import export_to_pdf, render_pdf_export_button
from src.theme import get_theme


@st.cache_data(ttl=3600, show_spinner="Carregando e processando dados...")
def get_processed_data() -> pd.DataFrame:
    """Carrega e enriquece dados com cache."""
    df = load_unified(anonymize=True)  # Anonimização ativada
    df = add_cohort_features(df)
    df = add_dealer_performance(df)
    return df


def main():
    # Inicializa tema premium (injeta CSS)
    init_theme()
    
    # Inicializa gerenciadores
    sidebar_mgr = SidebarManager()
    alert_system = AlertSystem()
    comparator = TemporalComparator()
    
    # Injeta overlay da sidebar para mobile
    st.markdown("""
    <div class="sidebar-overlay" id="sidebar-overlay"></div>
    <script>
    // Toggle sidebar overlay no mobile
    document.addEventListener('DOMContentLoaded', function() {
        const overlay = document.getElementById('sidebar-overlay');
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        const toggleBtn = document.querySelector('button[key="sidebar_toggle_btn"]');
        
        function closeSidebar() {
            sidebar.classList.remove('expanded');
            sidebar.removeAttribute('aria-expanded');
            sidebar.removeAttribute('data-open');
            overlay.classList.remove('visible');
        }
        
        function openSidebar() {
            sidebar.classList.add('expanded');
            sidebar.setAttribute('aria-expanded', 'true');
            sidebar.setAttribute('data-open', 'true');
            overlay.classList.add('visible');
        }
        
        function toggleSidebar() {
            if (sidebar.classList.contains('expanded') || sidebar.hasAttribute('aria-expanded')) {
                closeSidebar();
            } else {
                openSidebar();
            }
        }
        
        // Click no overlay fecha sidebar
        if (overlay) {
            overlay.addEventListener('click', closeSidebar);
        }
        
        // Click no botão toggle
        if (toggleBtn) {
            toggleBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                toggleSidebar();
            });
        }
        
        // Fechar sidebar ao clicar em link/item dentro dela (mobile)
        if (sidebar) {
            sidebar.addEventListener('click', function(e) {
                if (window.innerWidth <= 768 && e.target.closest('a, button, .stSelectbox, .stMultiSelect, .stButton')) {
                    setTimeout(closeSidebar, 100);
                }
            });
        }
        
        // Fechar sidebar ao redimensionar para desktop
        window.addEventListener('resize', function() {
            if (window.innerWidth > 768) {
                closeSidebar();
            }
        });
    });
    </script>
    """, unsafe_allow_html=True)
    
    # Inicializa tema premium (injeta CSS)
    init_theme()
    
    # Inicializa gerenciadores
    sidebar_mgr = SidebarManager()
    alert_system = AlertSystem()
    comparator = TemporalComparator()
    
    # Renderiza sidebar com gerenciador
    def render_sidebar_content():
        st.markdown("## 📊 Dashboard B2B Churn")
        st.markdown("---")
        
        # Botão de refresh
        if st.button("🔄 Recarregar Dados", width="stretch"):
            st.cache_data.clear()
            st.rerun()
        
        # Info de atualização
        st.caption("Dados: Abril a Junho 2026")
        st.caption("Fonte: CSVs mensais + consolidado")
        st.caption("🔒 Dados anonimizados automaticamente")
        
        st.markdown("---")
        
        # Toggle de tema
        theme_toggle_sidebar()
        
        st.markdown("---")
        
        # Configuração de Alertas
        with st.expander("⚙️ Configurar Alertas", expanded=False):
            alert_system.configure_alerts()
        
        st.markdown("---")
        
        # Comparação Temporal
        with st.expander("🔄 Comparação Temporal", expanded=False):
            available_periods = sorted(st.session_state.get('df_all', pd.DataFrame())["MES_ANO"].dropna().unique()) if 'df_all' in st.session_state else []
            comparator.render_comparison_panel(available_periods)
        
        st.markdown("---")
        
        # Exportação PDF
        with st.expander("📄 Exportar Relatório", expanded=False):
            render_pdf_export_button(
                st.session_state.get('df_filtered', pd.DataFrame()),
                st.session_state.get('kpis', {}),
                st.session_state.get('charts', {}),
                periodo=st.session_state.get('periodo_str', '')
            )
        
        st.markdown("---")
        
        # Upload de novo CSV (incremental)
        with st.expander("📤 Adicionar Novo Mês"):
            uploaded = st.file_uploader(
                "Selecione CSV mensal",
                type=["csv"],
                help="Arquivo com mesmo formato de junho/maio"
            )
            if uploaded:
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
                    tmp.write(uploaded.getvalue())
                    tmp_path = tmp.name
                try:
                    from pathlib import Path
                    incremental_update(Path(tmp_path))
                    st.success("✅ Dados atualizados!")
                    st.cache_data.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro: {e}")
        
    # Renderiza sidebar com gerenciador
    sidebar_mgr.render_sidebar(render_sidebar_content)
    
    # Carrega dados
    try:
        df = get_processed_data()
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        st.stop()
    
    if df.empty:
        empty_state("Nenhum dado carregado. Verifique os arquivos CSV na pasta data/raw/")
        st.stop()
    
    # Armazena df completo para comparação temporal
    st.session_state['df_all'] = df
    
    # Filtros globais na sidebar (renderizados dentro do sidebar_mgr)
    # Precisamos renderizar filtros aqui fora do sidebar_mgr pois precisam do df
    with st.sidebar:
        if not sidebar_mgr.is_collapsed:
            st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
            filters = filter_sidebar(df, key_prefix="global")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            filters = {}
    
    # Aplica filtros
    df_filtered = apply_filters(df, filters)
    
    # Armazena para uso em outros componentes
    st.session_state['df_filtered'] = df_filtered
    
    # Indicador de filtros ativos
    if filters:
        active_filters = ", ".join([f"{k}: {len(v) if isinstance(v, list) else 1}" for k, v in filters.items()])
        info_box(f"Filtros ativos: {active_filters}", "info")
    
    # Caption dinâmico do período
    theme = get_theme()
    meses_ativos = sorted(df_filtered["MES_ANO"].dropna().unique()) if not df_filtered.empty else []
    periodo_str = " → ".join(meses_ativos) if meses_ativos else ""
    if periodo_str:
        st.session_state['periodo_str'] = periodo_str
        st.caption(f"📅 Período filtrado: {periodo_str} | {len(df_filtered):,} registros")
    
    # KPIs principais
    kpis = calculate_overall_kpis(df_filtered)
    st.session_state['kpis'] = kpis
    
    # Avalia alertas
    trend = calculate_monthly_trend(df_filtered)
    alerts = alert_system.evaluate_alerts(kpis, trend)
    alert_system.render_alert_banner()
    
    # Comparação temporal
    comparison_enabled = comparator.enabled
    df_a, df_b = pd.DataFrame(), pd.DataFrame()
    kpis_a, kpis_b, delta = {}, {}, {}
    
    if comparison_enabled:
        df_a, df_b = comparator.split_data(df_filtered)
        if not df_a.empty and not df_b.empty:
            kpis_a = calculate_overall_kpis(df_a)
            kpis_b = calculate_overall_kpis(df_b)
            delta = comparator.calculate_delta(kpis_a, kpis_b)
            comparator.render_side_by_side_kpis(kpis_a, kpis_b, delta)
            st.markdown("---")
    
    # Armazena para exportação
    st.session_state['charts'] = {
        "Evolução Mensal": line_churn_trend(calculate_monthly_trend(df_filtered), "Evolução Mensal do Churn"),
        "Voluntário vs Involuntário": donut_voluntario_involuntario(df_filtered, "Voluntário vs Involuntário"),
        "Top 10 Planos": bar_churn_by_dim(calculate_churn_by_dimension(df_filtered, "PLANO", 10), "PLANO", "Top 10 Planos"),
        "Top 10 UFs": bar_churn_by_dim(calculate_uf_metrics(df_filtered).head(10), "UF", "Top 10 UFs", horizontal=True),
        "Top 10 Motivos": bar_motivo_breakdown(calculate_motivo_breakdown(df_filtered, 10), "Top 10 Motivos"),
        "Heatmap Plano x Motivo": heatmap_plano_motivo(calculate_plano_motivo_heatmap(df_filtered)),
        "Faixa de Tempo": bar_faixa_tempo(calculate_faixa_tempo_distribution(df_filtered)),
        "Cohort": cohort_heatmap(calculate_cohort_retention(df_filtered).tail(12), show_rate=False),
    }
    
    # KPIs principais no topo
    mom_delta = f"{kpis.get('mom_change_pct', 0):.1f}%" if kpis.get('mom_change_pct') is not None else None
    
    metric_row([
        {"label": "Total Churn", "value": format_number(kpis["total"]), 
         "delta": f"{kpis.get('mom_change_pct', 0):.1f}%" if kpis.get('mom_change_pct') is not None else None, "delta_color": "normal"},
        {"label": "Voluntário", "value": format_number(kpis["voluntario"]), 
         "delta": f"{kpis['pct_voluntario']}%", "delta_color": "normal"},
        {"label": "Involuntário", "value": format_number(kpis["involuntario"]), 
         "delta": f"{kpis['pct_involuntario']}%", "delta_color": "inverse"},
        {"label": "RV = SIM", "value": format_number(kpis["rv_sim"]), 
         "delta": f"{kpis['pct_rv']}%", "delta_color": "normal"},
    ])
    
    metric_row([
        {"label": "Churn Precoce (≤90d)", "value": f"{kpis['pct_precoce_90']}%", 
         "delta": f"≤30d: {kpis['pct_precoce_30']}%", "delta_color": "inverse"},
        {"label": "Top 5 Dealers", "value": f"{kpis['concentracao_top5_dealers']}%", 
         "delta": "Concentração", "delta_color": "off"},
        {"label": "Top 3 Motivos", "value": f"{kpis['concentracao_top3_motivos']}%", 
         "delta": "Concentração", "delta_color": "off"},
        {"label": "Média vs Mediana", "value": f"{kpis['gap_media_mediana']:.0f}d gap", 
         "delta": f"Média {kpis['tempo_medio']:.0f}d", "delta_color": "off"},
    ])
    
    # Comparação temporal KPIs
    if comparison_enabled and delta:
        comparator.render_side_by_side_kpis(kpis_a, kpis_b, delta)
        st.markdown("---")
    
    st.markdown("---")
    
    # Navegação por abas
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Visão Executiva", 
        "🔍 Análise de Causas", 
        "👥 Performance Equipes", 
        "📈 Tendências & Cohort"
    ])
    
    with tab1:
        render_executive_view(df_filtered)
    
    with tab2:
        render_causes_analysis(df_filtered)
    
    with tab3:
        render_team_performance(df_filtered)
    
    with tab4:
        render_trends_cohort(df_filtered)


def render_executive_view(df: pd.DataFrame):
    """Página 1: Visão Executiva (gráficos clicáveis filtram os painéis abaixo)."""
    from src.comparator import TemporalComparator
    from src.utils import clickable_chart, apply_click_filter
    
    page_header("Visão Executiva", "KPIs gerais, tendências, composição e top clientes")
    
    if df.empty:
        empty_state()
        return
    
    # Linha 1: Tendência (clicável — mês selecionado filtra os painéis abaixo)
    st.markdown("### 📈 Evolução Temporal")
    trend = calculate_monthly_trend(df)
    click_mes = clickable_chart(
        line_churn_trend(trend, "Evolução Mensal do Churn"), "exec_trend",
        hint="💡 Clique em um ponto/mês para filtrar os painéis abaixo (clique de novo para limpar).",
    )
    df_mes = apply_click_filter(df, "MES_ANO", click_mes)
    
    # Linha 2: Composição + Top Planos
    st.markdown("### 🎯 Composição e Concentração")
    col1, col2 = st.columns([2, 3])
    
    with col1:
        click_classe = clickable_chart(
            donut_voluntario_involuntario(df_mes, "Voluntário vs Involuntário"), "exec_donut"
        )
        df_c1 = apply_click_filter(df_mes, "DESCLASSIFICACAOBAIXA", click_classe)
    
    with col2:
        top_planos = calculate_churn_by_dimension(df_c1, "PLANO", 10)
        click_plano = clickable_chart(
            bar_churn_by_dim(top_planos, "PLANO", "Top 10 Planos com Mais Churn"), "exec_planos"
        )
        df_c2 = apply_click_filter(df_c1, "PLANO", click_plano)
    
    # Linha 3: Composição RV + Top UFs
    col3, col4 = st.columns([2, 3])
    
    with col3:
        fig = stacked_bar_composition(df_c2, "Composição: Vol/Invol × RV")
        st.plotly_chart(fig, width="stretch")
    
    with col4:
        uf_data = calculate_uf_metrics(df_c2).head(10)
        click_uf = clickable_chart(
            bar_churn_by_dim(uf_data, "UF", "Top 10 UFs por Churn", horizontal=True), "exec_uf"
        )
        df_c3 = apply_click_filter(df_c2, "UF", click_uf)
    
    # Linha 4: Mapa UF (largura total para melhor visualização geográfica)
    st.markdown("### 🗺️ Distribuição Geográfica")
    try:
        fig = map_uf_churn(df_c3)
        st.plotly_chart(fig, width="stretch")
    except Exception:
        info_box("Mapa indisponível - exibindo barras por UF", "warning")
        uf_data = calculate_uf_metrics(df_c3).head(15)
        fig = bar_churn_by_dim(uf_data, "UF", "Churn por UF", horizontal=True)
        st.plotly_chart(fig, width="stretch")
    
    # Top Clientes
    st.markdown("### 🏆 Top Clientes com Mais Churn")
    top_clientes = calculate_top_clientes_churn(df_c3, 10)
    if not top_clientes.empty:
        display_cols = ["CLIENTE", "UF", "DEALER", "QTD_LINHAS", "TOTAL_CHURN", "PLANOS", "MOTIVOS", "PRIMEIRA_BAIXA", "ULTIMA_BAIXA"]
        display_df = top_clientes[display_cols].copy()
        display_df.columns = ["Cliente", "UF", "Dealer", "Qtd Linhas", "Total Churn", "Planos", "Motivos", "1ª Baixa", "Última Baixa"]
        from src.utils import dataframe_with_config
        dataframe_with_config(display_df, height=350)
    
    # Comparação temporal charts
    comparator = TemporalComparator()
    if comparator.enabled:
        st.markdown("---")
        st.markdown("### 🔄 Comparação Temporal: Gráficos")
        comparator.render_comparison_charts(
            st.session_state['df_all'][st.session_state['df_all']['MES_ANO'] == st.session_state.period_a],
            st.session_state['df_all'][st.session_state['df_all']['MES_ANO'] == st.session_state.period_b]
        )
        comparator.render_delta_summary(
            comparator.calculate_delta(
                calculate_overall_kpis(st.session_state['df_all'][st.session_state['df_all']['MES_ANO'] == st.session_state.period_a]),
                calculate_overall_kpis(st.session_state['df_all'][st.session_state['df_all']['MES_ANO'] == st.session_state.period_b])
            )
        )
    
    # Exportação — sempre visível (sem expander colapsável)
    from src.utils import export_section
    export_section(df_c3, "churn_filtrado_executivo.csv", title="Exportação — Dados Executivos")


def render_causes_analysis(df: pd.DataFrame):
    """Página 2: Análise de Causas."""
    page_header("Análise de Causas", "Motivos de churn, planos, tempo de vida e categorias")
    
    if df.empty:
        empty_state()
        return
    
    # Linha 1: Distribuição de Motivos (treemap clicável — filtra os painéis abaixo)
    st.markdown("### 🔍 Distribuição de Motivos")
    from src.utils import clickable_chart, apply_click_filter, export_section
    
    val_tree = clickable_chart(
        treemap_motivo_hierarchy(df), "causas_tree",
        hint="💡 Clique em um bloco (motivo ou classificação) para filtrar os painéis abaixo (clique de novo para limpar).",
    )
    dim_tree = None
    if val_tree:
        motivos_set = set(df["MOTIVO_BAIXA"].astype(str))
        desclass_set = set(df["DESCLASSIFICACAOBAIXA"].astype(str))
        if val_tree in motivos_set:
            dim_tree = "MOTIVO_BAIXA"
        elif val_tree in desclass_set:
            dim_tree = "DESCLASSIFICACAOBAIXA"
    df1 = apply_click_filter(df, dim_tree, val_tree)
    
    # Top Motivos (clicável — refina o filtro por motivo)
    motivos = calculate_motivo_breakdown(df1, 15)
    click_motivo = clickable_chart(bar_motivo_breakdown(motivos), "causas_motivos")
    df2 = apply_click_filter(df1, "MOTIVO_BAIXA", click_motivo)
    
    # Linha 2: Heatmap Plano x Motivo (largura total para legibilidade)
    st.markdown("### 🔥 Heatmap: Plano vs Motivo")
    heatmap_data = calculate_plano_motivo_heatmap(df2)
    fig = heatmap_plano_motivo(heatmap_data)
    st.plotly_chart(fig, width="stretch")
    
    # Linha 3: Faixa de tempo + Box plot
    st.markdown("### ⏱️ Análise Temporal")
    col3, col4 = st.columns([1, 1])
    
    with col3:
        faixa = calculate_faixa_tempo_distribution(df2)
        fig = bar_faixa_tempo(faixa)
        st.plotly_chart(fig, width="stretch")
    
    with col4:
        fig = box_tempo_by_categoria(df2)
        st.plotly_chart(fig, width="stretch")
    
    # Linha 4: Porte x Categoria (largura total)
    st.markdown("### 📊 Porte x Categoria de Churn")
    cross = calculate_porte_categoria_cross(df2)
    fig = bar_porte_categoria_stacked(cross)
    st.plotly_chart(fig, width="stretch")
    
    # Exportação — sempre visível, refletindo o clique-filtro atual
    export_section(
        df2, "churn_motivos_detalhado.csv",
        title="Exportação — Dados de Motivos",
        detail_df=calculate_motivo_breakdown(df2, 50),
        detail_title="Detalhamento dos motivos (até 50)",
    )


def render_team_performance(df: pd.DataFrame):
    """Página 3: Performance por Equipes."""
    page_header("Performance por Equipes", "Ranking de Dealers, Diretores e Gerentes com drill-down")
    
    if df.empty:
        empty_state()
        return
    
    # Filtro adicional para esta página
    col_f1, col_f2 = st.columns([1, 3])
    with col_f1:
        view_level = st.selectbox(
            "Nível de Visualização",
            ["Dealer", "Diretor", "Gerente Divisão"],
            key="team_view_level"
        )
    
    # Métricas por nível
    if view_level == "Dealer":
        dim = "DEALER"
        ranking = calculate_dealer_ranking(df, 20)
    elif view_level == "Diretor":
        dim = "DIRETOR"
        ranking = calculate_churn_by_dimension(df, "DIRETOR", 20)
        for col in ["GERENTE_DIVISAO", "DEALER", "TOP_MOTIVO"]:
            if col not in ranking.columns:
                ranking[col] = ""
    else:
        dim = "GERENTE_DIVISAO"
        ranking = calculate_churn_by_dimension(df, "GERENTE_DIVISAO", 20)
        for col in ["DEALER", "DIRETOR", "TOP_MOTIVO"]:
            if col not in ranking.columns:
                ranking[col] = ""
    
    # Gráfico de barras (clicável — ativa o drill-down da entidade abaixo)
    from src.utils import clickable_chart, export_section
    click_entity = clickable_chart(
        bar_churn_by_dim(ranking.head(15), dim, f"Top 15 {view_level}s por Churn", horizontal=True),
        "team_bar",
        hint="💡 Clique em uma barra para detalhar a entidade no drill-down abaixo (clique de novo para limpar).",
    )
    
    # Tabela ranking
    st.markdown(f"### 📋 Ranking Completo de {view_level}s")
    fig_table = table_dealer_ranking(ranking, f"Ranking de {view_level}s")
    st.plotly_chart(fig_table, width="stretch")
    
    # Drill-down (por clique no gráfico de ranking ou pelo seletor)
    st.markdown("---")
    st.markdown("### 🔍 Drill-down")
    
    entities = sorted(df[dim].dropna().unique())
    if click_entity:
        selected_entity = click_entity
        info_box(
            f"Drill-down ativado por clique no gráfico: <strong>{selected_entity}</strong> "
            f"— clique de novo na barra para limpar.",
            "info"
        )
    else:
        selected_entity = st.selectbox(
            f"Selecione {view_level} para detalhar",
            options=[""] + entities,
            key=f"drilldown_{dim}"
        )
    
    if selected_entity:
        df_drill = df[df[dim] == selected_entity]
        
        kpis_drill = calculate_overall_kpis(df_drill)
        metric_row([
            {"label": f"Churn {selected_entity}", "value": format_number(kpis_drill["total"])},
            {"label": "% Voluntário", "value": format_pct(kpis_drill["pct_voluntario"])},
            {"label": "% RV", "value": format_pct(kpis_drill["pct_rv"])},
            {"label": "Tempo Médio", "value": format_number(kpis_drill["tempo_medio"], 1)},
        ])
        
        # Top motivos desse entity
        motivos = calculate_motivo_breakdown(df_drill, 10)
        fig = bar_motivo_breakdown(motivos, f"Motivos - {selected_entity}")
        st.plotly_chart(fig, width="stretch")
        
        # Top planos
        planos = calculate_churn_by_dimension(df_drill, "PLANO", 10)
        fig = bar_churn_by_dim(planos, "PLANO", f"Planos - {selected_entity}")
        st.plotly_chart(fig, width="stretch")
        
        # Exportação — sempre visível
        export_section(
            df_drill, f"churn_{selected_entity}.csv",
            title="Exportação — Clientes", extra_name=str(selected_entity),
        )


def render_trends_cohort(df: pd.DataFrame):
    """Página 4: Tendências & Cohort Analysis."""
    page_header("Tendências & Cohort Analysis", "Evolução temporal, cohorts com taxa e análise preditiva simples")
    
    if df.empty:
        empty_state()
        return
    
    # Linha 1: Tendência mensal detalhada (largura total, clicável — mês filtra os painéis abaixo)
    st.markdown("### 📈 Evolução Detalhada")
    trend = calculate_monthly_trend(df)
    from src.utils import clickable_chart, apply_click_filter, export_section
    click_mes = clickable_chart(
        line_churn_trend(trend, "Evolução Mensal Detalhada"), "tend_trend",
        hint="💡 Clique em um ponto/mês para filtrar comparativos, scatter e exportação (clique de novo para limpar). A cohort pode continuar na visão geral pois usa mês de ativação.",
    )
    df_mes = apply_click_filter(df, "MES_ANO", click_mes)
    
    # Linha 2: Comparativo mensal por plano/classe
    st.markdown("### 📊 Comparativos Mensais")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig = bar_comparativo_mensal(df_mes, "PLANO_CATEGORIA", "Churn por Categoria de Plano x Mês")
        st.plotly_chart(fig, width="stretch")
    
    with col2:
        fig = bar_comparativo_mensal(df_mes, "DESCLASSIFICACAOBAIXA", "Churn Voluntário vs Involuntário x Mês")
        st.plotly_chart(fig, width="stretch")
    
    # Linha 3: Cohort Analysis
    st.markdown("### 👥 Cohort Analysis")
    st.caption("Linhas = Mês de Ativação | Colunas = Mês Relativo (M+1 = mês seguinte à ativação, etc.)")
    st.caption("⚠️ Nota: Base ativa total não disponível. Cohort size = clientes únicos com churn no mês de ativação (proxy).")
    
    cohort_counts = calculate_cohort_retention(df)
    
    if not cohort_counts.empty:
        # Filtra apenas cohorts recentes (2025+) para visualização limpa
        recent_cohorts = cohort_counts[cohort_counts.index.str.startswith(('2025', '2026'))]
        if recent_cohorts.empty:
            recent_cohorts = cohort_counts.tail(12)
        
        # Heatmap de contagem
        fig = cohort_heatmap(recent_cohorts, show_rate=False, title="Cohort - Contagem de Churn por Mês Relativo")
        st.plotly_chart(fig, width="stretch")
        
        # Gráfico de linha: evolução do churn por cohort (top 5 cohorts por volume)
        st.markdown("**Evolução do Churn por Cohort (Top 5 por volume)**")
        cohort_totals = recent_cohorts.sum(axis=1).sort_values(ascending=False)
        top_cohorts = cohort_totals.head(5).index.tolist()
        
        if top_cohorts:
            plot_data = recent_cohorts.loc[top_cohorts].T.reset_index()
            plot_data.columns = ['MES_RELATIVO'] + top_cohorts
            plot_data['MES_RELATIVO_NUM'] = plot_data['MES_RELATIVO'].str.replace('M+', '').astype(int)
            plot_data = plot_data.sort_values('MES_RELATIVO_NUM')
            
            from src.charts import get_colors, apply_layout
            
            fig = go.Figure()
            _colors = get_colors()
            for i, cohort in enumerate(top_cohorts):
                fig.add_trace(go.Scatter(
                    x=plot_data['MES_RELATIVO'], y=plot_data[cohort],
                    mode='lines+markers', name=cohort,
                    line=dict(color=_colors.color_sequence[i % len(_colors.color_sequence)], width=3),
                    marker=dict(size=9),
                    hovertemplate=f"<b>{cohort}</b><br>Mês Relativo: %{{x}}<br>Churn: %{{y:,.0f}}<extra></extra>",
                ))
            
            fig = apply_layout(
                fig, "Churn Acumulado por Cohort ao Longo do Tempo",
                height=520, margin=dict(l=70, r=60, t=80, b=70),
            )
            fig.update_layout(
                xaxis_title="Mês Relativo",
                yaxis_title="Churn Acumulado",
                yaxis=dict(rangemode="tozero", tickformat=",.0f"),
                hovermode="x unified",
            )
            st.plotly_chart(fig, width="stretch")
    else:
        info_box("Dados insuficientes para cohort analysis (precisa de múltiplos meses de ativação)", "warning")
    
    # Linha 4: Scatter Tempo x RV
    st.markdown("### 🎯 Tempo de Vida vs RV")
    fig = scatter_tempo_vida_rv(df_mes)
    st.plotly_chart(fig, width="stretch")
    
    # Previsão simples (média móvel)
    st.markdown("### 🔮 Projeção Simples (Média Móvel 3M)")
    if len(trend) >= 3:
        trend["MA3"] = trend["TOTAL"].rolling(3, min_periods=1).mean()
        next_month = trend["MA3"].iloc[-1]
        ultimos = ", ".join(format_number(v, 0) for v in trend["TOTAL"].tail(3).tolist())
        info_box(
            f"Projeção para o próximo mês: <strong>{format_number(next_month, 0)} churns</strong> — "
            f"média móvel de 3 meses (últimos valores: {ultimos})",
            "info"
        )
    
    # Exportação — sempre visível, respeitando o clique-filtro de mês
    export_section(df_mes, "churn_tendencias.csv", title="Exportação — Dados de Tendências")


# Import para usar nas páginas
from src.metrics import calculate_overall_kpis, calculate_motivo_breakdown

if __name__ == "__main__":
    main()