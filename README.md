# 🏎️ Formula 1 2025 Season Analysis Dashboard

> An interactive, data-driven analytics dashboard that dissects the 2025 F1 season through six distinct performance lenses — built with Python, Streamlit, and Plotly.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

<p align="center">
  <img src="banner.png" alt="F1 2025 Dashboard Banner" width="100%">
</p>

---

## 📌 Overview

Formula 1 generates an enormous amount of performance data every race weekend — but raw lap times and points tables rarely tell the full story. This project transforms a season's worth of race, qualifying, and reliability data into a **polished, F1-branded analytics dashboard** that surfaces the *why* behind the championship standings.

Rather than building a single chart, the dashboard is structured as **six independent analytical narratives**, each answering a specific question a team strategist or F1 fan would actually ask — from *"Does qualifying pace predict race results?"* to *"Which drivers are wasting their pace by not finishing races?"*

**📊 Dataset:** 2025 F1 season — race pace, qualifying pace, points, DNFs, sprint results

---

## ✨ Key Features

- **6 Independent Analytical Modules** — each with its own KPIs, visualization, ranked leaderboards, and written insights
- **Dynamic Filtering Engine** — filter by team, driver, race-count threshold, or include/exclude part-season drivers, with every chart, KPI, and table reacting instantly
- **Custom KPI Cards** — driver headshots paired with computed metrics (fastest pace, best points-per-race, reliability, etc.), with graceful image fallbacks
- **Auto-Generated Data Storytelling** — narrative insight boxes are *not* static text; they're dynamically computed from the filtered dataset every time a user changes a filter
- **Official F1 Team Color Mapping** — every visualization uses real 2025 livery colors for instant team recognition
- **Custom Dark "Pit Lane" Theme** — hand-built CSS overrides on top of Streamlit's component model (cards, sidebar, dataframes, dividers, hover states)
- **Responsive Two-Panel Layout** — primary chart paired with live leaderboard tables (Top 5 / Bottom 5) for at-a-glance context without leaving the page

---

## 📊 The Six Insights

| # | Insight | Core Question Answered |
|---|---------|------------------------|
| 1 | **Race Pace vs. Points Efficiency** | Does being fast actually translate into scoring points? |
| 2 | **Race Consistency vs. Reliability** | Who delivers the same lap time every lap, and who actually finishes races? |
| 3 | **Team Dominance Hierarchy** | Which constructors win through driver depth vs. a single superstar? |
| 4 | **DNF Risk Profile** | How many championship points does unreliability actually cost? |
| 5 | **Saturday vs. Sunday Pace** | Does qualifying speed predict race-day performance? |
| 6 | **Sprint vs. Race Masters** | Are sprint-format specialists the same drivers who win on Sundays? |

Each module computes its metrics **live** from the filtered dataframe — nothing is hardcoded — so the written analysis updates automatically when a user filters down to a specific team or driver subset.

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **App Framework** | [Streamlit](https://streamlit.io/) | Reactive web UI, sidebar filters, state-driven re-rendering |
| **Data Processing** | [Pandas](https://pandas.pydata.org/) / [NumPy](https://numpy.org/) | Aggregation, groupby analytics, vectorized efficiency calculations |
| **Visualization** | [Plotly Express](https://plotly.com/python/plotly-express/) / [Graph Objects](https://plotly.com/python/graph-objects/) | Interactive scatter plots, bar charts, trend lines, reference lines |
| **Image Handling** | [Pillow (PIL)](https://python-pillow.org/) | Driver headshot rendering with fallback handling |
| **Styling** | Custom CSS injected via `st.markdown` | F1-branded dark theme, hover animations, gradient cards |

---

## 🧠 Engineering Highlights

A few implementation details worth calling out for a technical reviewer:

- **Single source-of-truth filtering pipeline** — all six insights consume the same `filtered_df`, so adding a new page never requires duplicating filter logic.
- **Defensive rendering** — every driver headshot lookup is wrapped in a `try/except` with a styled placeholder fallback, so a missing image file never breaks the layout.
- **Derived metrics computed once, reused everywhere** — `efficiency` (points-per-race normalized by pace) is calculated centrally and feeds the scatter plot, KPI cards, leaderboards, and narrative text consistently.
- **Edge-case handling for sparse data** — the Sprint vs. Race module gracefully handles seasons/filters where no sprint races occurred, rather than throwing on an empty dataframe.
- **Dynamic correlation interpretation** — Pearson correlation coefficients are programmatically bucketed into "Strong / Moderate / Weak" with matching color coding, rather than just displaying a raw number.

---

## 📁 Project Structure

```
f1_analysis_project/
│
├── st_f1_project.py          # Main Streamlit application
├── F1_project.ipynb          # Exploratory data analysis & feature engineering
├── final_f1_data.csv         # Season dataset (race pace, points, DNFs, etc.)
├── media_1.csv                # Supplementary race/session data
├── media_2.csv
├── media_3.csv
├── banner.png                 # Dashboard header banner
├── f1_headshot/                # Driver headshot images
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/TANMAY-0306/f1_analysis_project.git
cd f1_analysis_project

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run st_f1_project.py
```

The app will open automatically at `http://localhost:8501`.

### `requirements.txt`

```
streamlit
pandas
numpy
plotly
Pillow
```

---

## 📈 Dataset

The dashboard runs on `final_f1_data.csv`, a per-driver season aggregate with the following columns:

| Column | Description |
|---|---|
| `DriverNumber` | Driver's car number (used as dataframe index) |
| `Driver`, `TeamName` | Driver and constructor identity |
| `RacesEntered`, `DNFs`, `DNF_Rate` | Race participation and retirement metrics |
| `MeanPositionDelta`, `MedianPositionDelta` | Average/median positions gained or lost during races |
| `FinishCount`, `FinishRate` | Races completed and finish reliability |
| `TotalRacePoints`, `PointsPerRace` | Points scored in points-paying (non-sprint) races |
| `MeanRacePace`, `MedianRacePace` | Average/median race lap time (seconds) |
| `MeanQualifyingPace`, `MedianQualifyingPace` | Average/median qualifying lap time (seconds) |
| `MedianRaceIQR` | Interquartile range of race lap times — a consistency measure |
| `SprintStarts`, `SprintFinishes`, `SprintFinishRate`, `SprintDNFs` | Sprint race participation and reliability |
| `MeanSprintPositionDelta`, `MedianSprintPositionDelta`, `SprintPositionDeltaIQR` | Sprint position-change metrics |
| `TotalSprintPoints`, `SprintPointsPerSprint` | Sprint-format scoring |
| `TotalPoints`, `SprintPointShare`, `NormalizedTotalPoints` | Combined season scoring, with sprint contribution share and a normalized total |
| `HeadshotUrl` | Local path to driver headshot image |

---

## 🗺️ Roadmap

- [ ] Add real screenshots of each insight page to this README
- [ ] Build an **XGBoost classification model** to predict podium finishes using race pace, qualifying pace, and reliability features
- [ ] Add export-to-PDF for individual insight reports

---

## 👤 Author

**Tanmay Chadha**
[LinkedIn](https://www.linkedin.com/in/tanmaychadha03) · [Email](mailto:chadhatanmay85@gmail.com)

If you found this project interesting, feel free to ⭐ the repo or reach out — always happy to talk F1 data or Streamlit engineering.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
