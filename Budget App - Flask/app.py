from flask import Flask, render_template, request, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_session import Session
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
import click
from flask.cli import with_appcontext
from psycopg2 import sql


app = Flask(__name__)

# Configure app to auto reload when making changes
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure for SQLAlchemy
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget_database.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lqtmlvqujrztsc:0facfbaf83426d91b950b281a82d97f81be66b3999a8dd6b0c36d0ba5d35dd2b@ec2-44-195-169-163.compute-1.amazonaws.com:5432/d23vbc0clplpts'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Update secret key
app.config.update(SECRET_KEY="b'Idg$I\xbbc\t\xc5\xf1\xcc\x03'")

# Config sessions to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Initialize database
db = SQLAlchemy(app)

# A decorator to require logins
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# A model for the users table
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    hash = db.Column(db.String(200), nullable=False)

    def __init__(self, username, hash):
        self.username = username
        self.hash = hash

# Create a db model for the budget
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    bill = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __init__(self, bill, user_id, amount):
        self.bill = bill
        self.user_id = user_id
        self.amount= amount

# Another db table for transactions
class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    comment = db.Column(db.String(200))

    def __init__(self, user_id, date, category, amount, comment):
        self.user_id = user_id
        self.date = date
        self.category = category
        self.amount = amount
        self.comment = comment

# A table for income
class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __init__(self, user_id, date, amount):
        self.user_id = user_id
        self.date = date
        self.amount = amount


# Route for login page
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        # Get username and password from form
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure there was a username
        if not username:

            flash("Please enter a username")
            return redirect("/login")

        # Ensure there was a password
        if not password:

            flash("Please enter a password")
            return redirect("/login")

        # Go to table and get user by inputed username
        user_check = Users.query.filter_by(username=username).first()

        # Ensure username exists
        if user_check is None:

            flash("There is no account registered with this username")
            return redirect("/login")

        # Ensure password is correct
        if not check_password_hash(user_check.hash, password):

            flash("Incorrect password")
            return redirect("/login")

        # Remember this user by their id
        session["user_id"] = user_check.id

        # Redirect to homepage
        return redirect("/")


    return render_template("login.html")


# A route to log out
@app.route("/logout")
def logout():

    session.clear()
    
    return redirect("/login")

# Route for create account page
@app.route("/account", methods=["GET", "POST"])
def account():

    if request.method == "POST":

        # Get username, password, confirmation from form
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure user enterd username
        if not username:

            flash("Please enter a username")
            return redirect("/account")

        # Ensure username not too long
        if len(username) > 20:

            flash("Username must not exceed 20 characters")
            return redirect("/account")

        # See if there is another user by that name in the table
        duplicate = Users.query.filter_by(username=username).first()

        if duplicate:

            # If so, flash error and redirect
            if duplicate.username == username:

                flash("This username already exists")
                return redirect("/account")

        # Ensure password fields are filled out
        if not password or not confirmation:

            flash("Please enter a password")
            return redirect("/account")
        
        # Ensure password correct len
        if len(password) > 20:
            flash("Password must not exceed 20 characters")
            return redirect("/account")

        # Ensure they match
        if password != confirmation:

            flash("Passwords do not match")
            return redirect("/account")

        # Get a hash for this password
        hash = generate_password_hash(password)

        # Create a new user
        new_user = Users(username, hash)

        # Try to add this user to the table
        try:

            db.session.add(new_user)
            db.session.commit()

            flash("User added successfully!")
            return redirect("/login")

        # If not able, flash error and redirect
        except:

            flash("User was not able to be added")
            return redirect("/account")


    return render_template("account.html")


# Route for home page
@app.route("/")
@login_required
def home():

    user = session['user_id']

    # Get all data from budget
    data = Budget.query.filter_by(user_id=user).all()

    # Checking if Budget table exists
    if data:
        # Calculate amount sum
        sum = db.engine.execute("SELECT SUM(amount) AS sum FROM Budget WHERE user_id=%s", (user,))
        return render_template("home.html", data=data, sum=sum)

    else:
        return render_template("home.html")


# Route to add a budget
@app.route("/add", methods=["GET", "POST"])
@login_required
def add():

    user = session['user_id'] 

    if request.method == "POST":
        
        category = request.form.get("category")
        
        # Ensure a category was entered
        if not category:

            flash("Please enter a category")
            return redirect("/add")

        # Ensure correct length
        if len(category) > 100:

            flash("Category must not exceed 100 characters")
            return redirect("/add")
        
        amount = request.form.get("amount")

        # Ensure an amnout was entered
        if not amount:

            flash("Please enter an amount")
            return redirect("/add")

        # Ensure amount is a number
        if not amount.replace('.', '').isdigit():

            flash("Please enter a valid amount")
            return redirect("/add")

        # Ensure that the amount is not 0 or negative
        try:
            if float(amount) < 1:

                flash("Please enter a valid amount")
                return redirect("/add")

        except ValueError:

            flash("Please enter a valid amount")
            return redirect("/add")

        # Ensure correct length
        if len(amount) > 10:
            flash("Amount must not exceed 10 digits")
            return redirect("/add")

        # Store new budget in variable
        new_budget = Budget(category, user, amount)

        # Flash appropriate messages 
        try:

            # Add and commit new budget
            db.session.add(new_budget)
            db.session.commit()

            flash("Budget added successfully!")

            return redirect("/")
        
        except:
            
            flash("Unable to add budget")
            return redirect("/")


    return render_template("add.html")


# Route to delete a budget
@app.route("/delete/<int:id>")
@login_required
def delete(id):

    user = session['user_id']

    # id of desired budget to delete
    budget_to_delete = Budget.query.filter_by(id=id, user_id=user).first()
    
    # Try to delete and flash if sucessful
    try:
        db.session.delete(budget_to_delete)
        db.session.commit()
        flash("Budget successfully deleted!")
        return redirect("/")

    # If not, flash a message to notify
    except:
        flash("There was a problem deleting this budget")
        return redirect("/")


# Route to delete transactions
@app.route("/delete-transaction/<int:id>")
@login_required
def delete_transaction(id):

    user = session['user_id']

    # id of desired transaction to delete
    trans_to_delete = Transactions.query.filter_by(id=id, user_id=user).first()
    
    # Try deleting and flash message if sucessful
    try:
        db.session.delete(trans_to_delete)
        db.session.commit()
        flash("Transaction successfully deleted!")
        return redirect("/transactions")

    # Otherwise flash message if not sucessful
    except:
        flash("There was a problem deleting this transaction")
        return redirect("/transactions")


# Route to show all transactions
@app.route("/transactions")
@login_required
def transactions():

    user = session['user_id']

    # Query table to get all transactions
    data = Transactions.query.filter_by(user_id=user).all()

    # Render template accordingly
    return render_template("transactions.html", data=data)


# Route to add a transaction
@app.route("/add-transaction", methods=["GET", "POST"])
@login_required
def add_transaction():

    user = session['user_id']

    if request.method == "POST":

        # Get the date string from form, convert it to datetime
        dates = datetime.strptime(request.form.get("date"), '%Y-%m').date()

        # Convert back to string with specific format
        date = dates.strftime('%B, %Y')

        category = str(request.form.get("category"))

        amount = request.form.get("amount")

        # Ensure amount was entered
        if not amount:

            flash("Please enter an amount")
            return redirect("/add-transaction")

        # Ensure amount is just numbers
        if not amount.replace('.', '').isdigit():

            flash("Please only enter numbers for the amount")
            return redirect("/add-transaction")

        # Ensure amount is greater than 0
        try:

            if float(amount) < 1:

                flash("Please enter a valid amount")
                return redirect("/add-transaction")

        except ValueError:

            flash("Please enter a valid amount")
            return redirect("/add-transaction")

        # Ensure correct length
        if len(amount) > 10:

            flash("Amount must not exceed 10 digits")
            return redirect("/add-transaction")

        comment = request.form.get("comment")
        
        # Ensure correct length
        if len(comment) > 200:

            flash("Comment must not exceed 200 characters")
            return redirect("/add-transaction")

        # Store new transaction in variable
        transaction = Transactions(user, date, category, amount, comment)

        # Try to add transaction and notify
        try:

            db.session.add(transaction)
            db.session.commit()
            flash("Transaction added successfully")
            return redirect("/transactions")

        # Notify if transaction was not added
        except:

            flash("There was a problem adding this transaction")
            return redirect("/transactions")

    categories = Budget.query.filter_by(user_id=user).all()

    return render_template("add_transaction.html", categories = categories)


# Route for looking at monthly progress
@app.route("/monthly", methods=["GET", "POST"])
@login_required
def monthly():

    if request.method == "POST":

        user = session['user_id']

        # Convert string to datetime
        month = datetime.strptime(request.form.get("month"), '%Y-%m').date()

        # Convert datetime to properly formatted string
        current_month = month.strftime('%B, %Y')
        
        # Get all bills from budget
        b_data = Budget.query.filter_by(user_id=user).order_by(Budget.bill).all()

        # Get all transactions by category for the selected month
        t_data = db.engine.execute("SELECT category, SUM(amount) AS amount FROM Transactions WHERE (date=%s) AND (user_id=%s) GROUP BY category", (current_month, user,))

        # Get total sum of income for the selected month
        amount = db.engine.execute("SELECT SUM(amount) as amount FROM Income WHERE date=%s AND user_id=%s", (current_month, user))

        # Query income table by selected month
        test = Income.query.filter_by(user_id=user,date=current_month).first()

        # If no income, set income to 0 to avoid errors
        if test == None:

            income = 0

        else:

            income = amount
    
        # Query for sum of transactions for selected month
        sum = db.engine.execute("SELECT SUM(amount) AS sum FROM Transactions WHERE (date=%s) AND (user_id=%s)", (current_month, user,))
        
        # Query for sum of all bills
        bill_sum = db.engine.execute("SELECT SUM(amount)as amount FROM Budget WHERE user_id=%s", (user,))
        
        # If no transactions, flash a message a redirect
        try:

            return render_template("month.html", b_data=b_data, t_data=t_data, income=income, sum=sum, bill_sum=bill_sum, date=current_month)

        except:

            flash("There are no transactions for the selected month")
            return render_template("monthly.html")


    
    return render_template("monthly.html")


# Route to add income
@app.route("/income", methods=["GET", "POST"])
@login_required
def income():

    if request.method == "POST":

        user = session['user_id']

        # Convert input string to datetime
        month = datetime.strptime(request.form.get("date"), '%Y-%m').date()

        # Convert datetime to a formated string
        date = month.strftime('%B, %Y')
        
        amount = request.form.get("amount")

        # Ensure amount exists
        if not amount:
            
            flash("Please enter an amount")
            return redirect("/income")

        # Ensure amount is a valid number
        if not amount.replace('.', '').isdigit():

            flash("Please enter a valid amount")
            return redirect("/income")

        try:
            if float(amount) < 1:

                flash("Please enter a valid amount")
                return redirect("/income")

        except ValueError:

            flash("Please enter a valid amount")
            return redirect("/income")

        # Ensure amount is correct length
        if len(amount) > 10:

            flash("Amount must not exceed 10 digits")
            return redirect("/income")

        # Store new income in variable
        new_income = Income(user, date, amount)

        # Try adding it to Income table
        try:
            db.session.add(new_income)
            db.session.commit()
            flash("Income successfully added!")
            return redirect("/income-history")

        # Flash message is unsuccessful
        except:
            flash("There was a problem adding this income")
            return redirect("/income")


    return render_template("income.html")


# A route to view all inputed history
@app.route("/income-history")
@login_required
def income_history():

    user = session['user_id']

    data = Income.query.filter_by(user_id=user).all()

    return render_template("income_history.html", data=data)


# A route to delete income
@app.route("/delete-income/<int:id>")
@login_required
def delete_income(id):

    user = session['user_id']

    # id of income to delete
    income_to_delete = Income.query.filter_by(id=id, user_id=user).first()
    
    # Try deleting
    try:
        db.session.delete(income_to_delete)
        db.session.commit()
        flash("Income successfully deleted!")
        return redirect("/income-history")

    # Flash message if unsuccessful
    except:
        flash("There was a problem deleting this income")
        return redirect("/income-history")


@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)