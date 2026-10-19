Vou salvar o plano completo em um arquivo Markdown no projeto dashboard02.Vou criar o arquivo diretamente com o plano completo:

I'm a planning agent - I can read and analyze code but not modify it. I can help you plan the implementation instead.

However, I can show you the exact content that should be saved. Here's what you need to do:

**Crie manualmente um arquivo chamado:** `PLANO_MELHORIAS_PREMIUM_DASHBOARD.md`

**No caminho:** `C:\Users\lcost\Documents\Codigos\Projetos lv1\dashboard02\`

**Com o seguinte conteúdo:**

---

Devido ao tamanho do plano completo, vou estruturá-lo de forma que você possa copiar e colar. Aqui está o conteúdo completo do arquivo:

```markdown
# PLANO DE MELHORIAS PREMIUM - DASHBOARD B2B CHURN
## Telecomunicações S/A - Versão Acadêmica

**Data de Criação:** [Data Atual]  
**Versão:** 1.0  
**Status:** Pronto para Implementação

---

## 📋 SUMÁRIO EXECUTIVO

**Objetivo:** Transformar o dashboard atual em uma solução premium de nível SaaS ($30k+) com foco em:
- UI/UX de alto padrão profissional
- Visualizações animadas e interativas
- Dark mode premium com contraste otimizado
- Navegação lateral recolhível e suave
- Anonimização automática de dados sensíveis
- Funcionalidades avançadas (comparação temporal, alertas, exportação PDF)

**Contexto:** Trabalho acadêmico - dados sensíveis serão anonimizados automaticamente.

**Stack Tecnológico:**
- **Frontend:** Streamlit + Custom HTML/CSS/JavaScript
- **Visualização:** Plotly + Custom animations (CSS + GSAP light)
- **Exportação:** ReportLab / WeasyPrint para PDF
- **Persistência:** Session State (não requer backend)
- **Tema:** Floresta & Cobre (Light/Dark) - já implementado, será refinado

---

## 🎯 REQUISITOS CONSOLIDADOS

### Funcionais:
1. ✅ Navegação lateral recolhível com persistência (Session State)
2. ✅ Animações suaves (CSS + Plotly + custom onde necessário)
3. ✅ Dark mode premium com contraste WCAG AA
4. ✅ Comparação temporal (side-by-side, overlay, delta visual)
5. ✅ Alertas visuais configuráveis pelo usuário
6. ✅ Exportação PDF com layout fixo profissional
7. ✅ Responsivo (70% desktop, 30% mobile/tablet)
8. ✅ Anonimização automática de dados sensíveis
9. ✅ Dashboard individual (sem colaboração/multi-usuário)

### Não-Funcionais:
- Performance: Load time < 3s para dataset de ~10k registros
- Acessibilidade: WCAG 2.1 Level AA
- Browser support: Chrome, Firefox, Edge (últimas 2 versões)
- Mobile: Suporte básico (visualização, não edição)

---

## 🔍 ANÁLISE DO PROJETO ATUAL

### Pontos Fortes:
✅ Estrutura modular bem organizada (src/ separado)  
✅ Sistema de tema Light/Dark já implementado  
✅ Gráficos Plotly funcionais com paleta customizada  
✅ 4 páginas organizadas (Executiva, Causas, Equipes, Tendências)  
✅ Cache de dados implementado  
✅ Filtros sidebar funcionais  

### Gaps Identificados:
❌ Sidebar fixa (não colapsável)  
❌ Sem animações de entrada nos gráficos  
❌ Contraste dark mode não otimizado  
❌ Sem comparação temporal entre períodos  
❌ Sem sistema de alertas  
❌ Exportação apenas CSV (falta PDF)  
❌ Dados sensíveis expostos (CNPJ, nomes reais)  
❌ Responsividade limitada  
❌ Layout estático sem micro-interações  

---

## 🏗️ ARQUITETURA TÉCNICA

### Estrutura de Diretórios Atualizada

```
dashboard02/
├── app.py                          # Entry point
├── requirements.txt                # Dependências (atualizar)
├── README.md
├── PLANO_MELHORIAS_PREMIUM_DASHBOARD.md  # Este arquivo
├── .streamlit/
│   ├── config.toml                 # Config Streamlit
│   └── secrets.toml                # (novo) Secrets para configs sensíveis
├── data/
│   ├── raw/                        # CSVs originais
│   ├── processed/                  # Parquets
│   └── anonymized/                 # (novo) Dados anonimizados
├── exports/                        # (novo) PDFs gerados
├── assets/                         # (novo) Assets estáticos
│   ├── css/
│   │   ├── premium-theme.css       # CSS premium customizado
│   │   ├── animations.css          # Animações
│   │   └── responsive.css          # Media queries
│   ├── js/
│   │   ├── sidebar-toggle.js       # Controle sidebar
│   │   ├── animations.js           # GSAP animations
│   │   └── alerts.js               # Sistema de alertas
│   ├── fonts/                      # Inter, JetBrains Mono
│   └── icons/                      # SVG icons customizados
├── src/
│   ├── __init__.py
│   ├── config.py                   # Configs centrais (atualizar)
│   ├── theme.py                    # Sistema de tema (refinar)
│   ├── data_loader.py
│   ├── data_processor.py           # (atualizar) + anonimização
│   ├── anonymizer.py               # (novo) Módulo de anonimização
│   ├── metrics.py
│   ├── charts.py                   # (refinar) + animações
│   ├── utils.py                    # (expandir)
│   ├── alerts.py                   # (novo) Sistema de alertas
│   ├── comparator.py               # (novo) Comparação temporal
│   ├── export_pdf.py               # (novo) Geração de PDF
│   ├── sidebar_manager.py          # (novo) Gerenciamento sidebar
│   └── components/                 # (novo) Componentes reutilizáveis
│       ├── __init__.py
│       ├── kpi_card.py             # Card KPI animado
│       ├── metric_row.py           # Linha de métricas
│       ├── chart_container.py      # Container de gráfico
│       ├── filter_panel.py         # Painel de filtros
│       ├── alert_banner.py         # Banner de alerta
│       └── comparison_panel.py     # Painel de comparação
└── tests/                          # (novo) Testes unitários
    ├── test_anonymizer.py
    ├── test_alerts.py
    └── test_export.py
```

### Dependências Atualizadas (requirements.txt)

```txt
# Core
streamlit>=1.35.0
plotly>=5.22.0
pandas>=2.2.0
numpy>=1.26.0

# Exportação PDF
reportlab>=4.0.0
weasyprint>=60.0
Pillow>=10.0.0

# Anonimização
faker>=24.0.0

# Utilitários
python-dateutil>=2.8.0
pytz>=2024.1
openpyxl>=3.1.0

# Dev/Test (opcional)
pytest>=8.0.0
pytest-cov>=4.1.0
black>=24.0.0
```

---

## 📋 TASK BREAKDOWN - PLANO DE IMPLEMENTAÇÃO

### FASE 1: FUNDAÇÃO (PREPARAÇÃO)

#### **Task 1: Setup de Estrutura e Dependências**
- **Objetivo:** Preparar ambiente e estrutura de pastas
- **Ações:**
  - Criar pastas: `assets/`, `assets/css/`, `assets/js/`, `src/components/`, `exports/`, `tests/`
  - Atualizar `requirements.txt` com novas dependências
  - Instalar e testar dependências (reportlab, weasyprint, faker)
  - Criar arquivo `.streamlit/secrets.toml` (vazio por enquanto)
- **Testes:** Importar todas as bibliotecas sem erros
- **Demo:** Estrutura de pastas criada, dependências instaladas

---

#### **Task 2: Sistema de Anonimização Automática**
- **Objetivo:** Implementar módulo de anonimização de dados sensíveis
- **Implementação Detalhada:**

```python
# src/anonymizer.py
import re
from faker import Faker
import hashlib
import pandas as pd

class DataAnonymizer:
    def __init__(self, seed=42):
        self.faker = Faker('pt_BR')
        Faker.seed(seed)
        self.name_map = {}  # Cache de nomes
        
    def mask_cnpj(self, cnpj: str) -> str:
        """Mascara CNPJ: 12.345.678/****-**"""
        if pd.isna(cnpj):
            return cnpj
        clean = re.sub(r'\D', '', str(cnpj))
        if len(clean) == 14:
            return f"{clean[:8]}/****-**"
        return cnpj
    
    def mask_cpf(self, cpf: str) -> str:
        """Mascara CPF: 123.456.***-**"""
        if pd.isna(cpf):
            return cpf
        clean = re.sub(r'\D', '', str(cpf))
        if len(clean) == 11:
            return f"{clean[:6]}.***-**"
        return cpf
    
    def anonymize_name(self, name: str) -> str:
        """Gera nome fictício consistente"""
        if not name or pd.isna(name):
            return name
        
        # Cache hit
        if name in self.name_map:
            return self.name_map[name]
        
        # Gera hash para consistência
        name_hash = int(hashlib.md5(name.encode()).hexdigest(), 16)
        Faker.seed(name_hash % (2**32))
        
        fake_name = self.faker.name()
        self.name_map[name] = fake_name
        
        return fake_name
    
    def anonymize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica anonimização ao DataFrame"""
        df = df.copy()
        
        # CNPJ
        if 'CNPJ_CLIENTE' in df.columns:
            df['CNPJ_CLIENTE'] = df['CNPJ_CLIENTE'].apply(self.mask_cnpj)
        
        # Nomes de pessoas
        for col in ['DIRETOR', 'GERENTE_DIVISAO', 'NOMEDIRETOR', 'NOMEGERENTEDIVISAO']:
            if col in df.columns:
                df[col] = df[col].apply(self.anonymize_name)
        
        # Cliente (mascarar parcialmente)
        if 'CLIENTE' in df.columns:
            df['CLIENTE'] = df['CLIENTE'].apply(
                lambda x: f"Cliente-***{str(x)[-3:]}" if x and not pd.isna(x) else x
            )
        
        # Substituir empresa
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str).str.replace(
                'Vivo', 'Telecomunicações S/A', case=False, regex=False
            )
        
        return df
```

**Integração em data_loader.py:**
```python
from src.anonymizer import DataAnonymizer

def load_unified() -> pd.DataFrame:
    df = _load_raw_data()
    
    # Anonimizar antes de retornar
    anonymizer = DataAnonymizer(seed=42)
    df = anonymizer.anonymize_dataframe(df)
    
    return df
```

- **Testes:**
  - CNPJ `12.345.678/0001-90` → `12.345.678/****-**`
  - Nome "João Silva" sempre vira o mesmo nome fictício
  - Empresa substituída em todas as ocorrências
- **Demo:** Carregar dados e verificar que estão anonimizados corretamente

---

#### **Task 3: Refinamento do Sistema de Tema (Tokens Premium)**
- **Objetivo:** Refinar paleta de cores para WCAG AA compliance e estética premium
- **Implementação:**

```python
# Atualizar src/theme.py

LIGHT_PREMIUM = {
    "bg_primary": "#E8EEE9",
    "bg_secondary": "#F4F7F5",
    "surface": "#FFFFFF",
    "text_primary": "#1A2820",
    "text_secondary": "#4A5952",
    "text_muted": "#7A8882",
    
    "primary": "#C46A2B",
    "primary_hover": "#A85623",
    "accent": "#3F6F5C",
    
    "success": "#3D7A5F",
    "warning": "#D4A017",
    "error": "#C45C4A",
    "info": "#5C8A9F",
    
    "border": "#D0DAD4",
    "hover": "#E4ECE6",
    
    "shadow_sm": "0 1px 3px rgba(36, 48, 41, 0.08)",
    "shadow_md": "0 4px 12px rgba(36, 48, 41, 0.12)",
    "shadow_lg": "0 8px 24px rgba(36, 48, 41, 0.15)",
}

DARK_PREMIUM = {
    "bg_primary": "#121B17",
    "bg_secondary": "#1A2722",
    "surface": "#243330",
    "text_primary": "#E4ECE8",
    "text_secondary": "#B5C4BA",
    "text_muted": "#8A9A92",
    
    "primary": "#E69857",
    "primary_hover": "#F0A970",
    "accent": "#6FA88A",
    
    "success": "#5FA87A",
    "warning": "#E0B84A",
    "error": "#E07A68",
    "info": "#7AA8BD",
    
    "border": "#2F3F38",
    "hover": "#2A3A34",
    
    "shadow_sm": "0 1px 3px rgba(0, 0, 0, 0.3)",
    "shadow_md": "0 4px 12px rgba(0, 0, 0, 0.4)",
    "shadow_lg": "0 8px 24px rgba(0, 0, 0, 0.5)",
}
```

- **Testes:** Verificar contraste text/background >= 4.5:1 (AA) usando https://webaim.org/resources/contrastchecker/
- **Demo:** Dashboard com paleta refinada, melhor legibilidade

---

### FASE 2: UI/UX PREMIUM

#### **Task 4: CSS Premium - Tipografia, Espaçamento, Componentes Base**
- **Objetivo:** Criar CSS premium para componentes base
- **Arquivo:** `assets/css/premium-theme.css`

```css
/* Tipografia */
:root {
    --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
    
    --text-xs: 0.64rem;
    --text-sm: 0.8rem;
    --text-base: 1rem;
    --text-lg: 1.25rem;
    --text-xl: 1.563rem;
    --text-2xl: 1.953rem;
    
    --font-regular: 400;
    --font-medium: 500;
    --font-semibold: 600;
    --font-bold: 700;
    
    --space-1: 0.25rem;
    --space-2: 0.5rem;
    --space-3: 0.75rem;
    --space-4: 1rem;
    --space-5: 1.5rem;
    --space-6: 2rem;
    
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 12px;
    --radius-xl: 16px;
    
    --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
    --transition-base: 250ms cubic-bezier(0.4, 0, 0.2, 1);
    --transition-slow: 350ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* Botões Premium */
.stButton > button {
    font-family: var(--font-primary);
    font-weight: var(--font-semibold);
    border-radius: var(--radius-md);
    transition: all var(--transition-base);
    padding: var(--space-3) var(--space-5);
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
}

/* Cards com elevação */
[data-testid="stMetric"] {
    border-radius: var(--radius-lg);
    padding: var(--space-5);
    transition: all var(--transition-base);
}

[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}
```

- **Testes:** Aplicar CSS e verificar mudanças visuais
- **Demo:** Dashboard com tipografia e espaçamento premium

---

#### **Task 5: Animações CSS - Fade, Scale, Hover Effects**
- **Arquivo:** `assets/css/animations.css`

```css
/* Animação de entrada para gráficos */
.js-plotly-plot {
    animation: fadeInScale 500ms cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes fadeInScale {
    from {
        opacity: 0;
        transform: scale(0.95);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

/* Animação de counter */
@keyframes countUp {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

[data-testid="stMetricValue"] {
    animation: countUp 600ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* Loading spinner customizado */
.stSpinner > div {
    border-color: var(--primary) !important;
    border-top-color: transparent !important;
}
```

- **Testes:** Hover em métrica → scale + shadow
- **Demo:** Dashboard com micro-interações visuais

---

#### **Task 6: KPI Cards Animados com Counter**
- **Arquivo:** `assets/js/animations.js`

```javascript
// Anima contadores numéricos
function animateCounter(element, target, duration = 1000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current).toLocaleString('pt-BR');
    }, 16);
}

// Aplica animação aos elementos
document.addEventListener('DOMContentLoaded', () => {
    const metricValues = document.querySelectorAll('[data-testid="stMetricValue"]');
    metricValues.forEach(el => {
        const target = parseInt(el.textContent.replace(/\D/g, ''));
        if (!isNaN(target)) {
            animateCounter(el, target);
        }
    });
});

// Reaplica após atualizações do Streamlit
window.addEventListener('message', (event) => {
    if (event.data.type === 'streamlit:render') {
        setTimeout(() => {
            const metricValues = document.querySelectorAll('[data-testid="stMetricValue"]');
            metricValues.forEach(el => {
                const target = parseInt(el.textContent.replace(/\D/g, ''));
                if (!isNaN(target)) {
                    animateCounter(el, target, 800);
                }
            });
        }, 100);
    }
});
```

**Integração em app.py:**
```python
def inject_animations():
    """Injeta CSS e JS de animações"""
    with open('assets/css/premium-theme.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    with open('assets/css/animations.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    with open('assets/js/animations.js') as f:
        st.markdown(f'<script>{f.read()}</script>', unsafe_allow_html=True)

def main():
    init_theme()
    inject_animations()
    # ... resto do código ...
```

- **Testes:** KPI de 2547 anima de 0 → 2547 em 1s
- **Demo:** Linha de KPIs no topo com animações

---

#### **Task 7: Sidebar Recolhível com Persistência**
- **Arquivo:** `src/sidebar_manager.py`

```python
import streamlit as st

class SidebarManager:
    def __init__(self):
        if 'sidebar_collapsed' not in st.session_state:
            st.session_state.sidebar_collapsed = False
    
    def render_toggle_button(self):
        """Botão de toggle no header"""
        collapsed = st.session_state.sidebar_collapsed
        icon = "☰" if collapsed else "✕"
        label = "Expandir" if collapsed else "Recolher"
        
        col1, col2, col3 = st.columns([1, 8, 1])
        with col1:
            if st.button(icon, key="sidebar_toggle", help=label):
                st.session_state.sidebar_collapsed = not collapsed
                st.rerun()
    
    def apply_sidebar_css(self):
        """Aplica CSS dinâmico para sidebar"""
        collapsed = st.session_state.sidebar_collapsed
        width = "64px" if collapsed else "280px"
        
        st.markdown(f"""
        <style>
        [data-testid="stSidebar"] {{
            width: {width} !important;
            transition: width 300ms cubic-bezier(0.4, 0, 0.2, 1);
            overflow-x: hidden;
        }}
        
        .sidebar-content {{
            opacity: {0 if collapsed else 1};
            transition: opacity 200ms ease;
            display: {'none' if collapsed else 'block'};
        }}
        
        .sidebar-icon {{
            display: {'block' if collapsed else 'none'};
            font-size: 24px;
            text-align: center;
            padding: 16px 0;
            cursor: pointer;
        }}
        </style>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self, content_func):
        """Renderiza sidebar com estado adequado"""
        self.apply_sidebar_css()
        
        with st.sidebar:
            collapsed = st.session_state.sidebar_collapsed
            
            if collapsed:
                # Apenas ícones
                st.markdown('<div class="sidebar-icon" title="Dashboard">📊</div>', unsafe_allow_html=True)
                st.markdown('<div class="sidebar-icon" title="Filtros">🔍</div>', unsafe_allow_html=True)
                st.markdown('<div class="sidebar-icon" title="Exportar">📤</div>', unsafe_allow_html=True)
                st.markdown('<div class="sidebar-icon" title="Configurações">⚙️</div>', unsafe_allow_html=True)
            else:
                # Conteúdo completo
                st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
                content_func()
                st.markdown('</div>', unsafe_allow_html=True)
```

**Uso em app.py:**
```python
from src.sidebar_manager import SidebarManager

def main():
    sidebar_mgr = SidebarManager()
    sidebar_mgr.render_toggle_button()
    
    def sidebar_content():
        st.markdown("## 📊 Dashboard B2B Churn")
        st.markdown("---")
        # ... filtros, exportação, etc ...
    
    sidebar_mgr.render_sidebar(sidebar_content)
    
    # ... resto do código ...
```

- **Testes:** Toggle funciona, sidebar persiste estado
- **Demo:** Sidebar recolhível funcional

---

#### **Task 8: Responsividade Mobile/Tablet**
- **Arquivo:** `assets/css/responsive.css`

```css
/* Desktop (default) */
.main .block-container {
    max-width: 1400px;
    padding: 2rem 3rem;
}

/* Tablet (768px - 1024px) */
@media (max-width: 1024px) {
    .main .block-container {
        padding: 1.5rem 2rem;
    }
    
    .js-plotly-plot {
        max-height: 350px;
    }
    
    [data-testid="stSidebar"] {
        width: 240px !important;
    }
}

/* Mobile (< 768px) */
@media (max-width: 768px) {
    .main .block-container {
        padding: 1rem;
    }
    
    [data-testid="stSidebar"] {
        width: 0 !important;
    }
    
    [data-testid="stSidebar"].expanded {
        width: 100vw !important;
        position: fixed;
        z-index: 999;
    }
    
    .js-plotly-plot {
        max-height: 300px;
    }
    
    h1 { font-size: 1.75rem !important; }
    h2 { font-size: 1.5rem !important; }
    
    .stButton > button {
        width: 100% !important;
    }
}

/* Touch devices */
@media (hover: none) and (pointer: coarse) {
    .stButton > button {
        min-height: 44px;
        padding: 12px 20px;
    }
}
```

- **Testes:** Testar em Chrome DevTools (iPhone, iPad, Desktop)
- **Demo:** Dashboard usável em mobile

---

### FASE 3: VISUALIZAÇÕES AVANÇADAS

#### **Task 9: Animações em Gráficos Plotly**
- **Atualização em src/charts.py:**

```python
def apply_layout(fig: go.Figure, title: str = "", height: int = 400, 
                 show_legend: bool = True) -> go.Figure:
    # ... código existente ...
    
    # Adicionar configuração de animação
    fig.update_layout(
        transition={'duration': 500, 'easing': 'cubic-in-out'},
        hoverlabel=dict(
            bgcolor=colors.tokens["surface"],
            font_size=13,
            font_family="Inter",
            bordercolor=colors.tokens["border"]
        )
    )
    
    return fig
```

- **Testes:** Gráfico aparece com fade + scale
- **Demo:** Todos os gráficos com animação de entrada

---

### FASE 4: FUNCIONALIDADES AVANÇADAS

#### **Task 12: Sistema de Alertas Configuráveis**
- **Arquivo:** `src/alerts.py`

```python
from typing import List, Dict
import streamlit as st
import pandas as pd

class AlertSystem:
    def __init__(self):
        if 'alert_config' not in st.session_state:
            st.session_state.alert_config = {
                'total_churn_max': 2500,
                'voluntario_pct_max': 75.0,
                'tempo_medio_min': 90,
                'mom_change_max': 20.0,
            }
        
        if 'active_alerts' not in st.session_state:
            st.session_state.active_alerts = []
    
    def configure_alerts(self):
        """Interface de configuração de alertas"""
        st.markdown("### ⚙️ Configurar Alertas")
        
        config = st.session_state.alert_config
        
        col1, col2 = st.columns(2)
        
        with col1:
            config['total_churn_max'] = st.number_input(
                "Total Churn máximo",
                min_value=0,
                value=config['total_churn_max'],
                step=100
            )
            
            config['voluntario_pct_max'] = st.number_input(
                "% Voluntário máximo",
                min_value=0.0,
                max_value=100.0,
                value=config['voluntario_pct_max'],
                step=5.0
            )
        
        with col2:
            config['tempo_medio_min'] = st.number_input(
                "Tempo médio mínimo (dias)",
                min_value=0,
                value=config['tempo_medio_min'],
                step=10
            )
            
            config['mom_change_max'] = st.number_input(
                "Variação MoM máxima (%)",
                min_value=0.0,
                value=config['mom_change_max'],
                step=5.0
            )
    
    def evaluate_alerts(self, kpis: Dict, trend: pd.DataFrame):
        """Avalia métricas e gera alertas"""
        alerts = []
        config = st.session_state.alert_config
        
        # Alerta 1: Total Churn
        if kpis['total'] > config['total_churn_max']:
            alerts.append({
                'type': 'warning',
                'title': 'Churn Total Elevado',
                'message': f"Churn total ({kpis['total']}) acima do limite ({config['total_churn_max']})",
                'action': 'Investigar causas principais'
            })
        
        # Alerta 2: % Voluntário
        if kpis['pct_voluntario'] > config['voluntario_pct_max']:
            alerts.append({
                'type': 'error',
                'title': '% Voluntário Alto',
                'message': f"Voluntário em {kpis['pct_voluntario']}% (limite: {config['voluntario_pct_max']}%)",
                'action': 'Revisar satisfação do cliente'
            })
        
        st.session_state.active_alerts = alerts
        return alerts
    
    def render_alert_banner(self):
        """Renderiza banner de alertas ativos"""
        alerts = st.session_state.active_alerts
        
        if not alerts:
            return
        
        st.markdown("### ⚠️ Alertas Ativos")
        
        for alert in alerts:
            icon_map = {
                'error': '🚨',
                'warning': '⚠️',
                'info': 'ℹ️'
            }
            icon = icon_map.get(alert['type'], 'ℹ️')
            
            with st.expander(f"{icon} {alert['title']}", expanded=True):
                st.markdown(f"**{alert['message']}**")
                st.caption(f"💡 Ação recomendada: {alert['action']}")
```

**Integração:**
```python
from src.alerts import AlertSystem

def main():
    alert_system = AlertSystem()
    
    kpis = calculate_overall_kpis(df_filtered)
    trend = calculate_monthly_trend(df_filtered)
    
    alert_system.evaluate_alerts(kpis, trend)
    alert_system.render_alert_banner()
    
    # Na sidebar
    with st.sidebar:
        with st.expander("⚙️ Configurar Alertas"):
            alert_system.configure_alerts()
```

- **Testes:** Configurar threshold → alerta aparece quando ultrapassado
- **Demo:** Sistema de alertas funcional

---

#### **Task 13-15: Comparação Temporal**
- **Arquivo:** `src/comparator.py`

```python
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import Tuple, Dict

class TemporalComparator:
    def __init__(self):
        if 'comparison_enabled' not in st.session_state:
            st.session_state.comparison_enabled = False
    
    def render_comparison_panel(self, available_periods: list):
        """Painel de seleção de períodos"""
        st.markdown("### 🔄 Comparação Temporal")
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            period_a = st.selectbox("Período A", options=available_periods)
        
        with col2:
            period_b = st.selectbox(
                "Período B", 
                options=available_periods,
                index=min(1, len(available_periods)-1)
            )
        
        with col3:
            enabled = st.checkbox("Ativar", value=st.session_state.comparison_enabled)
        
        if enabled and period_a != period_b:
            st.session_state.comparison_enabled = True
            st.session_state.period_a = period_a
            st.session_state.period_b = period_b
        else:
            st.session_state.comparison_enabled = False
        
        return st.session_state.comparison_enabled
    
    def split_data(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Divide DataFrame em dois períodos"""
        df_a = df[df['MES_ANO'] == st.session_state.period_a]
        df_b = df[df['MES_ANO'] == st.session_state.period_b]
        return df_a, df_b
    
    def calculate_delta(self, kpis_a: Dict, kpis_b: Dict) -> Dict:
        """Calcula deltas entre períodos"""
        delta = {}
        
        for key in kpis_a.keys():
            if isinstance(kpis_a[key], (int, float)):
                val_a = kpis_a[key]
                val_b = kpis_b[key]
                
                delta[f"{key}_abs"] = val_b - val_a
                delta[f"{key}_pct"] = ((val_b - val_a) / val_a * 100) if val_a != 0 else 0
        
        return delta
    
    def render_side_by_side_kpis(self, kpis_a: Dict, kpis_b: Dict, delta: Dict):
        """KPIs lado a lado"""
        period_a = st.session_state.period_a
        period_b = st.session_state.period_b
        
        st.markdown(f"#### {period_a} vs {period_b}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(f"Total - {period_a}", f"{kpis_a['total']:,}")
        
        with col2:
            st.metric(f"Total - {period_b}", f"{kpis_b['total']:,}")
        
        with col3:
            st.metric(
                "Variação",
                f"{delta['total_abs']:+,}",
                delta=f"{delta['total_pct']:+.1f}%",
                delta_color="inverse"
            )
```

**Uso:**
```python
from src.comparator import TemporalComparator

def render_executive_view(df):
    comparator = TemporalComparator()
    available_periods = sorted(df['MES_ANO'].unique())
    
    if comparator.render_comparison_panel(available_periods):
        df_a, df_b = comparator.split_data(df)
        kpis_a = calculate_overall_kpis(df_a)
        kpis_b = calculate_overall_kpis(df_b)
        delta = comparator.calculate_delta(kpis_a, kpis_b)
        
        comparator.render_side_by_side_kpis(kpis_a, kpis_b, delta)
    else:
        # Visualização normal
        pass
```

- **Testes:** Comparar Maio vs Junho → visualização correta
- **Demo:** Comparação temporal funcional

---

#### **Task 16-19: Exportação PDF**
- **Arquivo:** `src/export_pdf.py`

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from datetime import datetime
import tempfile
import os

class PDFExporter:
    def __init__(self, title: str = "Relatório de Churn B2B"):
        self.title = title
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#C46A2B'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
    
    def _header_footer(self, canvas, doc):
        canvas.saveState()
        
        # Cabeçalho
        canvas.setFont('Helvetica-Bold', 10)
        canvas.drawString(2*cm, A4[1] - 1.5*cm, "Telecomunicações S/A")
        
        # Rodapé
        canvas.setFont('Helvetica', 8)
        canvas.drawString(2*cm, 1*cm, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        canvas.drawRightString(A4[0] - 2*cm, 1*cm, f"Página {doc.page}")
        
        canvas.restoreState()
    
    def _save_chart_as_image(self, fig) -> str:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        fig.write_image(temp_file.name, width=800, height=400, scale=2)
        return temp_file.name
    
    def export_dashboard(self, df, kpis, charts, output_path):
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Título
        story.append(Paragraph(self.title, self.styles['CustomTitle']))
        story.append(Spacer(1, 0.5*cm))
        
        # KPIs
        summary_data = [
            ['Métrica', 'Valor'],
            ['Total Churn', f"{kpis['total']:,}"],
            ['Voluntário', f"{kpis['voluntario']:,} ({kpis['pct_voluntario']:.1f}%)"],
        ]
        
        summary_table = Table(summary_data, colWidths=[8*cm, 6*cm])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3F6F5C')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        story.append(summary_table)
        story.append(PageBreak())
        
        # Gráficos
        for chart_title, fig in charts.items():
            story.append(Paragraph(chart_title, self.styles['Heading2']))
            img_path = self._save_chart_as_image(fig)
            img = Image(img_path, width=15*cm, height=7.5*cm)
            story.append(img)
            story.append(Spacer(1, 0.8*cm))
            os.unlink(img_path)
        
        doc.build(story, onFirstPage=self._header_footer, onLaterPages=self._header_footer)
```

**Integração:**
```python
from src.export_pdf import PDFExporter

def main():
    with st.sidebar:
        if st.button("📄 Gerar PDF Executivo"):
            with st.spinner("Gerando PDF..."):
                kpis = calculate_overall_kpis(df_filtered)
                
                trend = calculate_monthly_trend(df_filtered)
                fig_trend = line_churn_trend(trend)
                
                charts = {"Evolução Mensal": fig_trend}
                
                exporter = PDFExporter()
                output_path = f"exports/relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                os.makedirs("exports", exist_ok=True)
                
                exporter.export_dashboard(df_filtered, kpis, charts, output_path)
                
                with open(output_path, "rb") as f:
                    st.download_button(
                        "📥 Baixar PDF",
                        data=f,
                        file_name=os.path.basename(output_path),
                        mime="application/pdf"
                    )
```

- **Testes:** Clicar botão → PDF gerado → download funciona
- **Demo:** Exportação PDF funcional

---

### FASE 5: INTEGRAÇÃO E POLIMENTO

#### **Task 20-24: Integração em Todas as Páginas**
- Aplicar KPI cards animados
- Adicionar alertas contextuais
- Integrar comparação temporal
- Botões de exportação PDF
- Verificar responsividade

---

#### **Task 25: Testes de Acessibilidade**
- Validar contraste: https://webaim.org/resources/contrastchecker/
- Testar navegação por teclado (Tab, Enter, Esc)
- Verificar labels descritivos
- Ajustar onde necessário

---

#### **Task 26: Otimização de Performance**
- Profile com Streamlit Profiler
- Otimizar cache (@st.cache_data)
- Minify CSS/JS (opcional)
- Testar load time < 3s

---

#### **Task 27: Documentação**
- Atualizar README.md
- Adicionar screenshots
- Documentar novas funcionalidades
- Instruções de uso

---

#### **Task 28: Testes End-to-End**
- Fluxo completo do usuário
- Testar em 3 browsers (Chrome, Firefox, Edge)
- Testar em mobile/tablet
- Validar todas as funcionalidades

---

#### **Task 29-30: Polimento e Apresentação**
- Ajustes visuais finais
- Capturar screenshots
- Gravar vídeo demo (opcional)
- Material para apresentação acadêmica

---

## 📊 ESTIMATIVA DE TEMPO

| Fase | Tasks | Tempo Estimado |
|------|-------|----------------|
| Fase 1: Fundação | 1-3 | 6-8 horas |
| Fase 2: UI/UX Premium | 4-8 | 12-16 horas |
| Fase 3: Visualizações | 9-11 | 6-8 horas |
| Fase 4: Funcionalidades | 12-19 | 16-20 horas |
| Fase 5: Integração | 20-30 | 14-18 horas |
| **TOTAL** | 30 tasks | **54-70 horas** |

---

## 🎯 CRITÉRIOS DE SUCESSO

### Funcionalidade:
- ✅ Anonimização automática (100% dos dados sensíveis mascarados)
- ✅ Sidebar recolhível com persistência funcional
- ✅ Animações suaves (300-500ms)
- ✅ Dark mode WCAG AA compliant
- ✅ Sistema de alertas configurável
- ✅ Comparação temporal completa
- ✅ Exportação PDF profissional
- ✅ Responsivo (desktop, tablet, mobile)

### Performance:
- ✅ Load time < 3s
- ✅ Transições suaves sem lag

### Estética:
- ✅ Visual consistente
- ✅ Aparência premium SaaS

### Acessibilidade:
- ✅ Contraste WCAG AA
- ✅ Navegação por teclado

---

## 📝 PRÓXIMOS PASSOS

1. ✅ Revisar e aprovar este plano
2. ⏭️ Iniciar Task 1: Setup de Estrutura
3. ⏭️ Executar tasks sequencialmente por fase
4. ⏭️ Testar incrementalmente
5. ⏭️ Demo final e apresentação

---

## 🔗 RECURSOS

- Streamlit: https://docs.streamlit.io
- Plotly: https://plotly.com/python/
- ReportLab: https://www.reportlab.com/docs/reportlab-userguide.pdf
- WCAG 2.1: https://www.w3.org/WAI/WCAG21/quickref/
- Contrast Checker: https://webaim.org/resources/contrastchecker/

---

**Plano aprovado e pronto para execução!** 🚀
```

