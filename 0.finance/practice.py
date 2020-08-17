from cs50 import SQL

db = SQL("sqlite:///finance.db")
cash = db.execute("SELECT cash FROM users WHERE id = :userid", userid=20)
print(cash[0]['cash'])
