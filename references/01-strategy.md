# 01 — Estratégia (Smart Bidding, AI Max, Attribution, Audiences)

> Carregue este arquivo quando o usuário perguntar sobre estratégia de lance, AI Max, attribution, audiências, sazonalidade ou tomada de decisão de alto nível.

---

## 1. Smart Bidding em 2026 — o que mudou

### O grande shift: tROAS virou o default preferido (quando há valor)

Para contas com valor de conversão rastreável, **tROAS** é a escolha em 2026. O Google passou a otimizar por valor, não só por volume — o algoritmo prioriza conversões de US$ 200 sobre 10 conversões de US$ 20. Sem valor de conversão, você está deixando isso na mesa.

| Estratégia | Quando usar | Volume mínimo | Riscos |
|---|---|---|---|
| **Maximize Conversions** | Saída do learning phase, contas novas, fase de coleta de dados | Qualquer | Sem teto de CPA — pode escalar gastos sem controle |
| **Maximize Conversions + tCPA cap** | Transição entre Max Conv e tCPA puro | 10–25 conv/mês | Caps muito agressivos limitam volume |
| **Target CPA (tCPA)** | Lead gen, custo conhecido, foco em eficiência | 30+ conv/30d (oficial: 50) | Pode reduzir volume; sensível a mudanças >20% |
| **Target ROAS (tROAS)** | E-commerce, lead gen com valor por lead | 50+ conv/30d **+ valor** | Sem valor confiável é pior que tCPA |
| **Maximize Clicks** | Awareness, awareness/discovery, sites institucionais | Qualquer | Não otimiza para conversão |
| **Manual CPC** | Casos muito específicos (compliance, testes) | Qualquer | Esforço alto, perdendo todos os sinais que Smart Bidding lê |

### Novidades 2026 dignas de nota

- **Cart Value Optimization** (e-commerce): se o usuário adiciona produtos ao carrinho, o lance é ajustado pelo valor do carrinho em real-time. Habilitar via Merchant Center.
- **Profit Margin Bidding**: você sobe margem por SKU para o Merchant Center; Smart Bidding prioriza alto-margem sobre alto-revenue. **Mata o vício de "ROAS lindo, lucro zero"**.
- **Seasonality Adjustments**: avise o algoritmo sobre eventos previsíveis (Black Friday, lançamento, feira). Sem isso, ele super-reage à anomalia. Use para janelas de 1–14 dias com mudança de CR esperada >10%.

### Regras de ouro do learning phase

O learning phase **dura 7–14 dias** e reseta quando você:

- Muda a estratégia de lance.
- Muda o tCPA/tROAS target em **mais de 20%**.
- Muda o budget em **mais de 20%**.
- Adiciona/remove keywords ou ad groups significativos.
- Pausa e reativa a campanha.

**Implicações práticas:**
- Não toque em targets toda semana. Espere 14 dias antes de avaliar.
- Se precisa cortar CPA em 30%, faça em **dois passos** de 15% com 14 dias entre eles.
- Não copie/duplica campanhas para "reset" sem motivo — você joga fora 100% do aprendizado.

### Setting realistic targets

- **Initial tCPA**: defina **igual ou 10–20% acima do CPA atual médio**. Se o seu CPA atual é US$ 50, comece em US$ 55.
- **Initial tROAS**: defina **abaixo do ROAS atual** (90% dele) para o algoritmo ter folga e otimizar volume primeiro.
- **Ramp**: reduza tCPA (ou suba tROAS) em **10–15% a cada 2 semanas**, sempre confirmando que volume não despencou.
- **Floor**: nunca defina tCPA tão baixo que o algoritmo pause delivery — ele vai parar de gastar antes de aceitar a conv.

---

## 2. AI Max for Search — guia de migração 2026

### O que é

AI Max **não é uma campanha nova** — é um conjunto de 3 features ativáveis dentro de campanhas Search existentes:

1. **Search Term Matching**: expansão broad-match-like + "keywordless targeting" — Google encontra queries relevantes que você não cobriu.
2. **Text Customization**: AI gera copy adicional puxando do site e dos assets que você já forneceu.
3. **Final URL Expansion**: roteia automaticamente para a melhor landing page do site.

### Cronograma forçado

A partir de **setembro/2026**, Google **migra automaticamente** todas as Dynamic Search Ads (DSA), Automatically Created Assets (ACA) e broad match para o framework AI Max. Quem ainda não migrou vai ser migrado.

### Performance esperada (oficial Google)

- +14% conversões / valor a CPA similar — caso geral.
- +27% — em campanhas que ainda dependem majoritariamente de exact + phrase.

### Quando ativar agora vs esperar

**Ative agora se:**
- Tracking sólido (Enhanced Conversions ON, ≥30 conv/mês, valor por conv configurado).
- Site bem estruturado (landing pages dedicadas, conteúdo limpo).
- Você tem capacidade de monitorar search terms semanalmente.
- Já roda broad match com Smart Bidding sem desastre.

**Espere se:**
- Tracking ruim ou incerto.
- Site genérico/B2B com landing única.
- Vertical sensível (legal, financeiro, saúde) onde texto AI-gerado pode causar problema.
- Você não consegue revisar search terms e final URLs com cadência.

### Controles obrigatórios após ativar AI Max

- **Brand exclusion lists**: bloqueie marcas de competidor que você NÃO quer aparecer.
- **Locations of interest**: especifique geografia onde vale ad-show, mesmo que o user esteja fora.
- **Negative keywords**: reforce, não relaxe. AI Max expande mais que broad clássico.
- **Final URL inclusions/exclusions**: defina padrões de URL elegíveis vs não.

---

## 3. Attribution em 2026 — Data-Driven Attribution (DDA)

### Estado atual

Apenas **2 modelos sobrevivem**: Last Click e Data-Driven Attribution. First click, linear, time-decay, position-based foram aposentados.

**DDA é o default para todas as novas conversion actions.** Não há mais mínimo de dados para usar DDA, mas o Google recomenda **200+ conv + 2.000+ ad interactions/30d** para ele performar bem.

### Como DDA funciona

Machine learning compara paths de usuários que converteram com paths de quem não converteu. Identifica quais touchpoints "fizeram a diferença". Distribui crédito **fracionado** entre todas as interações com ads na jornada.

### Por que importa para Smart Bidding

Smart Bidding **lê crédito de DDA** para decidir lances. Se você está em Last Click, você está dizendo ao algoritmo "só conta o último clique" — ele não consegue valorizar awareness/middle-funnel campaigns adequadamente. **Migre para DDA antes de qualquer otimização séria de Smart Bidding.**

### Enhanced Conversions — não opcional em 2026

Enhanced Conversions envia dados hashed (email, telefone) do usuário para casar com a conta Google dele. Recupera **20–40% das conversões perdidas** com cookies/iOS restrictions.

**Tipos:**
- **Enhanced Conversions for Web**: e-commerce e form-fills.
- **Enhanced Conversions for Leads**: B2B / lead gen, casa o lead com a conv quando ele fecha (offline).

**Mudança junho/2026**: Enhanced Conversions for Web e for Leads serão **unificadas em um único toggle**. Sem mais "que método uso?".

### Offline Conversion Import (OCI) para lead gen

O fluxo:
1. Lead clica → GCLID gravado no formulário (hidden field).
2. CRM grava GCLID + email hashed junto do lead.
3. Quando o lead fecha (sale, qualificação), CRM envia evento de volta para Google Ads via API ou upload.
4. Smart Bidding aprende: "leads desse perfil de search/keyword fecham mais".

**Sem OCI, você está otimizando para volume de leads, não qualidade.** Se 30% dos leads viram cliente e 70% são lixo, Smart Bidding não sabe disso e otimiza para média.

### Consent Mode v2

Em mercados com GDPR/LGPD: implementar Consent Mode v2 para que sinais de conversão de usuários que rejeitaram cookies ainda alimentem modelagem (não rastreamento individual).

---

## 4. Audience Targeting 2026

### Hierarquia de audiences (ordem de impacto)

1. **Customer Match (1P data)** — sua lista de clientes, leads qualificados, churn. Casos de uso:
   - Excluir clientes atuais de prospecting.
   - Listar lookalike (Demand Gen).
   - Audience signal em PMax.
2. **Your Data Segments (ex-remarketing)** — visitantes do site, App users, video viewers.
3. **Custom Segments** — keywords de competidor + URLs de competidor + apps.
4. **In-Market** — Google identifica usuários ativamente pesquisando categoria.
5. **Affinity** — interesses gerais (top of funnel).
6. **Detailed Demographics** — idade, paternidade, educação, employment.

### O que mudou em 2026

- **API change crítica (1 abril 2026)**: Customer Match uploads via Google Ads API param de funcionar para developers que ainda não usam. Migrar para **Data Manager API**.
- **Lookalike**: agora exclusivo de **Demand Gen campaigns**. Mín 1.000 active matched users na seed.
- **"Your data segments"**: novo nome para listas de remarketing — reflete que esses dados alimentam Smart Bidding e PMax, não só retargeting.

### Audience Strategy por funnel stage

| Stage | Audience | Campanha |
|---|---|---|
| **Aware** | Affinity, Custom intent (URLs de blog/educational) | Display, Demand Gen |
| **Interest** | In-Market, Custom segments (competidor) | Search broad + Display |
| **Consideration** | Site visitors, video 75% viewers | Search exact/phrase + RLSA |
| **Decision** | Cart abandoners, pricing page visitors | RLSA aggressive bid + Shopping |
| **Customer** | Customer Match (excluir de aquisição, incluir em retention) | RLSA upsell, email match Display |

### Audience signals em PMax

PMax aceita "audience signals" — você dá pista do alvo, ele expande. O signal **não trava** o targeting; é input para o algoritmo. Componentes:

1. **Customer Match**: top 10% LTV.
2. **Your Data**: visitantes que viram página de pricing.
3. **Custom Segments**: pessoas pesquisando competidor.
4. **Demographics**: faixa etária/income que historicamente converte.

### RLSA (Remarketing Lists for Search Ads)

Permite **mudar bids/copy** quando alguém na sua lista pesquisa termo genérico. Exemplo: visitante voltou e busca "best CRM" — você pode subir +50% e mostrar "Welcome back, ready to start?". Em campanhas com Smart Bidding, **as listas viram sinal automático** (não precisa setar bid adjustment).

---

## 5. Quando reestruturar a estratégia

Sintomas de que **está na hora de mudar de fase estratégica**:

| Sintoma | Próximo passo estratégico |
|---|---|
| Atinge meta de CPA mas volume estagnado por 2+ meses | Considerar tROAS (com valor) ou subir tCPA gradualmente |
| ROAS bate target mas lucro líquido estagnado | Migrar para Profit Margin bidding |
| Branded search cresceu organicamente | Adicionar campanha de Brand defense (ROI altíssimo) |
| Concorrente pesado entrou no leilão (Auction Insights) | Defender Brand + investir em diferenciação na copy |
| Search saturou (IS > 80%, custo subindo) | Expandir para PMax, Demand Gen, Display |
| Lead gen com 30% lead-to-customer conhecido | Implementar OCI para otimização por qualidade |
| Diversos verticais/produtos no mesmo conjunto | Quebrar em accounts/campaigns separadas para Smart Bidding aprender melhor |

---

## 6. Fontes (research 2026)

- [Smart Bidding 2026 — groas.ai](https://groas.ai/post/google-ads-smart-bidding-strategy-guide-2026-target-cpa-vs-target-roas)
- [Value Based Bidding 2026 — Brainmine](https://www.brainminetech.com/blog/how-value-based-bidding-is-changing-the-way-google-ads-scales-profit-in-2026/)
- [About Target ROAS — Google Ads Help](https://support.google.com/google-ads/answer/6268637)
- [AI Max for Search Campaigns — Google Ads Help](https://support.google.com/google-ads/answer/15910187)
- [DSA upgrading to AI Max — Google Blog](https://blog.google/products/ads-commerce/dsa-upgrade-to-ai-max-2026/)
- [AI Max Migration Guide — Vizup](https://www.tryvizup.com/blog/replace-dynamic-search-ads-with-ai-max-your-2026-migration-guide)
- [Attribution Modeling 2026 — ALM Corp](https://almcorp.com/blog/attribution-modeling-google-ads/)
- [Future of attribution is data-driven — Google Blog](https://blog.google/products/ads-commerce/data-driven-attribution-new-default/)
- [Customer Match — Google Ads Help](https://support.google.com/google-ads/answer/6379332)
- [Customer Match API change April 2026 — ALM Corp](https://almcorp.com/blog/google-ads-api-customer-match-disabled-april-2026/)
- [Audience Targeting 2026 — AdNabu](https://blog.adnabu.com/google-ads/google-ads-audience-targeting/)
- [Enhanced Conversions for Leads — Google Ads Help](https://support.google.com/google-ads/answer/15713840)
