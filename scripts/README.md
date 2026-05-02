# Scripts — Google Ads Manager Skill

Three Python scripts for Google Ads reporting and analysis.

---

## 1. `n_gram_analysis.py` — Search Term N-gram Analysis

Reads a Google Ads **Search Terms** CSV and produces a `ngram_report.csv` with 1-gram, 2-gram, and 3-gram aggregates. Includes suggested actions (PROMOTE, NEGATIVE, SCALE, OPTIMIZE, MONITOR).

**How to export the input CSV:**
1. Google Ads → Keywords → Search Terms
2. Select date range (30–90 days recommended)
3. Download → CSV

**Run:**
```bash
python n_gram_analysis.py search_terms.csv
python n_gram_analysis.py search_terms.csv --min-cost 10 --out april_ngrams.csv
```

**Output columns:** `n, gram, queries, clicks, impr, cost, conv, ctr_%, cvr_%, cpc, cpa, roas, suggested_action`

**Interpret results:**
- `PROMOTE` → add as exact or phrase keyword
- `NEGATIVE` → zero CVR with real spend → add as negative
- `SCALE` → 5+ conversions, good CPA → increase bids/budget
- `REVIEW` → high spend, 0 conversions → check match type or negative
- `OPTIMIZE` → high CPA → fix landing page or match type

---

## 2. `build_report.py` — Internal Monthly Report (.docx)

Generates the full internal `.docx` report (10 sections: executive summary, performance, device/schedule, counties, auction insights, search terms, work done, diagnosis, action plan, client alignment).

**Font:** Calibri. **Target:** internal / agency use.

**Run:**
```bash
python build_report.py
```

Output path is hardcoded in the script — update `out_path` at the bottom before each month.

**Sections:**
1. Resumo Executivo (KPI cards)
2. Performance — Comparativo
3. Análise por Dimensão (device + schedule)
4. Desempenho por Condado
5. Concorrência — Auction Insights
6. Termos de Pesquisa & Negativas
7. O Que Foi Feito no Mês
8. O Que Puxou o Resultado
9. Plano de Ação
10. Alinhamento com o Cliente

---

## 3. `build_report_cliente.py` — Client Report (.docx)

Generates the client-facing `.docx` (7 sections, simplified language, Montserrat font, positive framing). Uses `Heading 2` for top-level sections and `Heading 3` for numbered subsections — generates a Word auto table of contents.

**Run:**
```bash
python build_report_cliente.py
```

Output path is hardcoded — update `out_path` at the bottom before each month.

**Sections:**
- Resumo do Mês (KPI cards)
- 1. Performance — Comparativo Mensal
- 2. Ações Realizadas no Mês
- 3. Posicionamento no Leilão
- 4. Desempenho por Região
- 5. Plano de Otimização
- 6. Realocação de Verba
- 7. Observações Estratégicas

---

## Requirements

```
pip install python-docx pandas
```

Montserrat must be installed on the system (the client report uses it). Download free at fonts.google.com/specimen/Montserrat.
