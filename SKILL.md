---
name: google-ads-manager
description: "Google Ads avançado 2026 — estratégia, Smart Bidding, AI Max, pesquisa de keywords, leilão, A/B testing, criação de campanhas, otimização contínua e relatórios em Python/docx."
version: "2.0.0"
author: community
license: MIT

category: marketing
tags:
  - google-ads
  - ppc
  - sem
  - smart-bidding
  - ai-max
  - performance-max
  - keyword-research
  - auction-insights
  - reporting
department: Marketing

models:
  recommended:
    - claude-opus-4-7
    - claude-sonnet-4-6

capabilities:
  - advanced_bidding_strategy
  - keyword_research_and_intent_mapping
  - auction_insights_analysis
  - ab_testing_design
  - campaign_creation
  - negative_keyword_n_gram
  - quality_score_optimization
  - ai_max_migration
  - reporting_automation
  - docx_report_generation

languages:
  - pt
  - en
---

# Google Ads Manager — Edição Avançada 2026

Skill de **alto nível** para gestão de Google Ads em 2026: foco em **estratégia, decisão e diagnóstico**, não em "checklist genérico". Use esta skill quando o usuário pedir análises de conta, criação de campanhas, otimização de CPA/ROAS, pesquisa de keywords, interpretação de Auction Insights, planejamento de testes A/B ou geração de relatórios.

> **Como esta skill funciona:** este `SKILL.md` é o ponto de entrada — leve e sempre carregado. Para temas profundos, leia o arquivo de referência apropriado em `references/`. Para gerar relatórios `.docx`, use os scripts em `scripts/`.

---

## Quando usar esta skill

| Situação | Arquivo a consultar |
|---|---|
| "Cria/restrutura/avalia uma campanha" | `references/04-campaign-creation.md` + `references/01-strategy.md` |
| "Analisa minha conta / CSVs / .docx" | `references/06-optimization-playbook.md` + `references/07-reporting-and-gaql.md` |
| "Por que meu CPA subiu / ROAS caiu?" | `references/03-bidding-and-auction.md` + `references/06-optimization-playbook.md` |
| "Que keywords negativar / pesquisa de palavras" | `references/02-keyword-research.md` |
| "Como testar mudança de copy/lance/landing" | `references/05-ab-testing.md` |
| "Posso ativar/migrar para AI Max?" | `references/01-strategy.md` (seção AI Max) |
| "Gera relatório .docx do mês" | `scripts/build_report.py` (interno) ou `scripts/build_report_cliente.py` (cliente) |
| "Análise de n-grams nos search terms" | `scripts/n_gram_analysis.py` |

---

## Princípios de operação (2026)

Estes princípios moldam **toda recomendação** que você faz. Quando algo no que o usuário descreve violar um deles, levante a bandeira antes de seguir.

### 1. Intent-based, não keyword-based

Em 2026 o sistema do Google opera por **intenção**, não por correspondência literal. Exact match agora cobre variantes de mesma intenção; phrase match cobre paráfrases; broad match é uma engine de descoberta guiada por sinais de conversão. **Negativas viraram o principal mecanismo de controle**, não as match types.

### 2. Smart Bidding precisa de combustível

tCPA quer 30+ conversões/30d para estabilizar. tROAS quer 50+ conversões/30d **com valor**. Maximize Conversions é o "modo de saída do learning phase" — não um destino final. Mudanças >20% em target/budget reiniciam o learning. **Não toque em targets a cada 3 dias.**

### 3. Bid adjustments manuais são quase todos ignorados em Smart Bidding

Ajustes de localização, dispositivo, audiência, schedule — o algoritmo **já considera tudo internamente**. As exceções que ainda funcionam: `-100%` (exclusão total) e ajustes em campanhas de Maximize Clicks/Manual CPC. Se você ver "+20% mobile" numa campanha em tCPA, isso só esticou o CPA-alvo em mobile.

### 4. Quality Score é dinheiro real

Subir QS de 5 para 7 reduz CPC efetivo em **>40%**. 36% das keywords no mercado estão em QS≤5 — esse é dinheiro queimado. Os 3 componentes: expected CTR (qualidade do anúncio), ad relevance (estrutura do ad group), landing page experience (velocidade + message match).

### 5. Tracking é a fundação

Em 2026, **DDA (Data-Driven Attribution) é default**. Sem Enhanced Conversions + tagueamento sólido, Smart Bidding está dirigindo cego. Para leads, Enhanced Conversions for Leads + offline conversion import (CRM → Google) é obrigatório acima de US$ 50/dia.

### 6. PMax e AI Max são potentes mas precisam de borda

PMax sem search themes + negativas + exclusões de placement vira "escoadouro de budget para tráfego incremental duvidoso". Search themes (até 50/asset group em 2026) + negative keywords no nível de conta + Account-Level Placement Exclusions (lançado jan/2026) são os 3 controles obrigatórios.

### 7. Match types ainda existem — mas o papel mudou

- **Exact**: keywords-rainha (10–20+ conv com bom CPA), brand defense, tópicos de alto custo onde precisamos de teto.
- **Phrase**: principal motor de growth na maioria das contas; equilibra reach e relevância.
- **Broad**: discovery — só com tracking sólido + 50–100 conv/mês na campanha + Smart Bidding maduro.

### 8. Estrutura: STAG > SKAG (na maioria dos casos)

SKAGs morreram para 90% das contas. STAGs (Single-Theme Ad Groups, 5–15 keywords por intenção) alimentam Smart Bidding e RSAs. SKAGs ainda fazem sentido para keywords-rainha de altíssimo volume + alto CPC onde controle granular paga o esforço.

---

## Fluxo de trabalho recomendado

### A. Diagnóstico de conta existente

1. **Contexto**: pergunte/confirme — vertical, objetivo (leads/ROAS), ticket médio, mercado/geo, budget mensal, sazonalidade.
2. **Leia os dados**: CSVs do Google Ads (campaigns, ad groups, keywords, search terms, locations, devices, hourly, auction insights). Se o usuário tem .docx de meses anteriores, leia para entender histórico.
3. **Aplique o `references/06-optimization-playbook.md`** — seção "Diagnóstico em 30 minutos". Marque sintomas → causas prováveis → testes para validar.
4. **Quantifique**: quanto está sendo desperdiçado (zero-conv waste), qual a oportunidade (top performers sub-budgetados), gargalo principal (tracking? copy? landing? estrutura?).
5. **Apresente em 3 partes**: Panorama → Problemas → Plano de ação priorizado por impacto/esforço.

### B. Criação de campanha do zero

Siga o passo-a-passo de `references/04-campaign-creation.md`. Resumo:

1. Definir objetivo de conversão e valor (mesmo que estimado) → habilita tROAS no futuro.
2. Mapear intenção (problem-aware → solution-aware → product-aware → brand-aware) → uma campanha por estágio quando budget permite.
3. Estrutura: 1 campanha por intenção × geo × tipo de produto. STAGs com 5–15 keywords / 1 tema cada.
4. Match types: começar com **Phrase + Exact**. Broad só quando houver dados.
5. RSA: 12–15 headlines, 4 descriptions, **sem pinning** (a menos que haja motivo legal/branding). Variar ângulos.
6. Extensões: sitelinks (mín. 6, com descrição), callouts (mín. 8), structured snippets, calls (se faz sentido), location.
7. Lance: começar em **Maximize Conversions com tCPA-cap** (sem cap se ≤20 conv/mês de histórico). Migrar para tCPA puro após 30 conv/30d.
8. Negativas: lista inicial agressiva (free, jobs, salary, DIY, tutorial, courses) + lista por vertical.
9. Tracking: confirmar conversões primárias vs secundárias. Habilitar Enhanced Conversions.
10. **Não lance sem definir o critério de sucesso e janela de avaliação** (mín. 14 dias para qualquer veredito).

### C. Otimização contínua

Cadência recomendada:

- **Diário (5 min)**: anomalias (CPA dobrou? gasto bateu o cap antes do horário? CTR caiu 30%?). Use script de anomaly detection.
- **Semanal (60–90 min)**: search terms (negativas + promoção a exact), QS<6, ad strength <Good, lances, sitelinks subperformers.
- **Quinzenal**: realocação de budget entre campanhas, revisar Auction Insights, decidir testes A/B.
- **Mensal**: relatório completo (use `scripts/build_report.py`), revisão de attribution, plano para o próximo mês.

Detalhes em `references/06-optimization-playbook.md`.

### D. Geração de relatório `.docx`

Use os scripts em `scripts/`. Eles geram dois formatos:

- **`build_report.py`** — relatório interno completo (10 seções, Auction Insights, alertas internos, lista de negativas).
- **`build_report_cliente.py`** — versão cliente (Montserrat, tom positivo, omite falhas internas, Resumo do Mês como Heading 2 e tópicos como Heading 3 para sumário/TOC).

Ambos usam `python-docx`. Antes de rodar, ajuste o conteúdo das seções com os números do mês. Veja `references/07-reporting-and-gaql.md` para o template completo de relatório e queries GAQL para extrair os dados.

---

## O que NÃO fazer (anti-padrões comuns 2026)

- ❌ Mudar tCPA target em mais de 20% de uma vez (reseta learning).
- ❌ Pinhar headlines em RSA "para garantir copy" (mata ad strength + impede otimização).
- ❌ Criar SKAG de 1 keyword com phrase match em campanha de baixo volume (Smart Bidding fica sem dados).
- ❌ Confiar em ajustes de bid mobile/local em campanhas tCPA/tROAS (ignorados).
- ❌ Rodar PMax sem search themes nem negativas nem exclusões de placement.
- ❌ Subir conversões secundárias para primárias só "para alimentar Smart Bidding" (envenena o sinal).
- ❌ Pausar campanha de Brand para "economizar" — Brand é defesa contra concorrente comprando seu nome.
- ❌ Comparar CPA mensal sem ajustar para sazonalidade ou mudança de mix de campanhas.
- ❌ "Ativar broad match e ver no que dá" sem 50+ conv/mês e tracking sólido.
- ❌ Usar Last Click attribution em conta com jornada multi-touch (em 2026, DDA é default — use).

---

## Snapshot de benchmarks 2026 (Search, cross-industry)

| Métrica | Mediana 2026 | Sinal de saúde |
|---|---|---|
| CPC médio | US$ 4,22 | Depende muito de vertical (legal/finance >US$10, e-comm/local US$1,5–4) |
| CTR | 6,11% | Acima de 4% em search é saudável; <2% pede revisão de copy/QS |
| Conversion rate | 7,04% | Caiu 9% YoY — gargalo migrou de ad para landing |
| CPA médio | US$ 53,52 | Subiu 6% YoY; CPC subiu 12% — page CVR amorteceu |

Verticais (medianas):
- **Home/Local Services**: CPC alto, CPA mediano (~US$ 28 home & garden), demanda forte.
- **Legal**: CPC US$ 6–15+, CPA US$ 80–200+.
- **B2B SaaS**: CPC US$ 3–8, CPA US$ 80–250.
- **E-commerce**: CPC US$ 0,80–3, ROAS-alvo 3–5x.

Use estes benchmarks como **referência para sanity check**, não como meta. Meta sempre vem do **modelo de unidade econômica do cliente** (LTV / payback period).

---

## Estrutura desta skill

```
google-ads-manager/
├── SKILL.md                            # este arquivo (entry point)
├── references/
│   ├── 01-strategy.md                  # Smart Bidding, AI Max, attribution, audiences
│   ├── 02-keyword-research.md          # Intent mapping, match types, n-gram, SQR mining
│   ├── 03-bidding-and-auction.md       # Bidding strategies, Auction Insights
│   ├── 04-campaign-creation.md         # Step-by-step setup, RSA, extensions, negatives
│   ├── 05-ab-testing.md                # Experiments, significance, design
│   ├── 06-optimization-playbook.md     # Daily/weekly/monthly + diagnóstico
│   └── 07-reporting-and-gaql.md        # GAQL queries + Python report templates
└── scripts/
    ├── build_report.py                 # Relatório interno completo (.docx)
    ├── build_report_cliente.py         # Relatório cliente (Montserrat, Heading 2/3)
    ├── n_gram_analysis.py              # N-gram analysis dos search terms
    └── README.md                       # Como usar os scripts
```

---

## Como interpretar os números (regras de bolso)

- **Impression Share Lost (Budget) > 20%** → orçamento subdimensionado para a demanda (ou tCPA muito agressivo).
- **Search IS Lost (Rank) > 30%** → QS baixo ou bid muito conservador → atacar QS antes de subir bid.
- **Absolute Top IS < 30%** em brand campaigns → competidor comprando seu nome — defenda agressivamente.
- **Overlap rate > 50% com X concorrente** → competidor direto; estudar copy e landing dele.
- **CTR mobile <50% do desktop** → landing não-responsiva ou copy não otimizada para tela pequena.
- **Conv. rate cai >25% MoM mantendo o resto** → suspeitar de tracking quebrado **antes** de copy/landing.
- **CPA semanal sobe e CTR também sobe** → match expansion trouxe tráfego pior; focar em negatives.
- **CPA subiu mas CTR caiu** → competição aumentou ou QS caiu; ver Auction Insights.

---

## Output esperado por tipo de pedido

### "Analisa minha conta"
1. **Panorama (3 frases)**: gasto, conversões, CPA, tendência vs mês anterior.
2. **Top 3 sintomas** com evidência numérica (ex: "Campanha X gastou US$60 sem conversões em 30d").
3. **Plano em ondas**: imediato (semana 1), médio (semana 2–4), estrutural (mês 2+).
4. **Ofereça gerar `.docx`** com `scripts/build_report.py`.

### "Cria uma campanha"
1. Confirme: vertical, geo, budget/dia, ticket/CPA-alvo, conversão primária.
2. Entregue YAML estruturado + RSAs prontas + lista de negativas + extensões.
3. Aponte critério de sucesso e janela de avaliação.

### "Por que CPA subiu?"
Diagnóstico estruturado:
- Volume mudou? (conv↓ → CPA↑)
- CTR mudou? (problemas de copy/QS)
- CPC mudou? (Auction Insights — competição? QS↓?)
- Mix de campanhas mudou? (campanha cara virou maior fatia?)
- Tracking ok? (testar enhanced conversions, conferir tag)

Sempre quantificar antes de prescrever.

---

*Google Ads Manager v2.0 — focado em decisão estratégica, não em checklist.*
