<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=6A0DAD&height=180&section=header&text=ETL%20Banking%20Data%20Pipeline&fontSize=40&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Extract%20%7C%20Transform%20%7C%20Load%20%7C%20Analyze&descAlignY=58&descAlign=50" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-7B2FBE?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/BeautifulSoup-4B0082?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Status-Complete-6A0DAD?style=for-the-badge" />
</p>

---

## 📌 Project Overview

A fully automated, end-to-end **ETL (Extract, Transform, Load) pipeline** built in Python that scrapes real-world banking data from Wikipedia, transforms market capitalization values across multiple currencies, and loads the structured output into both a **CSV file** and a **SQLite relational database** — with full pipeline logging at every stage.

This project demonstrates core **Data Engineering** competencies including web scraping, data transformation, multi-format data loading, SQL querying, and production-style logging.

---

## 🎯 Problem Statement

Global banking market capitalization data is published in USD only. Financial analysts and data teams often need this data converted across multiple currencies (GBP, EUR, INR) in a structured, queryable format — not scattered across web pages.

This pipeline automates that entire workflow: from raw web data to a clean, analysis-ready database.

---

## 🏗️ Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ETL PIPELINE FLOW                        │
│                                                             │
│  🌐 Wikipedia        🔄 Transform         💾 Load          │
│  ───────────         ───────────         ──────             │
│  Web Scraping   →   Currency       →    CSV File            │
│  (BeautifulSoup)    Conversion          SQLite DB           │
│                     (USD→GBP            code_log.txt        │
│                      USD→EUR                                │
│                      USD→INR)                               │ 
│                                                             │
│  📋 Logging at every stage via code_log.txt                 │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚙️ What Each Function Does

| Function | Type | Description |
|:---|:---:|:---|
| `log_progress()` | Utility | Timestamps and logs every pipeline stage to `code_log.txt` |
| `extract()` | Extract | Scrapes top 10 largest banks by market cap from Wikipedia using BeautifulSoup |
| `transform()` | Transform | Reads exchange rates from CSV and converts USD market cap to GBP, EUR, and INR |
| `load_to_csv()` | Load | Saves the transformed DataFrame to a structured CSV file |
| `load_to_db()` | Load | Writes the DataFrame to a SQLite database table using pandas `to_sql` |
| `run_query()` | Analyze | Executes and prints SQL queries against the loaded database |

---

## 📊 Data Flow

### Stage 1 — Extract
Scrapes the **Top 10 Largest Banks** table from Wikipedia (archived version):
```
Columns extracted:
├── Name          (Bank name)
└── MC_USD_Billion (Market Cap in USD Billions)
```

### Stage 2 — Transform
Reads `exchange_rate.csv` and applies currency conversion:
```
MC_USD_Billion  →  MC_GBP_Billion  (× GBP rate)
MC_USD_Billion  →  MC_EUR_Billion  (× EUR rate)
MC_USD_Billion  →  MC_INR_Billion  (× INR rate)
```

### Stage 3 — Load
```
Output 1: Largest_banks_data.csv  (flat file for Excel/BI tools)
Output 2: Banks.db → Largest_banks table (SQLite for SQL queries)
```

### Stage 4 — Query
```sql
-- All banks with full currency data
SELECT * FROM Largest_banks;

-- Average market cap in GBP
SELECT AVG(MC_GBP_Billion) FROM Largest_banks;

-- Top 5 banks by name
SELECT Name FROM Largest_banks LIMIT 5;
```

---

## 📁 Repository Structure

```
ETL-BANKING-DATA-PIPELINE/
│
├── bank_project.py          # Main ETL pipeline script
├── exchange_rate.csv        # Currency conversion rates (GBP, EUR, INR)
├── Largest_banks_data.csv   # Output: transformed data in CSV format
├── Banks.db                 # Output: SQLite database with loaded table
├── code_log.txt             # Pipeline execution log with timestamps
└── README.md
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|:---|:---|
| **Python 3.x** | Core pipeline language |
| **BeautifulSoup4** | HTML parsing and web scraping |
| **Requests** | HTTP requests to fetch Wikipedia page |
| **Pandas** | Data manipulation and transformation |
| **NumPy** | Numerical operations |
| **SQLite3** | Relational database for structured storage |
| **Datetime** | Timestamp generation for logging |

---

## 🚀 How to Run

### Prerequisites
```bash
pip install requests beautifulsoup4 pandas numpy
```

### Run the Pipeline
```bash
python bank_project.py
```

### Expected Output
```
Query: SELECT * FROM Largest_banks
                      Name  MC_USD_Billion  MC_GBP_Billion  MC_EUR_Billion  MC_INR_Billion
0            JPMorgan Chase          432.92          346.34          402.62        35910.71
1           Bank of America          231.52          185.22          215.31        19204.58
...

Query: SELECT AVG(MC_GBP_Billion) FROM Largest_banks
   AVG(MC_GBP_Billion)
0              151.987

Query: SELECT Name from Largest_banks LIMIT 5
              Name
0   JPMorgan Chase
1  Bank of America
2    ICBC
3  Agricultural Bank of China
4         Bank of China
```

---

## 📋 Pipeline Log Sample

```
2025-07-30-21:11:15 : Preliminaries complete. Initiating ETL process
2025-07-30-21:11:15 : Data extraction complete. Initiating Transformation process
2025-07-30-21:11:15 : Data transformation complete. Initiating Loading process
2025-07-30-21:11:15 : Data saved to CSV file
2025-07-30-21:11:15 : SQL Connection initiated
2025-07-30-21:11:15 : Data loaded to Database as a table, Executing queries
2025-07-30-21:11:15 : Process Complete
2025-07-30-21:11:15 : Server Connection closed
```

---

## 💡 Key Learnings

- Implemented a **production-style ETL pipeline** with modular functions
- Applied **web scraping** on real Wikipedia data using BeautifulSoup
- Performed **multi-currency transformation** using exchange rate mapping
- Loaded data to **both flat file (CSV) and relational database (SQLite)**
- Built **end-to-end logging** with timestamped entries for pipeline monitoring
- Executed **analytical SQL queries** directly on the loaded database

---

## 🔮 Future Improvements

- [ ] Schedule pipeline with **Apache Airflow** for daily runs
- [ ] Add **data validation** checks between each stage
- [ ] Expand to load into **PostgreSQL or BigQuery** for cloud storage
- [ ] Build a **Power BI dashboard** on top of the SQLite output
- [ ] Add **error handling and retry logic** for web scraping failures
- [ ] Containerize with **Docker** for portable deployment

---

## 👤 Author

**Muhammad Obaid Ullah**
Data Analytics | BS Software Engineering @ PAF-IAST

[![GitHub](https://img.shields.io/badge/GitHub-Obaydawan-181717?style=flat-square&logo=github)](https://github.com/Obaydawan)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/obayd-awan)

---

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=6A0DAD&height=100&section=footer" />
</p>
