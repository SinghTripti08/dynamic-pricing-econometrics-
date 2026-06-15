import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_panel_data(num_products=5, weeks=52):
    np.random.seed(42)
    start_date = datetime(2025, 1, 1)
    
    # baseline structures for products
    product_profiles = {
        0: {"name": "Premium Organic Coffee", "base_price": 15.0, "true_elasticity": -1.2, "base_demand": 500},
        1: {"name": "Eco-Friendly Detergent", "base_price": 12.0, "true_elasticity": -0.8, "base_demand": 400},
        2: {"name": "Wireless Charging Pad", "base_price": 25.0, "true_elasticity": -2.1, "base_demand": 300},
        3: {"name": "Ergonomic Office Chair", "base_price": 150.0, "true_elasticity": -1.5, "base_demand": 80},
        4: {"name": "Stainless Water Bottle", "base_price": 20.0, "true_elasticity": -0.5, "base_demand": 600}
    }
    
    data_rows = []
    
    for prod_id, profile in product_profiles.items():
        for week in range(weeks):
            current_date = start_date + timedelta(weeks=week)
            
            # simulate price variation (random shocks around base price)
            price_shock = np.random.normal(0, 0.08 * profile["base_price"])
            price = max(profile["base_price"] * 0.7, min(profile["base_price"] * 1.3, profile["base_price"] + price_shock))
            
            # Competitor prices follw with variations
            competitor_price = price * np.random.uniform(0.9, 1.1)
            
            # binary promotional flags (15% chance)
            is_promo = 1 if np.random.rand() < 0.15 else 0
            
            # seasonal demand multiplier (sine wave peak in summer/winter holidays),formula
            seasonality = 1.0 + 0.15 * np.sin(2 * np.pi * week / 52)
            
            # Log-Log underlying structural model generation
            # log(Q) = log(α) + β*log(P) + γ*Promo + δ*log(CompPrice) + Seasonal Shock + Error? idk neeed to confirm
            log_base = np.log(profile["base_demand"])
            log_price_term = profile["true_elasticity"] * np.log(price)
            promo_term = 0.35 * is_promo  # Promo increases sales by ~35%
            comp_term = 0.25 * np.log(competitor_price)
            random_noise = np.random.normal(0, 0.05)
            
            log_quantity = log_base + log_price_term + promo_term + comp_term + random_noise
            quantity = int(np.exp(log_quantity) * seasonality)
            quantity = max(1, quantity) # floor at 1 unit
            
            revenue = quantity * price
            
            data_rows.append({
                "week_start": current_date,
                "product_id": prod_id,
                "product_name": profile["name"],
                "price": round(price, 2),
                "competitor_price": round(competitor_price, 2),
                "is_promo": is_promo,
                "units_sold": quantity,
                "gross_revenue": round(revenue, 2)
            })
            
    df = pd.DataFrame(data_rows)
    df.to_csv("data/simulated_retail_panel.csv", index=False)
    print("Panel dataset successfully generated at: data/simulated_retail_panel.csv")

if __name__ == "__main__": #to stimulate cpp structure
    import os
    os.makedirs("data", exist_ok=True)
    generate_panel_data()
