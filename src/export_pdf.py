"""
Módulo de Exportação PDF para Dashboard B2B Churn.
Gera relatórios executivos profissionais em PDF.
"""
import os
import tempfile
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, Image, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.colors import HexColor
import plotly.io as pio


class PDFExporter:
    """Exportador de relatórios em PDF com layout profissional."""
    
    def __init__(self, title: str = "Relatório de Churn B2B"):
        self.title = title
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configura estilos customizados para o relatório."""
        # Título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=HexColor('#C46A2B'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=HexColor('#3F6F5C'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
        
        # Seção
        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=HexColor('#1A2820'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
        
        # Corpo
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=HexColor('#243029'),
            spaceAfter=8,
            leading=14,
            fontName='Helvetica'
        ))
        
        # Rodapé
        self.styles.add(ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=HexColor('#7A8882'),
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
    
    def _header_footer(self, canvas, doc):
        """Desenha cabeçalho e rodapé em cada página."""
        canvas.saveState()
        
        # Cabeçalho
        canvas.setFont('Helvetica-Bold', 10)
        canvas.setFillColor(HexColor('#3F6F5C'))
        canvas.drawString(2*cm, A4[1] - 1.5*cm, "Telecomunicações S/A - Dashboard B2B Churn")
        
        # Linha decorativa
        canvas.setStrokeColor(HexColor('#C46A2B'))
        canvas.setLineWidth(1)
        canvas.line(2*cm, A4[1] - 1.7*cm, A4[0] - 2*cm, A4[1] - 1.7*cm)
        
        # Rodapé
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(HexColor('#7A8882'))
        canvas.drawString(2*cm, 1*cm, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        canvas.drawRightString(A4[0] - 2*cm, 1*cm, f"Página {doc.page}")
        
        canvas.restoreState()
    
    def _save_chart_as_image(self, fig, width=800, height=450) -> Optional[str]:
        """Salva gráfico Plotly como imagem temporária."""
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            fig.write_image(temp_file.name, width=width, height=height, scale=2)
            return temp_file.name
        except Exception as e:
            print(f"Erro ao salvar gráfico: {e}")
            return None
    
    def _create_kpi_table(self, kpis: Dict) -> Table:
        """Cria tabela de KPIs para o PDF."""
        summary_data = [
            ['Métrica', 'Valor'],
            ['Total Churn', f"{kpis.get('total', 0):,}"],
            ['Voluntário', f"{kpis.get('voluntario', 0):,} ({kpis.get('pct_voluntario', 0):.1f}%)"],
            ['Involuntário', f"{kpis.get('involuntario', 0):,} ({kpis.get('pct_involuntario', 0):.1f}%)"],
            ['RV = SIM', f"{kpis.get('rv_sim', 0):,} ({kpis.get('pct_rv', 0):.1f}%)"],
            ['Tempo Médio (dias)', f"{kpis.get('tempo_medio', 0):.1f}"],
            ['Tempo Mediano (dias)', f"{kpis.get('tempo_mediano', 0):.1f}"],
            ['Churn Precoce (≤90d)', f"{kpis.get('pct_precoce_90', 0):.1f}%"],
            ['Top 5 Dealers', f"{kpis.get('concentracao_top5_dealers', 0):.1f}%"],
            ['Top 3 Motivos', f"{kpis.get('concentracao_top3_motivos', 0):.1f}%"],
        ]
        
        table = Table(summary_data, colWidths=[10*cm, 6*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#3F6F5C')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F4F7F5')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        return table
    
    def _create_top_table(self, df: pd.DataFrame, columns: List[str], title: str, max_rows: int = 10) -> Table:
        """Cria tabela genérica para top N."""
        if df.empty:
            return None
        
        df_display = df.head(max_rows).copy()
        
        # Formatar colunas numéricas
        for col in df_display.columns:
            if df_display[col].dtype in ['int64', 'float64']:
                if 'pct' in col.lower() or 'tempo' in col.lower():
                    df_display[col] = df_display[col].apply(lambda x: f"{x:.1f}" if pd.notna(x) else "-")
                else:
                    df_display[col] = df_display[col].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else "-")
        
        headers = [c.replace('_', ' ').title() for c in df_display.columns]
        data = [headers] + df_display.values.tolist()
        
        table = Table(data, colWidths=[16*cm / len(df_display.columns)] * len(df_display.columns))
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#C46A2B')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F4F7F5')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        return table
    
    def export_dashboard(self, 
                         df: pd.DataFrame, 
                         kpis: Dict, 
                         charts: Dict[str, any],
                         output_path: str,
                         periodo: str = "") -> bool:
        """
        Exporta dashboard completo para PDF.
        
        Args:
            df: DataFrame filtrado
            kpis: Dicionário de KPIs
            charts: Dicionário {titulo: figura_plotly}
            output_path: Caminho do arquivo PDF de saída
            periodo: String descrevendo o período filtrado
            
        Returns:
            bool: True se sucesso, False caso contrário
        """
        try:
            # Criar diretório se não existir
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            doc = SimpleDocTemplate(
                output_path, 
                pagesize=A4,
                leftMargin=2*cm,
                rightMargin=2*cm,
                topMargin=2.5*cm,
                bottomMargin=2*cm
            )
            
            story = []
            
            # Título
            story.append(Paragraph(self.title, self.styles['CustomTitle']))
            
            if periodo:
                story.append(Paragraph(f"Período: {periodo}", self.styles['CustomSubtitle']))
            
            story.append(Spacer(1, 0.5*cm))
            
            # KPIs
            story.append(Paragraph("Indicadores Principais", self.styles['SectionTitle']))
            story.append(self._create_kpi_table(kpis))
            story.append(Spacer(1, 0.5*cm))
            
            # Gráficos
            for chart_title, fig in charts.items():
                story.append(PageBreak())
                story.append(Paragraph(chart_title, self.styles['SectionTitle']))
                story.append(Spacer(1, 0.3*cm))
                
                img_path = self._save_chart_as_image(fig)
                if img_path and os.path.exists(img_path):
                    img = Image(img_path, width=16*cm, height=9*cm)
                    story.append(img)
                    story.append(Spacer(1, 0.5*cm))
                    os.unlink(img_path)
            
            # Tabelas de Top N
            story.append(PageBreak())
            story.append(Paragraph("Top 10 Planos com Mais Churn", self.styles['SectionTitle']))
            from src.metrics import calculate_churn_by_dimension
            top_planos = calculate_churn_by_dimension(df, "PLANO", 10)
            if not top_planos.empty:
                table = self._create_top_table(
                    top_planos[["PLANO", "TOTAL", "VOLUNTARIO", "INVOLUNTARIO", "PCT_VOLUNTARIO", "PCT_RV", "TEMPO_MEDIO"]],
                    ["PLANO", "TOTAL", "VOLUNTARIO", "INVOLUNTARIO", "PCT_VOLUNTARIO", "PCT_RV", "TEMPO_MEDIO"],
                    "Top Planos"
                )
                if table:
                    story.append(table)
            
            story.append(Spacer(1, 0.5*cm))
            
            # Top Motivos
            story.append(Paragraph("Top 10 Motivos de Churn", self.styles['SectionTitle']))
            from src.metrics import calculate_motivo_breakdown
            top_motivos = calculate_motivo_breakdown(df, 10)
            if not top_motivos.empty:
                table = self._create_top_table(
                    top_motivos[["MOTIVO_BAIXA", "TOTAL", "VOLUNTARIO", "INVOLUNTARIO", "PCT_TOTAL"]],
                    ["MOTIVO_BAIXA", "TOTAL", "VOLUNTARIO", "INVOLUNTARIO", "PCT_TOTAL"],
                    "Top Motivos"
                )
                if table:
                    story.append(table)
            
            # Top Clientes
            story.append(Spacer(1, 0.5*cm))
            story.append(Paragraph("Top 10 Clientes com Mais Churn", self.styles['SectionTitle']))
            from src.metrics import calculate_top_clientes_churn
            top_clientes = calculate_top_clientes_churn(df, 10)
            if not top_clientes.empty:
                table = self._create_top_table(
                    top_clientes[["CLIENTE", "UF", "QTD_LINHAS", "TOTAL_CHURN", "PLANOS", "MOTIVOS"]],
                    ["CLIENTE", "UF", "QTD_LINHAS", "TOTAL_CHURN", "PLANOS", "MOTIVOS"],
                    "Top Clientes"
                )
                if table:
                    story.append(table)
            
            # Build PDF
            doc.build(story, onFirstPage=self._header_footer, onLaterPages=self._header_footer)
            return True
            
        except Exception as e:
            print(f"Erro ao gerar PDF: {e}")
            return False


def export_to_pdf(df: pd.DataFrame, 
                  kpis: Dict, 
                  charts: Dict[str, any],
                  output_dir: str = "exports",
                  filename: str = None) -> Optional[str]:
    """
    Função auxiliar para exportar dashboard para PDF.
    
    Returns:
        Caminho do arquivo gerado ou None se erro
    """
    if filename is None:
        filename = f"relatorio_churn_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    output_path = os.path.join(output_dir, filename)
    
    exporter = PDFExporter()
    success = exporter.export_dashboard(df, kpis, charts, output_path)
    
    if success:
        return output_path
    return None


# Função para uso direto no Streamlit
def render_pdf_export_button(df: pd.DataFrame, kpis: Dict, charts: Dict, periodo: str = "") -> None:
    """Renderiza botão de exportação PDF no Streamlit."""
    import streamlit as st
    
    if st.button("📄 Gerar Relatório PDF", width="stretch"):
        with st.spinner("Gerando PDF..."):
            filename = f"relatorio_churn_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            output_path = os.path.join("exports", filename)
            os.makedirs("exports", exist_ok=True)
            
            exporter = PDFExporter()
            success = exporter.export_dashboard(df, kpis, charts, output_path, periodo)
            
            if success and os.path.exists(output_path):
                with open(output_path, "rb") as f:
                    st.download_button(
                        label="📥 Baixar PDF",
                        data=f,
                        file_name=filename,
                        mime="application/pdf",
                        width="stretch"
                    )
                st.success("✅ PDF gerado com sucesso!")
            else:
                st.error("Erro ao gerar PDF. Verifique os logs.")