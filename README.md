# DAOlytics

**DAOlytics** is an entry-level SaaS project designed for small crypto traders and micro DAOs.  
It automates trade and treasury analytics by taking CSV data and generating clean metrics and charts.

---

## 🚀 Problem

Small traders and DAO managers struggle with:

- Tracking profit/loss accurately
- Monitoring win rate and trade performance
- Creating reports efficiently
- Avoiding spreadsheet errors

DAOlytics solves this by:

1. Uploading CSVs of trades or treasury transactions
2. Generating PnL, win rate, and charts
3. Delivering downloadable reports

---

## 🧰 Tech Stack

| Layer | Tech |
|-------|------|
| Backend | Python + FastAPI |
| Frontend | HTML + Jinja2 templates |
| Database | SQLite |
| Authentication | Email/password + bcrypt |
| Analytics | Pandas + Matplotlib |
| Deployment | Local / Render / Heroku (optional) |

---

## ⚡ Features

- User registration and login
- CSV file upload
- Automatic analysis:
  - Profit & Loss calculation
  - Win rate percentage
  - PnL over time chart
- Downloadable chart/report
- Portfolio-ready structure

---

## 🏗️ Installation / Running Locally

1. Clone the repo:

```bash
git clone https://github.com/Murry80/daolytics.git
cd daolytics
