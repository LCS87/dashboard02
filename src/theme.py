"""
Sistema de tema Floresta & Cobre Premium - Light/Dark mode para Streamlit + Plotly.
Versão refinada com tokens estendidos para WCAG AA compliance e estética premium.
Inclui correções para sobreposição de texto e renderização de fontes.
"""
from typing import Literal, Dict, Any

ThemeMode = Literal["light", "dark"]

# ============================================================
# Tokens de Cor - Floresta & Cobre PREMIUM
# Contraste verificado para WCAG 2.1 AA (>= 4.5:1)
# ============================================================

LIGHT_PREMIUM = {
    "bg_primary": "#E8EEE9",
    "bg_secondary": "#F4F7F5",
    "surface": "#FFFFFF",
    "surface_elevated": "#FCFDFC",
    "text_primary": "#1A2820",
    "text_secondary": "#4A5952",
    "text_muted": "#5F6D67",
    "text_inverse": "#FFFFFF",
    "primary": "#C46A2B",
    "primary_hover": "#A85623",
    "primary_light": "#E8C4B0",
    "accent": "#3F6F5C",
    "accent_hover": "#335A4A",
    "success": "#3D7A5F",
    "success_light": "#D4E9DF",
    "warning": "#D4A017",
    "warning_dark": "#B88A14",
    "warning_light": "#F5EDCC",
    "error": "#C45C4A",
    "error_light": "#F5DCD8",
    "info": "#5C8A9F",
    "info_light": "#DCE8EC",
    "border": "#D0DAD4",
    "border_focus": "#C46A2B",
    "border_error": "#C45C4A",
    "hover": "#E4ECE6",
    "active": "#D8E3DC",
    "shadow_sm": "0 1px 2px rgba(26, 40, 32, 0.06)",
    "shadow_md": "0 4px 12px rgba(26, 40, 32, 0.10)",
    "shadow_lg": "0 8px 24px rgba(26, 40, 32, 0.12)",
    "shadow_xl": "0 16px 48px rgba(26, 40, 32, 0.15)",
    "voluntario": "#3D7A5F",
    "involuntario": "#C45C4A",
    "rv_sim": "#C46A2B",
    "rv_nao": "#7A857E",
    "sidebar_bg": "#F4F7F5",
    "sidebar_border": "#D0DAD4",
}

DARK_PREMIUM = {
    "bg_primary": "#121B17",
    "bg_secondary": "#1A2722",
    "surface": "#243330",
    "surface_elevated": "#2A3A36",
    "text_primary": "#E4ECE8",
    "text_secondary": "#B5C4BA",
    "text_muted": "#93A39B",
    "text_inverse": "#121B17",
    "primary": "#E69857",
    "primary_hover": "#F0A970",
    "primary_light": "#3A2A20",
    "accent": "#6FA88A",
    "accent_hover": "#85B89A",
    "success": "#5FA87A",
    "success_light": "#1F3A2A",
    "warning": "#E0B84A",
    "warning_dark": "#3A3010",
    "warning_light": "#3D351A",
    "error": "#E07A68",
    "error_light": "#3A1F1C",
    "info": "#7AA8BD",
    "info_light": "#1C2D33",
    "border": "#2F3F38",
    "border_focus": "#E69857",
    "border_error": "#E07A68",
    "hover": "#2A3A34",
    "active": "#30403A",
    "shadow_sm": "0 1px 2px rgba(0, 0, 0, 0.3)",
    "shadow_md": "0 4px 12px rgba(0, 0, 0, 0.4)",
    "shadow_lg": "0 8px 24px rgba(0, 0, 0, 0.5)",
    "shadow_xl": "0 16px 48px rgba(0, 0, 0, 0.6)",
    "voluntario": "#5FA87A",
    "involuntario": "#E07A68",
    "rv_sim": "#E69857",
    "rv_nao": "#8A968E",
    "sidebar_bg": "#1A2722",
    "sidebar_border": "#2F3F38",
}

LIGHT = {
    "bg": LIGHT_PREMIUM["bg_primary"],
    "surface": LIGHT_PREMIUM["surface"],
    "text": LIGHT_PREMIUM["text_primary"],
    "muted": LIGHT_PREMIUM["text_muted"],
    "primary": LIGHT_PREMIUM["primary"],
    "accent": LIGHT_PREMIUM["accent"],
    "voluntario": LIGHT_PREMIUM["voluntario"],
    "involuntario": LIGHT_PREMIUM["involuntario"],
    "warning": LIGHT_PREMIUM["warning"],
    "rv_nao": LIGHT_PREMIUM["rv_nao"],
    "border": LIGHT_PREMIUM["border"],
    "hover": LIGHT_PREMIUM["hover"],
}

DARK = {
    "bg": DARK_PREMIUM["bg_primary"],
    "surface": DARK_PREMIUM["surface"],
    "text": DARK_PREMIUM["text_primary"],
    "muted": DARK_PREMIUM["text_muted"],
    "primary": DARK_PREMIUM["primary"],
    "accent": DARK_PREMIUM["accent"],
    "voluntario": DARK_PREMIUM["voluntario"],
    "involuntario": DARK_PREMIUM["involuntario"],
    "warning": DARK_PREMIUM["warning"],
    "rv_nao": DARK_PREMIUM["rv_nao"],
    "border": DARK_PREMIUM["border"],
    "hover": DARK_PREMIUM["hover"],
}

LIGHT_SEQUENCES = {
    "volume": ["#C46A2B", "#3F6F5C", "#6FA88A", "#D4A017", "#8A968E", "#5C6B62", "#CAD6CF"],
    "risk": ["#C45C4A", "#D4A017", "#E08A4F", "#3D7A5F", "#3F6F5C"],
    "categorical": ["#C46A2B", "#3F6F5C", "#6B7FA3", "#C45C4A", "#D4A017", "#5FA87A", "#8A5FA0", "#2C5F73", "#A65A76", "#7A857E"],
    "diverging": ["#C45C4A", "#FFFFFF", "#3D7A5F"],
    # Escalas de heatmap/mapa: sempre claras, para o texto escuro das células
    # manter contraste AA tanto no modo claro quanto no escuro.
    "sequential_volume": ["#F4F7F5", "#E8EEE9", "#D5E2DA", "#B9D0C3", "#98BEAA", "#6FA88A"],
    "sequential_risk": ["#F5F1EC", "#EFDCCE", "#E6C2AC", "#DFA88E", "#D98F74", "#D47E5F"],
}

DARK_SEQUENCES = {
    "volume": ["#E69857", "#6FA88A", "#5FA87A", "#E0B84A", "#8A968E", "#8A9A92", "#6B7B72"],
    "risk": ["#E07A68", "#E0B84A", "#E69857", "#5FA87A", "#6FA88A"],
    "categorical": ["#E69857", "#6FA88A", "#8FA8C4", "#E0B84A", "#B58BC9", "#7AA8BD", "#E07A68", "#9AA79E", "#8A5FA0", "#D4A017"],
    "diverging": ["#E07A68", "#243330", "#5FA87A"],
    # Mesmas escalas claras do light: células claras -> texto escuro legível.
    "sequential_volume": ["#F4F7F5", "#E8EEE9", "#D5E2DA", "#B9D0C3", "#98BEAA", "#6FA88A"],
    "sequential_risk": ["#F5F1EC", "#EFDCCE", "#E6C2AC", "#DFA88E", "#D98F74", "#D47E5F"],
}


def get_tokens(mode="light"):
    return LIGHT if mode == "light" else DARK


def get_premium_tokens(mode="light"):
    return LIGHT_PREMIUM if mode == "light" else DARK_PREMIUM


def get_sequences(mode="light"):
    return LIGHT_SEQUENCES if mode == "light" else DARK_SEQUENCES


def get_plotly_template(mode="light"):
    tokens = get_tokens(mode)
    seq = get_sequences(mode)
    
    if mode == "light":
        base_template = "plotly_white"
        paper_bg = tokens["surface"]
        plot_bg = tokens["surface"]
        grid_color = tokens["border"]
        axis_color = tokens["muted"]
        font_color = tokens["text"]
    else:
        base_template = "plotly_dark"
        paper_bg = tokens["surface"]
        plot_bg = tokens["surface"]
        grid_color = tokens["border"]
        axis_color = tokens["muted"]
        font_color = tokens["text"]
    
    return {
        "layout": {
            "template": base_template,
            "separators": ",.",
            "paper_bgcolor": paper_bg,
            "plot_bgcolor": plot_bg,
            "font": {"color": font_color, "family": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"},
            "title": {"font": {"color": font_color, "size": 16}},
            "xaxis": {
                "gridcolor": grid_color,
                "linecolor": grid_color,
                "tickfont": {"color": axis_color},
                "titlefont": {"color": tokens["muted"]},
                "zerolinecolor": grid_color,
            },
            "yaxis": {
                "gridcolor": grid_color,
                "linecolor": grid_color,
                "tickfont": {"color": axis_color},
                "titlefont": {"color": tokens["muted"]},
                "zerolinecolor": grid_color,
            },
            "legend": {
                "bgcolor": "rgba(0,0,0,0)",
                "font": {"color": font_color},
                "bordercolor": tokens["border"],
                "borderwidth": 1,
            },
            "colorway": seq["categorical"],
            "colorscale": {
                "sequential": seq["sequential_volume"],
                "diverging": seq["diverging"],
            },
            "hoverlabel": {
                "bgcolor": tokens["surface"],
                "font": {"color": font_color},
                "bordercolor": tokens["border"],
            },
            "transition": {"duration": 300, "easing": "cubic-in-out"},
        }
    }


def get_css(mode="light"):
    tokens = get_premium_tokens(mode)
    
    info_colors = {
        "info": {"bg": tokens["info_light"], "border": tokens["info"], "icon": "ℹ️"},
        "success": {"bg": tokens["success_light"], "border": tokens["success"], "icon": "✅"},
        "warning": {"bg": tokens["warning_light"], "border": tokens["warning"], "icon": "⚠️"},
        "error": {"bg": tokens["error_light"], "border": tokens["error"], "icon": "❌"},
    }
    
    css_rules = []
    for type_name, colors in info_colors.items():
        css_rules.append(f'''
        .st-info-box-{type_name} {{
            background-color: {colors["bg"]};
            border-left: 4px solid {colors["border"]};
            padding: 12px 16px;
            border-radius: 8px;
            margin: 8px 0;
        }}''')
    
    font_import = """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    """
    
    # Build CSS template using format to avoid f-string issues
    css_template = font_import + """
    <style>
    /* ========== TEXT RENDERING FIXES - PREVENT OVERLAPPING ========== */
    * {{
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
        text-rendering: optimizeLegibility !important;
    }}
    
    /* Prevent text overlapping globally */
    html, body, div, span, p, h1, h2, h3, h4, h5, h6, a, span, label, button, input, select, textarea, td, th, li {{
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        word-break: break-word !important;
        hyphens: auto !important;
        line-height: 1.5 !important;
    }}
    
    /* Prevent overlapping in specific Streamlit components */
    [data-testid="stMarkdown"], 
    [data-testid="stMarkdownContainer"],
    [data-testid="stCaption"],
    [data-testid="stText"],
    .stMarkdown,
    .stCaption,
    .stText {{
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        word-break: break-word !important;
        white-space: normal !important;
        line-height: 1.6 !important;
    }}
    
    /* Fix for stMetric overlapping */
    [data-testid="stMetric"] {{
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }}
    
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {{
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
    }}
    
    /* Fix for sidebar text */
    [data-testid="stSidebar"] * {{
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        word-break: break-word !important;
        white-space: normal !important;
    }}
    
    /* Fix for buttons */
    .stButton > button {{
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
    }}
    
    /* Fix for tabs */
    .stTabs [data-baseweb="tab"] {{
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
    }}
    
    /* Fix for selectbox/multiselect */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {{
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }}
    
    /* Fix for dataframes */
    .stDataFrame, 
    .stDataFrame [data-testid="stTable"] {{
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }}
    
    /* Fix for expanders */
    .streamlit-expanderHeader,
    .streamlit-expanderContent {{
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
    }}
    
    /* Fix for alerts/info boxes */
    .stAlert, .stInfo, .stSuccess, .stWarning, .stError,
    .st-info-box-info, .st-info-box-success, .st-info-box-warning, .st-info-box-error {{
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
    }}
    
    /* Fix for tooltips and popovers */
    [data-tooltip], [role="tooltip"] {{
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
        max-width: 300px !important;
    }}
    
    /* ========== TEMA FLORESTA & COBRE PREMIUM ========== */
    
    :root {{
        --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        --font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', 'Monaco', monospace;
        
        --radius-sm: 4px;
        --radius-md: 8px;
        --radius-lg: 12px;
        --radius-xl: 16px;
        
        --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-base: 250ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-slow: 350ms cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .stApp {{
        background-color: {bg_primary};
        font-family: var(--font-primary) !important;
        font-size: 1rem;
        line-height: 1.6;
    }}
    
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
        border-right: 1px solid {sidebar_border};
        transition: width 300ms cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    [data-testid="stSidebar"] * {{
        color: {text_primary} !important;
        font-family: var(--font-primary) !important;
    }}
    
    .main .block-container {{
        background-color: {bg_primary};
        padding-top: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 1400px;
        font-family: var(--font-primary) !important;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        color: {text_primary} !important;
        font-family: var(--font-primary) !important;
        font-weight: 600 !important;
        line-height: 1.3 !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }}
    
    h1 {{ font-size: 2rem !important; letter-spacing: -0.02em; }}
    h2 {{ font-size: 1.5rem !important; letter-spacing: -0.01em; }}
    h3 {{ font-size: 1.25rem !important; }}
    
    p, span, div, label {{ 
        color: {text_primary} !important; 
        font-family: var(--font-primary) !important;
        line-height: 1.6 !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }}
    
    .stMarkdown, .stText {{ font-family: var(--font-primary) !important; line-height: 1.6 !important; }}
    
    code, pre {{ font-family: var(--font-mono) !important; line-height: 1.5 !important; }}
    
    [data-testid="stMetric"] {{
        background-color: {surface};
        border: 1px solid {border};
        border-radius: var(--radius-lg);
        padding: 1.5rem;
        transition: all var(--transition-base);
        box-shadow: {shadow_sm};
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }}
    
    [data-testid="stMetric"]:hover {{
        transform: translateY(-2px);
        box-shadow: {shadow_lg};
        border-color: {primary};
    }}
    
    [data-testid="stMetric"] > div {{
        color: {text_primary} !important;
    }}
    
    [data-testid="stMetricLabel"] {{
        color: {text_secondary} !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        line-height: 1.4 !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
    }}
    
    [data-testid="stMetricValue"] {{
        color: {text_primary} !important;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        font-family: var(--font-primary) !important;
        line-height: 1.2 !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
    }}
    
    [data-testid="stMetricDelta"] {{
        color: {primary} !important;
        font-weight: 600 !important;
        line-height: 1.4 !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }}
    
    /* Buttons */
    .stButton > button {{
        background-color: {primary};
        color: {text_inverse};
        border: none;
        border-radius: var(--radius-md);
        font-weight: 600;
        font-family: var(--font-primary);
        padding: 0.75rem 1.5rem;
        transition: all var(--transition-base);
        font-size: 0.875rem;
        white-space: normal !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }}
    
    .stButton > button:hover {{
        background-color: {primary_hover};
        transform: translateY(-1px);
        box-shadow: {shadow_md};
    }}
    
    .stButton > button:active {{
        transform: translateY(0);
        box-shadow: {shadow_sm};
    }}
    
    .stButton > button[kind="secondary"] {{
        background-color: {surface};
        color: {text_primary};
        border: 1px solid {border};
    }}
    
    .stButton > button[kind="secondary"]:hover {{
        background-color: {hover};
        border-color: {primary};
    }}
    
    .stSelectbox > div > div,
    .stMultiSelect > div > div {{
        background-color: {surface};
        border: 1px solid {border};
        border-radius: var(--radius-md);
        font-family: var(--font-primary);
        white-space: normal !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }}
    
    .stSelectbox label,
    .stMultiSelect label {{
        color: {text_primary} !important;
        font-weight: 500;
        line-height: 1.5 !important;
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: {surface};
        border: 1px solid {border};
        border-radius: var(--radius-lg);
        padding: 0.25rem;
        gap: 0.25rem;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        color: {text_secondary};
        font-weight: 500;
        font-family: var(--font-primary);
        border-radius: var(--radius-md);
        padding: 0.5rem 1rem;
        transition: all var(--transition-fast);
        white-space: normal !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {primary} !important;
        color: {text_inverse} !important;
        box-shadow: {shadow_sm};
    }}
    
    /* Expander */
    .streamlit-expanderHeader {{
        background-color: {surface};
        border: 1px solid {border};
        border-radius: var(--radius-md);
        color: {text_primary} !important;
        font-weight: 500;
        font-family: var(--font-primary);
        padding: 0.75rem 1rem;
        line-height: 1.5 !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
    }}
    
    .streamlit-expanderContent {{
        background-color: {bg_primary};
        border: 1px solid {border};
        border-top: none;
        border-radius: 0 0 var(--radius-md) var(--radius-md);
        padding: 1rem;
    }}
    
    /* Dataframe */
    .stDataFrame {{
        background-color: {surface};
        border: 1px solid {border};
        border-radius: var(--radius-lg);
        overflow: hidden;
    }}
    
    .stDataFrame [data-testid="stTable"] {{
        font-family: var(--font-primary);
        font-size: 0.875rem;
        line-height: 1.5 !important;
    }}
    
    /* File uploader */
    .stFileUploader {{
        background-color: {surface};
        border: 2px dashed {border};
        border-radius: var(--radius-lg);
        padding: 2rem;
        transition: all var(--transition-base);
    }}
    
    .stFileUploader:hover {{
        border-color: {primary};
        background-color: {primary_light};
    }}
    
    .st-info-box-info {{
        background-color: {info_light};
        border-left: 4px solid {info};
        padding: 12px 16px;
        border-radius: 8px;
        margin: 8px 0;
        line-height: 1.6 !important;
    }}
    .st-info-box-success {{
        background-color: {success_light};
        border-left: 4px solid {success};
        padding: 12px 16px;
        border-radius: 8px;
        margin: 8px 0;
        line-height: 1.6 !important;
    }}
    .st-info-box-warning {{
        background-color: {warning_light};
        border-left: 4px solid {warning};
        padding: 12px 16px;
        border-radius: 8px;
        margin: 8px 0;
        line-height: 1.6 !important;
    }}
    .st-info-box-error {{
        background-color: {error_light};
        border-left: 4px solid {error};
        padding: 12px 16px;
        border-radius: 8px;
        margin: 8px 0;
        line-height: 1.6 !important;
    }}
    
    .stCaption, .stMarkdown small {{
        color: {text_muted} !important;
        font-size: 0.75rem !important;
        line-height: 1.5 !important;
    }}
    
    hr {{
        border-color: {border} !important;
        margin: 1.5rem 0;
    }}
    
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    ::-webkit-scrollbar-track {{
        background: {bg_primary};
    }}
    ::-webkit-scrollbar-thumb {{
        background: {text_muted};
        border-radius: 4px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: {primary};
    }}
    
    .js-plotly-plot {{
        background-color: {surface} !important;
        border-radius: var(--radius-lg);
        border: 1px solid {border};
        box-shadow: {shadow_sm};
        animation: fadeInScale 400ms cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    @keyframes fadeInScale {{
        from {{
            opacity: 0;
            transform: scale(0.98);
        }}
        to {{
            opacity: 1;
            transform: scale(1);
        }}
    }}
    
    @keyframes countUp {{
        from {{
            opacity: 0;
            transform: translateY(10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    [data-testid="stMetricValue"] {{
        animation: countUp 600ms cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .stSpinner > div {{
        border-color: {primary} !important;
        border-top-color: transparent !important;
    }}
    
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {{
        background-color: {surface};
        border: 1px solid {border};
        border-radius: var(--radius-md);
        color: {text_primary};
        font-family: var(--font-primary);
        line-height: 1.5 !important;
    }}
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: {border_focus};
        box-shadow: 0 0 0 3px {primary_light};
    }}
    
    .stCheckbox label,
    .stRadio label {{
        color: {text_primary} !important;
        line-height: 1.5 !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
    }}
    
    .stSlider [data-baseweb="slider"] {{
        color: {primary} !important;
    }}
    
    .stDownloadButton > button {{
        background-color: {accent} !important;
    }}
    
    .stDownloadButton > button:hover {{
        background-color: {accent_hover} !important;
    }}
    
    @keyframes slideDown {{
        from {{
            opacity: 0;
            transform: translateY(-10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .alert-banner {{
        animation: slideDown 300ms ease;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }}
    
    @keyframes slideDown {{
        from {{
            opacity: 0;
            transform: translateY(-10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    [data-testid="stMetricValue"] {{
        animation: countUp 600ms cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    @keyframes countUp {{
        from {{
            opacity: 0;
            transform: translateY(10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .stSpinner > div {{
        border-color: {primary} !important;
        border-top-color: transparent !important;
    }}
    
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {{
        background-color: {surface};
        border: 1px solid {border};
        border-radius: var(--radius-md);
        color: {text_primary};
        font-family: var(--font-primary);
        line-height: 1.5 !important;
    }}
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: {border_focus};
        box-shadow: 0 0 0 3px {primary_light};
    }}
    
    .stCheckbox label,
    .stRadio label {{
        color: {text_primary} !important;
        line-height: 1.5 !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
    }}
    
    .stSlider [data-baseweb="slider"] {{
        color: {primary} !important;
    }}
    
    .stDownloadButton > button {{
        background-color: {accent} !important;
    }}
    
    .stDownloadButton > button:hover {{
        background-color: {accent_hover} !important;
    }}
    
    @keyframes slideDown {{
        from {{
            opacity: 0;
            transform: translateY(-10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .alert-banner {{
        animation: slideDown 300ms ease;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }}
    
    @keyframes slideDown {{
        from {{
            opacity: 0;
            transform: translateY(-10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    [data-testid="stMetricValue"] {{
        animation: countUp 600ms cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    @keyframes countUp {{
        from {{
            opacity: 0;
            transform: translateY(10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .stSpinner > div {{
        border-color: {primary} !important;
        border-top-color: transparent !important;
    }}
    
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {{
        background-color: {surface};
        border: 1px solid {border};
        border-radius: var(--radius-md);
        color: {text_primary};
        font-family: var(--font-primary);
        line-height: 1.5 !important;
    }}
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: {border_focus};
        box-shadow: 0 0 0 3px {primary_light};
    }}
    
    .stCheckbox label,
    .stRadio label {{
        color: {text_primary} !important;
        line-height: 1.5 !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
    }}
    
    .stSlider [data-baseweb="slider"] {{
        color: {primary} !important;
    }}
    
    .stDownloadButton > button {{
        background-color: {accent} !important;
    }}
    
    .stDownloadButton > button:hover {{
        background-color: {accent_hover} !important;
    }}
    
    /* Alert/Info banner animations */
    .alert-banner {{
        animation: slideDown 300ms ease;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
    }}
    
    @keyframes slideDown {{
        from {{
            opacity: 0;
            transform: translateY(-10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    [data-testid="stMetricValue"] {{
        animation: countUp 600ms cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    @keyframes countUp {{
        from {{
            opacity: 0;
            transform: translateY(10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .stSpinner > div {{
        border-color: {primary} !important;
        border-top-color: transparent !important;
    }}
    
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {{
        background-color: {surface};
        border: 1px solid {border};
        border-radius: var(--radius-md);
        color: {text_primary};
        font-family: var(--font-primary);
        line-height: 1.5 !important;
    }}
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: {border_focus};
        box-shadow: 0 0 0 3px {primary_light};
    }}
    
    .stCheckbox label,
    .stRadio label {{
        color: {text_primary} !important;
        line-height: 1.5 !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
    }}
    
    .stSlider [data-baseweb="slider"] {{
        color: {primary} !important;
    }}
    
    .stDownloadButton > button {{
        background-color: {accent} !important;
    }}
    
    .stDownloadButton > button:hover {{
        background-color: {accent_hover} !important;
    }}
    
    /* ========== PREMIUM v2: PAINÉIS, TIPOGRAFIA E MOVIMENTO ========== */
    .block-container {{
        padding-top: 1.3rem;
        padding-bottom: 2.5rem;
        max-width: 1440px;
    }}

    /* Head de página premium */
    .page-head {{
        padding-bottom: 0.75rem;
        margin-bottom: 0.5rem;
        border-bottom: 1px solid {border};
    }}
    .page-head h1 {{
        font-size: 1.9rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        line-height: 1.2;
        margin: 0;
        color: {text_primary};
    }}
    .page-sub {{
        color: {text_muted};
        font-size: 0.95rem;
        margin: 0.2rem 0 0;
        border: none;
    }}

    /* Títulos de seção uniformes */
    [data-testid="stMarkdownContainer"] h3 {{
        font-size: 1.08rem;
        font-weight: 700;
        letter-spacing: -0.01em;
        margin: 1.15rem 0 0.4rem;
    }}

    /* Card visual para gráficos Plotly (painel uniforme) */
    [data-testid="stPlotlyChart"], .stPlotlyChart {{
        background-color: {surface} !important;
        border: 1px solid {border};
        border-radius: 14px;
        box-shadow: {shadow_sm};
        padding: 6px 2px 2px 2px;
        overflow: hidden;
    }}

    /* Cards de KPI */
    [data-testid="stMetric"] {{
        background-color: {bg_secondary};
        border: 1px solid {border};
        border-radius: 14px;
        padding: 0.85rem 1.1rem !important;
        box-shadow: {shadow_sm};
    }}
    [data-testid="stMetricLabel"] p, [data-testid="stMetricLabel"] span {{
        color: {text_muted} !important;
        font-size: 0.78rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    [data-testid="stMetricValue"] {{
        font-size: 1.65rem !important;
        font-weight: 700 !important;
    }}
    [data-testid="stMetricDelta"] {{
        margin-top: 0.25rem;
    }}

    /* Animação de entrada suave (respeita reduced-motion) */
    @keyframes fadeUp {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    @media (prefers-reduced-motion: no-preference) {{
        [data-testid="stPlotlyChart"], [data-testid="stMetric"] {{
            animation: fadeUp 0.45s ease-out backwards;
        }}
    }}

    /* Skeleton shimmer (carregamento percebido) */
    .kpi-skeleton {{
        height: 84px;
        border-radius: 14px;
        background: linear-gradient(90deg, {bg_secondary} 25%, {surface} 45%, {bg_secondary} 65%);
        background-size: 300% 100%;
        animation: shimmer 1.3s linear infinite;
    }}
    .skeleton-line {{
        height: 14px;
        border-radius: 7px;
        margin: 8px 0;
        background: linear-gradient(90deg, {bg_secondary} 25%, {surface} 45%, {bg_secondary} 65%);
        background-size: 300% 100%;
        animation: shimmer 1.3s linear infinite;
    }}
    @keyframes shimmer {{
        0% {{ background-position: 150% 0; }}
        100% {{ background-position: -150% 0; }}
    }}

    /* Empty state premium */
    .empty-panel {{
        text-align: center;
        padding: 2.4rem 1.5rem;
        border: 1px dashed {border};
        border-radius: 14px;
        background-color: {bg_secondary};
    }}
    .empty-panel .empty-ico {{
        font-size: 2.4rem;
        display: inline-block;
        margin-bottom: 0.6rem;
    }}
    .empty-panel h4 {{
        color: {text_primary};
        margin: 0 0 0.3rem;
    }}
    .empty-panel p {{
        color: {text_muted};
        font-size: 0.94rem;
        margin: 0;
    }}

    /* Responsive - Mobile/Tablet adjustments handled in responsive.css */
    
    </style>
    """
    
    # Format the template with tokens
    return css_template.format(**tokens)


# ============================================================
# Helper para uso rápido nos charts
# ============================================================

class ThemeColors:
    """Proxy para acessar cores do tema ativo via session_state."""
    
    def __init__(self, mode="light"):
        self.mode = mode
        self._tokens = get_tokens(mode)
        self._premium_tokens = get_premium_tokens(mode)
        self._sequences = get_sequences(mode)
    
    @property
    def tokens(self):
        return self._tokens
    
    @property
    def premium_tokens(self):
        return self._premium_tokens
    
    @property
    def sequences(self):
        return self._sequences
    
    def get(self, key, default=None):
        return self._tokens.get(key, default)
    
    # Atalhos para compatibilidade com código existente
    @property
    def primary(self): return self._tokens["primary"]
    @property
    def secondary(self): return self._tokens["accent"]
    @property
    def success(self): return self._tokens["voluntario"]
    @property
    def danger(self): return self._tokens["involuntario"]
    @property
    def warning(self): return self._tokens["warning"]
    @property
    def info(self): return self._tokens["accent"]
    @property
    def light(self): return self._tokens["surface"]
    @property
    def dark(self): return self._tokens["text"]
    @property
    def voluntario(self): return self._tokens["voluntario"]
    @property
    def involuntario(self): return self._tokens["involuntario"]
    @property
    def rv_sim(self): return self._tokens["primary"]
    @property
    def rv_nao(self): return self._tokens["rv_nao"]
    
    @property
    def color_sequence(self):
        return self._sequences["categorical"]
    
    @property
    def template(self):
        return "plotly_white" if self.mode == "light" else "plotly_dark"


def get_theme_colors(mode=None):
    import streamlit as st
    if mode is None:
        mode = st.session_state.get("theme_mode", "light")
    return ThemeColors(mode)


# Alias para compatibilidade
def get_theme(mode=None):
    """Retorna objeto ThemeColors do tema ativo."""
    return get_theme_colors(mode)