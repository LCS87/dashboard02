# Dashboard B2B Churn - Telecomunicações S/A

> Dashboard analítico premium para monitoramento e análise de churn em clientes B2B do setor de telecomunicações.

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📋 Visão Geral

Este dashboard foi desenvolvido como parte de um trabalho acadêmico para análise de churn em clientes B2B. O sistema processa dados mensais de abandono de clientes corporativos, anonimiza automaticamente dados sensíveis e apresenta visualizações interativas e relatórios executivos profissionais.

### Destaques

- 🎨 **UI/UX Premium**: Design SaaS de alto padrão com tema Floresta & Cobre
- 🌓 **Dark Mode**: Tema escuro otimizado para WCAG AA (acessibilidade)
- 📄 **Exportação PDF**: Geração de relatórios executivos profissionais
- 🔒 **Anonimização Automática**: Mascaramento inteligente de CNPJ, CPF, nomes e dados sensíveis
- 🔄 **Comparação Temporal**: Análise side-by-side entre dois períodos
- ⚠️ **Sistema de Alertas**: Notificações configuráveis baseadas em thresholds
- 📱 **Responsivo**: Funcional em desktop, tablet e mobile
- 📊 **Visualizações Interativas**: 15+ gráficos interativos usando Plotly

---

## 🚀 Funcionalidades

### 1. Sistema de Anonimização Automática

O dashboard implementa um sistema robusto de anonimização que:

- **Mascara CNPJ**: `12.345.678/0001-90` → `12.345.678/****-**`
- **Mascara CPF**: `123.456.789-00` → `123.456.***-**`
- **Anonimiza Nomes**: Gera nomes fictícios consistentes (determinístico)
- **Substitui Empresas**: "V**o" → "Telecomunicações S/A"
- **Mascara Telefone**: `(11) 99999-8888` → `(11) 9****-8888`
- **Mascara Email**: `joao@empresa.com` → `j****@empresa.com`

### 2. Visualizações Premium

O dashboard inclui 15+ gráficos interativos:

| Gráfico | Descrição |
|---------|-----------|
| **Evolução Mensal** | Linha do tempo do churn com animações |
| **Donut Composição** | Voluntário vs Involuntário |
| **Top Planos** | Barras horizontais com top 10 planos |
| **Top UFs** | Mapa coroplético e barras por estado |
| **Top Motivos** | Análise detalhada dos motivos de churn |
| **Heatmap Plano x Motivo** | Matriz de correlação entre planos e motivos |
| **Faixa de Tempo** | Distribuição de tempo de vida do cliente |
| **Cohort Analysis** | Retenção e churn por cohorte de ativação |
| **Scatter RV x Tempo** | Correlação entre chamada de retorno e tempo de vida |
| **Ranking Dealer** | Tabela interativa de performance por dealer |

### 3. Análise de Dados

#### KPIs Principais

- **Total Churn**: Quantidade absoluta de cancelamentos
- **Voluntário/Involuntário**: Classificação e porcentagem
- **RV (Chamada de Retorno)**: Clientes com chamada de retorno
- **Tempo Médio/Mediano**: Duração do relacionamento
- **Churn Precoce**: Cancelamentos em ≤90 dias
- **Concentração**: Top 5 dealers e top 3 motivos
- **Variação MoM**: Mudança mês a mês (%)

#### Níveis de Análise

1. **Visão Executiva**: KPIs gerais, tendências, composição e top clientes
2. **Análise de Causas**: Motivos, planos, tempo de vida e categorias
3. **Performance Equipes**: Ranking de dealers, diretores e gerentes com drill-down
4. **Tendências & Cohort**: Evolução temporal, cohorts e projeção simples

### 4. Sistema de Alertas Configuráveis

O usuário pode configurar thresholds para receber alertas visuais:

| Alerta | Descrição |
|--------|-----------|
| **Total Churn** | Notifica quando ultrapassa limite configurado |
| **% Voluntário** | Alerta quando churn voluntário está muito alto |
| **Tempo Médio** | Avisa quando tempo de vida está abaixo do mínimo |
| **Variação MoM** | Notifica mudanças significativas mês a mês |
| **Churn Precoce** | Alerta quando muitos churns ocorrem em ≤90 dias |

### 5. Comparação Temporal

Permite comparar dois períodos lado a lado:

- Seleção de dois meses para comparação
- KPIs lado a lado com deltas (% e valor absoluto)
- Gráficos comparativos side-by-side
- Resumo visual das variações

### 6. Exportação de Relatórios

#### Exportação PDF

Gera relatórios executivos profissionais com:

- Cabeçalho e rodapé fixos
- Tabela de KPIs
- Gráficos convertidos em imagens
- Top 10 Planos, Motivos e Clientes
- Layout A4 profissional

#### Exportação CSV

Opções para exportar:

- Dados brutos filtrados
- Tabelas resumidas por dimensão
- Detalhamento completo de motivos

### 7. UI/UX Premium

#### Tema Floresta & Cobre

- **Light Mode**: Verde esmeralda (#3F6F5C) e cobre (#C46A2B)
- **Dark Mode**: Fundo escuro (#121B17) com cores adaptadas
- **Contraste AA**: Todos os elementos verificados para acessibilidade

#### Animações

- Fade-in nos cards de KPI
- Scale hover nos métricos
- Animação de counter nos números
- Transições suaves em todos os componentes

#### Sidebar Recolhível

- Toggle expand/recolher
- Persistência no state
- Mobile overlay
- Desktop narrow mode (64px)

#### Responsividade

- Desktop: 1400px max-width com padding generoso
- Tablet (768px-1024px): Ajuste automático
- Mobile: Overlay sidebar e layout em coluna

---

## 🛠️ Stack Tecnológica

### Backend

- **Python 3.10+**
- **Streamlit** (1.35+) - Framework principal
- **Pandas** (2.2+) - Processamento de dados
- **Plotly** (5.22+) - Visualizações interativas
- **NumPy** (1.26+) - Cálculos numéricos

### Exportação

- **ReportLab** (4.0+) - Geração de PDF
- **WeasyPrint** (60+) - Renderização HTML→PDF
- **Pillow** (10+) - Manipulação de imagens

### Anonimização

- **Faker** (24+) - Geração de dados fictícios
- **Hashlib** - Geração de hash determinístico

### Utilitários

- **python-dateutil** - Manipulação de datas
- **pytz** - Suporte a fusos horários
- **openpyxl** - Leitura/escrita de Excel

---

## 📦 Instalação

### Requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

### Passos

1. Clone o repositório ou acesse a pasta do projeto

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Coloque os arquivos CSV na pasta `data/raw/`:

```
data/raw/
├── RelatorioInfoB2B_Churn_abril-maio-junho.csv
├── RelatorioInfoB2B_Churn_maio.csv
└── Relatorio_Info_B2B_Churn_junho.csv
```

4. Execute o dashboard:

```bash
streamlit run app.py
```

5. Acesse em seu navegador: `http://localhost:8501`

---

## 📁 Estrutura do Projeto

```
dashboard02/
├── app.py                    # Entry point principal
├── requirements.txt          # Dependências Python
├── README.md                # Este arquivo
├── LICENSE                  # Licença MIT
│
├── src/
│   ├── __init__.py
│   ├── config.py            # Configurações centrais
│   ├── theme.py             # Sistema de tema (Light/Dark)
│   ├── anonymizer.py        # Módulo de anonimização
│   ├── data_loader.py       # Carregamento de dados
│   ├── data_processor.py    # Processamento e enriquecimento
│   ├── metrics.py           # Cálculo de KPIs
│   ├── charts.py            # Geração de gráficos Plotly
│   ├── utils.py             # Funções utilitárias
│   ├── alerts.py            # Sistema de alertas
│   ├── comparator.py        # Comparação temporal
│   ├── export_pdf.py        # Exportação para PDF
│   └── sidebar_manager.py   # Gerenciamento de sidebar
│
├── data/
│   └── raw/                 # Arquivos CSV originais
│
├── exports/                 # PDFs gerados
├── assets/                  # CSS, JS e assets estáticos
│   ├── css/
│   ├── js/
│   └── fonts/
│
└── tests/                   # Testes unitários (opcional)
```

---

## 🔍 Como Usar

### Navegação

1. **Sidebar**: Use para filtros, configuração de alertas e exportação
2. **Tabs**: Acesse as quatro seções principais
3. **Clique nos gráficos**: Alguns gráficos permitem drill-down clicando nos elementos

### Filtros

No sidebar, você pode filtrar por:

- **Mês/Ano**: Selecionar período específico
- **UF**: Estado brasileiro
- **Região**: Norte, Sul, Nordeste, etc.
- **Categoria de Plano**: Classificação dos planos
- **RV (Chamada de Retorno)**: Sim/Não

### Configurar Alertas

1. Clique em "⚙️ Configurar Alertas" na sidebar
2. Ajuste os thresholds conforme necessário
3. Alertas visuais aparecerão no topo da página

### Comparar Períodos

1. Clique em "🔄 Comparação Temporal" na sidebar
2. Selecione dois períodos (ex: Abril 2025 vs Maio 2025)
3. Habilite a comparação
4. KPIs lado a lado com deltas aparecerão

### Exportar Relatório

1. Clique em "📄 Exportar Relatório" na sidebar
2. Clique em "Gerar Relatório PDF"
3. O PDF será baixado automaticamente

---

## 🎨 Design System

### Cores

| Função | Light Mode | Dark Mode |
|--------|------------|-----------|
| Primary | #C46A2B (Cobre) | #E69857 |
| Accent | #3F6F5C (Verde Esmeralda) | #6FA88A |
| Success | #3D7A5F | #5FA87A |
| Warning | #D4A017 | #E0B84A |
| Error | #C45C4A | #E07A68 |
| Info | #5C8A9F | #7AA8BD |

### Tipografia

- **Primary**: Inter (Google Fonts)
- **Mono**: JetBrains Mono / Fira Code
- **Weights**: 400, 500, 600, 700

### Componentes

- **Cards**: Border radius 12px, sombras suaves
- **Botões**: Border radius 8px, hover effect
- **Inputs**: Border radius 8px, focus ring
- **Gráficos**: Border radius 12px, borda sutil

---

## 📊 Exemplos de Uso

### 1. Análise Mensal Rápida

1. Selecione um mês na sidebar
2. Acesse "📊 Visão Executiva"
3. Observe os KPIs principais no topo
4. Navegue pelos gráficos clicáveis para drill-down

### 2. Investigação de Causas

1. Acesse "🔍 Análise de Causas"
2. Clique no treemap para filtrar por motivo
3. Observe o heatmap Plano x Motivo
4. Analise a distribuição de tempo de vida

### 3. Avaliação de Performance de Equipes

1. Acesse "👥 Performance Equipes"
2. Selecione o nível (Dealer, Diretor, Gerente)
3. Clique em uma barra para drill-down
4. Analise motivos e planos específicos

### 4. Análise de Tendências

1. Acesse "📈 Tendências & Cohort"
2. Observe a evolução mensal
3. Analise a cohort analysis
4. Verifique a projeção simples (média móvel)

---

## 🧪 Testes

Para executar os testes (opcional):

```bash
pytest tests/ -v
```

---

## 📝 Notas Técnicas

### Anonimização

A anonimização é determinística: o mesmo input sempre gera o mesmo output. Isso permite comparações consistentes entre sessões.

### Performance

- **Cache**: Dados processados são cacheados por 1 hora
- **Lazy loading**: Gráficos são renderizados apenas quando necessários
- **Optimized queries**: Queries Pandas otimizadas para grandes datasets

### Limitações Conhecidas

- Dados sensíveis devem ser removidos antes de compartilhar o repo
- Relatórios PDF são gerados no servidor, não no navegador
- Animações complexas requerem navegador moderno

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

## 👨‍💻 Autor

Desenvolvido para análise de churn em clientes B2B do setor de telecomunicações.

---

## 🙏 Agradecimentos

- Streamlit pela excelente framework
- Plotly pelos gráficos interativos
- Comunidade Python pelo ecossistema incrível

---

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório do projeto.

---

**Última atualização:** Outubro 2026
