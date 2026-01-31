import imfp

# Step 1: List available databases (optional, to explore)
databases = imfp.imf_databases()
print(databases)  # Look for 'WEO', 'GDD', 'FM', etc.

# Step 2: Example - Debt-to-GDP from World Economic Outlook (WEO)
# Indicator for general government gross debt as % of GDP is often 'GGXWDG_NGDP'
df_weo = imfp.imf_dataset(
    database_id="WEO",              # Dataset code
    country=["NGA"],                # or "NGA" for single
    indicator=["GGXWDG_NGDP"],      # Debt % of GDP (adjust if needed)
    start_year=2000,                # Optional: filter years
    end_year=2025
)

print(df_weo.head())                # Pandas DataFrame with time series
print(df_weo.tail())                # Recent values

# If you want forecasts too (WEO has them)
# The DataFrame will have columns like 'year', 'value', 'country', etc.

# Step 3: Example - From Global Debt Database (GDD) if available in imfp
# GDD indicators might include public debt stock or ratios (check params first)
params_gdd = imfp.imf_parameters("GDD")  # See available indicators/dimensions
print(params_gdd)

df_gdd = imfp.imf_dataset(
    database_id="GDD",
    country=["NGA"],
    # indicator=...  # Use imf_parameters to find exact codes, e.g. public debt % GDP
    start_year=2010
)
print(df_gdd)