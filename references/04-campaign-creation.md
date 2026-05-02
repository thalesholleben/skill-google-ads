# 04 - Campaign Creation (step-by-step 2026)

> Load this file when the user asks to create or restructure a campaign, configure a new account, or define account structure.

---

## 1. Before touching Google Ads - prerequisites

Do not create a campaign without answering these questions. If anything is missing, **talk to the client first**.

| Question | Why it matters |
|---|---|
| What is the goal? lead/sale/install/call | Defines conversion action and bid strategy |
| What is the average order value (B2C) or LTV (B2B)? | Defines target CPA / target ROAS |
| Margin or markup? | Without margin, "5x ROAS" can be unprofitable |
| Service geography? | Location targeting |
| Audience language? | Language settings + copy |
| Known seasonality? | Calendar + Seasonality Adjustments |
| Site / landing ready? | Prerequisite for QS and tracking |
| Tracking implemented? | **GA4 + Google tag + Enhanced Conversions ON** |
| Monthly budget? | Defines which strategy is viable |
| Main competitors? | Brand defense + Competitor campaigns |
| Clear differentiation? | Input for copy |

### Minimum to start

- Site with HTTPS, privacy policy, visible contact information.
- Conversion action configured with value, even if estimated.
- Google tag installed and validated through Tag Assistant.
- Enhanced Conversions enabled.
- GA4 linked with Google Ads for audiences and imported conversions.
- Budget >= 30 x target CPA / month as a rule of thumb for data.

---

## 2. Account structure - models by context

### A. Lead Gen / Local Service account template

```text
Account
|-- [Brand] Brand Defense
|   `-- Ad Group: Brand Terms (exact + phrase)
|
|-- [Search] Specific Services - [service] - [geo]
|   |-- Ad Group: Service A (5-15 keywords)
|   `-- Ad Group: Service B
|
|-- [Search] Phone Leads - [service] - [geo]
|   `-- Ad Group: General (Call extension priority)
|
|-- [Search] Competitor - [vertical]
|   `-- Ad Group: Competitor [name] (phrase only)
|
`-- [Display/PMax] Remarketing - visitors
    `-- Asset Group: Remarketing
```

### B. E-commerce account template

```text
Account
|-- [Brand] Defense
|
|-- [Search] Generic - [parent category]
|   |-- Ad Group: Subcategory A (Phrase + Exact)
|   `-- Ad Group: Subcategory B
|
|-- [Shopping] Standard
|
|-- [PMax] Performance Max
|   `-- Asset Groups by category/persona
|
`-- [Display] Remarketing
```

### C. B2B SaaS account template

```text
Account
|-- [Brand] Defense
|
|-- [Search] Product-aware
|   |-- Ad Group: Core feature 1
|   `-- Ad Group: Core feature 2
|
|-- [Search] Solution-aware
|   |-- Ad Group: Use case 1
|   `-- Ad Group: Use case 2
|
|-- [Search] Problem-aware
|   `-- Ad Group: Pain point keywords (phrase + broad with Smart Bidding)
|
|-- [Search] Competitor
|
`-- [Demand Gen] Top of funnel
```

### Campaign split rules

Create a **separate campaign** when:
- Budget needs independent control.
- Audience is radically different.
- Geography is different.
- Ad scheduling is different.
- A different bid strategy makes sense, for example Brand on Max Conv and Non-Brand on tCPA.

Create a **separate ad group** when:
- Theme/intent is different enough to need distinct copy.
- Landing page is different.

---

## 3. Step-by-step setup (Search campaign - YAML for clarity)

```yaml
campaign:
  name: "[Search] Floor Removal - Phone Leads - Orlando"
  type: SEARCH

  # === BUDGET & BIDDING ===
  daily_budget: 30 USD
  bid_strategy: MAXIMIZE_CONVERSIONS
  bid_target_cpa: null   # add after 30 conv/30d

  # === LOCATIONS ===
  locations:
    target: "Orange County, Florida"
    radius_targeting: false
    location_options: PRESENCE         # do NOT use PRESENCE_OR_INTEREST without reason

  # === LANGUAGES ===
  languages: [en, es]   # include Spanish in FL/TX/CA by default

  # === NETWORKS ===
  networks:
    google_search: true
    search_partners: false   # start OFF, enable later only if search is strong
    display: false           # NEVER in a Search campaign; Display Network for Search is a trap

  # === SCHEDULE ===
  ad_schedule:
    enabled: false   # let Smart Bidding decide; enable only for Maximize Clicks

  # === DEVICES ===
  devices:
    all_enabled: true
    exclude:
      - tablets: false   # tablets outperform expectations in some niches

  # === AD ROTATION ===
  ad_rotation: OPTIMIZE

  # === FREQUENCY CAPPING ===
  # Not applicable to Search; applies to Display/PMax/Demand Gen

  # === CONVERSION ACTIONS ===
  conversion_actions:
    - "Phone Call (offline OCI)"      # PRIMARY
    - "Form Submit"                   # PRIMARY
    - "Page View Pricing"             # SECONDARY; do not optimize for this

  # === ATTRIBUTION ===
  attribution_model: DATA_DRIVEN
  conversion_window: 30_days

  # === EXCLUSIONS ===
  audience_exclusions:
    - "Existing Customers (Customer Match)"
    - "Recent Form Submitters (last 30d)"
```

---

## 4. Ad groups and keywords

### How many keywords per ad group?

- **STAG (Single Theme Ad Group)**: 5-15 keywords in the same theme/intent.
- **SKAG**: 1 keyword, rare in 2026 and only for very high-volume queen keywords.

### Match type structure inside an ad group

```yaml
ad_group: "Floor Removal Service"
keywords:
  exact_match:
    - "[floor removal]"           # proven queen keyword
    - "[floor demolition]"

  phrase_match:
    - '"floor removal service"'
    - '"floor demolition service"'
    - '"remove old floor"'
    - '"tile removal"'             # strong subcategory
    - '"hardwood removal"'

  broad_match:
    # ONLY if campaign has 50+ conv/month + solid tracking
    - "floor removal Orlando"
    - "carpet removal contractor"
```

### Ad group negatives

```yaml
ad_group_negatives:
  - "[free]"           # exact, do not negative phrase "free"
  - "DIY"
  - "tutorial"
  - "video"
  - "rental"           # if you are a removal service, not rental
```

---

## 5. RSA (Responsive Search Ads) - 2026 best practices

### Minimum composition

- **15 headlines**, the maximum allowed. Full diversity.
- **4 descriptions**, the maximum. Each with a different angle.
- **2 RSAs per ad group** with different final URLs to test landing pages.
- **Target Ad Strength: Excellent**, or at least Good.

### Headline distribution model

Distribute the 15 slots:

| Category | Quantity | Example |
|---|---:|---|
| Keyword headlines | 3 | "Floor Removal Orlando", "Pro Floor Demo Service", "{Keyword:Floor Removal} Experts" |
| Benefit/USP | 3 | "Same-Day Service Available", "Licensed & Insured Crew", "No Mess, No Damage" |
| Social proof | 2 | "5 Star on Google - 200+ Reviews", "Trusted by 500+ Homeowners" |
| CTA | 3 | "Get Free Estimate Today", "Call Now (407) XXX-XXXX", "Schedule Free Consultation" |
| Urgency / offer | 2 | "Free Quote in 24 Hours", "Book This Week - Save 10%" |
| Differentiator | 2 | "Family-Owned Since 2008", "Eco-Friendly Disposal Included" |

### Descriptions (4 slots)

```text
Description 1 (benefit-focused):
"Professional floor removal in Orlando. Tile, hardwood, carpet, vinyl - we handle it.
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

### Pinning - when to use it and when not to

**Pinning follows the LESS IS MORE rule in 2026.** Pinning prevents Ad Strength from reaching Excellent and lowers it automatically.

**Use ONLY when:**
- Compliance/regulatory needs require it, for example a fixed healthcare disclaimer in position 3.
- Brand guidelines require the brand name in headline 1.
- You are testing a specific headline in a specific position, limited to 14 days.

**NEVER pin:**
- More than 1 headline in position 1.
- Because of personal preference without data.
- Multiple headlines broadly. If needed, use **multi-pin**: 2-3 headlines competing for one position.

### How to improve Ad Strength from Average to Good/Excellent

Google evaluates:

1. **Headline diversity**: benefit, feature, CTA, and other types.
2. **Including popular keywords in headlines**: main ad group keyword in at least 3 headlines.
3. **More unique headlines**: unique words, not the same word repeated in 5 headlines.
4. **Including more headlines**: use all 15 slots.

Specific actions:
- Headlines should use at least 25 of 30 characters.
- Descriptions should use 80-90 of 90 characters.
- Each description ends with a CTA or unique differentiator.

---

## 6. Extensions / Assets required in 2026

Extensions are **free** and increase CTR by **10-25%**. In 2026, **Google evaluates relevance through extensions** - not using them creates an implicit penalty.

### Required extensions by campaign

#### Sitelinks: minimum 6, ideal 8
- **2 description lines** each, the high-performance 2026 format.
- Specific pages, not the home page.
- Examples for Floor Removal:
  - "Tile Removal" -> /tile-removal | "Same-day quote, no obligation. Pro tile demo crews."
  - "Hardwood Removal" -> /hardwood | "Careful removal of nail-down or glue-down floors."
  - "Free Estimate" -> /quote | "Online form, response in 1 hour business hours."
  - "Service Areas" -> /coverage | "Orange, Seminole, Lake, Osceola counties."

#### Callouts: minimum 8

Short non-clickable text up to 25 characters, shown below the description.

```text
"Free Estimates"
"Licensed & Insured"
"Same-Day Service"
"Family-Owned"
"5 Star Google Reviews"
"Eco-Friendly Disposal"
"No Hidden Fees"
"Serving Central FL"
```

#### Structured Snippets: minimum 1, ideal 2 categories

Categorized lists. Google chooses the header; you provide values.

```text
Header: "Service Catalog"
Values: ["Tile Removal", "Hardwood Removal", "Carpet Pulling", "Vinyl Removal", "Subfloor Prep"]

Header: "Brands"  # only if selling products
Values: [...]
```

#### Call Extension

For **lead gen with phone as conversion**:
- Phone tracking number is preferred because it measures conversions.
- Mobile-only ON when campaigns are >70% mobile.
- Schedule, for example 8am-6pm business hours.

#### Location Extension

- Link Google Business Profile.
- Shows map, address, and hours in ads.
- Critical for local services.

### Extension hierarchy in 2026

```text
Account level   -> evergreen: Free Estimates, Licensed, etc.
Campaign level  -> theme: Tile campaign has tile-specific callouts
Ad Group level  -> tactical: current offer, seasonal
```

Google now **mixes extensions from different levels** in the same ad, so using all levels is an advantage, not a conflict.

---

## 7. Negatives - initial launch list

Before turning the campaign on, configure a **universal negative list** at account level:

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
  - "how to"        # phrase match; blocks "how to remove floor yourself"
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

Add a vertical-specific list:

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
  - barato        # unless this is your positioning

b2b_negatives:
  - personal use
  - student
  - individual
  - "open source"

legal_services_negatives:
  - "free consultation"   # if you charge for it
  - pro bono
  - aid
  - legal aid
```

---

## 8. Tracking checklist before launch

Without this, **do not launch**. Delaying launch 3 days is better than running 30 days with broken tracking.

- [ ] Google tag installed on every page and validated in Tag Assistant.
- [ ] Conversion action created and linked: Phone Call, Form Submit, etc.
- [ ] Conversion action marked as **Primary** only for actions you want to optimize.
- [ ] Correct conversion category: Lead, Purchase, etc.
- [ ] Conversion value filled in, even if estimated, for Smart Bidding.
- [ ] Enhanced Conversions ON with hashed user data.
- [ ] GA4 linked to Google Ads.
- [ ] GA4 audiences imported.
- [ ] Test conversion: perform 1 real conversion such as form submit or call, then validate it appears in Google Ads within 24h.

---

## 9. Launch - first 14 days

### Day 0 launch
- Pre-budget locked.
- Universal negatives applied.
- 2 RSAs per ad group, Ad Strength >= Good.
- All extensions configured.
- **Bid strategy: Maximize Conversions**, no cap for first 72h, then add cap if spend rises too much.

### Days 1-3: aggressive monitoring, minimal changes
- Verify ads are serving; Search Terms should show impressions.
- Detect broken tracking: clicks > 50 and 0 conversions appearing -> suspicious.
- Identify obvious negatives from clearly irrelevant search terms.

### Days 4-7
- Add negatives based on search terms.
- Pause headlines with "Low" rating.
- Check Quality Score baseline.

### Days 8-14
- First serious performance read.
- If 10+ conversions -> continue Maximize Conversions with cap.
- If 30+ conversions -> migrate to Maximize Conversions with tCPA cap.
- Decide whether day 14 moves to pure tCPA; requires 30+ conversions.

### Day 14 formal review
- If reaching expected CPA -> pure tCPA, target = current CPA x 1.0.
- If CPA is much higher -> adjust copy / negatives / targeting.
- If 0 conversions in 14 days with 50+ clicks -> reassess landing/copy/offer. Pause and replan.

---

## 10. PMax - advanced 2026 setup

### When PMax is worth creating

- Search already runs well and Smart Bidding has learned signals.
- You have quality assets: images, video, varied copy.
- Conversion tracking is solid.
- PMax has at least $30/day; below that, data is weak.

### Asset Group structure

**1 PMax campaign, multiple asset groups by:**
- Product/service category.
- Audience persona.
- Funnel stage.

```yaml
pmax_campaign:
  name: "[PMax] Floor Removal - Orlando"
  budget: 40 USD/day
  bid: tCPA $50

  asset_groups:
    - name: "Tile Removal - Homeowners"
      audience_signal:
        custom_segments: ["tile removal", "kitchen renovation"]
        in_market: ["Home Improvement"]
        your_data: ["Site Visitors 30d"]
      headlines: 15 tile-focused variations
      descriptions: 4
      images: 10-20
      videos: 2-5, autogenerated or owned
      logos: required
      search_themes:    # NEW 2026 - up to 50 per asset group
        - "tile removal Orlando"
        - "remove kitchen tile"
        - "professional tile demolition"
        # ... up to 50

    - name: "Hardwood Removal - Homeowners"
      # ... similar

    - name: "Carpet Removal - Property Managers"
      audience_signal:
        custom_segments: ["property management software"]
        # ...
```

### Search Themes - essential 2026 controls

Search Themes, up to 50 per asset group in 2026, **are keyword-like signals** for PMax. Without them, PMax drifts.

**Recommended distribution from 30-45 total themes:**
- 20-30 core themes based on proven intent from Search campaign search terms.
- 15-20 discovery themes: long-tail, new territories.
- 5-10 seasonal/tactical themes: campaigns, events, launches.

### Brand exclusion + Negative keywords + Placement exclusions

In PMax, always configure **all 3** controls:

```yaml
pmax_controls:
  brand_exclusions:
    - "Competitor A"
    - "Competitor B"   # brands where you do NOT want to appear

  negative_keyword_lists:    # account-level, now applicable to PMax
    - universal_negatives_list
    - vertical_negatives_list

  account_placement_exclusions:    # NEW Jan/2026
    - mfa_sites_list
    - mobile_game_spam_list
    - low_quality_youtube_channels_list

  audience_exclusions:
    - "Existing Customers (Customer Match)"
    - "Recent Buyers 30d"
```

---

## 11. Common campaign creation pitfalls

| Mistake | Consequence | Fix |
|---|---|---|
| Launching with 1 RSA | No rotation, no test, weak Ad Strength | 2+ RSAs per ad group |
| Location "Presence or Interest" without reason | Captures people who only searched the place | Use `PRESENCE` in most cases |
| Search Partners ON from day 1 | Questionable traffic quality | Start OFF; test separately |
| Display Network enabled in Search campaign | Mixed traffic, polluted data | Always OFF in Search |
| Budget too low: < 5x expected CPA/day | Not enough data for Smart Bidding | Minimum 30x target CPA/month |
| Conversion not tracked by value | Cannot use tROAS later | Always estimate value |
| Copying campaign to "reset" | Throws away QS history | Pause weak keywords, keep campaign |
| Pinning every headline | Ad Strength drops, optimization dies | Do not pin, or use multi-pin sparingly |
| Negatives only after seeing search terms | Burns the first week of budget | Initial list of 50-100 universal negatives |
| Launching PMax without Search | PMax canibalizes low-intent queries | Search first, then PMax |

---

## 12. Sources (2026 research)

- [Account Structure 2026 - WordStream](https://www.wordstream.com/blog/google-ads-account-structure)
- [Account Structure Framework 2026 - groas.ai](https://groas.ai/post/google-ads-account-structure-in-2026-the-framework-that-actually-works)
- [STAG vs SKAG - sitecentre](https://www.sitecentre.com.au/blog/stag-vs-skag-campaigns)
- [Are SKAGs Still Relevant? - Store Growers](https://www.storegrowers.com/single-keyword-ad-groups/)
- [RSA Best Practices 2026 - Search South](https://www.search-south.com/2026/02/21/responsive-search-ads-best-practice-in-2026/)
- [Pinning RSA - Search South](https://www.search-south.com/2026/03/11/pinning-and-responsive-search-ads-when-should-you-use-it/)
- [Ad Strength - Google Ads Help](https://support.google.com/google-ads/answer/9921843)
- [Sitelinks 2026 - Search Scientists](https://www.searchscientists.com/adwords-help-sitelink-extensions/)
- [PMax 2026 Strategy - JumpFly](https://www.jumpfly.com/blog/mastering-google-performance-max-a-2026-strategy-guide/)
- [PMax Search Themes 2026 - ALM Corp](https://almcorp.com/blog/microsoft-performance-max-50-search-themes-2026-guide/)
- [PMax Optimization Tips - Search Engine Land](https://searchengineland.com/top-performance-max-optimization-tips-461913)
