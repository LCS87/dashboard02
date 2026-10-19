"""
Sistema de Alertas Configuráveis para Dashboard B2B Churn.
"""
import streamlit as st
import pandas as pd
from typing import Dict, List, Any
from src.theme import get_theme


class AlertSystem:
    """Sistema de alertas configuráveis por threshold."""
    
    def __init__(self):
        # Configurações padrão
        if 'alert_config' not in st.session_state:
            st.session_state.alert_config = {
                'total_churn_max': 2500,
                'voluntario_pct_max': 75.0,
                'tempo_medio_min': 90,
                'mom_change_max': 20.0,
            }
        
        if 'active_alerts' not in st.session_state:
            st.session_state.active_alerts = []
    
    def configure_alerts(self) -> None:
        """Interface de configuração de alertas na sidebar."""
        theme = get_theme()
        
        st.markdown("### ⚙️ Configurar Alertas")
        
        config = st.session_state.alert_config
        
        col1, col2 = st.columns(2)
        
        with col1:
            config['total_churn_max'] = st.number_input(
                "Total Churn máximo",
                min_value=0,
                value=int(config['total_churn_max']),
                step=100,
                help="Alerta quando churn total ultrapassar este valor"
            )
            
            config['voluntario_pct_max'] = st.number_input(
                "% Voluntário máximo",
                min_value=0.0,
                max_value=100.0,
                value=float(config['voluntario_pct_max']),
                step=5.0,
                help="Alerta quando % voluntário ultrapassar este valor"
            )
        
        with col2:
            config['tempo_medio_min'] = st.number_input(
                "Tempo médio mínimo (dias)",
                min_value=0,
                value=int(config['tempo_medio_min']),
                step=10,
                help="Alerta quando tempo médio cair abaixo deste valor"
            )
            
            config['mom_change_max'] = st.number_input(
                "Variação MoM máxima (%)",
                min_value=0.0,
                value=float(config['mom_change_max']),
                step=5.0,
                help="Alerta quando variação mês-a-mês ultrapassar este valor"
            )
        
        # Botão para resetar configurações
        if st.button("🔄 Resetar padrões", width="stretch"):
            st.session_state.alert_config = {
                'total_churn_max': 2500,
                'voluntario_pct_max': 75.0,
                'tempo_medio_min': 90,
                'mom_change_max': 20.0,
            }
            st.rerun()
    
    def evaluate_alerts(self, kpis: Dict, trend: pd.DataFrame = None) -> List[Dict]:
        """Avalia métricas e gera alertas baseados nos thresholds configurados."""
        alerts = []
        config = st.session_state.alert_config
        
        # Alerta 1: Total Churn
        if kpis.get('total', 0) > config['total_churn_max']:
            alerts.append({
                'type': 'error',
                'title': '🚨 Churn Total Elevado',
                'message': f"Churn total ({kpis['total']:,}) acima do limite ({config['total_churn_max']:,})",
                'action': 'Investigar causas principais e comparar com período anterior'
            })
        
        # Alerta 2: % Voluntário
        if kpis.get('pct_voluntario', 0) > config['voluntario_pct_max']:
            alerts.append({
                'type': 'error',
                'title': '🚨 % Voluntário Alto',
                'message': f"Voluntário em {kpis['pct_voluntario']:.1f}% (limite: {config['voluntario_pct_max']:.1f}%)",
                'action': 'Revisar satisfação do cliente e causas de cancelamento voluntário'
            })
        
        # Alerta 3: Tempo médio
        if kpis.get('tempo_medio', 999999) < config['tempo_medio_min']:
            alerts.append({
                'type': 'warning',
                'title': '⚠️ Tempo de Vida Baixo',
                'message': f"Tempo médio ({kpis['tempo_medio']:.0f} dias) abaixo do mínimo ({config['tempo_medio_min']} dias)",
                'action': 'Analisar churn precoce (≤90 dias) e qualidade de ativação'
            })
        
        # Alerta 4: MoM Change
        if trend is not None and len(trend) >= 2:
            mom_change = trend['MOM_CHANGE_PCT'].iloc[-1]
            if pd.notna(mom_change) and abs(mom_change) > config['mom_change_max']:
                alert_type = 'error' if mom_change > 0 else 'warning'
                alerts.append({
                    'type': alert_type,
                    'title': f'{"🚨" if mom_change > 0 else "⚠️"} Variação MoM Significativa',
                    'message': f"Variação mês-a-mês de {mom_change:+.1f}% (limite: ±{config['mom_change_max']:.1f}%)",
                    'action': 'Analisar drivers da variação e comparar com sazonalidade'
                })
        
        # Alerta 5: Churn precoce
        if kpis.get('pct_precoce_90', 0) > 20:
            alerts.append({
                'type': 'warning',
                'title': '⚠️ Churn Precoce Elevado',
                'message': f"{kpis['pct_precoce_90']:.1f}% dos churns ocorrem em ≤90 dias",
                'action': 'Revisar processo de onboarding e qualidade de ativação'
            })
        
        st.session_state.active_alerts = alerts
        return alerts
    
    def render_alert_banner(self) -> None:
        """Renderiza banner de alertas ativos no topo da página."""
        alerts = st.session_state.active_alerts
        theme = get_theme()
        
        if not alerts:
            return
        
        # CSS para banner
        st.markdown(f"""
        <style>
        .alert-banner {{
            padding: 1rem 1.25rem;
            border-radius: var(--radius-lg, 12px);
            margin-bottom: 1rem;
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
            animation: slideDown 300ms cubic-bezier(0.4, 0, 0.2, 1);
            border-left: 4px solid;
        }}
        
        @keyframes slideDown {{
            from {{ opacity: 0; transform: translateY(-10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .alert-banner-error {{
            background-color: {theme.premium_tokens.get('error_light', '#F5DCD8')};
            border-left-color: {theme.premium_tokens.get('error', '#C45C4A')};
            color: {theme.premium_tokens.get('text_primary', '#1A2820')};
        }}
        
        .alert-banner-warning {{
            background-color: {theme.premium_tokens.get('warning_light', '#F5EDCC')};
            border-left-color: {theme.premium_tokens.get('warning', '#D4A017')};
            color: {theme.premium_tokens.get('text_primary', '#1A2820')};
        }}
        
        .alert-banner-info {{
            background-color: {theme.premium_tokens.get('info_light', '#DCE8EC')};
            border-left-color: {theme.premium_tokens.get('info', '#5C8A9F')};
            color: {theme.premium_tokens.get('text_primary', '#1A2820')};
        }}
        
        .alert-banner-icon {{
            font-size: 1.25rem;
            flex-shrink: 0;
            margin-top: 0.125rem;
        }}
        
        .alert-banner-content {{ flex: 1; }}
        .alert-banner-title {{
            font-weight: 600;
            font-size: 0.9375rem;
            margin-bottom: 0.25rem;
        }}
        .alert-banner-message {{
            font-size: 0.875rem;
            color: {theme.premium_tokens.get('text_secondary', '#4A5952')};
            margin-bottom: 0.5rem;
        }}
        .alert-banner-action {{
            font-size: 0.8125rem;
            color: {theme.premium_tokens.get('text_muted', '#7A8882')};
            font-style: italic;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        # Render alerts
        for alert in alerts:
            type_class = f"alert-banner-{alert['type']}"
            icon = "🚨" if alert['type'] == 'error' else "⚠️"
            
            st.markdown(f"""
            <div class="alert-banner {type_class}">
                <span class="alert-banner-icon">{icon}</span>
                <div class="alert-banner-content">
                    <div class="alert-banner-title">{alert['title']}</div>
                    <div class="alert-banner-message">{alert['message']}</div>
                    <div class="alert-banner-action">💡 {alert['action']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def get_alert_summary(self) -> Dict[str, int]:
        """Retorna resumo dos alertas por tipo."""
        alerts = st.session_state.active_alerts
        summary = {'error': 0, 'warning': 0, 'info': 0}
        for alert in alerts:
            summary[alert['type']] = summary.get(alert['type'], 0) + 1
        return summary


# Função auxiliar para uso rápido
def create_alert_system() -> AlertSystem:
    return AlertSystem()