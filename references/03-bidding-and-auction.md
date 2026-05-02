# 03 — Bidding Strategies e Auction Insights

> Carregue este arquivo quando o usuário perguntar sobre estratégia de lance, ajustes, leilão, competição, Auction Insights ou impression share.

---

## 1. Quality Score e Ad Rank em profundidade

### Como Ad Rank é calculado (em cada leilão, em real-time)

```
Ad Rank = bid × Quality Score signals × extension impact × auction-time signals
```

**Quality Score signals** (visíveis no relatório de keyword, mas o real é dinâmico):
1. Expected CTR
2. Ad relevance
3. Landing page experience

**Auction-time signals** (você não vê, mas afetam):
- Device do user
- Localização exata
- Time of day
- Histórico recente do usuário
- Match type usado
- Ad format/extensions exibidos

### O peso do Quality Score na economia

Tabela conservadora (varia por vertical):

| QS | CPC efetivo (vs QS=10) |
|---|---|
| 10 | 1.0× (menor) |
| 7 | 1.4× |
| 5 | 2.0× |
| 3 | 4.0× |

**Sair de QS 5 para QS 7 reduz CPC em ~40%**. Em conta com US$ 20.000/mês, isso libera US$ 8.000 sem aumentar budget.

**36% das keywords no mercado em 2026 estão em QS≤5** — esse é o dinheiro mais fácil de recuperar em qualquer auditoria.

### Como atacar cada componente

#### Expected CTR
- Reescrever RSAs com **15 headlines diversas** (benefit, feature, social proof, CTA, urgency, differentiator).
- Garantir que **a keyword principal do ad group apareça em headlines** (Dynamic Keyword Insertion ou hard-coded).
- Pausar headlines com baixo "preferences" / "low" rating.
- Ad Strength **Excellent** dá +15% CTR vs Poor (Google data).

#### Ad Relevance
- Reduzir keywords por ad group se diversidade de tema for alta. **Se um ad group tem keywords sobre "kanban" e "gantt chart", quebre em 2.**
- Keywords no headline da RSA.
- Description com a "promessa" alinhada à keyword.

#### Landing Page Experience
- **Velocidade é a #1**: caindo de 5s para 2s, QS sobe 2–3 pontos em poucas semanas (caso real).
- **Message match**: H1 da landing repete (com sinônimo) a keyword/headline do ad.
- Mobile-first design (>60% do tráfego em search é mobile na maioria das verticals).
- Form acima da dobra ou CTA claro acima da dobra.
- Sem pop-ups intrusivos (Core Web Vitals penaliza).
- HTTPS, política de privacidade, contato visível (sinais de confiança que Google avalia).

### Métrica oculta: histórico

Quality Score **persiste** ao longo do tempo. Uma keyword com 6 meses de histórico forte aguenta um ad ruim por algumas semanas; keyword nova é avaliada quase só por sinais imediatos.

**Implicação**: ao migrar campanha, **prefira reusar a campanha existente** (pausando keywords ruins) em vez de criar nova do zero. Você joga fora todo o histórico de QS.

---

## 2. Bidding Strategies — escolha por contexto

### Decisão flowchart

```
Tem ≥30 conversões/mês na campanha?
├── Não → Maximize Conversions (sem cap, ou com cap 1.5× CPA-alvo)
│         OU Maximize Clicks (se prioridade é tráfego/awareness)
│
└── Sim → Tem valor por conversão (revenue ou estimado)?
          ├── Não → Target CPA
          │         (target = CPA atual × 1.0 a 1.1)
          │
          └── Sim → Target ROAS
                    (target = ROAS atual × 0.9 para começar)
```

### Detalhes operacionais

**Maximize Conversions**
- Bom para começar e sair do learning phase.
- Sem teto: pode escalar gasto de US$ 30/dia para US$ 80/dia se houver demanda.
- **Sempre** cap o budget para evitar surpresa.

**Maximize Conversions com tCPA cap** (transição)
- Use por 14–30 dias entre Max Conv e tCPA puro.
- Cap = 1.3–1.5× do CPA alvo final.

**Target CPA (tCPA)**
- Stable após 30+ conv/30d.
- Ramp gradual: -10 a -15% a cada 14 dias.
- **Erro**: cair tCPA de US$ 50 para US$ 30 em 7 dias → reset de learning + queda de volume.

**Target ROAS (tROAS)**
- Precisa de **valor** confiável (não só "é uma conversão").
- E-commerce: revenue real. Lead gen: valor médio do lead × probabilidade de fechamento.
- Target inicial: 90% do ROAS atual.
- Mais sensível que tCPA — varia mais com sazonalidade.

**Maximize Clicks**
- Awareness, top-of-funnel, sites informacionais.
- Aceita bid adjustments (raro em Smart Bidding).
- Sem foco em conversão.

**Manual CPC**
- Hoje em 2026: só em casos muito específicos (compliance que proíbe automation, testes A/B de bid, contas com <10 conv/mês onde Smart Bidding não tem dados).

### Portfolio Bidding (estratégia compartilhada)

Permite **agrupar campanhas** no mesmo target/estratégia. Vantagens:
- Aprendizado cruzado: 3 campanhas com 15 conv cada viram "45 conv" para o algoritmo.
- Gestão central: muda 1 target em vez de 3.
- **Pode pareiar com Shared Budget** → +13% conversões em média (Google data).

Quando usar:
- Múltiplas campanhas com mesmo objetivo (mesmo CPA-alvo).
- Volume baixo individual mas total razoável.
- Múltiplos geos com performance similar.

### Shared Budgets

1 budget para múltiplas campanhas. Google distribui por demanda real-time.

**Quando usar:**
- Campanhas com mesmo objetivo + targets similares.
- Você quer dynamic allocation sem micro-gestão.

**Quando NÃO usar:**
- Campanhas com objetivos diferentes (Brand vs Non-Brand).
- Quando você quer garantir minimum budget para uma campanha específica.
- Em experimentos (não compatível).
- Em PMax (não compatível).

**Recomendação de allocation por objetivo:**
- 50–60% conversion-focused (Search exact/phrase, RLSA, Shopping)
- 20–30% prospecting (Search broad, PMax, Demand Gen)
- 10–20% Brand defense

---

## 3. Bid Adjustments — o que ainda funciona em 2026

### A grande verdade: Smart Bidding ignora quase tudo

Em campanhas com tCPA / tROAS / Maximize Conversions:

| Ajuste | Funciona? |
|---|---|
| Device | ❌ ignorado (exceto -100%) |
| Location | ❌ ignorado (exceto -100%) |
| Demographic | ❌ ignorado (exceto -100%) |
| Audience | ❌ ignorado (Smart Bidding já vê isso) |
| Ad Schedule (dayparting) | ❌ ignorado |

### O que ainda **funciona**:

1. **Exclusion (-100%)**: bloqueia totalmente o segmento. Útil para:
   - Excluir mobile em campanha que landing é desktop-only.
   - Excluir geos onde você não atende.
   - Excluir audiences (clientes atuais em campanha de aquisição).

2. **Bid Adjustments em Maximize Clicks / Manual CPC**: aqui sim funcionam normalmente.

3. **Location targeting com targets diferentes**: você cria 2 campanhas idênticas para 2 geos com tCPA diferentes. **Isto sim** dá controle granular de CPA por geo.

### Implicação

Não perca tempo configurando "+20% mobile, -15% noite, +10% feminino entre 25–34" em campanhas com Smart Bidding. **Tudo isso é ruído ignorado.**

### Estrutura como bid adjustment

A forma 2026 de "ajustar lance por geo" é:

```
Antes (legacy):
1 campanha, target Florida + Orlando bid +30%

Agora (2026):
Campanha A: target apenas Orlando, tCPA US$ 40
Campanha B: target Florida ex-Orlando, tCPA US$ 60
```

Isso dá controle real. Mesmo princípio para device, geo, daypart.

---

## 4. Auction Insights — leitura completa

### Métricas explicadas

#### Impression Share (IS)
```
IS = Impressões recebidas / Impressões elegíveis
```
- 80%+ → forte presença, considere PMax/Display para escalar.
- 50–80% → saudável.
- < 50% → algo está limitando — ver IS Lost.

#### Search IS Lost (Budget)
- Quanto você perdeu por **budget**.
- > 20% → orçamento está limitando. Decisão: subir budget (se CPA está bom) ou subir tCPA (se quer mais volume).

#### Search IS Lost (Rank)
- Quanto você perdeu por **Ad Rank** (QS + bid).
- > 30% → QS baixo ou bid muito conservador. **Atacar QS antes** (mais barato e durável que subir bid).

#### Absolute Top Impression Share
- % de vezes que o seu ad apareceu na **posição #1** absoluta (acima de tudo).
- Brand campaigns: ideal **>80%**. < 50% → competidor está comprando seu nome agressivamente.
- Non-Brand: 30–50% saudável.

#### Top Impression Share
- % de vezes que apareceu nas posições topo (1–4).
- Lead gen: alvo 60–80%.

#### Overlap Rate
- Quantas vezes outro advertiser apareceu **no mesmo leilão** que você.
- Identifica competidores **diretos**. Foco no top 3.

#### Position Above Rate
- Quando você e outro estão no leilão, % das vezes que ELE apareceu acima.
- > 50% = ele tem QS+bid melhor que você. Estudar a copy + landing dele.

#### Outranking Share
- % das vezes que VOCÊ apareceu acima do outro (ou ele não apareceu).
- Métrica de "vitória" sobre competidor específico.

### Interpretação por sintoma

| Sintoma | Diagnóstico | Ação |
|---|---|---|
| IS Lost (Budget) > 30% | Demanda > budget | Subir budget se CPA bom; ou apertar tCPA para gastar menos onde converte mais |
| IS Lost (Rank) > 40% | QS ruim ou bid baixo | Atacar Ad Strength + landing speed; testar tCPA mais alto por 14d |
| Absolute Top IS < 30% em Brand | Competidor comprando sua marca | Subir bid em Brand; campanha defensiva agressiva |
| Overlap > 60% com X | Competidor direto | Análise profunda do anúncio + landing dele; diferenciação |
| Position Above Rate > 60% para todos top 5 | Ad Rank fraco geral | Revisão completa: copy, extensions, landing pages |
| Volume estável mas IS caiu | Mercado expandiu (mais elegível, você não cresceu) | Testar broad match cuidadosamente; abrir mais geos |

### Quem comprar Brand do competidor?

**Sim**: se você é challenger num mercado dominado, e tem proposição de valor clara para diferenciar. Use **phrase match** do nome do competidor + copy "compare" + landing dedicada.

**Não**: se o competidor tem brand muito mais forte (você só vai aumentar o CPC dele e o seu).

**Cuidado**: NUNCA use exact match do nome do competidor (Google penaliza). E não use "[Competitor Name]" em headline (contra políticas do Google — termos comerciais protegidos).

---

## 5. Diagnóstico: "Por que meu CPC subiu?"

Em ordem de probabilidade:

### 1. Quality Score caiu
- Conferir QS médio das top 20 keywords (gasto). Caiu? → sim, é isso.
- Causa raiz: novo ad rodando ruim, landing lenta após update, sazonalidade.

### 2. Competição entrou
- Auction Insights: novo player no top 5? Overlap rate aumentou?
- Resposta: revisão completa de copy + extensions + landing.

### 3. Match expansion (close variants)
- Search terms relatório: queries novas que apareceram nas últimas 4 semanas?
- Pode ser que keyword exact agora pegou variants mais caros.
- Resposta: negativar variants ruins.

### 4. tCPA / tROAS apertado demais
- Você reduziu target recentemente? CPC sobe quando algoritmo precisa "comprar" só conv mais caros para hit target.
- Resposta: relaxar target temporariamente.

### 5. Sazonalidade
- Sazonalidade real? (Black Friday, fim do mês, feriados).
- Resposta: usar Seasonality Adjustment se for evento previsível.

### 6. Mudanças de auction structure (Google)
- Updates do Google às vezes recalibram leilões.
- Acompanhar Google Ads blog.

---

## 6. Quando subir / cortar bids (mesmo em Smart Bidding)

Em Smart Bidding **você não muda bid keyword-a-keyword** — você muda **target**.

### Subir tCPA (alvo de CPA mais alto = aceito pagar mais por conv)

- **Quando**: você está battendo o target de longe (CPA real 30% abaixo do alvo) e quer mais volume.
- **Como**: aumentar tCPA em 15–20% e observar 14 dias.
- **Sinal de ajuste**: volume cresce > target ainda batido → bom.

### Cortar tCPA (alvo mais agressivo)

- **Quando**: CPA real está acima do alvo e você precisa apertar.
- **Como**: cortar **gradualmente**, -10 a -15% a cada 2 semanas.
- **Risco**: pode reduzir volume. Se conversões caem proporcionalmente, é redução natural; se caem **mais que proporcionalmente**, target está apertado demais.

### Quando NÃO mexer

- Após mudança recente (espere 14d).
- Em campanhas com volume muito baixo (<10 conv/mês — sinal não confiável).
- Em meio a evento sazonal (espere passar).

---

## 7. Fontes (research 2026)

- [Quality Score — Google Ads Help](https://support.google.com/google-ads/answer/6167118)
- [Quality Score 2026 — Store Growers](https://www.storegrowers.com/google-ads-quality-score/)
- [Quality Score in automation-heavy accounts — Optmyzr](https://www.optmyzr.com/blog/google-ads-quality-score/)
- [Bid Adjustments 2026 — Bigeye](https://www.bigeyeagency.com/insights/google-ads-bid-adjustments-in-2026-what-still-works-whats-changed-and-where-most-campaign-managers-get-it-wrong)
- [Auction Insights — Google Ads Help](https://support.google.com/google-ads/answer/2579754)
- [Auction Insights 2026 — Growth Minded Marketing](https://growthmindedmarketing.com/blog/google-ads-auction-insights/)
- [Auction Insights to Outrank — Search Engine Land](https://searchengineland.com/google-ads-auction-insights-461513)
- [Shared Budgets 2026 — Digital Marketing Knight](https://www.digitalmarketingknight.com/using-shared-budgets-in-google-ads/)
- [Portfolio Bid Strategies — PixelRush](https://pixelrush.io/blog/how-to-use-portfolio-bid-strategies-in-google-ads-and-why-you-should/)
- [Ad Rank 2026 — Digital Marketing Knight](https://www.digitalmarketingknight.com/google-ads-ad-rank-explained/)
