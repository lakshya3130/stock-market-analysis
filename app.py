from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import yfinance as yf
import requests
from textblob import TextBlob

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Lakshya@19',
    'database': 'stock_app'
}

db = mysql.connector.connect(**db_config)
cursor = db.cursor(dictionary=True)

NEWS_API_KEY = 'your_news_api_key'


# ---------------- SYMBOL MAPPING ----------------
symbol_to_name = {
    "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "Tata Consultancy Services",
    "HDFCBANK.NS": "HDFC Bank",
    "INFY.NS": "Infosys",
}


def get_company_name(stock_symbol):
    if stock_symbol in symbol_to_name:
        return symbol_to_name[stock_symbol]

    try:
        stock = yf.Ticker(stock_symbol)
        return stock.info.get("longName", stock_symbol)
    except:
        return stock_symbol


@app.route('/')
def home():
    return render_template('index.html')


# ---------------- USER AUTH ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, password)
            )
            db.commit()
            return redirect('/login')
        except mysql.connector.Error:
            return "Username already exists."

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_input = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password_input):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect('/dashboard')

        return "Invalid credentials."

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# ---------------- DASHBOARD ----------------
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect('/login')

    dates, prices = [], []
    stock_symbol, price = "", "N/A"

    if request.method == 'POST':
        stock_symbol = request.form['symbol'].strip().upper()

        try:
            stock = yf.Ticker(stock_symbol)
            data = stock.history(period="1d")

            # SAFE PRICE FETCH
            if not data.empty and 'Close' in data.columns:
                price = round(data['Close'].iloc[-1], 2)

            # SAFE CHART FETCH
            hist_data = stock.history(period="7d")
            if not hist_data.empty and 'Close' in hist_data.columns:
                dates = [str(date.date()) for date in hist_data.index]
                prices = [round(p, 2) for p in hist_data['Close'].tolist()]

            session['last_stock'] = stock_symbol

        except:
            price = "N/A"

    return render_template(
        'dashboard.html.jinja2',
        stock_symbol=stock_symbol,
        price=price,
        dates=dates,
        prices=prices
    )


# ---------------- NEWS ----------------
@app.route('/news')
def news():
    if 'username' not in session:
        return redirect('/login')

    stock_symbol = session.get('last_stock', '')
    if not stock_symbol:
        return redirect('/dashboard')

    company_name = get_company_name(stock_symbol)
    sentiment_counts = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
    headlines = []

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q=\"{company_name}\"&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    )

    try:
        response = requests.get(url).json()
        articles = response.get('articles', [])[:10]

        for article in articles:
            title = article.get('title', '')
            if not title:
                continue

            polarity = TextBlob(title).sentiment.polarity
            sentiment = "Positive" if polarity > 0 else "Negative" if polarity < 0 else "Neutral"

            sentiment_counts[sentiment] += 1

            headlines.append({
                'title': title,
                'source': article.get('source', {}).get('name', ''),
                'url': article.get('url', '#'),
                'sentiment': sentiment
            })

    except:
        pass

    session['sentiment_data'] = headlines

    return render_template(
        'news.html',
        stock_symbol=stock_symbol,
        company_name=company_name,
        headlines=headlines,
        sentiment_counts=sentiment_counts
    )


# ---------------- SENTIMENT ----------------
@app.route('/sentiment')
def sentiment():
    headlines = session.get('sentiment_data', [])
    stock_symbol = session.get('last_stock', '')

    if not headlines:
        return redirect('/dashboard')

    sentiment_counts = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
    for h in headlines:
        sentiment_counts[h['sentiment']] += 1

    return render_template(
        'sentiment.html',
        stock_symbol=stock_symbol,
        headlines=headlines,
        sentiment_counts=sentiment_counts
    )


# ---------------- PORTFOLIO ----------------
@app.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    if request.method == 'POST':

        # ADD STOCK
        if 'add_stock' in request.form:
            symbol = request.form['symbol'].strip().upper()
            quantity = int(request.form['quantity'])
            price = float(request.form['price'])

            cursor.execute(
                "INSERT INTO portfolio (user_id, symbol, quantity, price) VALUES (%s, %s, %s, %s)",
                (user_id, symbol, quantity, price)
            )
            db.commit()

        # REMOVE STOCK
        if 'remove_stock' in request.form:
            stock_id = int(request.form['remove_stock'])
            cursor.execute(
                "DELETE FROM portfolio WHERE id = %s AND user_id = %s",
                (stock_id, user_id)
            )
            db.commit()

    cursor.execute("SELECT * FROM portfolio WHERE user_id = %s", (user_id,))
    holdings = cursor.fetchall()

    total_value = 0

    for stock in holdings:
        try:
            live_data = yf.Ticker(stock['symbol']).history(period="1d")

            if not live_data.empty and 'Close' in live_data.columns:
                live_price = live_data['Close'].iloc[-1]
            else:
                live_price = stock['price']

        except:
            live_price = stock['price']

        stock['live_price'] = round(live_price, 2)
        stock['total'] = round(stock['quantity'] * live_price, 2)
        total_value += stock['total']

    return render_template(
        'portfolio.html',
        holdings=holdings,
        total=round(total_value, 2)
    )


if __name__ == '__main__':
    app.run(debug=True)
