# 📊 Claude Code Usage Analytics Platform

## 🌟 Project Overview
This platform is a **comprehensive end-to-end analytics solution** designed to process raw telemetry data from **Claude Code (Anthropic's CLI tool)** and transform it into **actionable business intelligence**.

The project includes:

- A robust **ETL pipeline**
- A structured **SQL storage layer**
- An interactive **Streamlit analytics dashboard**

The platform provides insights into:

- Developer behavior
- Token consumption
- Infrastructure cost distribution

---

# 🚀 Key Features

### ⚙️ Scalable ETL Pipeline
- Ingests complex **nested JSONL telemetry logs**
- Cleans and normalizes raw telemetry data
- Joins logs with **employee metadata**

### 🗄️ Structured Storage
- Uses **SQLite** for efficient querying
- Optimized schema for analytical workloads

### 📊 Interactive Visualization
Dashboard features include:

- Real-time filtering by **engineering practice**
- Filtering by **AI model**
- KPI tracking:
  - Total Cost
  - Active Users
  - Token Usage
  - Event Count
- **Peak usage hour analysis**
- **Tool distribution charts**

### 🤖 Predictive Analytics (Bonus)
Integrated **Machine Learning (Linear Regression)** to forecast **daily infrastructure spend for the next 7 days**.

### 🛡️ Data Validation
- Handles malformed logs
- Automated data sanitization
- Duplicate cleaning

---

# 🛠️ Tech Stack

| Category | Technology |
|--------|--------|
| Language | Python 3.x |
| Data Engineering | Pandas, JSON, SQLite3 |
| Visualization | Streamlit, Plotly Express |
| Machine Learning | Scikit-learn (Linear Regression) |
| Environment | Python Virtual Environment (venv) |

---

# 🏗️ Architecture

### 1️⃣ Data Generation
Synthetic telemetry generation simulating **real-world Claude Code usage**.

### 2️⃣ ETL Process (`process_data.py`)

**Extract**
- Reads raw JSONL telemetry logs

**Transform**
- Flattens nested JSON structures
- Cleans duplicates
- Merges logs with CSV employee metadata

**Load**
- Stores clean dataset into a **SQLite database**

### 3️⃣ Analytics Interface (`app.py`)
- Serves an interactive **Streamlit dashboard**
- Runs **predictive models** dynamically

---

# ⚙️ Installation & Setup

## 1️⃣ Clone the Repository

```bash
git clone <your-repository-url>
cd <folder-name>
```

---

## 2️⃣ Set Up Virtual Environment

```bash
python -m venv .venv
```

### Activate (Windows)

```bash
.venv\Scripts\activate
```

### Activate (macOS/Linux)

```bash
source .venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Generate & Process Data

> **Note:** The raw dataset can exceed **500MB**, so it is generated locally.

### Generate Raw Telemetry

```bash
python generate_fake_data.py --num-users 100 --num-sessions 5000 --days 60
```

### Run ETL Pipeline (Creates SQL Database)

```bash
python process_data.py
```

---

## 5️⃣ Launch Dashboard

```bash
streamlit run app.py
```

---

# 📈 Insights Preview

Based on the analyzed telemetry:

### ⏰ Peak Activity
Developer activity peaks between **09:00 – 18:00**, aligning with standard business hours.

### 👨‍💻 Top Consumers
**Frontend** and **ML Engineering** practices generate the highest **token expenditure**.

### 🧠 Model Preference
**Claude Haiku** is the most frequently used model (**~39%**), indicating preference for **speed in routine coding tasks**.

### 🛠️ Tool Usage
Most triggered tools:

- `Read`
- `Bash`

This suggests heavy **code exploration and terminal interaction**.

---

## 🤖 LLM Usage Log

This project was developed using an **AI-assisted workflow**, following the AI-first philosophy encouraged by Provectus.

### Tools Used
- Claude 3.5 Sonnet
- ChatGPT

### How AI Was Used
AI tools were used to accelerate development and assist in several areas:

- Designing the **ETL pipeline structure**
- Generating and refining **SQL schema**
- Assisting with **JSON telemetry parsing**
- Creating **Plotly-based visualizations**
- Debugging and improving parts of the Python code

### Developer Validation
All AI-generated code was carefully **reviewed, tested, and integrated manually**.

Special attention was given to:

- Data integrity
- Timestamp parsing and type-safety
- Performance considerations in the ETL pipeline
---

# 📁 Project Structure

```
.
├── generate_fake_data.py   # Telemetry simulator
├── process_data.py         # ETL pipeline + SQL loader
├── app.py                  # Streamlit dashboard + ML forecasting
├── employees.csv           # Static employee metadata
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── claude_analytics.db     # SQLite database (generated after ETL)
```

---

# 📌 Summary

This project demonstrates a **complete analytics workflow**:

**Raw Telemetry → ETL Processing → SQL Storage → Interactive Analytics → ML Forecasting**

It showcases **data engineering, analytics, and machine learning integration in a single platform**.