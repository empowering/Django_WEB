## export API_KEY=pk_df09f1aeb44740248ac5f0ac95814416

import os
import sqlite3

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd, total


# Configure application
app = Flask(__name__)
app.run(debug=True, host='0.0.0.0')

# Debug Mode
app.config['ENV'] = 'development'


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


# Make sure API key is set

if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    userid = session["user_id"]

    # SQLite DB 연결
    conn = sqlite3.connect('finance.db', timeout=5, check_same_thread = False)
    # Connection 으로부터 Cursor 생성
    cur = conn.cursor()
    # SQL 쿼리 실행
    cur.execute("SELECT * FROM portfolio WHERE user_id = (?)", (userid,))
    # 데이타 Fetch
    rows = cur.fetchall()
    return render_template("main.html", portfolio = rows)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol") :
            return apology("You forgot to type symbol", 403)
        if not lookup(request.form.get("symbol")):
            return apology("invalid Symbol name", 403)
        else :
            # take info through user's input / lookup function
            userid = session["user_id"]
            symbol = request.form.get("symbol")
            shares = int(request.form.get("shares"))
            name = lookup(symbol)["name"]
            price = lookup(symbol)["price"]

            # import portfolio from db
            rows = db.execute("SELECT * FROM portfolio WHERE user_id = :userid AND symbol = :symbol",
                          userid=userid, symbol=symbol)
            # import cash balance from db
            cash = db.execute("SELECT cash FROM users WHERE id = :userid", userid=userid)
            balance = float(cash[0]['cash']) - total(float(shares),price)
            balance = round(balance,2)

            # Create NEW ONE if the user purchased shares from the symbol
            if not balance < 0:
                db.execute("UPDATE users SET cash = :cash WHERE id = :userid", cash=balance, userid=userid)
                db.execute("INSERT INTO purchases (user_id, Symbol, Shares) VALUES(?,?,?)", userid, symbol, shares)

                if len(rows) != 1 :
                    db.execute("INSERT INTO portfolio (user_id, Symbol, Name, Shares, Price, TOTAL) VALUES(?,?,?,?,?,?)", userid, symbol, name, shares, price, round(total(shares,price),2))

                # Else, update the existing table
                else :
                    newshares = rows[0]["Shares"] + int(shares)
                    newtotal = total(newshares,price)
                    db.execute("UPDATE portfolio SET Shares = :shares, TOTAL = :total WHERE user_id = :userid and Symbol =:symbol", shares=newshares, total=newtotal, userid=userid, symbol=symbol)

                userpf = db.execute("SELECT * FROM portfolio WHERE user_id = :user_id", user_id=userid)
                return render_template("portfolio.html", portfolio = userpf, message = f"Successfully bought {shares} stocks of {name} !", cash=balance)
                
            else :
                return apology("NEED more CASH !!!", 100 )

    ## if method is get
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    userid = session["user_id"]
    # SQLite DB 연결
    conn = sqlite3.connect('finance.db', timeout=5, check_same_thread = False)
    # Connection 으로부터 Cursor 생성
    cur = conn.cursor()
    # SQL 쿼리 실행
    cur.execute("SELECT * FROM purchases WHERE user_id = (?)", (userid,))
    # 데이타 Fetch
    rows = cur.fetchall()
    return render_template("history.html", portfolio=rows)
    #return render_template("history.html", portfolio = rows)                                



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        password = request.form.get("password")

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET" :
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        return render_template("quoted.html", symbol=lookup(symbol))


@app.route("/register", methods=["GET", "POST"])
def register():
        if request.method == "GET" :
            return render_template("register.html")
        else:
            username = request.form.get("username")
            hash = request.form.get("hash")
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=generate_password_hash(hash))
            # Create the portfolio db when registered
            db.execute("CREATE TABLE IF NOT EXISTS portfolio(user_id int,Symbol text, Name text, Shares int, Price real, TOTAL real, FOREIGN KEY(user_id) REFERENCES users(id));")
            # Create purchase tracking table
            db.execute("CREATE TABLE IF NOT EXISTS purchases (user_id INT, Symbol TEXT, Shares INT, Transacted DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(user_id) REFERENCES users(id))")
            return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get('selectSymbol')

        # take info through user's input / lookup function
        userid = session["user_id"]
        shares = int(request.form.get("shares"))
        price = lookup(symbol)["price"]

        # import portfolio from db
        rows = db.execute("SELECT * FROM portfolio WHERE user_id = :userid AND symbol = :symbol",
                        userid=userid, symbol=symbol)
        # import cash balance from db
        cash = db.execute("SELECT cash FROM users WHERE id = :userid", userid=userid)
        balance = float(cash[0]['cash']) + price*float(shares)
        balance = round(balance,2)

        # Comparing # of shares before selling with # of willing share
        originShares = int(rows[0]['Shares'])
        validShares = originShares - int(shares)
        newtotal = round(total(validShares, price),2)

        if not validShares > 0 :
            return apology("TOO many Shares !! ", 100)
        else :
            db.execute("UPDATE users SET cash = :cash WHERE id = :userid", cash=balance, userid=userid)
            db.execute("UPDATE portfolio SET Shares = :shares, TOTAL = :total WHERE user_id = :userid and Symbol =:symbol", shares=validShares, total=newtotal, userid=userid, symbol=symbol)
            db.execute("INSERT INTO purchases (user_id, Symbol, Shares) VALUES(?,?,?)", userid, symbol, shares*(-1))


            userpf = db.execute("SELECT * FROM portfolio WHERE user_id = :user_id", user_id=userid)
            return render_template("portfolio.html", portfolio = userpf, message = f"Successfully Sold {shares} stocks of {symbol} !", cash=balance)
        
    ## if method is get
    else:
        userid = session["user_id"]
        symbols = db.execute("SELECT * FROM portfolio WHERE user_id = :userid", userid=userid)
        return render_template("sell.html", symbols = symbols)



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
