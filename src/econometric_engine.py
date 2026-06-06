import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

def compute_elasticities(csv_path="data/simulated_retail_panel.csv"):
    df = pd.read_csv(csv_path)
    
    # log transformations for log-log regression interpretation
    df['log_units_sold'] = np.log(df['units_sold'])
    df['log_price'] = np.log(df['price'])
    df['log_competitor_price'] = np.log(df['competitor_price'])
    
    unique_products = df['product_id'].unique()
    elasticity_map = {}
    
    for pid in unique_products:
        sub_df = df[df['product_id'] == pid]
        
        # OLS structural formula specifying control variables
        formula = "log_units_sold ~ log_price + log_competitor_price + is_promo"
        model = smf.ols(formula=formula, data=sub_df).fit()
        
        # extraction coefficients
        elasticity_coeff = model.params['log_price']
        p_value = model.pvalues['log_price']
        r_squared = model.rsquared
        
        product_name = sub_df['product_name'].iloc[0]
        base_avg_price = sub_df['price'].mean()
        base_avg_units = sub_df['units_sold'].mean()
        
        elasticity_map[pid] = {
            "product_name": product_name,
            "elasticity": round(elasticity_coeff, 3),
            "p_value": round(p_value, 4),
            "r_squared": round(r_squared, 3),
            "avg_price": round(base_avg_price, 2),
            "avg_units": round(base_avg_units, 1),
            "intercept": model.params['Intercept'],
            "comp_coeff": model.params['log_competitor_price'],
            "promo_coeff": model.params['is_promo']
        }
        
    return elasticity_map

if __name__ == "__main__":
    results = compute_elasticities()
    for k, v in results.items():
        print(f"Product: {v['product_name']} | Elasticity: {v['elasticity']} (p-val: {v['p_value']})")
