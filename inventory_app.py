from flask import Flask, render_template, request, redirect, g
import sqlite3
from forms import CategoryForm, SearchForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

DATABASE = "inventory.db"


# =========================
# DATABASE CONNECTION
# =========================
def get_db():
    # TO-DO: return sqlite3 connection stored in g


# =========================
# CLEANUP CONNECTION
# =========================
@app.teardown_appcontext
def close_connection(exception):
    # TO-DO: close db connection if it exists in g


# =========================
# INITIALIZE DATABASE
# =========================
def init_db():
    # TO-DO: create products table if not exists with columns: id, name, category, price, stock

    #Inserts some initial values into products
    cur = conn.execute("SELECT COUNT(*) FROM products")
    if cur.fetchone()[0] == 0:
        conn.executemany("""
            INSERT INTO products (name, category, price, stock)
            VALUES (?, ?, ?, ?)
        """, [
            ("Laptop", "Electronics", 999.99, 10),
            ("Mouse", "Electronics", 19.99, 50),
            ("Desk Chair", "Furniture", 149.99, 20),
            ("Notebook", "Office", 3.99, 200)
        ])

    conn.commit()


@app.route("/")
def home():
    return redirect("/search")


# =========================
# MAIN SEARCH
# =========================
@app.route("/search", methods=["GET", "POST"])
def search():
    form = CategoryForm()

    form.search_type.choices = [
        ("category", "Search by Category"),
        ("name", "Search by Name")
    ]

    if request.method == "POST":
        choice = form.search_type.data

        if choice == "category":
            return redirect("/search/category")
        elif choice == "name":
            return redirect("/search/name")

    return render_template("search.html", form=form)


# =========================
# SEARCH BY CATEGORY
# =========================
@app.route("/search/category", methods=["GET", "POST"])
def search_category():
    form = SearchForm()

    conn = get_db()
    categories = conn.execute(
        "SELECT DISTINCT category FROM products"
    ).fetchall()

    if request.method == "POST":
        category = request.form["search_text"]
        return redirect(f"/results/category?category={category}")

    return render_template(
        "search_category.html",
        form=form,
        categories=categories
    )

# =========================
# SEARCH BY NAME
# =========================
@app.route("/search/name", methods=["GET", "POST"])
def search_name():
    form = SearchForm()

    if request.method == "POST":
        name = request.form["search_text"]
        return redirect(f"/results/name?name={name}")

    return render_template("search_name.html", form=form)


# =========================
# RESULTS: CATEGORY
# =========================
@app.route("/results/category")
def results_by_category():
    category = request.args.get("category")

    conn = get_db()
    results = conn.execute(
        "SELECT * FROM products WHERE category = ?",
        (category,)
    ).fetchall()

    return render_template("results.html", results=results)


# =========================
# RESULTS: NAME
# =========================
@app.route("/results/name")
def results_by_name():
    name = request.args.get("name")

    conn = get_db()
    results = conn.execute(
        #TO-DO: select statement string that searches where text exists in name
        #Hint: Use "LIKE" instead of "=" as used in RESULTS: CATEGORY
        (f"%{name}%",)
    ).fetchall()

    return render_template("results.html", results=results)

# =========================
# ADD: PRODUCT/INVENTORY
# =========================
@app.route("/add", methods=["GET", "POST"])
def add_item():
    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        price = request.form["price"]
        stock = request.form["stock"]

        #TO-DO: input validation that handles data types & non-negative numbers
        #& provide validation messages if inputs are invalid
        
        conn = get_db()

        #TO-DO: conn.execute statement to add new product with all 4 fields
        #& return statement to let user know they have added product successfully


    return render_template("add_item.html")


# =========================
# MAIN BLOCK
# =========================
#TO-DO: Run app using port 5001
#Recommended: run init_db() automatically in main block
