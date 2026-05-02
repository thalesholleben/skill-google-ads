# 02 — Keyword Research e Match Types em 2026

> Carregue este arquivo quando o usuário pedir pesquisa de keywords, mapeamento de intenção, decisão de match types, análise de search terms ou negativas avançadas.

---

## 1. Princípio fundamental — Google Ads roda em INTENÇÃO, não em palavra

Em 2026, todos os match types operam em **intent matching**:

- **Exact** match: cobre a query exata + variantes com mesmo significado (sinônimos, ordem trocada, termos implícitos).
- **Phrase** match: cobre paráfrases que carregam o mesmo significado da frase (mesmo com palavras antes/depois ou ordem ligeiramente diferente).
- **Broad** match: usa o keyword como ponto de partida + landing page + ad copy + signals do Smart Bidding para encontrar queries relevantes — pode estar muito longe do termo literal.

**Implicação prática:** keywords não delimitam mais o tráfego. **Negativas + Smart Bidding + landing page é o que delimita.**

---

## 2. Intent Mapping — o framework

Antes de listar keywords, mapeie **estágios de jornada**. Isso define:
- Qual campanha cada keyword pertence.
- Qual landing page.
- Qual lance e mensagem.

### Os 4 estágios (B2B / lead gen)

| Estágio | Como o user pesquisa | Volume | CPA esperado |
|---|---|---|---|
| **Problem-aware** | "como motivar time remoto", "produtividade caindo" | Alto | Alto (longo path-to-conv) |
| **Solution-aware** | "ferramenta de gestão de projetos", "software de PM" | Médio-Alto | Médio |
| **Product-aware** | "Asana vs Monday", "best Kanban tool 2026" | Médio | Médio-Baixo |
| **Brand-aware** | "[brand]", "[brand] login", "[brand] pricing" | Baixo (mas convertem) | Baixíssimo |

### Os 3 estágios (e-commerce)

| Estágio | Como o user pesquisa | Match |
|---|---|---|
| **Discovery** | "best running shoes for flat feet" | Phrase + Broad |
| **Comparison** | "Nike Pegasus 41 vs Brooks Ghost 16" | Exact + Phrase |
| **Transactional** | "Nike Pegasus 41 size 10 buy" | Exact |

### Erro comum

Misturar estágios no mesmo ad group → uma única RSA tenta servir intenções diferentes → relevância e CTR caem → QS cai → CPC sobe.

**Regra**: 1 estágio por ad group (STAG); copy e landing alinhados àquele estágio.

---

## 3. Process de Keyword Research

### Step 1 — Seed list

Colete de 5 fontes:

1. **Brainstorm interno**: 20–30 termos que você usaria.
2. **Site do cliente**: extrair títulos, h2, listas de produto.
3. **Site dos concorrentes** (top 3): mesma extração + diferenciais que eles destacam.
4. **Search terms já reais**: se existe conta com 30+ dias, mine os search terms convertendo.
5. **Customer service / vendas**: que perguntas chegam? que dores os clientes mencionam?

### Step 2 — Expand

- **Google Keyword Planner**: filtrar por volume mensal, competição, faixa de CPC. Marcar keywords com volume 100–10.000 (sweet spot).
- **Search com `*`** (wildcard): "best * software for [vertical]" gera ideias.
- **Google "People Also Ask"** + autocomplete: pegar perguntas longas (long-tail).
- **AnswerThePublic**: question-based queries.
- **Concorrentes via SEMrush/Ahrefs**: keywords que pagam (Top Paid Keywords).
- **AI tools**: Claude/ChatGPT — peça "gere 30 keywords problem-aware para X com volume estimado".

### Step 3 — Cluster por intent + tema

Use planilha. Para cada keyword:

| Coluna | Exemplo |
|---|---|
| Keyword | "kanban software for small teams" |
| Volume | 1.200/mês |
| CPC est. | US$ 4,50 |
| Intent | Solution-aware |
| Tema | Kanban |
| Match sugerida | Phrase |
| Landing | /kanban-tool |

Agrupe por **(Intent, Tema)** → cada grupo vira um ad group.

### Step 4 — Decidir match types por keyword

Use a lógica abaixo (não a "lei geral"):

```
SE keyword é brand → Exact (defesa)
SE keyword tem 30+ conv com bom CPA → Exact (consolidar)
SE volume médio + intent forte → Phrase (motor de growth)
SE volume alto + intenção genérica + Smart Bidding maduro + budget → Broad (discovery)
SE volume baixo (< 50/mês) + cauda longa → Phrase ou Broad em campanha discovery
```

### Step 5 — Negative seeds (lista inicial)

Antes de lançar, prepare negativas óbvias:

```yaml
universal_negatives:
  - free, gratis, grátis, gratuit
  - download, torrent, crack, pdf
  - jobs, job, vagas, salary, salário
  - tutorial, courses, course, training, certification
  - DIY, "how to do" (depende do contexto)
  - reviews (se você não quer ser comparado)
  - meaning, definition, what is (top of funnel sem intenção)
  - reddit, quora, forum (busca de opinião, não compra)
  - alternativas (se você é o líder, ou positiva se você é challenger)
  
ecommerce_specific:
  - used, segunda mão, refurbished
  - cheap, barato (a menos que seja seu posicionamento)
  - vs (a menos que esteja em comparison campaign)
  
b2b_specific:
  - student, estudante
  - personal use, individual
  - open source, free trial only

local_services_specific:
  - DIY, tutorial, video, youtube
  - rental, locação (se você é venda)
  - course, certification
```

---

## 4. Match Types — manual avançado 2026

### Exact Match `[keyword]`

**Quando usar:**
- Keywords-rainha provadas (10+ conversões com bom CPA).
- Brand defense (`[brand]`, `[brand login]`).
- Casos de altíssimo volume + alto CPC onde precisamos de teto.

**Risco:** mesmo exact pega close variants. Monitorar search terms semanalmente para variantes ruins.

### Phrase Match `"keyword"`

**Quando usar:**
- Motor principal de growth na maioria das contas.
- Volume médio + intenção razoavelmente clara.
- Quando ainda não tem dados suficientes para promover para exact.

**Boa prática 2026:**
- Pareie phrase + Smart Bidding (tCPA/tROAS) com 30–50 conv na campanha.
- Use múltiplas phrase variations em vez de uma exact.

### Broad Match `keyword`

**Pré-requisitos rigorosos antes de ativar:**
- ✅ Tracking sólido (Enhanced Conversions ON, conversões primárias bem definidas).
- ✅ 50–100 conversões/mês na campanha.
- ✅ Smart Bidding maduro (tCPA/tROAS rodando há 30+ dias).
- ✅ Capacidade de revisar search terms semanalmente (broad gera muito ruído).
- ✅ Lista robusta de negativas (mínimo 50–100 negativas iniciais).

**Sem esses pré-requisitos**, broad vira escoadouro de budget. Com eles, broad vira a maior fonte de descoberta da conta.

### Tabela de decisão rápida

| Cenário | Match recomendada |
|---|---|
| Conta nova, sem dados, lead gen | Phrase + Exact (50/50) |
| Conta nova, e-commerce com Shopping | Phrase + Broad (após 30d com Shopping ativo) |
| Conta madura, 100+ conv/mês, tCPA estável | Phrase principal + Exact rainha + Broad em campanha discovery separada |
| Brand campaign | Exact + Phrase (do nome da marca + termos genéricos) |
| Competitor campaign | Phrase (nome do competidor) — NUNCA exact (Google penaliza, e o user não quer o competidor literal) |
| Lançamento de produto novo | Exact + Phrase, sem Broad (Smart Bidding ainda não tem dados) |

---

## 5. N-gram analysis — método sistemático para search terms

### O que é

Em vez de revisar search terms um a um (impossível em escala), você quebra cada query em **fragments** de 1, 2 e 3 palavras (1-grams, 2-grams, 3-grams) e agrega métricas por fragmento.

**Por quê:** o "free" em "free download project management software" não aparece junto com "best free PM tools". Mas o **token "free"** soma gasto/conv/CTR de **todas** as queries que o contêm.

### Como rodar

**Passo 1**: exportar search terms report do Google Ads — janela 30–90 dias, todos os search terms da conta. Salvar em CSV.

**Passo 2**: rodar o script `scripts/n_gram_analysis.py` (incluído nesta skill). Output:
- Tabela de 1-grams ordenada por gasto, com Conv, CPA, CTR.
- Tabela de 2-grams.
- Tabela de 3-grams.

**Passo 3**: identificar n-grams de **alto gasto e zero conversões** → candidatos a negative.

**Passo 4**: identificar n-grams de **alto CTR e ótimo CPA** → candidatos a promover para exact match em ad group dedicado.

### Heurísticas para decisão

| Padrão | Ação |
|---|---|
| 1-gram com >US$ 50 gasto e 0 conv | Add como negative (se não for vital) |
| 1-gram com CPA 3x acima da média | Investigar; provavelmente negative |
| 2-gram com 5+ conv e CPA < média | Promover para exact em ad group focado |
| 3-gram com 10+ search distintas e bom CTR | Promover para keyword exata (alta intenção provada) |

### Frequência recomendada

- Contas pequenas (< US$ 1k/mês): mensal.
- Contas médias (US$ 1–10k/mês): quinzenal.
- Contas grandes (> US$ 10k/mês): semanal.

### Limites e cuidados

- N-grams ignoram **contexto** ("free shipping" vs "free download"). Sempre revise top hits manualmente antes de adicionar negative.
- 1-grams são potentes mas perigosos — uma negative de 1 palavra pode bloquear muito mais do que você imaginou. Use match type `phrase` ou `exact` na negative para limitar (ex: negative phrase "free trial" só bloqueia onde aparecem juntas).

---

## 6. Negative Keywords — estratégia avançada 2026

### Principais mudanças 2026

- **Limite expandido** (mar/2026): **10.000 keywords/campanha** e **10.000/ad group** (antes 5.000).
- **Account-Level Placement Exclusions** (jan/2026): bloquear sites/apps/canais YouTube em **todos os campaign types** (incluindo PMax e Demand Gen) de uma lista centralizada. Use para combater MFA (Made-for-Advertising) e mobile game spam.
- **Account-level negatives** continuam aplicando a Search/Shopping; para PMax/Demand Gen, use Brand Lists, Negative Keyword Lists at account level (recém-disponível para PMax) e exclusões de placement.

### Hierarquia de negativas

```
Account level         → universal (free, jobs, salary, etc)
  ↓
Negative Keyword List → reusável, share entre campaigns
  ↓
Campaign level        → específico do tipo de campanha
  ↓
Ad Group level        → cross-pollination entre groups (ex: "free" no group de paid, "premium" no free)
```

### Listas que toda conta deveria ter

1. **Universal Negatives** (account level): jobs, salary, free, download, torrent, crack, pdf, tutorial, course, certification, reddit, forum, what is, meaning, definition.
2. **Brand Defense** (account level): marcas concorrentes que você NÃO quer comprar (e vice-versa, se for protetivo).
3. **Cross-Pollination List** (ad-group level): impede que keyword do ad group A capture queries do ad group B.
4. **Vertical-Specific Negatives**: termos da indústria que sinalizam não-compra (ex: legal — "lawyer near me free" se você é firma paga; saúde — "home remedy" se você é medicamento).

### N-gram-driven negatives

Após cada n-gram analysis, gere **lote de negatives** e adicione **em batch** via Google Ads Editor (mais rápido que UI uma a uma).

---

## 7. Search Query Report (SQR) Mining — workflow

Workflow recomendado para mineração eficiente:

### 1. Promover top performers
- Search terms com **5+ conversões** e CPA abaixo da média → adicionar como **exact match** no ad group dedicado.
- Search terms com **alta CR + bom CPA + volume** → criar ad group novo se ainda não existe.

### 2. Negativar bottom performers
- Gasto > 3× CPA-alvo, sem conversão → negative immediate.
- Gasto > 10× CPA-alvo, 0 conv → 100% negative (sem dúvida).

### 3. Identificar gaps
- Search terms com **alto impr. share** mas **0 clique** → problema de copy/relevância (a query bate, mas o ad não convence).
- Search terms com **clique mas 0 conv** → problema de landing page ou intent mismatch (a query promete algo que a landing não entrega).

### 4. Detectar shifts de intenção
- Aparece uma query nova ganhando volume mês a mês? → tendência. Pode virar campanha dedicada.
- Query histórica perdeu volume? → competidor mudou estratégia, ou demanda caiu (ver Trends).

---

## 8. Keyword Tools — quando usar cada

| Ferramenta | Forte em | Custo |
|---|---|---|
| **Google Keyword Planner** | Volume oficial, CPC range, tendência | Grátis com conta Ads |
| **SEMrush** | Keywords pagas dos competidores, share of voice | US$ 130+/mês |
| **Ahrefs** | Difficulty SEO, content gap, organic share | US$ 100+/mês |
| **AnswerThePublic** | Question-based, long-tail | Grátis (limitado) / US$ 99/mês |
| **Soovle / Ubersuggest** | Multi-source autocomplete | Grátis / US$ 29/mês |
| **Claude/ChatGPT** | Brainstorm, clustering, copy generation | API/sub |

**Regra**: se o cliente já paga SEMrush/Ahrefs, comece por lá (dados de competidor). Se é conta nova / budget pequeno, Keyword Planner + AI é suficiente para começar.

---

## 9. Erros comuns em keyword research (e como evitar)

| Erro | Por quê é ruim | Correção |
|---|---|---|
| Listar 200 keywords e jogar em 1 ad group | RSAs ficam genéricos, QS despenca | Cluster em 8–12 STAGs de 5–15 keywords |
| Só keywords product-aware, ignorar problem-aware | Perde top-of-funnel; conta fica refém da demanda existente | Criar campanha problem-aware separada com landing educacional |
| Não pesquisar negatives antes de lançar | Primeiras semanas queimam US$ centenas | Lista inicial de 50–100 negatives universais |
| Confiar 100% em volume do Keyword Planner | Subestima long-tail; agrupa close variants | Validar com search terms reais após 30d |
| Comprar só keywords de competidor (sem brand) | Competidor compra a sua e você fica vulnerável | Sempre rodar Brand defense |
| Match type aleatório sem critério | Inconsistência → Smart Bidding sem padrão | Usar tabela de decisão da seção 4 |

---

## 10. Fontes (research 2026)

- [Match Types 2026 — Growth Minded Marketing](https://growthmindedmarketing.com/blog/keyword-match-types/)
- [Match Types 2026 — Stackmatix](https://www.stackmatix.com/blog/google-ads-keyword-match-types-guide)
- [Broad Match 2026 Playbook — ATTN Agency](https://www.attnagency.com/blog/google-ads-broad-match-strategy)
- [Negative Keywords 2026 — Optmyzr](https://www.optmyzr.com/blog/negative-keywords/)
- [N-gram Analysis Adalysis](https://adalysis.com/blog/n-gram-analysis-the-secret-to-scalable-search-term-management-in-google-ads/)
- [N-gram Layered — googleadsopenresearch](https://googleadsopenresearch.com/research/advanced-ngram-analysis/)
- [Account-Level Placement Exclusions — Karooya](https://www.karooya.com/blog/negative-keywords-in-google-ads-2026-are-you-using-them-to-filter-traffic-or-control-it/)
- [Keyword Research 2026 — SaaS Hero](https://www.saashero.net/google-ppc/google-ads-agency-keyword-research/)
- [Google Ads runs on intent — Search Engine Land](https://searchengineland.com/google-ads-intent-not-keywords-468271)
