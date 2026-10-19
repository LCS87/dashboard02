"""
Gerenciador de Sidebar recolhível com persistência no Session State.
Compatível com CSS responsivo (mobile overlay, desktop collapse).
"""
import streamlit as st
from typing import Callable, Optional


class SidebarManager:
    """Gerencia estado e renderização da sidebar recolhível."""
    
    def __init__(self, key: str = "sidebar_collapsed"):
        self.key = key
        if key not in st.session_state:
            st.session_state[key] = False
    
    @property
    def is_collapsed(self) -> bool:
        return st.session_state[self.key]
    
    def toggle(self) -> None:
        """Alterna estado da sidebar."""
        st.session_state[self.key] = not st.session_state[self.key]
        st.rerun()
    
    def apply_sidebar_css(self) -> None:
        """Aplica CSS dinâmico para sidebar recolhível (desktop)."""
        collapsed = self.is_collapsed
        width = "64px" if collapsed else "280px"
        
        st.markdown(f"""
        <style>
        /* Desktop: width fixa com transição */
        @media (min-width: 769px) {{
            [data-testid="stSidebar"] {{
                width: {width} !important;
                min-width: {width} !important;
                max-width: {width} !important;
                transition: width 300ms cubic-bezier(0.4, 0, 0.2, 1);
                overflow-x: hidden;
            }}
            
            .sidebar-content {{
                opacity: {0 if collapsed else 1};
                transition: opacity 200ms ease;
                display: {'none' if collapsed else 'block'};
            }}
            
            .sidebar-nav-icons {{
                display: {'block' if collapsed else 'none'} !important;
            }}
            
            /* Ocultar labels quando recolhido (desktop) */
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] .stMarkdown:not(:first-child),
            [data-testid="stSidebar"] .stSelectbox,
            [data-testid="stSidebar"] .stMultiSelect,
            [data-testid="stSidebar"] .stButton:not(:has(button[key="sidebar_toggle_btn"])),
            [data-testid="stSidebar"] .stExpander,
            [data-testid="stSidebar"] .stFileUploader {{
                display: {'none' if collapsed else 'block'} !important;
            }}
            
            /* Manter botão de toggle visível */
            [data-testid="stSidebar"] button[key="sidebar_toggle_btn"] {{
                display: block !important;
            }}
        }}
        
        /* Mobile: controlado via JS + CSS responsive.css */
        @media (max-width: 768px) {{
            [data-testid="stSidebar"] {{
                width: 280px !important;
                min-width: 280px !important;
                max-width: 280px !important;
            }}
            
            .sidebar-content {{
                display: block !important;
                opacity: 1 !important;
            }}
            
            .sidebar-nav-icons {{
                display: none !important;
            }}
        }}
        </style>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self, content_func: Callable[[], None]) -> None:
        """Renderiza sidebar com estado adequado."""
        self.apply_sidebar_css()
        
        with st.sidebar:
            collapsed = self.is_collapsed
            
            # Botão de toggle sempre visível
            if st.button("☰" if collapsed else "✕", 
                        key="sidebar_toggle_btn", 
                        help="Expandir" if collapsed else "Recolher"):
                self.toggle()
            
            if not collapsed:
                st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
                content_func()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                # Ícones de navegação quando recolhido (desktop)
                st.markdown('''
                <div class="sidebar-nav-icons">
                    <div title="Dashboard">📊</div>
                    <div title="Filtros">🔍</div>
                    <div title="Exportar">📤</div>
                    <div title="Configurações">⚙️</div>
                </div>
                ''', unsafe_allow_html=True)


def render_sidebar_toggle(key: str = "sidebar_collapsed") -> None:
    """Função auxiliar para renderizar apenas o toggle."""
    if key not in st.session_state:
        st.session_state[key] = False
    
    collapsed = st.session_state[key]
    icon = "☰" if collapsed else "✕"
    label = "Expandir" if collapsed else "Recolher"
    
    if st.button(icon, key=f"{key}_btn", help=label):
        st.session_state[key] = not collapsed
        st.rerun()