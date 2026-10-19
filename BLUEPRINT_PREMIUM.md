# Blueprint Premium — Dashboard Churn Teleco

> Ordem exata de construção (o "mapa de 30 minutos") aplicada a este projeto.

## 1. Layout
| Zona | Componente | Fonte |
|---|---|---|
| Sidebar | Filtros (mês/UF/região/plano/RV), toggle de tema dark/light, alertas premium | `src/sidebar_manager.py`, `src/alerts.py` |
| Header de página | Título 1.9rem/700 + eyebrow mutado + hairline border | `.page-head` (CSS tema) |
| Linha 1 | Tendência mensal hero (520px, largura total) | `line_churn_trend` |
| Linha 2 | Donut composição (500) + Top planos barras (500) — **alturas iguais** | `donut_*`, `bar_churn_by_dim` |
| Linha 3 | RV empilhado (500) + Top UFs (500) | `stacked_*`, barras UF |
| Linha 4 | Mapa Brasil coroplético (580, largura total) | `map_uf_churn` |
| Tabs | Visão Executiva / Causas / Equipes / Tendências& Cohort | styling tema |

## 2. Estilo de visualização de dados
- Locale pt-BR forçado: `layout.separators = ",."` (ticks, hovers, texttemplate, treemap): `1.234` / `12,3%`.
- Cards brancos (`paper = surface`) sobre fundo esmeralda do app — borda 1px, radius 14px, sombra sutil.
- Títulos dos gráficos **todos alinhados à esquerda** (x=0.02, 22px).
- Escalas de heatmap/mapa pastel-claras → texto escuro legível nos dois temas.
- Barras de valor rótuladas `pt-BR`, hover uniforme (fonte 15px, fundo surface).

## 3. Dark mode
Tokens `DARK_PREMIUM` (tudo ≥4.5:1 vs superfícies) + botões de hover copper-claro; `config.toml` sincronizado com os tokens light. Toggle de tema troca CSS **e** template Plotly na hora.

## 4. Navegação lateral
Streamlit sidebar + overlay JS mobile (hamburger, `.expanded`), transições 200ms, alvos de toque ≥44px no tablet/mobile (`assets/css/responsive.css`).

## 5. Estados vazios
`.empty-panel`: rótulo em card tracejado com ícone amplo, diagnóstico e instrução (`utils.empty_state`) — vazio nunca parece bug.

## 6. Carregamento
- `show_spinner` no cache de dados + spinner do tema.
- Classes `.kpi-skeleton` / `.skeleton-line` (shimmer 1.3s) disponíveis para futuros blocos pesados.

## 7. Tipografia / movimento
- Inter (400–700) via Google Fonts; h1/h3 padronizados; labels KPI em caps 0.78rem + letter-spacing.
- Entrada fadeUp 450ms nos cards (respeita `prefers-reduced-motion`).

## Resultado honesto
- **Feito e verificado:** alinhamento/uniformização de painéis, contraste AA auditado por script, pt-BR em tudo, dark mode real, cards, animação de entrada, crash do servidor corrigido, API `width=` migrada.
- **Limites:** skeleton só existe como CSS/util (Streamlit renderiza a página inteira de uma vez — não dá para trocar placeholder→gráfico elemento-a-elemento sem fragments); animações de gráfico via Plotly (tween de dados) ficam limitadas à re-renderização; filtragem depende do re-render do Streamlit.
- Nota visual estimada: **8,5–9/10** — teto realista para Streamlit sem fragments/custom components.
