
# 📈 Stock Market Analysis

A Flask-based Stock Market Analysis web application that provides users with real-time stock information, latest financial news, sentiment analysis, and portfolio management.

## 🚀 Features

- 📊 Live Stock Price Tracking
- 📰 Latest Stock Market News
- 😊 News Sentiment Analysis
- 💼 Portfolio Management
- 🔍 Search Stocks by Symbol
- 🔐 User Login & Registration
- 📱 Responsive Web Interface

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- Bootstrap
- Jinja2 Templates

### Backend
- Python
- Flask

### Database
- MySQL

### APIs & Libraries
- yFinance
- News API
- TextBlob
- Pandas
- Requests

---

## 📂 Project Structure

```text
stock_market_analyze/
│
├── app.py
├── requirements.txt
├── README.md
│
├── database/
│   └── schema.sql
│
├── static/
│   └── style.css
│
├── templates/
│   ├── dashboard.html.jinja2
│   ├── index.html
│   ├── layout.html
│   ├── login.html
│   ├── news.html
│   ├── portfolio.html
│   ├── register.html
│   └── sentiment.html
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/lakshya3130/stock-market-analysis.git
```

### 2. Move to the project directory

```bash
cd stock-market-analysis
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the MySQL database

Import the SQL file located at:

```text
database/schema.sql
```

### 5. Update the MySQL connection details

Open **app.py** and update:

- Host
- Username
- Password
- Database Name

### 6. Run the application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

## 📸 Screens

- Dashboard
- Login Page
- Register Page
- Live Stock Prices
- News Section
- Sentiment Analysis
- Portfolio

---

## 📈 Modules

### Dashboard
Displays live stock prices and market overview.

### News
Shows the latest financial news related to selected stocks.

### Sentiment Analysis
Analyzes market news using TextBlob to determine whether the sentiment is:

- Positive 😊
- Neutral 😐
- Negative 😞

### Portfolio
Allows users to manage stock holdings and track investments.

---

## 📦 Requirements

- Python 3.x
- Flask
- MySQL
- yfinance
- TextBlob
- Pandas
- Requests

Install using:

```bash
pip install -r requirements.txt
```

---

## 🎯 Future Improvements

- 📈 Interactive Charts
- 🔔 Price Alerts
- 🤖 AI Stock Prediction
- 📱 Mobile Responsive Dashboard
- ☁️ Cloud Deployment
- 📊 Portfolio Performance Graphs

---

## 👨‍💻 Author

**Lakshya Kumar Dehariya**

- GitHub: https://github.com/lakshya3130
- LinkedIn: https://www.linkedin.com/in/lakshya-dehariya-66a903339/

---

## ⭐ Support

If you found this project helpful, please consider giving it a ⭐ on GitHub.

---

## 📜 License

This project is developed for educational and learning purposes.
