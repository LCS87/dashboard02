"""
Módulo de Comparação Temporal para Dashboard B2B Churn.
Permite comparar dois períodos lado a lado.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import Tuple, Dict, List, Optional
from src.theme import get_theme


class TemporalComparator:
    """Compara dois períodos temporais lado a lado."""
    
    def __init__(self):
        if 'comparison_enabled' not in st.session_state:
            st.session_state.comparison_enabled = False
        if 'period_a' not in st.session_state:
            st.session_state.period_a = None
        if 'period_b' not in st.session_state:
            st.session_state.period_b = None
    
    @property
    def enabled(self) -> bool:
        return st.session_state.comparison_enabled
    
    def render_comparison_panel(self, available_periods: List[str]) -> bool:
        """Renderiza painel de seleção de períodos para comparação."""
        if not available_periods or len(available_periods) < 2:
            st.info("📅 Mínimo 2 períodos necessários para comparação")
            return False
        
        theme = get_theme()
        
        st.markdown("### 🔄 Comparação Temporal")
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            period_a = st.selectbox(
                "Período A (Base)",
                options=available_periods,
                index=0,
                key="comp_period_a"
            )
        
        with col2:
            period_b = st.selectbox(
                "Período B (Comparação)",
                options=available_periods,
                index=min(1, len(available_periods) - 1),
                key="comp_period_b"
            )
        
        with col3:
            enabled = st.checkbox(
                "Ativar", 
                value=st.session_state.comparison_enabled,
                key="comp_enabled"
            )
        
        if enabled and period_a != period_b:
            st.session_state.comparison_enabled = True
            st.session_state.period_a = period_a
            st.session_state.period_b = period_b
        else:
            st.session_state.comparison_enabled = False
        
        return st.session_state.comparison_enabled
    
    def split_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Divide DataFrame em dois períodos selecionados."""
        if not self.enabled:
            return df, pd.DataFrame()
        
        df_a = df[df['MES_ANO'] == st.session_state.period_a].copy()
        df_b = df[df['MES_ANO'] == st.session_state.period_b].copy()
        
        return df_a, df_b
    
    def calculate_delta(self, kpis_a: Dict, kpis_b: Dict) -> Dict:
        """Calcula deltas entre dois conjuntos de KPIs."""
        delta = {}
        
        for key in kpis_a.keys():
            if isinstance(kpis_a[key], (int, float)) and isinstance(kpis_b.get(key), (int, float)):
                val_a = kpis_a[key]
                val_b = kpis_b[key]
                
                delta[f"{key}_a"] = val_a
                delta[f"{key}_b"] = val_b
                delta[f"{key}_abs"] = val_b - val_a
                delta[f"{key}_pct"] = ((val_b - val_a) / val_a * 100) if val_a != 0 else 0
        
        return delta
    
    def render_side_by_side_kpis(self, kpis_a: Dict, kpis_b: Dict, delta: Dict) -> None:
        """Renderiza KPIs lado a lado com deltas."""
        period_a = st.session_state.period_a
        period_b = st.session_state.period_b
        theme = get_theme()
        
        st.markdown(f"#### {period_a} vs {period_b}")
        
        # KPIs principais para comparação
        kpi_items = [
            ("Total Churn", "total", "total"),
            ("Voluntário", "voluntario", "voluntario"),
            ("Involuntário", "involuntario", "involuntario"),
            ("% Voluntário", "pct_voluntario", "pct_voluntario"),
            ("RV = SIM", "rv_sim", "rv_sim"),
            ("Tempo Médio (dias)", "tempo_medio", "tempo_medio"),
        ]
        
        cols = st.columns(len(kpi_items))
        
        for i, (label, key_a, key_delta) in enumerate(kpi_items):
            with cols[i]:
                val_a = kpis_a.get(key_a, 0)
                val_b = kpis_b.get(key_a, 0)
                delta_abs = delta.get(f"{key_delta}_abs", 0)
                delta_pct = delta.get(f"{key_delta}_pct", 0)
                
                # Formatação
                if "pct" in key_delta or "Tempo" in label:
                    fmt_a = f"{val_a:.1f}" if isinstance(val_a, float) else f"{val_a:,}"
                    fmt_b = f"{val_b:.1f}" if isinstance(val_b, float) else f"{val_b:,}"
                    delta_fmt = f"{delta_abs:+.1f}" if isinstance(delta_abs, float) else f"{delta_abs:+,}"
                else:
                    fmt_a = f"{val_a:,}"
                    fmt_b = f"{val_b:,}"
                    delta_fmt = f"{delta_abs:+,}"
                
                st.metric(
                    label=f"{label} - {period_b}",
                    value=fmt_b,
                    delta=f"{delta_fmt} ({delta_pct:+.1f}%)",
                    delta_color="inverse" if key_delta in ["total", "voluntario", "involuntario"] else "normal"
                )
    
    def render_comparison_charts(self, df_a: pd.DataFrame, df_b: pd.DataFrame) -> None:
        """Renderiza gráficos comparativos."""
        if df_a.empty or df_b.empty:
            st.warning("Dados insuficientes para um dos períodos")
            return
        
        period_a = st.session_state.period_a
        period_b = st.session_state.period_b
        
        # Comparação por categoria de plano
        from src.metrics import calculate_churn_by_dimension
        from src.charts import bar_churn_by_dim
        
        st.markdown("##### Churn por Categoria de Plano")
        
        plano_a = calculate_churn_by_dimension(df_a, "PLANO_CATEGORIA", 10)
        plano_b = calculate_churn_by_dimension(df_b, "PLANO_CATEGORIA", 10)
        
        # Merge para gráfico lado a lado
        if not plano_a.empty and not plano_b.empty:
            merged = plano_a[["PLANO_CATEGORIA", "TOTAL"]].merge(
                plano_b[["PLANO_CATEGORIA", "TOTAL"]],
                on="PLANO_CATEGORIA",
                how="outer",
                suffixes=(f"_{period_a}", f"_{period_b}")
            ).fillna(0)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name=period_a,
                x=merged["PLANO_CATEGORIA"],
                y=merged[f"TOTAL_{period_a}"],
                marker_color="#C46A2B"
            ))
            fig.add_trace(go.Bar(
                name=period_b,
                x=merged["PLANO_CATEGORIA"],
                y=merged[f"TOTAL_{period_b}"],
                marker_color="#3F6F5C"
            ))
            
            fig.update_layout(
                barmode="group",
                title="Churn por Categoria de Plano",
                height=350,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, width="stretch")
        
        # Comparação Voluntário vs Involuntário
        st.markdown("##### Voluntário vs Involuntário")
        
        tipo_a = calculate_churn_by_dimension(df_a, "DESCLASSIFICACAOBAIXA", 10)
        tipo_b = calculate_churn_by_dimension(df_b, "DESCLASSIFICACAOBAIXA", 10)
        
        if not tipo_a.empty and not tipo_b.empty:
            merged_tipo = tipo_a[["DESCLASSIFICACAOBAIXA", "TOTAL"]].merge(
                tipo_b[["DESCLASSIFICACAOBAIXA", "TOTAL"]],
                on="DESCLASSIFICACAOBAIXA",
                how="outer",
                suffixes=(f"_{period_a}", f"_{period_b}")
            ).fillna(0)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name=period_a,
                x=merged_tipo["DESCLASSIFICACAOBAIXA"],
                y=merged_tipo[f"TOTAL_{period_a}"],
                marker_color="#C46A2B"
            ))
            fig.add_trace(go.Bar(
                name=period_b,
                x=merged_tipo["DESCLASSIFICACAOBAIXA"],
                y=merged_tipo[f"TOTAL_{period_b}"],
                marker_color="#3F6F5C"
            ))
            
            fig.update_layout(
                barmode="group",
                title="Churn Voluntário vs Involuntário",
                height=300,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, width="stretch")
    
    def render_delta_summary(self, delta: Dict) -> None:
        """Renderiza resumo das variações."""
        theme = get_theme()
        
        # Principais deltas
        key_deltas = [
            ("total", "Total Churn"),
            ("voluntario", "Voluntário"),
            ("involuntario", "Involuntário"),
            ("pct_voluntario", "% Voluntário"),
            ("tempo_medio", "Tempo Médio"),
        ]
        
        st.markdown("##### 📊 Resumo das Variações")
        
        cols = st.columns(len(key_deltas))
        
        for i, (key, label) in enumerate(key_deltas):
            with cols[i]:
                abs_change = delta.get(f"{key}_abs", 0)
                pct_change = delta.get(f"{key}_pct", 0)
                
                if abs_change == 0 and pct_change == 0:
                    color = theme.premium_tokens.get('text_muted', '#7A8882')
                    trend = "→ Estável"
                elif abs_change > 0:
                    color = theme.premium_tokens.get('error', '#C45C4A')
                    trend = f"↑ +{abs_change:,.0f} ({pct_change:+.1f}%)"
                else:
                    color = theme.premium_tokens.get('success', '#3D7A5F')
                    trend = f"↓ {abs_change:,.0f} ({pct_change:+.1f}%)"
                
                st.markdown(f"""
                <div style="
                    padding: 0.75rem;
                    border-radius: 8px;
                    background: {theme.premium_tokens.get('surface', '#FFFFFF')};
                    border: 1px solid {theme.premium_tokens.get('border', '#D0DAD4')};
                    text-align: center;
                ">
                    <div style="font-size: 0.75rem; color: {theme.premium_tokens.get('text_secondary', '#4A5952')}; font-weight: 500;">{label}</div>
                    <div style="font-size: 1rem; font-weight: 600; color: {color};">{trend}</div>
                </div>
                """, unsafe_allow_html=True)


def create_comparator() -> TemporalComparator:
    return TemporalComparator()