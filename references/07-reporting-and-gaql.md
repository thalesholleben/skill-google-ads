# 07 — Reporting, GAQL e Automação Python

> Carregue este arquivo quando o usuário pedir para gerar relatórios, escrever queries GAQL, automatizar extração de dados ou montar dashboards de Google Ads.

---

## 1. GAQL — Google Ads Query Language

GAQL é a linguagem de consulta da Google Ads API. Sintaxe similar a SQL.

### Estrutura básica

```sql
SELECT
  [campos: resource.field, metrics.field, segments.field]
FROM
  [resource]
WHERE
  [conditions]
ORDER BY
  [field] DESC
LIMIT
  [n]
```

### Resources principais

| Resource | O que contém |
|---|---|
| `campaign` | Métricas por campanha |
| `ad_group` | Métricas por ad group |
| `keyword_view` | Métricas por keyword |
| `search_term_view` | Search terms reais disparados |
| `ad_group_ad` | Métricas por anúncio |
| `geographic_view` | Métricas por localização |
| `hourly_metrics_view` | Métricas por hora |
| `audience_view` | Métricas por audiência |
| `asset_view` | Métricas de assets/extensions |
| `campaign_audience_view` | Audiences em campaign level |

---

## 2. Queries prontas

### Performance de campanhas (últimos 30 dias)

```sql
SELECT
  campaign.name,
  campaign.status,
  campaign.bidding_strategy_type,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.average_cpc,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value,
  metrics.cost_per_conversion,
  metrics.search_impression_share,
  metrics.search_budget_lost_impression_share,
  metrics.search_rank_lost_impression_share,
  metrics.search_absolute_top_impression_share
FROM campaign
WHERE
  segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

---

### Search terms com gasto e conversões

```sql
SELECT
  search_term_view.search_term,
  search_term_view.status,
  campaign.name,
  ad_group.name,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.average_cpc,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion
FROM search_term_view
WHERE
  segments.date DURING LAST_30_DAYS
  AND metrics.impressions > 0
ORDER BY metrics.cost_micros DESC
LIMIT 1000
```

---

### Keywords com Quality Score

```sql
SELECT
  keyword_view.resource_name,
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  ad_group_criterion.quality_info.quality_score,
  ad_group_criterion.quality_info.creative_quality_score,
  ad_group_criterion.quality_info.post_click_quality_score,
  ad_group_criterion.quality_info.search_predicted_ctr,
  campaign.name,
  ad_group.name,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion,
  metrics.average_cpc
FROM keyword_view
WHERE
  segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
  AND ad_group_criterion.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

---

### Auction Insights por campanha

```sql
SELECT
  auction_insight.resource_name,
  campaign.name,
  auction_insight.domain,
  metrics.auction_insight_search_impression_share,
  metrics.auction_insight_search_overlap_rate,
  metrics.auction_insight_search_position_above_rate,
  metrics.auction_insight_search_top_impression_percentage,
  metrics.auction_insight_search_absolute_top_impression_percentage,
  metrics.auction_insight_search_outranking_share
FROM auction_insight
WHERE
  segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY metrics.auction_insight_search_impression_share DESC
```

---

### Performance por dispositivo

```sql
SELECT
  segments.device,
  campaign.name,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.average_cpc,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion,
  metrics.conversion_rate
FROM campaign
WHERE
  segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

---

### Performance por hora do dia

```sql
SELECT
  segments.hour,
  segments.day_of_week,
  campaign.name,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion
FROM campaign
WHERE
  segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY segments.day_of_week, segments.hour
```

---

### Performance por localização

```sql
SELECT
  geographic_view.country_criterion_id,
  geographic_view.location_type,
  campaign.name,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion
FROM geographic_view
WHERE
  segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

---

### Ad performance com Ad Strength

```sql
SELECT
  ad_group_ad.ad.id,
  ad_group_ad.ad.responsive_search_ad.headlines,
  ad_group_ad.ad_strength,
  ad_group_ad.policy_summary.approval_status,
  campaign.name,
  ad_group.name,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.conversions,
  metrics.cost_micros
FROM ad_group_ad
WHERE
  segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
  AND ad_group.status = 'ENABLED'
  AND ad_group_ad.status = 'ENABLED'
ORDER BY metrics.impressions DESC
```

---

### Zero-conversion wasted spend (search terms)

```sql
SELECT
  search_term_view.search_term,
  campaign.name,
  ad_group.name,
  metrics.cost_micros,
  metrics.clicks,
  metrics.conversions,
  metrics.impressions
FROM search_term_view
WHERE
  segments.date DURING LAST_30_DAYS
  AND metrics.conversions < 0.01
  AND metrics.cost_micros > 5000000
ORDER BY metrics.cost_micros DESC
LIMIT 200
```

*(cost_micros > 5000000 = > US$ 5 gastos sem conversão)*

---

### Série temporal semanal

```sql
SELECT
  segments.week,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion,
  metrics.conversion_rate
FROM campaign
WHERE
  segments.date BETWEEN '2026-01-01' AND '2026-04-27'
  AND campaign.status = 'ENABLED'
ORDER BY segments.week
```

---

## 3. Scripts de automação Google Ads (JavaScript)

### Budget pacing monitor (roda diário)

```javascript
// Enviado para email se gasto projetado > meta mensal × 1.10

function main() {
  var today = new Date();
  var dayOfMonth = today.getDate();
  var daysInMonth = new Date(today.getFullYear(), today.getMonth()+1, 0).getDate();
  
  var MONTHLY_BUDGET = 1800; // USD
  var EMAIL_RECIPIENT = "your-email@example.com";
  
  var campaigns = AdsApp.campaigns()
    .withCondition("Status = ENABLED")
    .forDateRange("THIS_MONTH")
    .get();
  
  var totalSpent = 0;
  while (campaigns.hasNext()) {
    var c = campaigns.next();
    totalSpent += c.getStatsFor("THIS_MONTH").getCost();
  }
  
  var projected = (totalSpent / dayOfMonth) * daysInMonth;
  var paceRatio = projected / MONTHLY_BUDGET;
  
  if (paceRatio > 1.10 || paceRatio < 0.80) {
    MailApp.sendEmail(
      EMAIL_RECIPIENT,
      "Alerta de Pacing Google Ads — " + today.toDateString(),
      "Gasto atual: $" + totalSpent.toFixed(2) + "\n" +
      "Projeção mês: $" + projected.toFixed(2) + "\n" +
      "Meta: $" + MONTHLY_BUDGET + "\n" +
      "Pacing: " + (paceRatio * 100).toFixed(1) + "%\n" +
      (paceRatio > 1.10 ? "⚠️ ACIMA do orçamento!" : "⚠️ ABAIXO do orçamento!")
    );
  }
}
```

---

### CPA anomaly detector (roda diário)

```javascript
function main() {
  var LOOKBACK_DAYS = 14;
  var CPA_SPIKE_FACTOR = 1.5;
  var EMAIL_RECIPIENT = "your-email@example.com";
  
  var campaigns = AdsApp.campaigns()
    .withCondition("Status = ENABLED")
    .get();
  
  var alerts = [];
  
  while (campaigns.hasNext()) {
    var c = campaigns.next();
    var statsYesterday = c.getStatsFor("YESTERDAY");
    var statsTrailing  = c.getStatsFor("LAST_14_DAYS");
    
    var convYesterday = statsYesterday.getConversions();
    var costYesterday = statsYesterday.getCost();
    var convTrailing  = statsTrailing.getConversions();
    var costTrailing  = statsTrailing.getCost();
    
    if (convTrailing < 5) continue; // sem dados suficientes
    
    var cpaYesterday = convYesterday > 0 ? costYesterday / convYesterday : 999;
    var cpaTrailing  = costTrailing / convTrailing;
    
    if (cpaYesterday > cpaTrailing * CPA_SPIKE_FACTOR) {
      alerts.push(c.getName() + ": CPA ontem=$" + cpaYesterday.toFixed(0) + 
                  " vs média 14d=$" + cpaTrailing.toFixed(0));
    }
    
    if (convYesterday === 0 && costYesterday > 50) {
      alerts.push(c.getName() + ": $" + costYesterday.toFixed(0) + " gastos, 0 conv ontem!");
    }
  }
  
  if (alerts.length > 0) {
    MailApp.sendEmail(
      EMAIL_RECIPIENT,
      "⚠️ Google Ads Anomalia Detectada",
      alerts.join("\n")
    );
  }
}
```

---

### Broken URL checker (roda diário)

```javascript
function main() {
  var EMAIL_RECIPIENT = "your-email@example.com";
  var brokenUrls = [];
  
  var ads = AdsApp.ads()
    .withCondition("Status = ENABLED")
    .withCondition("CampaignStatus = ENABLED")
    .get();
  
  while (ads.hasNext()) {
    var ad = ads.next();
    var url = ad.urls().getFinalUrl();
    if (!url) continue;
    
    try {
      var response = UrlFetchApp.fetch(url, {muteHttpExceptions: true});
      var code = response.getResponseCode();
      if (code >= 400) {
        brokenUrls.push(url + " → HTTP " + code + " (" + ad.getCampaign().getName() + ")");
      }
    } catch(e) {
      brokenUrls.push(url + " → Erro: " + e.message);
    }
  }
  
  if (brokenUrls.length > 0) {
    MailApp.sendEmail(
      EMAIL_RECIPIENT,
      "🔴 URLs Quebradas — Google Ads",
      brokenUrls.join("\n")
    );
  }
}
```

---

## 4. Formato dos relatórios `.docx` (Python)

Os scripts em `scripts/` geram relatórios Word. Estrutura de seções:

### Relatório interno (`build_report.py`)

```
1. Resumo Executivo
   - KPIs do período
   - Comparativo vs mês anterior

2. Performance por Campanha
   - Tabela: campanha × impressões × clicks × conv × CPA × CTR

3. Performance por Dispositivo
   - Tabela: Mobile / Desktop / Tablet

4. Search Terms — Top Performers
   - Top 20 queries com conversão

5. Zero-Conv Waste
   - Queries que queimaram budget sem conv

6. Auction Insights
   - Top 5 competidores + interpretation

7. Performance por Condado / Geo
   - Tabela: localização × conversões × CPA

8. Análise de Keywords
   - QS médio, keywords pausadas, recomendações

9. Palavras Negativas Adicionadas
   - Lista do período

10. Plano de Ação
    - Próximos passos priorizados
```

### Relatório cliente (`build_report_cliente.py`)

```
Resumo do Mês (Heading 2 — aparece no sumário)

1. Resultados do Período (Heading 3)
2. Qualidade do Tráfego (Heading 3)
3. Posicionamento no Mercado (Heading 3)
4. Melhorias Aplicadas (Heading 3)
5. Metas vs Realizado (Heading 3)
6. Realocação de Verba (Heading 3)
7. Observações Estratégicas (Heading 3)

[Fonte: Montserrat | Tom: positivo | Omite: falhas internas]
```

---

## 5. N-gram analysis em Python — como usar

O script `scripts/n_gram_analysis.py` analisa search terms de um CSV exportado do Google Ads.

### Input: exportar do Google Ads

1. Ir para **Keywords → Search Terms**.
2. Selecionar período (30–90 dias).
3. Colunas necessárias: `Search term`, `Clicks`, `Impressions`, `Cost`, `Conversions`, `CTR`, `Avg. CPC`.
4. Export → CSV.

### Rodar o script

```bash
python n_gram_analysis.py search_terms.csv
```

Output: `ngram_report.csv` com 3 abas:
- `1grams` — tokens únicos.
- `2grams` — pares de palavras.
- `3grams` — trios de palavras.

Cada aba ordenada por `Cost` descrescente, com colunas `Clicks`, `Conversions`, `CPA`, `CTR`.

### Interpretar resultados

```
1-gram: "free" | Cost: $85 | Conv: 0 → negative "free" (exact match)
1-gram: "removal" | Cost: $420 | Conv: 15 → core keyword, mantém

2-gram: "floor removal" | Cost: $220 | Conv: 12 → ótimo, promover para exact
2-gram: "diy floor" | Cost: $45 | Conv: 0 → negative "diy" ou phrase "diy floor"

3-gram: "remove tile yourself" | Cost: $30 | Conv: 0 → negative phrase
3-gram: "floor removal orlando" | Cost: $180 | Conv: 9 → EXACT MATCH NOW
```

---

## 6. Looker Studio — template de dashboard

Conexão: Google Ads Data Source → select account.

### Páginas recomendadas

**Página 1 — Executive Summary**
- Scorecards: Spend, Conversions, CPA, CTR, ROAS.
- Time series: Conv + CPA últimos 90 dias.
- Bar chart: Campaigns by Conversions (sorted).

**Página 2 — Keywords & Quality Score**
- Table: Keyword, QS, Impr, Clicks, Cost, Conv, CPA.
- Filter: QS slider (1–10).
- Conditional formatting: QS ≤ 5 em vermelho.

**Página 3 — Geo & Device**
- Geo map: Conversions by county.
- Table: Device, Conv, CPA, CTR.

**Página 4 — Auction Insights**
- Table: Competitor, IS, Overlap Rate, AbsTop Rate.
- Trend: weekly comparison.

**Página 5 — Search Terms**
- Table: Search term, Cost, Conv, CPA.
- Filter: Conversions = 0 (para waste analysis).

### Campos calculados úteis

```sql
-- ROAS
SUM(conversions_value) / SUM(cost)

-- CPA
SUM(cost) / SUM(conversions)

-- Conv Rate
SUM(conversions) / SUM(clicks)

-- Zero-conv waste %
SUM(IF(conversions = 0, cost, 0)) / SUM(cost)
```

---

## 7. Checklist de relatório mensal

Antes de entregar qualquer relatório, validar:

- [ ] Período correto (data início e fim conferidos com a conta).
- [ ] Conversões: contando **Primary only** (não mixed com Secondary).
- [ ] CPA calculado em cima de Primary conversions.
- [ ] Auction Insights com mesmo período do relatório.
- [ ] Benchmark: comparar com mês anterior + mesmo mês do ano anterior (sazonalidade).
- [ ] Anotações de eventos relevantes no período (lançamento de produto, mudança de landing, nova campanha).
- [ ] Próximos passos são **específicos e acionáveis** ("pausar keyword X") não vagos ("monitorar performance").

---

## 8. Fontes (research 2026)

- [GAQL Overview — Google Ads API](https://developers.google.com/google-ads/api/docs/query/overview)
- [GAQL Grammar — Google Ads API](https://developers.google.com/google-ads/api/docs/query/grammar)
- [Google Ads Scripts 2026 — groas.ai](https://groas.ai/post/best-google-ads-scripts-2026-install-guide-automation-limits)
- [Automate Reporting with AI — Cotera](https://cotera.co/articles/automate-google-ads-reporting-ai)
- [Scripts Automation 2026 — Yeezypay](https://yeezypay.io/blog/google-ads-scripts-in-2026-how-to-automate-monitor)
- [N-gram Analysis — Adalysis](https://adalysis.com/blog/n-gram-analysis-the-secret-to-scalable-search-term-management-in-google-ads/)
- [Free Python N-gram Script — Ayima](https://www.ayima.com/insights/ngram-script-for-google-ads.html)
