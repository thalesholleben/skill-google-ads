# 04: Campaign creation and account structure

> Load to build or restructure a campaign, design the account, write RSAs and assets, or prepare PMax. Through the
> API, everything starts `PAUSED` and every change runs with `validate_only` first.

Sources: `g/NNNN` = `https://support.google.com/google-ads/answer/NNNN`, checked on October 1, 2026, unless another
date is given.

---

## 1. Before touching the account

| Question | Why it matters |
|---|---|
| What is the goal and **what will the conversion actually measure**? | An action's name proves nothing: a form hosted on a third-party domain becomes an outbound click |
| Ticket, margin and close rate | they set the break-even CPA or ROAS; without them a target is a guess |
| Where is the business, and where is the person when they search? | targeting and local demand |
| Expected search volume and cost | Keyword Planner and forecast, in the account currency |
| Budget and who approves it | the account owner approves spend |
| A fast landing page ready | page experience is not fixed in the ad |
| Measurement ready | Google tag, primary conversion, Enhanced Conversions, GA4 linked |
| Competitors and differentiator | input for ad text and brand defense |

**Address and service area from the live website, not from old notes.** Businesses move and old scrapes stay wrong;
targeting built on an outdated address can leave the ads far from the actual store and miss the towns around it. Read the live site with a
browser User-Agent (some servers answer 403 to short User-Agents). For a physical store: a radius around the store,
sized by driving time, and the radius demand measured in the Keyword Planner before promising volume. Inside a
small radius, good searches are often only a few hundred a month, and the budget that turns into good clicks is
smaller than it looks.

**Business name in ads** (policy update for October 2026, `adspolicy/answer/18287059`, posted October 1, 2026): the
business name and the destination domain may differ only when the name reflects the advertiser's recognized brand,
there is a verified direct relationship with the domain owner, and the products or services are offered directly on
that domain. Resellers, booking intermediaries and affiliates cannot use the brand of what they sell as their
business name.

**Minimum to go live:** a primary conversion tested with one real conversion; the page live with HTTPS, contact
details and a privacy policy; the account spending limit checked (an old account budget almost fully spent stops
delivery, and no status warns about it: read `account_budget`); the site's Content Security Policy allowing the
conversion ping (`www.google.com/measurement/conversion`), or conversions silently fail.

---

## 2. Account structure

### A. Local lead generation (services)

```
Account
├── [Search] Brand                      (exact and phrase of the name)
├── [Search] Services, <region>         ad groups by service, 5 to 15 keywords each
├── [Search] Calls, <region>            if calls are the channel that closes
└── [Search] Competitors (optional)     competitor name in phrase, comparison page
```

### B. E-commerce

```
Account
├── [Search] Brand
├── [Search] Categories                 ad groups by subcategory
├── [Shopping] or [PMax] Feed           asset groups by category
└── [Demand Gen] Remarketing (optional)
```

### C. B2B SaaS with volume

```
Account
├── [Search] Brand
├── [Search] Product (features)
├── [Search] Solution (use cases)
├── [Search] Problem                    educational page
└── [Search] Competitors
```

### D. Low-volume B2B (few leads a month, high ticket)

```
Account
└── [Search] One campaign, Manual CPC with per-keyword caps
    ├── Ad group: vendor searches       ("<service> company", "<service> agency near me")
    └── Ad group: solution searches     ("<problem> software", "<process> management system")
        qualifying headlines (section 5), a landing page written for that buyer
```

**Split into another campaign** when the budget must be controlled separately, the region or audience is
different, or the bidding strategy is different. **Split into another ad group** when the theme needs another ad or
another page. **With low volume, consolidate:** every extra split fragments data that is already short (08).

---

## 3. Search campaign setup

```yaml
campaign:
  name: "[Search] Services, <region>"
  status: PAUSED                    # everything starts paused; turning on is a separate step
  type: SEARCH
  budget_daily: <proposal for the owner> # spend needs approval
  bidding: <by regime, 03 section 3> # low: MANUAL_CPC or MAXIMIZE_CLICKS with a cap
  networks:
    google_search: true
    search_partners: false          # turn on only as an isolated test
    display_expansion: false        # spends leftover Search budget on Display; off for lead gen
  locations:
    targets: ["<cities, regions or a radius you actually serve>"]
    option: PRESENCE_OR_INTEREST    # Google's recommendation for Search (g/1722043)
    # PRESENCE for local services that only serve people who are in the area (heuristic) or sensitive sectors
  languages: n/a                    # language targeting removed from Search in September 2026 (g/1722078)
  ad_schedule: <only if the business has hours and the channel is calls>
  conversion_goals: <primary actions that measure leads or sales; everything else secondary>
  ai_max: false                     # only in medium or high regimes (01, section 6)
```

- **Language:** since September 2026, Search ignores the language setting; the ad matches through its own language
  and the page. For a bilingual audience, write ads in the other language too.
- **Search partners and Display expansion:** both remain optional under "Networks" (`g/7193800`, `g/1722047`).

---

## 4. Ad groups and keywords

- 5 to 15 keywords per ad group, one theme and one intent. Phrase and exact at the start (02, section 3).
- Broad only in the right regime. A broad keyword with a phrase sibling that does not convert falls under gate D
  in medium or high regimes, and only with gate B's click minimum; in the low regime, only gate B (08, section 4).
- Starter negatives: the universal list and the industry list (02, section 4), tested against the seed keywords.

---

## 5. Responsive search ads (RSA)

**Limits:** up to **15 headlines** of 30 characters, **4 descriptions** of 90, paths of 15; at most **3 enabled RSAs
per ad group** (a fourth returns `RESOURCE_LIMIT`; to swap, pause one and create the new one in the same request, in
that order).

**Ad Strength** (`g/9921843`):
- Poor to Excellent gives on average **+15% conversions** (RSA and sitelinks combined). **Ad Strength is not used in
  the auction nor in Quality Score.**
- Official best practice: **at least 2 RSAs rated Good or Excellent per ad group, each with its own final URL**;
  the 2nd RSA yields +6.6% conversions and the 3rd, +3.7%.
- 6+ sitelinks count toward Good or better; text generated by text customization also counts.
- In low-volume accounts, `ad_group_ad_asset_view.performance_label` comes back `NOT_APPLICABLE`: you cannot pick
  headlines by label.

**Pinning:** pinning reduces combinations, and repeated or similar pins lower the rating. Google suggests pinning 1
or 2 essential headlines and, if needed, putting several versions in the same position. Legitimate uses:
- legal or brand requirements;
- **filtering out non-buyers**: a qualifying headline pinned in position 2 ("Projects from $X", "For companies with
  50+ employees") keeps price shoppers away. An ad that turns away the curious is doing its job when volume is
  scarce and each click is expensive.
With AI Max final URL expansion on, pins can be ignored (01, section 6).

**Composition** (heuristic): headlines with the ad group's keyword, benefit, proof, offer, call to action and
differentiator; descriptions with different angles, each ending in a call to action or differentiator. **The ad
only claims what the page publishes** (an ad that promises "published price list" after the page dropped its price
table is a disapproval or a disappointed lead waiting to happen).

**Changing text without recreating the ad:** an `AdService` update of the responsive search ad with the full lists
of headlines and descriptions (the update replaces, it does not merge); the ad keeps its ID and status. Call-only
ads cannot be created since January 2026 and stop serving in February 2027: the replacement is an RSA with a call
asset.

---

## 6. Assets (formerly extensions)

| Asset | Limits and rule | Source |
|---|---|---|
| Sitelink | text 25, two descriptions of 35 (fill both for the detailed format); up to 6 show on desktop and 8 on mobile; 6 per campaign give up to +3.5% conversions | `g/2375416` |
| Callout | 25 characters | API |
| Structured snippet | 13 fixed headers, 3 to 10 values of 25 (Google recommends 4+); up to 2 on desktop and 1 on mobile; in the API the header is the **exact translated string** of the ad's language (in English "Services" does not exist: use "Service catalog" or "Types"; in other languages, the translated header) | `g/6280012`, API |
| Call | a tracked number; calls from the ad show in `call_view` | API |
| Location | linked to the Business Profile | |

**Hierarchy:** sitelinks from every level (account, campaign, ad group) **show together**, without replacement; for
structured snippets the most granular level replaces the one above (`g/2375416`, `g/6280012`). Consequence: a
campaign-level asset shows in every ad group that has no asset of its own. An ad group with a new landing page
needs its own assets, with every value written on that page.

- Unused RSA headlines can take the space of sitelinks.
- Automatically created assets (`asset.source = AUTOMATICALLY_CREATED`) cannot be linked by hand; advertiser assets
  serve even when the ad group has automatic ones. The old ACA became AI Max text customization; account-level
  automated assets (dynamic sitelinks and snippets) are separate (`g/7331111`).
- **Automated promotions from October 12, 2026** (secondary source: Search Engine Land, October 2026, citing Google's
  notice): Search and PMax campaigns with location assets and no promotion assets can get promotion assets pulled
  from the website; they only show under Assets after they get impressions. Opt out at the account level in the
  automated asset settings (Automated Promotions). An expired promotion still on the page becomes an ad: check the
  site or opt out.
- Through the API, creating an asset and linking it are two `mutate` calls; the link cannot be validated with
  `validate_only` before the asset exists. Before creating, check whether the same `link_text` and `final_urls`
  already exist (select `asset.final_urls` in the preflight query), or a re-run duplicates assets.

---

## 7. Measurement checklist before going live

- [ ] Google tag on every page; primary conversion created and **tested with one real conversion**.
- [ ] Each primary action measures what it claims (final page HTML fetched with a browser User-Agent, the public
      GTM container read); counting "One" for leads.
- [ ] Calls: a minimum call duration on the action, the call asset pointing to the right action, and the campaign
      goal including the call category as biddable.
- [ ] Enhanced Conversions on (one switch since June 2026); GA4 linked; consent set up as the site requires.
- [ ] Account spending limit and payment method checked.

---

## 8. First 14 days

- **Day 0:** the paused campaign reviewed (ad text against the page, negatives, assets, measurement); turning on is
  a separate step, with confirmation of what was approved.
- **Days 1 to 3:** is the ad serving? (`ad_group_ad.primary_status` and the day's impressions; `campaign.primary_status`
  can lag 40+ minutes). Clearly wrong search terms: gate A.
- **Days 4 to 7:** search terms and negatives; no cutting on performance with low volume.
- **Day 14:** the first reading by the rules written before launch (08, section 8). In a low regime, 14 days rarely
  decide performance; they decide delivery, intent and copy.

---

## 9. Performance Max

- **Official budget:** an average daily budget of at least **3x the CPA** of the campaign's actions (`g/15864652`).
  "Search before PMax" is a heuristic, not a rule.
- **Priority:** a search identical to an exact Search keyword beats PMax; an identical search theme shares priority
  with phrase and broad (`g/7478529`).
- **Search themes:** up to 50 per asset group, with the same priority as phrase and broad (`g/14767319`).
- **Controls:** campaign and account negatives (only Search and Shopping inventory; up to 10,000 per campaign,
  `g/15726455`); brand exclusions (`g/13721847`); account-level placement exclusions, which apply to Display, Video,
  Search, PMax, Demand Gen and App (`g/7331110`).
- **Reports:** channel performance (Insights > Channel performance, `g/16260130`); search terms in the API through
  `campaign_search_term_view`; placements in `performance_max_placement_view`.
- **PMax experiments:** Uplift, Upgrade (Shopping, DSA or Display to PMax) and Optimization (final URL expansion,
  assets) (`g/12997711`).

---

## 10. Common creation mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| One RSA per ad group | no rotation, low rating | 2 RSAs rated Good or Excellent, each with its own URL |
| Search partners on from day 1 | traffic of uncertain quality | test it in isolation |
| Display expansion on a lead campaign | mixed traffic | off |
| A conversion nobody checked | CPA compared in the wrong unit | section 7 |
| A new campaign turned on directly | spend before review | starts `PAUSED`, turning on is a separate step |
| An ad that promises what the page does not say | disapproval, frustrated leads | ad text checked against the page |
| Targeting from an old address | the ad shows far from the business | the live site and a radius around it |
| Copying a campaign "to reset" it | recreated keywords start without history (heuristic) | adjust the existing campaign |

---

## Sources

Google Ads Help (October 1, 2026): `g/1722043` location options; `g/1722078` language; `g/7193800` Display
expansion; `g/1722047` search partners; `g/9921843` Ad Strength; `g/2375416` sitelinks; `g/6280012` structured
snippets; `g/7331111` assets; `g/7331110` placement exclusions; `g/7478529` priority; `g/15864652` PMax budget;
`g/14767319` search themes; `g/15726455` PMax negatives; `g/13721847` brand settings; `g/16260130` channel
performance; `g/12997711` PMax experiments. Policy: business name update
(https://support.google.com/adspolicy/answer/18287059, October 2026).
API: structured snippet headers (https://developers.google.com/google-ads/api/data/structured-snippet-headers);
deprecations (https://developers.google.com/google-ads/api/docs/deprecations).
Secondary: automated promotions (https://searchengineland.com/google-ads-will-automatically-pull-promotions-from-advertisers-websites-493225, October 2026).
