import imfp
import pandas as pd

# Fetch parameters for WEO
params = imfp.imf_parameters("WEO")

# Print high-level structure
print("Available parameter keys in params:", list(params.keys()))

# Focus on 'indicator' (most useful for finding debt codes)
if 'indicator' in params:
    indicators_df = params['indicator']
    
    # Print columns and shape
    print("\nColumns in 'indicator' DataFrame:", indicators_df.columns.tolist())
    print("Number of rows:", len(indicators_df))
    
    # Print first 10 rows (or more) to see actual data
    print("\nFirst 10 rows of indicators:\n")
    print(indicators_df.head(10).to_string(index=False))
    
    # Print a few sample values from each object/string column to spot descriptions
    print("\nSampling possible description columns:")
    for col in indicators_df.columns:
        if indicators_df[col].dtype == 'object':
            unique_vals = indicators_df[col].dropna().unique()[:5]  # First 5 unique
            print(f"Column '{col}': {unique_vals}")
    
    # Try to auto-detect a description column and filter for 'debt'
    desc_candidates = [col for col in indicators_df.columns if 'desc' in col.lower() or 'title' in col.lower() or 'note' in col.lower() or 'label' in col.lower()]
    if desc_candidates:
        desc_col = desc_candidates[0]  # Take the first likely one
        print(f"\nTrying filter on likely description column: '{desc_col}'")
        debt_indicators = indicators_df[
            indicators_df[desc_col].str.contains("debt", case=False, na=False)
        ]
        if not debt_indicators.empty:
            print("\nFound debt-related indicators (showing code + description):")
            print(debt_indicators.head(15))  # Adjust as needed
        else:
            print("No matches for 'debt' — try keywords like 'gross debt', 'government debt', etc.")