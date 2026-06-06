# Econometric Pricing Engine & Causal Analytics System

An end-to-end management analytics platform implementing econometric models to isolate price elasticity of demand and estimate the causal impact of promotional and marketing strategies on e-commerce product lines.

<Image src="image_agent_tag_15967704299291182697" alt="Comparison graphs showing static single price points vs multiple optimized dynamic pricing horizons maximizing area of revenue yield curve" caption="Economic Revenue Optimization Curves" />

## 🎯 Project Objective & Business Case
Corporate strategy relies heavily on business intelligence tools that state *what* happened. This system adds value by answering *why* it happened and isolating structural coefficients. By controlling for confounding factors like seasonal demand shocks, competitive shifts, and marketing actions, this platform provides accurate elasticity estimates to build interactive risk-simulation tools.

### Key Strategic Highlights
* **Elasticity Mapping:** Isolated exact elasticity figures ranging from high price-sensitivity (Wireless Charging Pad: -2.1) to inelastic strong performers (Water Bottle: -0.5).
* **Causal Control Validation:** Fitted multivariate Log-Log linear frameworks, mitigating bias from competitor activity or promotions.
* **Executive Decision Tools:** Built a Python Streamlit application allowing non-technical managers to run pricing scenarios via slider matrices.

---

## 🛠️ Tech Stack & Methods
* **Analysis & Modeling Frameworks:** Python (`statsmodels`, `pandas`, `numpy`)
* **Interactive UI:** `Streamlit`, `Plotly Express`
* **Core Framework:** Log-Log Multivariate OLS Regressions:
$$\log(\text{Units Sold}) = \beta_0 + \beta_1 \log(\text{Price}) + \beta_2 \log(\text{Competitor Price}) + \beta_3 (\text{Is Promo}) + \epsilon$$

---

## 🚀 Execution & Quick Start

1. **Install Dependencies:**
```bash
   pip install -r requirements.txt
