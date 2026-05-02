# 06 — Optimization Playbook (diagnóstico, daily/weekly/monthly, benchmarks)

> Carregue este arquivo quando o usuário pedir para otimizar uma conta, fazer auditoria, planejar próximos passos, ou quando quiser referência de cadência operacional.

---

## 1. Diagnóstico em 30 minutos (auditoria rápida)

Workflow para ler uma conta nova ou problemática rápido. Use os CSVs/UI nesta ordem:

### Passo 1 — Visão geral (5 min)

| Olhar | O que procurar |
|---|---|
| Performance Tab → últimos 30d | Tendência de Conv, CPA, CTR vs período anterior |
| Recomendações (Recommendations Tab) | Score de otimização, mas tomar com cuidado (muitas são pró-Google, não pró-conta) |
| Account-level alertas | Disapprovals, limiteds, falta de budget |

### Passo 2 — Onde vai o dinheiro (5 min)

| Olhar | Sintomas |
|---|---|
| Campanha → Cost (descrescente) | Top 3 campanhas concentram quanto? Concentração saudável: 60–80% nas top 3 |
| Campanha → Conv. count (descrescente) | É a mesma ordem do Cost? Se não, investigar gap |
| Campanha → CPA | Variação 3–5× entre campanhas é normal; >10× é red flag |

### Passo 3 — Quality Score audit (5 min)

| Olhar | Sintoma |
|---|---|
| Keywords filtrar por QS | % de keywords com QS ≤ 5? Se > 30%, é grande oportunidade |
| Keywords com gasto top 10 | QS deles? Se ≤ 6, atacar PRIMEIRO (alto ROI de melhoria) |

### Passo 4 — Search Terms (10 min)

| Olhar | Ação |
|---|---|
| Search Terms → Cost descrescente, Conv = 0 | Candidatos a negative |
| Search Terms → Conv > 5, alto CTR | Candidatos a promote para exact |
| Search Terms → "free", "DIY", "tutorial", "salary", "jobs" | Lista de negatives óbvias |

### Passo 5 — Ad copy & extensions (3 min)

| Olhar | Sintoma |
|---|---|
| Ad Strength por ad group | Quantos com "Poor" ou "Average"? Esses precisam refresh |
| Sitelinks / Callouts / Snippets | Todos preenchidos? Mín 6 sitelinks, 8 callouts |
| Extensions com Impr = 0 | Não estão servindo — investigar (rejeição? baixo Ad Rank?) |

### Passo 6 — Auction Insights (2 min)

| Olhar | Sintoma |
|---|---|
| Top 3 competidores | Quem domina overlap rate? |
| Position Above Rate | > 50% para todos = você está abaixo, atacar Ad Rank |
| Abs Top IS em Brand | < 60% = competidor comprando seu nome |

### Outputs do diagnóstico

Após 30 min você deve ter:

1. **3 maiores fontes de waste** (com $ quantificado).
2. **3 maiores oportunidades** (com $ ou volume estimado).
3. **3 ações imediatas** (essa semana).
4. **3 ações estruturais** (próximas 4 semanas).

---

## 2. Cadência operacional

### Diário (5 min) — Anomaly check

Rode automatizado (script + email/Slack alert) ou check manual.

**Triggers de alarme:**
- CPA diário > 1.5× CPA média trailing 14d.
- Gasto diário > 1.3× gasto médio trailing 14d.
- Conv = 0 em campanha com histórico de >3 conv/dia.
- CTR diário < 50% da média.
- Bid limited / budget limited de novas campanhas.

**Causa comum:** tracking quebrado, landing fora do ar, rejeição de ad.

### Semanal (60–90 min)

**Bloco 1 — Search Terms (20 min)**
- Mineração de top 100 search terms por gasto.
- Adicionar 5–20 negatives.
- Promover 1–3 search terms top performers para exact.

**Bloco 2 — Quality Score & Ad Performance (15 min)**
- Filter keywords QS < 6 com gasto > $X.
- Avaliar ad relevance / landing page experience flag.
- Pausar headlines com "Low" performance rating.

**Bloco 3 — Bid review (15 min)**
- Em Smart Bidding: ajustar **target** se Conv volume não bate (não mexer toda semana).
- Em Maximize Clicks/Manual: ajustar bids granular se necessário.
- Verificar IS Lost (Budget) e (Rank) por campanha.

**Bloco 4 — Extensions (10 min)**
- Quais sitelinks têm 0 impr? Pausar/substituir.
- Adicionar callouts sazonais se aplicável.
- Verificar location extension (GBP linkado).

**Bloco 5 — Audience review (5 min)**
- Performance dos audience signals em PMax.
- Listas de Customer Match atualizadas (refresh recomendado a cada 30d).

### Quinzenal (90 min)

- **Realocação de budget**: campanhas batendo target com IS limited (Budget) → subir 20%; campanhas com CPA muito acima do alvo → cortar ou pausar.
- **Auction Insights**: deep-dive em mudanças de competidor.
- **Decisão de testes A/B**: definir próximo experiment.
- **Asset refresh em PMax**: rodar Asset Reporting, substituir baixo desempenho.

### Mensal (3–4 horas)

**Bloco 1 — Análise estratégica (60 min)**
- KPIs do mês vs metas vs mês anterior.
- Tracking de progresso de testes ativos.
- Decisões de bid strategy (migrar para tROAS? adicionar target tROAS?).
- Plano para o mês seguinte.

**Bloco 2 — N-gram analysis (30 min)**
- Rodar `scripts/n_gram_analysis.py` em search terms últimos 30d.
- Adicionar lote de negatives + promover top n-grams.

**Bloco 3 — Auction Insights review (30 min)**
- Mudanças entre competidores.
- Brand defense status.
- Identificação de novas threats.

**Bloco 4 — Reporting (60 min)**
- Gerar `.docx` com `scripts/build_report.py` (interno) e `scripts/build_report_cliente.py` (cliente).
- Apresentar findings para stakeholder.

**Bloco 5 — Tracking review (15 min)**
- Conv actions: Primary corretas? Valor up-to-date?
- Enhanced Conversions: status "active" e match rate > 70%.
- DDA: status ON.

### Trimestral (1 dia)

- Auditoria estrutural completa.
- Revisão de match types & keyword strategy.
- Account-level negatives review.
- Customer Match list cleanup.
- Reorganização de campanhas/ad groups se necessário.
- Budget allocation review com base em ROI por campanha.

---

## 3. Diagnóstico avançado por sintoma

### Sintoma: "CPA subiu de US$ 50 para US$ 80 em 30 dias"

Decomposição:

```
CPA = Cost / Conv

CPA subiu se:
  - Cost subiu (mais clicks, mesmo conv) → CPC subiu OU CTR subiu sem conv subir
  - Conv caiu (mesmo cost) → CR caiu
  - Ambos
```

**Investigar em ordem:**

1. **Tracking** — Conv volume despencou em data específica? (Verificar implementação tag, mudanças de site).
2. **CPC** — subiu? Auction Insights → competição entrou? QS caiu?
3. **CR** — caiu? Search Terms relevant? Landing page mudou? Form mudou? Speed?
4. **Mix** — campanha cara virou maior fatia? (PMax escalou?)
5. **Sazonalidade** — comparar com mesmo mês ano anterior.

### Sintoma: "CTR alto (8%) mas conv. rate baixíssimo (1%)"

Diagnóstico: **clickbait** ou **mismatch ad↔landing**.

**Ações:**
- Auditar headlines: prometendo algo que landing não entrega?
- Search Terms: queries irrelevantes clicando? (Negatives).
- Landing: message match com a query / headline?
- Form: muito longo? Friction?

### Sintoma: "Volume estagnado há 2 meses, target batido"

Diagnóstico: oportunidade de **escalar**.

**Ações em ordem:**
1. **Subir tCPA em 15%** ou **cortar tROAS em 10%** — abre headroom de leilão.
2. **Verificar IS Lost (Budget)** — se > 20%, subir budget primeiro.
3. **Adicionar match types broader** — phrase → phrase + broad em campanha discovery.
4. **Adicionar Search Themes** em PMax existente.
5. **Expandir geos** (se geos vizinhos têm mesmo perfil de cliente).
6. **Lançar PMax** se ainda não tem.

### Sintoma: "Brand campaign tem CPA US$ 8 e Non-Brand US$ 80"

Esse é o caso normal! Brand é defesa de quem já te conhece. Mas:

**Verificar:**
- Brand está com Abs Top IS > 80%? Se < 60%, competidor comprando seu nome.
- Brand está canibalizando organic? **Em geral, não** — quem clica no ad clica no organic se ad não estiver lá. Mas testar pausing por 2 semanas se quer evidência (cuidado: competitors podem tomar o slot).

### Sintoma: "Ad Strength 'Poor' em todas RSAs, não consigo subir"

**Causas comuns:**
1. Keyword não aparece em headlines.
2. Headlines repetitivas (mesmas palavras várias vezes).
3. Pinning excessivo.
4. Falta de CTAs / benefits / unique angles.

**Solução**: refazer com 15 headlines diversas seguindo os templates de `04-campaign-creation.md`.

---

## 4. Realocação de budget (framework)

### Princípio

**Mova budget de campanhas com `CPA Real / CPA Alvo > 1.3` para campanhas com `< 0.8`**, mas nunca aumente uma campanha em mais de 30% de uma vez (reseta learning).

### Tabela de decisão

| CPA real / CPA alvo | Conv. trend (vs mês anterior) | Ação |
|---|---|---|
| < 0.8 | Estável ou crescente | Subir budget +20% |
| < 0.8 | Decrescente | Investigar (saturação?), manter por mais 14d |
| 0.8 – 1.2 | Qualquer | Manter |
| 1.2 – 1.5 | Estável ou crescente | Apertar tCPA -10% antes de cortar budget |
| > 1.5 | Decrescente | Cortar 30% ou pausar |

### Exemplo prático

```
Campanha A: budget $30/dia, CPA US$ 35 vs alvo US$ 40, IS Lost (Budget) = 25% → SUBIR +20% = $36/dia
Campanha B: budget $30/dia, CPA US$ 70 vs alvo US$ 50, conv caindo → CORTAR -30% = $21/dia OU pausar
Total: -$3/dia (sobra para teste novo ou Display Remarketing)
```

---

## 5. Benchmarks 2026 (para sanity check)

### Cross-industry medianas Search

| Métrica | Mediana 2026 | Trend YoY |
|---|---|---|
| CPC | US$ 4,22 | +12% |
| CTR | 6,11% | +7% |
| Conv. Rate | 7,04% | -9% |
| CPA | US$ 53,52 | +6% |

**Insight 2026:** CPC subiu mais que CPA → conversion rate (page-side) **amorteceu** o impacto do CPC. Onde a page não acompanhou, CPA explodiu. **Landing pages viraram o gargalo.**

### Por vertical (medianas)

| Vertical | CPC US$ | CTR | Conv Rate | CPA US$ |
|---|---|---|---|---|
| Local Services / Home Services | 3–8 | 5–8% | 8–15% | 30–80 |
| E-commerce | 0,80–3 | 2–6% | 1–4% | 25–80 |
| B2B SaaS | 3–8 | 3–6% | 2–6% | 80–250 |
| Legal | 6–15+ | 4–8% | 3–8% | 80–200+ |
| Health & Wellness | 1–4 | 5–10% | 5–12% | 30–100 |
| Automotive (Service) | 2–5 | 6–10% | 8–14% | 25–70 |
| Education | 2–5 | 4–7% | 3–8% | 50–150 |
| Real Estate | 1–4 | 5–8% | 3–7% | 50–150 |
| Finance/Insurance | 5–15 | 4–7% | 4–10% | 80–250 |

**Não use estes números como meta** — meta vem da economia do cliente. Use como **sanity check**: "minha conta está em CPA US$ 200 numa vertical onde a mediana é US$ 50 → algo está muito errado, ou o cliente é um caso muito atípico (justificar)".

### CTR por posição (search)

- Posição 1 (Abs Top): 30–40% CTR (em search com intent forte).
- Posição 2: 12–18%.
- Posição 3: 6–10%.
- Posição 4+: 3–6%.

Esse decay justifica investimento em Quality Score / extensions para subir posição.

---

## 6. Anti-padrões em otimização

| Anti-padrão | Por quê é ruim | Faça |
|---|---|---|
| Mexer em tCPA toda semana | Reset learning, conv. trend caótica | Mexer no máximo a cada 14d |
| Pausar campanhas/keywords toda semana | Dados não acumulam, decisão é prematura | Esperar 14d de dados |
| Negativar 1 search term ruim e ignorar n-gram | Trabalho infinito, baixo impacto | N-gram analysis quinzenal |
| Aplicar todas Recomendações do Google | Muitas são para Google, não pra você | Avaliar ROI de cada uma |
| Ignorar Quality Score ("Smart Bidding cuida disso") | QS afeta CPC efetivo, não só posição | Atacar QS<6 sempre que possível |
| Comparar CPA mês com mês sem ajustar mix | Mistura mudanças de mix com mudanças de eficiência | Decompor CPA por campanha primeiro |
| Apostar tudo em PMax | Falta de visibilidade, perda de controle | Search base + PMax como complemento |
| "Vou pausar Brand para economizar" | Brand é defesa; pausar = competidor toma | Manter Brand sempre, otimizar custo |
| Mudar copy + landing + bid no mesmo experiment | Não consegue isolar causa | 1 variável por teste |
| Sem dashboard de KPIs | Decisões reativas, não proativas | Looker Studio / planilha automatizada |

---

## 7. Sinais de que a conta precisa de reestruturação (não só otimização)

Otimização incremental não resolve problemas estruturais. Sinais de que está na hora de **reestruturar**:

- Múltiplas verticals/produtos no mesmo conjunto de campanhas (Smart Bidding não consegue aprender padrões distintos).
- 90% das keywords em 2 ad groups (rebalance é urgente).
- Toda a conta em Manual CPC (subaproveitando AI).
- Sem tracking de valor (preso em tCPA quando poderia tROAS).
- Campanha pré-PMax + PMax canibalizando.
- 30+ campanhas com gasto < US$ 5/dia cada (consolidar).
- Performance "lateral" há 6+ meses sem inovação.

---

## 8. Template de plano de otimização

Use este template ao apresentar plano para o cliente.

```markdown
# Plano de Otimização — [Conta] — [Mês]

## Diagnóstico
- Gasto: US$ X. Conv: Y. CPA: US$ Z (target: US$ W).
- 3 sintomas principais:
  1. [sintoma com $ quantificado]
  2. [...]
  3. [...]

## Plano (4 ondas)

### Onda 1 — Esta semana (impacto imediato)
- [ ] Negativar [N] termos identificados (waste estimado: US$ X/mês)
- [ ] Pausar keyword(s) com 0 conv > US$ Y gasto
- [ ] Refresh de RSA em [ad group X] (Ad Strength: Poor → Good)

### Onda 2 — Próximas 2 semanas (correções estruturais)
- [ ] Restruturar ad group X (quebrar em 2)
- [ ] Subir tCPA da campanha Y de $A para $B (ramp gradual)
- [ ] Adicionar Customer Match para excluir clientes existentes

### Onda 3 — Próximas 4 semanas (testes e expansão)
- [ ] Lançar experiment: [hipótese H]
- [ ] Adicionar campanha de [vertical/audience nova]
- [ ] N-gram analysis + lote de negatives

### Onda 4 — Próximos 60 dias (estratégico)
- [ ] Migrar para tROAS após implementar conversion value
- [ ] Implementar OCI para qualificar leads downstream
- [ ] Ativar AI Max em campanhas existentes (após validação)

## Resultados esperados
- Q+30d: CPA cai de US$ Z para US$ Z' (-X%), volume estável ou +Y%.
- Q+60d: testar lift de tROAS / qualidade de leads.
- Q+90d: estrutura limpa, foundation para escalar.
```

---

## 9. Fontes (research 2026)

- [Quality Score 2026 — Optmyzr](https://www.optmyzr.com/blog/google-ads-quality-score/)
- [Benchmarks 2026 — Digital Applied](https://www.digitalapplied.com/blog/google-ads-benchmarks-2026-cpc-ctr-cvr-industry)
- [Benchmarks by Industry 2026 — Foundry CRO](https://foundrycro.com/blog/google-ads-benchmarks-by-industry-2026/)
- [PPC Benchmarks 2026 — WebFX](https://www.webfx.com/blog/marketing/ppc-benchmarks-to-know/)
- [CRO Best Practices 2026 — Aimers](https://aimers.io/blog/conversion-rate-optimization-best-practices)
- [Landing Page Optimization 2026 — SaaS Hero](https://www.saashero.net/google-ppc/google-ads-landing-page-optimization/)
- [N-gram Wasted Spend — Taikun Digital](https://www.taikundigital.com/blog/remove-ppc-waste-n-gram-analysis/)
- [Google Ads Scripts 2026 — groas.ai](https://groas.ai/post/best-google-ads-scripts-2026-install-guide-automation-limits)
