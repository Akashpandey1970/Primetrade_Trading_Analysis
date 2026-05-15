import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from scipy.stats import ttest_ind
import numpy as np

# System path insertion to safely discover sibling modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_loader import load_and_merge_data

app = FastAPI(title="Primetrade.ai Core Analytics Engine")

# Security Gateway (CORS) allowing browser-to-server cross routing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize data pipeline into operational RAM state
df = load_and_merge_data('data/hyperliquid_data.csv', 'data/fear_greed_index.csv')

# --- API ENDPOINT FOR DATA ---
@app.get("/api/metrics")
def calculate_system_metrics():
    total_trades = int(len(df))
    net_pnl = float(df['closedPnL'].sum()) if 'closedPnL' in df.columns else 0.0
    
    profitable_count = len(df[df['closedPnL'] > 0]) if 'closedPnL' in df.columns else 0
    win_rate = float((profitable_count / total_trades) * 100) if total_trades > 0 else 0.0

    fear_series = df[df['Classification'].str.lower() == 'extreme fear']['closedPnL'].dropna()
    greed_series = df[df['Classification'].str.lower() == 'extreme greed']['closedPnL'].dropna()
    
    t_stat, p_val = 0.0, 1.0
    if len(fear_series) > 1 and len(greed_series) > 1:
        t_stat, p_val = ttest_ind(fear_series, greed_series, equal_var=False)
        if np.isnan(t_stat) or np.isnan(p_val):
            t_stat, p_val = 0.0, 1.0

    return {
        "metrics": {
            "totalTrades": total_trades,
            "netPnL": round(net_pnl, 2),
            "winRate": round(win_rate, 1)
        },
        "stats": {
            "tStatistic": round(float(t_stat), 4),
            "pValue": round(float(p_val), 4),
            "significant": bool(p_val < 0.05),
            "verdict": "Statistically Significant Signal" if p_val < 0.05 else "Insignificant Market Noise"
        }
    }

# --- THE FIX: SERVE THE FRONTEND AS THE HOME PAGE ---
@app.get("/")
def serve_frontend():
    # Looks for 'public/index.html' from your root project directory
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'public', 'index.html'))
    return FileResponse(frontend_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend_server:app", host="127.0.0.1", port=8000, reload=True)