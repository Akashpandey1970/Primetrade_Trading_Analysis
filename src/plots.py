import matplotlib.pyplot as plt
import seaborn as sns

def plot_sentiment_performance(df):
    # Apply a professional dark theme suitable for Web3/Finance
    plt.style.use('dark_background')
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Standard order for the Fear & Greed Index classifications
    order = ['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed']
    
    # Validation
    if 'closedPnL' not in df.columns or 'Classification' not in df.columns:
        print("Error: Required columns ('closedPnL' and 'Classification') are missing.")
        return

    # Generate the Bar Plot
    sns.barplot(x='Classification', y='closedPnL', data=df, order=order, palette='coolwarm', ax=ax1)
    
    plt.title('Hyperliquid Trading Performance by Market Sentiment', fontsize=16, pad=20)
    plt.xlabel('Market Sentiment Classification', fontsize=12)
    plt.ylabel('Average Closed PnL (USDC)', fontsize=12)
    
    plt.tight_layout()
    plt.show()