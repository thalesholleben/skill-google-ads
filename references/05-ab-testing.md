# 05 — A/B Testing (Drafts & Experiments) em 2026

> Carregue este arquivo quando o usuário perguntar sobre testes, experiments, A/B, statistical significance, comparação de copy/lance/landing.

---

## 1. Quando usar Drafts & Experiments vs alternativas

### Drafts & Experiments (in-platform)

**Use quando** quer testar:
- Bid strategy (Maximize Conversions vs tCPA, tCPA vs tROAS).
- Bid target (tCPA US$ 40 vs US$ 50).
- Ad copy estrutural (mudança radical).
- Landing page (URL final diferente).
- Inclusão de search themes em PMax.
- Mudança de match types em larga escala.
- Audience signals em PMax.

**Vantagens:**
- Statistical significance automático (Jackknife resampling, 95% confidence).
- Split de tráfego aleatório (não viesado por hora/dia).
- Native attribution (mesma que Smart Bidding usa).
- Não precisa de ferramenta externa.

**Limitações:**
- Não comparam métricas de receita externa (precisa Google Analytics/CRM).
- Mínimo de 3–8 semanas para resultados confiáveis.
- Não funcionam em todas as campaign types (PMax tem suas próprias mecânicas).

### Alternativas

**Para landing pages**: Google Optimize foi descontinuado. Use **VWO, Optimizely, AB Tasty, Convert** ou bridge via **GA4 BigQuery + custom test**.

**Para creative em PMax**: usar Asset Reporting + remover/adicionar assets manualmente (não há experiment formal).

**Para mudanças "low-risk"**: aplicar diretamente, monitorar 14d, reverter se piora. Adequado para mudanças de extensions, adicionar negatives, ajustar lances < 20%.

---

## 2. Como rodar um experiment no Google Ads

### Setup passo-a-passo

#### 1. Criar Draft
- Em Campanhas → Drafts & Experiments → Drafts → New.
- Selecionar campanha base (a "control").
- Aplicar **uma única mudança** (regra 1 variável).

#### 2. Convert para Experiment
- Em Drafts → Apply → Run as experiment.
- Configurar:
  - **Nome**: descritivo (ex: "Test_tCPA_50_vs_60_2026Q2").
  - **Datas**: data de início + data de fim. Mín 3 semanas, ideal 6 semanas.
  - **Traffic split**: 50/50 padrão. Para teste arriscado: 30 (variation) / 70 (control).
  - **Search-based vs Cookie-based split**: cookie-based é o default, mais limpo.

#### 3. Goal metric
Defina **a métrica principal** que decide o teste:
- Lead gen: **Cost per conversion**.
- E-commerce com valor: **ROAS** ou **conversion value**.
- Awareness: **CTR** ou **CPM**.

### Sample size mínimo (regra de bolso)

Para detectar diferença com 95% de confiança:

| Lift relativo a detectar | Conversões/variant necessárias |
|---|---|
| 50% | ~100 |
| 30% | ~250 |
| 20% | ~400 |
| 10% | ~1.500 |

Se sua campanha total faz 100 conv/mês, você consegue detectar ~30% lift em ~5 semanas (250 / 50 = 5 semanas).

### Duração mínima

- **Mínimo**: 3 semanas (cobre variação semanal).
- **Recomendado**: 4–6 semanas (cobre eventos sazonais quinzenais).
- **Para tROAS / valor**: 6–8 semanas (variação maior).

**Não pare antes do prazo** mesmo se um lado está "vencendo". Variação aleatória pode reverter.

---

## 3. O que testar (priorização por impacto)

### Tier 1 — Alto impacto, baixo esforço
1. **Ad copy radical** (RSA nova com angle diferente).
2. **Landing page com message match forte vs genérica**.
3. **Add Enhanced Conversions** (aplicar mudança e medir lift de conv attribuída).
4. **tCPA + 20% para liberar volume** (em campanha capeada por target).

### Tier 2 — Alto impacto, médio esforço
5. **Mudança de bid strategy** (Max Conv → tCPA).
6. **Match type expansion** (adicionar broad em campanha exact-only).
7. **Split de campanha por geo** (1 campanha → 2 com targets diferentes).
8. **PMax + audience signals novos**.

### Tier 3 — Validação
9. **Pinning vs sem pinning**.
10. **Search Partners ON vs OFF**.
11. **Mais sitelinks (6 vs 8)**.
12. **Description longas vs curtas**.

### Tier 4 — Baixo impacto, evitar testar
13. Cor do botão.
14. Word-level changes em headlines.
15. Schedule fino-tunning em campanha tCPA (ignorado).

---

## 4. Anatomia de um teste bem desenhado

### Hipótese clara

❌ "Quero testar uma copy nova."
✅ "Hipótese: substituir 'Save Time' por 'Save 10+ Hours/Week' em 3 headlines aumentará CTR ≥10% em 4 semanas. Razão: especificidade aumenta credibilidade (referência: copy testing literature)."

### Métrica primária + guard-rails

**Primária**: CTR.
**Guard-rails** (não podem piorar significativamente):
- Conversion rate (≥-5% tolerância).
- CPA (≥+10% tolerância).
- Quality Score médio (não cair).

Se primária subiu mas guard-rail estourou, **rejeite o teste**.

### Critério de decisão pré-registrado

Antes de iniciar, escreva:

```
Vencedor se:
  - Primary metric difference > X with p < 0.05
  - All guard-rails dentro de tolerância

Inconclusivo se:
  - p > 0.05
  - Sample size < 250 conv/variant

Rollback se:
  - Guard-rail estourou
  - p < 0.05 mas em direção oposta à hipótese
```

### Single-variable rule

**Mude UMA coisa por experimento.** Multi-variant testing é tentador mas:
- Confunde causalidade.
- Multiplica sample size requerido.
- Em Google Ads, simplesmente não é suportado por Drafts & Experiments.

Exceção: testes mutually-exclusive (ex: 4 RSAs novas em rotação) não são "1 mudança", mas é teste de creative que naturalmente compara entre si.

---

## 5. Errors clássicos em A/B testing de Google Ads

### 1. "Pausei depois de 1 semana porque ficou claro que A é melhor"

Variação aleatória pode dar diferença de 30% em 7 dias e zerar em 21 dias. **Sempre cumpra a duração planejada.**

### 2. "Mudei a copy DURANTE o experiment"

Rebenta o teste. Se precisa mudar (ex: erro tipográfico), pause o experiment e reinicie com sample fresh.

### 3. "Comparei semana com semana sem rodar experiment formal"

Sazonalidade, tendência, eventos externos. Você não tem "controle". A semana 1 não é o controle da semana 2 — são dois cenários diferentes, ambos rodaram em condições diferentes.

### 4. "Aplicado mudança em todas as campanhas ao mesmo tempo"

Você não tem mais um controle. Faça em **1 campanha primeiro** com experiment formal, depois rolouts.

### 5. "Significância estatística significa que vou ganhar 30%"

Significância confirma que a diferença é real, não que será 30% em escala. Lift observado em test pequeno tende a ser **inflated** (regression to the mean).

### 6. "Test foi inconclusivo, vou aplicar a variação mesmo assim"

Se você "vai aplicar mesmo assim", **não rode o teste**. Mas se rodou, respeite o resultado: inconclusivo = sem evidência de melhora = manter status quo.

### 7. "Detectei outlier e removi do dataset"

Outliers em paid media geralmente são **dados reais** (ex: 1 cliente caro fechou). Removê-los enviesa. Use métricas robustas (mediana) se outliers preocupam.

---

## 6. Casos práticos comuns

### Caso 1: testar nova bid strategy

```
Hipótese: migrar de "Maximize Conv" para "tCPA US$ 50" reduzirá CPA em 15% sem perder >10% de volume.

Setup:
- Draft da campanha existente.
- Mudar bid strategy para tCPA US$ 50.
- Convert to experiment, 50/50 split, 6 semanas.

Decisão:
- CPA experiment / CPA control < 0.85 + p < 0.05 + Conv volume > 0.90 → APPLY
- Outros casos → ROLLBACK
```

### Caso 2: nova RSA com angle diferente

```
Hipótese: RSA com benefit headlines + social proof (vs current feature-focused) aumentará CTR ≥10%.

Setup:
- Draft da campanha.
- Pausar RSAs atuais, criar RSA nova.
- Convert to experiment, 50/50, 4 semanas.

Decisão:
- CTR > 1.10 × control + Conv rate ≥ control × 0.95 → APPLY
- CTR > 1.10 × control mas Conv rate < 0.90 × control → REJEITAR (clickbait)
```

### Caso 3: landing page nova

```
Hipótese: nova landing com form-3-fields (vs 7-fields) aumentará form completion ≥30%.

Setup:
- Em vez de Drafts & Experiments, usar VWO/Optimizely para split server-side.
- Manter URL Final do Google Ads inalterada (split é client/server-side).
- 4 semanas, 50/50.

Decisão:
- Form completion +30% + lead quality (downstream) ≥ control → APPLY
- Form completion +30% mas qualidade caiu (lead-to-customer ratio) → ANALISAR (pode ser ok se volume compensa)
```

### Caso 4: Search Themes em PMax

```
Hipótese: adicionar 30 search themes específicos a PMax aumentará Conv volume ≥15%.

Setup:
- Drafts & Experiments NÃO suporta PMax do mesmo jeito.
- Use Campaign Mix Experiments (beta 2026) — testa cross-campaign.
- Alternativa: criar 2 PMax campaigns, 1 com themes 1 sem, allocar budget igual.
- 6 semanas mínimo.

Decisão:
- Volume > 1.15 × control + CPA dentro de 1.10 × control → APPLY themes
```

---

## 7. Statistical concepts essenciais (sem jargão)

### Significance level (p-value)

P-value = probabilidade de observar diferença assim grande **se as duas variantes fossem iguais**.

- p < 0.05: 95% confiança que diferença é real.
- p < 0.01: 99% confiança.
- p > 0.05: insuficiente — não rejeita a hipótese nula.

### Confidence interval

Em vez de "lift de +12%", reporte "+12% ± 4% com 95% confidence".

Se o intervalo cruza 0 (ex: -2% a +18%), o teste é **inconclusivo** mesmo se p < 0.05 nominalmente.

### Power

Probabilidade de detectar diferença real (se ela existir). Power baixo (< 80%) significa que **mesmo se o teste não der significativo, pode haver diferença real que você não detectou**.

Para 80% power, 5% significance:
- 50% lift → 100 conv/variant.
- 30% lift → 250 conv/variant.
- 20% lift → 400 conv/variant.
- 10% lift → 1.500 conv/variant.
- 5% lift → 6.000 conv/variant.

### Multiple testing problem

Se você roda 20 testes simultaneamente e aceita p < 0.05, **estatisticamente** 1 vai sair "significativo" só por acaso. Para múltiplos testes, use Bonferroni correction (p < 0.05 / n) ou FDR (Benjamini-Hochberg).

Em prática: se está rodando 5+ testes no mesmo período, **eleve o critério para p < 0.01**.

---

## 8. Templates prontos

### Template de plano de experimento

```markdown
# Experiment: [nome curto]

**Hipótese:** [variação] aumentará/reduzirá [métrica] em [magnitude] em [período], 
porque [racional].

**Métrica primária:** [CPA / CTR / CVR / ROAS / etc]
**Guard-rails:**
  - [métrica 1] não pode cair mais que X%
  - [métrica 2] não pode subir mais que Y%

**Setup:**
  - Campanha base: [nome]
  - Mudança: [descrição em 1 frase]
  - Traffic split: 50/50
  - Início: [data]
  - Duração mínima: [3–6 semanas]
  - Sample size alvo: ≥ X conv/variant

**Critério de decisão:**
  - APPLY se: primary lift > Y%, p < 0.05, guard-rails OK.
  - ROLLBACK se: primary cai significantly OR guard-rail estoura.
  - INCONCLUSIVE se: p > 0.05 ao final do prazo → manter status quo.

**Aprendizado esperado:**
  - Independente do resultado, vamos aprender [insight].
```

### Checklist pré-lançamento de teste

- [ ] Hipótese escrita com magnitude esperada.
- [ ] Métrica primária + guard-rails definidos.
- [ ] Sample size mínimo verificado contra histórico de conv.
- [ ] Duração planejada (mínimo 3 semanas).
- [ ] Apenas UMA variável mudando.
- [ ] Critério de decisão pré-registrado.
- [ ] Calendário sem evento sazonal grande no meio (Black Friday, etc).
- [ ] Stakeholder informado: "não vou olhar antes de [data X]".

---

## 9. Fontes (research 2026)

- [Statistical methodology of experiments — Google Ads Help](https://support.google.com/google-ads/answer/9232676)
- [Google Ads Experimentation Tips 2026 — Growthspree](https://www.growthspreeofficial.com/blogs/best-tricks-and-tips-for-google-ads-experimentation-in-2026)
- [A/B Testing in Google Ads 2026 — site2b.ua](https://www.site2b.ua/en/web-blog-en/a-b-tests-in-google-ads-how-to-run-them-correctly-in-2026.html)
- [Google Ads Experiments B2B SaaS — Growthspree](https://www.growthspreeofficial.com/blogs/google-ads-experiments-b2b-saas-statistical-significance-methodology)
- [Experiment Center 2026 Guide — ALM Corp](https://almcorp.com/blog/google-ads-experiment-center-guide/)
- [Campaign Mix Experiments Beta — ALM Corp](https://almcorp.com/blog/google-ads-campaign-mix-experiments-complete-guide/)
- [Drafts Explained — Digital Marketing Knight](https://www.digitalmarketingknight.com/google-ads-draft-campaigns-explained/)
- [Ultimate Guide A/B Testing — AdNabu](https://blog.adnabu.com/google-ads/google-ads-ab-testing/)
