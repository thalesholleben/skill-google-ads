# 04 — Criação de Campanha (passo-a-passo 2026)

> Carregue este arquivo quando o usuário pedir para criar/restruturar uma campanha, configurar uma nova conta, ou definir estrutura de account.

---

## 1. Antes de tocar no Google Ads — pré-requisitos

Não crie campanha sem responder estas perguntas. Se faltar algo, **fale com o cliente antes**.

| Pergunta | Por quê importa |
|---|---|
| Qual é o objetivo? (lead/sale/install/call) | Define conversion action e bid strategy |
| Qual é o ticket médio (B2C) ou LTV (B2B)? | Define CPA-alvo / ROAS-alvo |
| Margem ou markup? | Sem margem, "ROAS 5x" pode ser prejuízo |
| Geografia do serviço? | Targeting de localização |
| Idioma do público? | Language settings + copy |
| Sazonalidade conhecida? | Calendar + Seasonality Adjustments |
| Site / landing pronto? | Pré-requisito para QS e tracking |
| Tracking implementado? | **GA4 + Google tag + Enhanced Conversions ON** |
| Budget mensal? | Define qual estratégia é viável |
| Concorrentes principais? | Brand defense + Competitor campaigns |
| Diferenciação clara? | Insumo para copy |

### Mínimo para começar

- ✅ Site com HTTPS, política de privacidade, contato visível.
- ✅ Conversion action configurada (com valor, mesmo estimado).
- ✅ Google tag instalada e validada via Tag Assistant.
- ✅ Enhanced Conversions ativada.
- ✅ GA4 linkado com Google Ads (audiences + conversions importadas).
- ✅ Budget ≥ 30× CPA-alvo / mês (regra de bolso para ter dados).

---

## 2. Estrutura de conta — modelos por contexto

### A. Conta de Lead Gen / Local Service (template)

```
Account
├── [Brand] Defesa de Marca
│   └── Ad Group: Brand Terms (exact + phrase)
│
├── [Search] Specific Services — [serviço] — [geo]
│   ├── Ad Group: Service A (5–15 keywords)
│   └── Ad Group: Service B
│
├── [Search] Phone Leads — [serviço] — [geo]
│   └── Ad Group: General (com Call extension prioridade)
│
├── [Search] Competitor — [vertical]
│   └── Ad Group: Competitor [nome] (phrase only)
│
└── [Display/PMax] Remarketing — visitantes
    └── Asset Group: Remarketing
```

### B. Conta E-commerce (template)

```
Account
├── [Brand] Defense
│
├── [Search] Generic — [categoria pai]
│   ├── Ad Group: Subcategoria A (Phrase + Exact)
│   └── Ad Group: Subcategoria B
│
├── [Shopping] Standard
│
├── [PMax] Performance Max
│   └── Asset Groups por categoria/persona
│
└── [Display] Remarketing
```

### C. Conta SaaS B2B (template)

```
Account
├── [Brand] Defense
│
├── [Search] Product-aware
│   ├── Ad Group: Core feature 1
│   └── Ad Group: Core feature 2
│
├── [Search] Solution-aware
│   ├── Ad Group: Use case 1
│   └── Ad Group: Use case 2
│
├── [Search] Problem-aware
│   └── Ad Group: Pain point keywords (phrase + broad com Smart Bidding)
│
├── [Search] Competitor
│
└── [Demand Gen] Top of funnel
```

### Regras de quebra de campanha

Crie **campanha separada** quando:
- Budget precisa ser controlado independentemente.
- Audience é radicalmente diferente.
- Geografia é diferente.
- Ad scheduling é diferente.
- Bid strategy diferente faz sentido (ex: Brand em Max Conv, Non-Brand em tCPA).

Crie **ad group separado** quando:
- Tema/intent é diferente o suficiente para precisar de copy distinta.
- Landing page é diferente.

---

## 3. Setup passo-a-passo (Search campaign — formato YAML para clareza)

```yaml
campaign:
  name: "[Search] Floor Removal — Phone Leads — Orlando"
  type: SEARCH
  
  # === BUDGET & BIDDING ===
  daily_budget: 30 USD
  bid_strategy: MAXIMIZE_CONVERSIONS
  bid_target_cpa: null   # adicionar após 30 conv/30d
  
  # === LOCATIONS ===
  locations:
    target: "Orange County, Florida"  # specific
    radius_targeting: false
    location_options: PRESENCE         # NÃO usar PRESENCE_OR_INTEREST sem motivo
  
  # === LANGUAGES ===
  languages: [en, es]   # incluir Spanish em FL/TX/CA por default
  
  # === NETWORKS ===
  networks:
    google_search: true
    search_partners: false   # iniciar OFF, ligar depois se search é forte
    display: false           # NUNCA em campanha Search ("Display Network for Search" é trap)
  
  # === SCHEDULE ===
  ad_schedule:
    enabled: false   # deixar smart bidding decidir; só ligar se Maximize Clicks
  
  # === DEVICES ===
  devices:
    all_enabled: true
    exclude:
      - tablets:  false   # tablets convertem melhor que esperado em alguns nichos
  
  # === AD ROTATION ===
  ad_rotation: OPTIMIZE
  
  # === FREQUENCY CAPPING ===  
  # Não aplicável a Search; aplicável a Display/PMax/Demand Gen
  
  # === CONVERSION ACTIONS ===
  conversion_actions:
    - "Phone Call (offline OCI)"      # PRIMARY
    - "Form Submit"                   # PRIMARY
    - "Page View Pricing"             # SECONDARY (não otimizar para esta)
  
  # === ATTRIBUTION ===
  attribution_model: DATA_DRIVEN
  conversion_window: 30_days
  
  # === EXCLUSIONS ===
  audience_exclusions:
    - "Existing Customers (Customer Match)"
    - "Recent Form Submitters (last 30d)"
```

---

## 4. Ad Groups e keywords

### Quantos keywords por ad group?

- **STAG (Single Theme Ad Group)**: 5–15 keywords no mesmo tema/intent.
- **SKAG**: 1 keyword (raro em 2026 — só para keywords-rainha de altíssimo volume).

### Estrutura de match types dentro de um ad group

```yaml
ad_group: "Floor Removal Service"
keywords:
  exact_match:
    - "[floor removal]"           # rainha provada
    - "[floor demolition]"
  
  phrase_match:
    - '"floor removal service"'
    - '"floor demolition service"'
    - '"remove old floor"'
    - '"tile removal"'             # subcategoria forte
    - '"hardwood removal"'
  
  broad_match:
    # SÓ se tem 50+ conv/mês na campanha + tracking sólido
    - "floor removal Orlando"
    - "carpet removal contractor"
```

### Negativas no ad group

```yaml
ad_group_negatives:
  - "[free]"           # exact, não negativar phrase "free"
  - "DIY"
  - "tutorial"
  - "video"
  - "rental"           # se você é serviço de remoção, não locação
```

---

## 5. RSA (Responsive Search Ads) — best practices 2026

### Composição mínima

- **15 headlines** (máximo permitido). Diversidade total.
- **4 descriptions** (máximo). Cada uma com angulo diferente.
- **2 RSAs por ad group** com URLs finais diferentes (testar landing).
- **Ad Strength alvo: Excellent** (ou pelo menos Good).

### Distribuição de headlines (modelo)

Dos 15 slots, distribua:

| Categoria | Quantidade | Exemplo |
|---|---|---|
| Keyword headlines | 3 | "Floor Removal Orlando", "Pro Floor Demo Service", "{Keyword:Floor Removal} Experts" |
| Benefit/USP | 3 | "Same-Day Service Available", "Licensed & Insured Crew", "No Mess, No Damage" |
| Social proof | 2 | "5★ on Google — 200+ Reviews", "Trusted by 500+ Homeowners" |
| CTA | 3 | "Get Free Estimate Today", "Call Now (407) XXX-XXXX", "Schedule Free Consultation" |
| Urgency / offer | 2 | "Free Quote in 24 Hours", "Book This Week — Save 10%" |
| Differentiator | 2 | "Family-Owned Since 2008", "Eco-Friendly Disposal Included" |

### Descriptions (4 slots)

```
Description 1 (benefit-focused):
"Professional floor removal in Orlando. Tile, hardwood, carpet, vinyl — we handle it. 
Free estimates. Fully licensed and insured."

Description 2 (process):
"Clean, dust-controlled removal. We protect your home, haul away debris, leave the 
subfloor ready for new install."

Description 3 (CTA + trust):
"Get a written quote in 24 hours. 200+ five-star reviews. Family-owned since 2008. 
Call (407) XXX-XXXX or book online."

Description 4 (urgency / differentiator):
"Same-week service available. Eco-friendly disposal included. No hidden fees. 
Schedule your free consultation today."
```

### Pinning — quando usar (e quando NÃO)

**Pinning é a regra do MENOS é MAIS em 2026.** Pinning impede que Ad Strength seja Excellent — ele cai automaticamente.

**Use SOMENTE quando:**
- Compliance/regulatório obriga (saúde: disclaimer fixo na posição 3).
- Brand guidelines exigem nome da marca em headline 1.
- Você está testando uma headline específica em uma posição (limite a 14 dias).

**NUNCA pinhe:**
- Mais de 1 headline em posição 1.
- Por "preferência pessoal" sem dado.
- Múltiplas headlines (use **multi-pin**: 2–3 headlines disputando uma posição — esse é o uso recomendado quando precisar pinhar).

### Ad Strength — como subir de "Average" para "Good/Excellent"

Componentes que Google avalia (visíveis no painel "Ad Strength"):

1. **Headline diversity** — variar tipos (benefit, feature, CTA, etc).
2. **Including popular keywords in headlines** — keyword principal do ad group em pelo menos 3 headlines.
3. **More unique headlines** — palavras únicas, não repetir mesma palavra em 5 headlines.
4. **Including more headlines** — usar todos os 15 slots.

Ações específicas:
- Headlines com no mínimo 25 caracteres usados (de 30 disponíveis).
- Descriptions com 80–90 caracteres (de 90 disponíveis).
- Cada description termina com CTA ou diferenciador único.

---

## 6. Extensions / Assets (obrigatórias em 2026)

Extensions são **gratuitas** e aumentam CTR em **10–25%**. Em 2026, **Google avalia relevância via extensions** — não usar = penalidade implícita.

### Extensions obrigatórias por campanha

#### Sitelinks (mín. 6, ideal 8)
- **2 linhas de descrição** cada (esse é o formato 2026 de alto desempenho).
- Páginas específicas, não home.
- Exemplos para Floor Removal:
  - "Tile Removal" → /tile-removal | "Same-day quote, no obligation. Pro tile demo crews."
  - "Hardwood Removal" → /hardwood | "Careful removal of nail-down or glue-down floors."
  - "Free Estimate" → /quote | "Online form, response in 1 hour business hours."
  - "Service Areas" → /coverage | "Orange, Seminole, Lake, Osceola counties."

#### Callouts (mín. 8)
Texto curto (até 25 char), não-clicável. Aparece sob a description.

```
"Free Estimates"
"Licensed & Insured"
"Same-Day Service"
"Family-Owned"
"5★ Google Reviews"
"Eco-Friendly Disposal"
"No Hidden Fees"
"Serving Central FL"
```

#### Structured Snippets (mín. 1, ideal 2 categorias)
Listas categorizadas. Google escolhe header, você dá os values.

```
Header: "Service Catalog"
Values: ["Tile Removal", "Hardwood Removal", "Carpet Pulling", "Vinyl Removal", "Subfloor Prep"]

Header: "Brands"  (apenas se vende produto)
Values: [...]
```

#### Call Extension
Para **lead gen com phone como conversão**:
- Phone tracking number (preferencial — mede conversões).
- Mobile-only ON (em campanhas com >70% mobile).
- Schedule (ex: 8h–18h business hours).

#### Location Extension
- Linkar Google Business Profile.
- Mostra mapa + endereço + horários nos ads.
- Crítico para local services.

### Hierarquia de extensions (2026)

```
Account level   → evergreen (Free Estimates, Licensed, etc)
Campaign level  → tema (campanha de "Tile" tem callouts específicos de tile)
Ad Group level  → tático (oferta atual, sazonal)
```

Google agora **mistura extensions de níveis diferentes** no mesmo ad — então usar todos os níveis é vantagem, não conflito.

---

## 7. Negativas — lista inicial de lançamento

Antes de ligar a campanha, configure **lista universal de negativas** no nível de conta:

```yaml
universal_negative_keywords:
  - free
  - gratis
  - grátis
  - download
  - torrent
  - crack
  - pdf
  - jobs
  - vagas
  - careers
  - salary
  - salário
  - tutorial
  - course
  - courses
  - certification
  - training
  - DIY
  - "how to"        # phrase match — bloqueia "how to remove floor yourself"
  - youtube
  - reddit
  - quora
  - forum
  - meaning
  - definition
  - "what is"
  - kid
  - kids
  - children
  - student
```

Adicione lista vertical-específica:

```yaml
local_services_negatives:
  - rental
  - locação
  - "rent a"
  - "video tutorial"

ecommerce_negatives:
  - used
  - segunda mão
  - refurbished
  - cheap
  - barato        # se não é seu posicionamento

b2b_negatives:
  - personal use
  - student
  - individual
  - "open source"

legal_services_negatives:
  - "free consultation"   # se você cobra
  - pro bono
  - aid
  - legal aid
```

---

## 8. Tracking checklist antes de ligar

Sem isso, **não ligue** a campanha. É melhor adiar lançamento 3 dias do que rodar 30 dias com tracking quebrado.

- [ ] Google tag instalado em todas as páginas (Tag Assistant valida).
- [ ] Conversion action criada e linkada (Phone Call, Form Submit, etc).
- [ ] Conversion action marcada como **"Primary"** (apenas as que você quer otimizar).
- [ ] Conversion category correto (Lead / Purchase / etc).
- [ ] Valor de conversão preenchido (mesmo que estimado — usa para Smart Bidding).
- [ ] Enhanced Conversions ON (envia hashed user data).
- [ ] GA4 linkado a Google Ads.
- [ ] Audiências do GA4 importadas.
- [ ] Test conversion: fazer 1 conv real (form submit / call), validar que aparece em Google Ads em até 24h.

---

## 9. Lançamento — primeiros 14 dias

### Dia 0 (lançamento)
- Pré-budget travado.
- Pré-negativas universais aplicadas.
- 2 RSAs por ad group, Ad Strength ≥ Good.
- Extensions todas configuradas.
- **Bid strategy: Maximize Conversions** (sem cap nas primeiras 72h, depois com cap se gasto subir muito).

### Dias 1–3 (monitor agressivo, ajustar pouco)
- Verificar se ads estão servindo (Search Terms já mostra impressões).
- Detectar tracking quebrado (clicks > 50, 0 conversões aparecendo → suspeita).
- Identificar negativas evidentes (search terms claramente irrelevantes).

### Dias 4–7
- Adicionar negatives baseado em search terms.
- Pausar headlines com "Low" rating.
- Verificar Quality Score baseline.

### Dias 8–14
- Primeira leitura séria de performance.
- Se 10+ conversões → continuar Maximize Conversions com cap.
- Se 30+ conversões → migrar para Maximize Conversions com tCPA cap.
- Decidir: dia 14 vai para tCPA puro? (precisa 30+ conv).

### Dia 14 — review formal
- Se está atingindo CPA esperado → tCPA puro, target = CPA atual × 1.0.
- Se CPA muito acima → ajuste de copy / negatives / targeting.
- Se 0 conversões em 14 dias com 50+ clicks → reavaliar landing/copy/oferta. Pausar e replanejar.

---

## 10. PMax — setup avançado 2026

### Quando vale criar PMax

- Existe Search rodando bem (Smart Bidding aprendeu sinais).
- Você tem assets de qualidade (imagens, video, copy variado).
- Conversion tracking sólido.
- ≥ US$ 30/dia para a PMax (abaixo, dados são fracos).

### Estrutura de Asset Groups

**1 PMax campaign, múltiplos asset groups por:**
- Categoria de produto/serviço.
- Audience persona.
- Estágio do funnel.

```yaml
pmax_campaign:
  name: "[PMax] Floor Removal — Orlando"
  budget: 40 USD/dia
  bid: tCPA $50
  
  asset_groups:
    - name: "Tile Removal — Homeowners"
      audience_signal:
        custom_segments: ["tile removal", "kitchen renovation"]
        in_market: ["Home Improvement"]
        your_data: ["Site Visitors 30d"]
      headlines: 15 variações tile-focadas
      descriptions: 4
      images: 10–20
      videos: 2–5 (autogen ou próprios)
      logos: necessário
      search_themes:    # NEW 2026 — até 50/asset group
        - "tile removal Orlando"
        - "remove kitchen tile"
        - "professional tile demolition"
        # ... até 50
    
    - name: "Hardwood Removal — Homeowners"
      # ...similar
    
    - name: "Carpet Removal — Property Managers"
      audience_signal:
        custom_segments: ["property management software"]
        # ...
```

### Search Themes — controles essenciais 2026

Search Themes (até 50/asset group em 2026) **são keywords-like signals** para PMax. Sem eles, PMax sai pela tangente.

**Distribuição recomendada (de 30–45 themes total):**
- 20–30 core themes baseados em intenção provada (do search terms da Search campaign).
- 15–20 discovery themes (long-tail, novos territórios).
- 5–10 sazonais/táticos (campanhas, eventos, lançamentos).

### Brand exclusion + Negative keywords + Placement exclusions

Em PMax, configure **os 3** controles sempre:

```yaml
pmax_controls:
  brand_exclusions:
    - "Competitor A"
    - "Competitor B"   # marcas que você NÃO quer aparecer
  
  negative_keyword_lists:    # account-level, agora aplicáveis a PMax
    - universal_negatives_list
    - vertical_negatives_list
  
  account_placement_exclusions:    # NEW jan/2026
    - mfa_sites_list   # Made-for-Advertising
    - mobile_game_spam_list
    - low_quality_youtube_channels_list
  
  audience_exclusions:
    - "Existing Customers (Customer Match)"
    - "Recent Buyers 30d"
```

---

## 11. Common pitfalls em criação de campanha

| Erro | Consequência | Correção |
|---|---|---|
| Lançar com 1 RSA | Sem rotation, sem teste, Ad Strength ruim | 2+ RSAs por ad group |
| Localização "Presence or Interest" sem motivo | Pega quem só **pesquisou** o lugar (não está lá) | Use `PRESENCE` na maioria |
| Search Partners ON desde dia 1 | Tráfego de qualidade questionável | Iniciar OFF; testar isolado |
| "Display Network" ligado em Search campaign | Mistura tráfego, polui dados | Sempre OFF em Search |
| Budget muito baixo (< 5× CPA esperado/dia) | Sem dados suficientes para Smart Bidding | Mín 30× CPA-alvo no mês |
| Conversion não rastreada por valor | Não pode usar tROAS no futuro | Sempre estimar valor |
| Copiar campanha existente "para reset" | Joga fora histórico de QS | Pausar keywords ruins, manter campanha |
| Pinhar todas as headlines | Ad Strength cai, otimização morre | Não pinhar, ou usar multi-pin sparingly |
| Negativas só após "ver os search terms" | Queima primeira semana de budget | Lista inicial de 50–100 negatives universais |
| Lançar PMax sem Search rodando | PMax canibaliza queries de baixa intenção | Search → PMax (depois) |

---

## 12. Fontes (research 2026)

- [Account Structure 2026 — WordStream](https://www.wordstream.com/blog/google-ads-account-structure)
- [Account Structure Framework 2026 — groas.ai](https://groas.ai/post/google-ads-account-structure-in-2026-the-framework-that-actually-works)
- [STAG vs SKAG — sitecentre](https://www.sitecentre.com.au/blog/stag-vs-skag-campaigns)
- [SKAG ainda relevante? — Store Growers](https://www.storegrowers.com/single-keyword-ad-groups/)
- [RSA Best Practices 2026 — Search South](https://www.search-south.com/2026/02/21/responsive-search-ads-best-practice-in-2026/)
- [Pinning RSA — Search South](https://www.search-south.com/2026/03/11/pinning-and-responsive-search-ads-when-should-you-use-it/)
- [Ad Strength — Google Ads Help](https://support.google.com/google-ads/answer/9921843)
- [Sitelinks 2026 — Search Scientists](https://www.searchscientists.com/adwords-help-sitelink-extensions/)
- [PMax 2026 Strategy — JumpFly](https://www.jumpfly.com/blog/mastering-google-performance-max-a-2026-strategy-guide/)
- [PMax Search Themes 2026 — ALM Corp](https://almcorp.com/blog/microsoft-performance-max-50-search-themes-2026-guide/)
- [PMax Optimization Tips — Search Engine Land](https://searchengineland.com/top-performance-max-optimization-tips-461913)
