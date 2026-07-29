# Funnel & Drop-off Analysis

**Python | Pandas | SciPy | SQLite | Streamlit | Plotly | Power BI**

Finding where users drop off in an online store — and proving, not just guessing, that it isn't a device, country, or channel problem.

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-3.0-150458?logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3.45-003B57?logo=sqlite&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.60-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-6.9-3F4F75?logo=plotly&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?logo=powerbi&logoColor=black)

---

## The Short Version

5,000 users visited this store. Only 1,010 bought something — a 20.2% overall conversion rate. That number alone doesn't tell you where to fix anything, so this project breaks the funnel into its five steps and finds the one that actually matters: **product page → cart**, where 59.89% of viewers leave without adding anything. Every other step converts above 70%. Then it tests whether device, country, referral source, or time spent on the page explain that drop-off — none of them do, which turns out to be the real finding.

## The Core Problem

**Product Page → Cart loses more users than any other step, by a wide margin.**

| Transition | Conversion | Drop-off |
|---|---:|---:|
| Home → Product Page | 79.74% | 20.26% |
| **Product Page → Cart** | **40.11%** | **59.89%** |
| Cart → Checkout | 70.23% | 29.77% |
| Checkout → Confirmation | 89.94% | 10.06% |

If that one step converted at even 45% instead of 40.11%, the funnel's own downstream rates put that at **+123 additional confirmed purchases per 5,000 sessions — a 12.2% relative lift in total conversions.** (This dataset has no price field, so this stops at conversions, not revenue — multiply by your own AOV to translate it.)

## What the Numbers Show

| Step | Sessions | % of Home | Step-over-Step |
|---|---:|---:|---:|
| Home | 5,000 | 100.00% | — |
| Product Page | 3,987 | 79.74% | 79.74% |
| Cart | 1,599 | 31.98% | 40.11% |
| Checkout | 1,123 | 22.46% | 70.23% |
| Confirmation | 1,010 | 20.20% | 89.94% |

## Four Things Tested — None of Them Explain It

| Factor | How It Was Tested | Result |
|---|---|---|
| Device Type | Chi-square, proceed-to-cart rate by segment | p = 0.9905 — **no difference** |
| Country | Chi-square, proceed-to-cart rate by segment | p = 0.9910 — **no difference** |
| Referral Source | Chi-square, proceed-to-cart rate by segment | p = 0.3835 — **no difference** |
| Time on product page | t-test, proceeded vs. didn't (97.7s vs. 96.1s) | p = 0.3119 — **no difference** |

## What Was Expected vs. What Actually Happened

| Assumption | Expected | Reality |
|---|---|---|
| Biggest leak is late in the funnel (checkout, payment friction) | ✅ | ❌ — checkout converts at 70%+; the leak is much earlier |
| Mobile converts worse than desktop | ✅ | ❌ — 40.0–40.3% across all three device types |
| Some country underperforms | ✅ | ❌ — 38.9–41.2% across all seven countries |
| More time on page signals more purchase intent | ✅ | ❌ — no statistical relationship |

## What Should Be Done

| Problem | Action | Why |
|---|---|---|
| 60% drop-off at Product Page → Cart, identical across every segment | Run session recordings / heatmaps on the product page itself | A uniform problem needs a page-level fix, not audience targeting |
| No segment to blame means no obvious hypothesis yet | User-test the add-to-cart flow specifically (pricing clarity, shipping-cost visibility, CTA prominence) | Generates concrete, testable hypotheses |
| Root cause still unconfirmed | A/B test the strongest hypothesis against the current page | Validates before full rollout |

## A Note on the Dataset

Every single test above came back not significant — device, country, referral source, and time-on-page all converge on almost exactly the same rate. In a real production dataset, you'd expect *some* natural variation even where nothing meaningful is going on. This uniformity is a reasonable signal the dataset is synthetic rather than logged from a real store. That doesn't make the analysis process wrong — the methodology here (funnel construction, chi-square testing, ruling factors in or out) is exactly what you'd run against real data — but the specific numbers shouldn't be quoted as real-world benchmarks.

## Data Quality Checks

- Verified every session's page sequence is a strict, ordered progression (0 out-of-order or skipped-step sessions)
- Verified `DeviceType`, `Country`, `ReferralSource`, and `UserID` never change mid-session
- Confirmed zero missing values across all 12,719 rows
- **Cross-validated the entire funnel two independent ways** — pandas and SQL (window functions) — and confirmed they match to the decimal

## Dataset

| Field | Value |
|---|---|
| Source | Kaggle — *(https://www.kaggle.com/datasets/sufya6/e-commerce-customer-journey-click-to-conversion)* |
| File | `customer_journey.csv` |
| Rows | 12,719 page-view events |
| Sessions / Users | 5,000 / 1,872 |
| Period | Jan – Aug 2025 |
| Missing values | 0 |

## Tools Used

| Tool | Used for |
|---|---|
| Python (pandas, scipy) | Funnel construction, segment analysis, chi-square/t-tests |
| SQLite | Independent validation of the funnel via SQL window functions |
| Matplotlib | Static funnel chart in the notebook |
| Streamlit + Plotly | Live interactive dashboard with filters and an in-app significance test |
| Power BI | Star-schema report — same analysis, BI-tool-native |
| Jupyter | Analysis notebook |

## Project Structure

```
funnel-analysis/
├── data/
│   ├── raw/customer_journey.csv
│   └── processed/          # dim_session, fact_pageviews, funnel_summary, segment_summary
├── notebooks/analysis.ipynb
├── sql/funnel_analysis.sql
├── streamlit_app/streamlit_app.py
├── powerbi/                # data model + DAX guide
├── case_study.md
├── README.md
└── requirements.txt
```

## How to Run This

1. **Clone this repo**
```bash
   git clone https://github.com/<your-username>/<repo-name>.git
   cd <repo-name>
```

2. **Set up the environment**
```bash
   python3 -m venv venv
   source venv/bin/activate
```

3. **Install the required libraries**
```bash
   pip install pandas numpy scipy matplotlib streamlit plotly jupyter ipykernel
```

4. **Launch the dashboard**
```bash
   streamlit run streamlit_app/streamlit_app.py
```
---

This project's real conclusion isn't the 59.89% number itself — it's that ruling factors *out* through actual testing, rather than assuming a segment is to blame, is what kept this from turning into a wrong recommendation.

## Author

**Dikshant Mahlawat** — [LinkedIn](https://www.linkedin.com/in/dikshant-mahlawat/) · [GitHub](https://github.com/thedikshantmahlawat) · [Kaggle](https://www.kaggle.com/dikshant200905)
