# ⚽ Football Player Performance Analytics Dashboard

An interactive, portfolio-quality football (soccer) analytics dashboard built with **Python**, **Streamlit**, **Pandas**, and **Plotly**.

---

> ⚠️ **SYNTHETIC DATA NOTICE**
> All player statistics in this dashboard are **computer-generated** using a reproducible NumPy random seed.
> They are intended **solely for demonstration and portfolio purposes** and do **not** represent real-world
> football results, transfers, or player performances.

---

## Features

| Page | What you get |
|---|---|
| **Overview** | KPI cards (players, goals, assists, minutes, avg rating), top-10 scorers bar chart, season comparison, rating histogram, searchable stats table & CSV download |
| **Player Analysis** | Two-player radar comparison, goals vs assists scatter, shots vs goals scatter with OLS trend line |
| **Team Analysis** | Goals & assists grouped bar, avg rating bar chart, team summary table |
| **Position Analysis** | Rating box plot, stacked avg-stats bar, player-count donut, position callout cards (GK/DEF/MID/FWD) |

**Sidebar filters:** Season · Team · Position · Player — cascade across all pages.

---

## Project Structure

```
Football Analysis Dashboard/
├── app.py                    # Main Streamlit application
├── football_players.csv      # Synthetic dataset (200 rows, 23 columns)
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## Dataset Schema

| Column | Type | Description |
|---|---|---|
| `player_id` | int | Unique player ID |
| `player_name` | str | Full name |
| `age` | int | Age 18–38 |
| `nationality` | str | Country |
| `team` | str | Club (5 fictional teams) |
| `position` | str | GK / DEF / MID / FWD |
| `season` | str | 2022-23 or 2023-24 |
| `matches_played` | int | Appearances |
| `minutes_played` | int | Total minutes |
| `goals` | int | Goals scored |
| `assists` | int | Assists |
| `shots` | int | Total shots |
| `shots_on_target` | int | Shots on target |
| `pass_accuracy` | float | Pass accuracy % |
| `key_passes` | int | Key passes |
| `dribbles_completed` | int | Successful dribbles |
| `tackles` | int | Tackles made |
| `interceptions` | int | Interceptions |
| `yellow_cards` | int | Yellow cards |
| `red_cards` | int | Red cards |
| `clean_sheets` | int | Clean sheets |
| `saves` | int | Saves (GK) |
| `rating` | float | Match rating 1–10 |

---

## Prerequisites

- Python 3.10 or higher
- pip

---

## Run Locally

1. **Clone or download** this repository.

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the dashboard:**
   ```bash
   streamlit run app.py
   ```

5. Open your browser at `http://localhost:8501` — the dashboard loads automatically.

---

## Deploy to Streamlit Community Cloud (Free)

1. Push this project to a **public GitHub repository**.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **"New app"** → select your repo → set **Main file path** to `app.py`.
4. Click **Deploy**. Your app gets a public URL in ~2 minutes.

No environment variables or secrets are required — the app is fully self-contained.

---

## KPI Calculations

All KPIs are computed dynamically from the **filtered** DataFrame:

| KPI | Formula |
|---|---|
| Total Players | `df['player_id'].nunique()` |
| Total Goals | `df['goals'].sum()` |
| Total Assists | `df['assists'].sum()` |
| Total Minutes Played | `df['minutes_played'].sum()` |
| Avg Player Rating | `df['rating'].mean()` (rounded to 2 dp) |

---

## Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web app framework |
| `pandas` | Data manipulation |
| `numpy` | Numerical operations & data generation |
| `plotly` | Interactive charts |
| `statsmodels` | OLS trendline on shots vs goals scatter |

---

## License

This project is released for educational and portfolio use. The synthetic dataset has no licensing restrictions.
