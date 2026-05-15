# 📈 Quantitative Trading Performance Analytics Portal
### *Hyperliquid DEX Execution Correlation with Crypto Fear & Greed Sentiment*

---

## 🎯 Project Overview
This production-ready engineering pipeline evaluates the impact of market psychology on decentralized exchange execution. By correlating over **211,000 live trade logs** from the **Hyperliquid DEX** with historical timelines from the **Crypto Fear & Greed Index**, the application discovers whether extreme crowd emotions present statistically valid trading signals ("Alpha").

The system is engineered as a modern, decoupled full-stack architecture running a high-performance **FastAPI data engine** linked dynamically to an interactive, responsive, dark-themed HTML/JS terminal front-end dashboard.

---

## 🏗️ System Architecture & Project Structure
The repository is strictly structured using standard enterprise data science and web development patterns:

```text
▼ PRIMETRADE_TRADING_ANALYSIS
  ▶ data/               # Raw underlying Web3 & Sentiment CSV files
  ▶ notebooks/          # Exploratory Analysis Jupyter Notebook with custom UI cards
  ▶ output/             # Exported visual analysis assets (Equity curve, distributions)
  ▼ public/             
      📄 index.html     # Front-End Terminal Dashboard (Vanilla JS Fetch Streams)
  ▼ src/                
      📄 backend_server.py # FastAPI Application Server Gateway
      📄 data_loader.py    # Robust Data Ingestion & Case-Insensitive Fuzzy Mapping
      📄 plots.py         # Matplotlib/Seaborn Analytical visualization suites
  📄 requirements.txt   # Framework package dependency manifest
