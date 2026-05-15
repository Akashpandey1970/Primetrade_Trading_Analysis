import pandas as pd

def load_and_merge_data(trader_path, sentiment_path):
    # Load files
    trader_df = pd.read_csv(trader_path)
    sentiment_df = pd.read_csv(sentiment_path)

    # 1. FIX TRADER TIMESTAMP
    # Your CSV uses 'Timestamp'. We convert it to numeric first to avoid NaT errors.
    if 'Timestamp' in trader_df.columns:
        # Convert to numeric, then to datetime
        t_numeric = pd.to_numeric(trader_df['Timestamp'], errors='coerce')
        trader_df['Date'] = pd.to_datetime(t_numeric, unit='ms').dt.normalize()
    
    # 2. FIX SENTIMENT DATE
    s_date_col = 'Date' if 'Date' in sentiment_df.columns else 'date'
    sentiment_df['Date'] = pd.to_datetime(sentiment_df[s_date_col]).dt.normalize()

    # 3. STANDARDIZE CLASSIFICATION
    if 'Classification' not in sentiment_df.columns:
        # Find column that looks like 'classification' or 'value'
        c_col = next((c for c in sentiment_df.columns if 'class' in c.lower()), None)
        if c_col:
            sentiment_df = sentiment_df.rename(columns={c_col: 'Classification'})

    # 4. CLEAN AND MERGE
    trader_df = trader_df.dropna(subset=['Date'])
    sentiment_df = sentiment_df.dropna(subset=['Date']).drop_duplicates('Date')

    # Use 'left' join so the code doesn't crash if dates don't overlap perfectly
    merged_df = pd.merge(trader_df, sentiment_df, on='Date', how='left')
    
    # Fill missing values so the chart can still draw
    merged_df['Classification'] = merged_df['Classification'].fillna('Neutral')

    # 5. MAP PNL
    pnl_col = 'Closed PnL' if 'Closed PnL' in merged_df.columns else 'closedPnL'
    if pnl_col in merged_df.columns:
        merged_df['closedPnL'] = merged_df[pnl_col].fillna(0)

    print(f"Merge Successful! Rows processed: {len(merged_df)}")
    return merged_df