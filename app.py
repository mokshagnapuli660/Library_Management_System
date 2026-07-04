from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def check_login():

    username = request.form["username"]
    password = request.form["password"]

    if username == "admin" and password == "admin123":
        session["user"] = username
        return redirect("/")

    return "<h3>Invalid Username or Password</h3>"

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

app.secret_key = "library123"

# Home Page
@app.route("/")
def home():

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    # Total Books
    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]

    # Total Students
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    # Total Issued Books
    cursor.execute("SELECT COUNT(*) FROM issued_books")
    total_issued = cursor.fetchone()[0]

    # Available Books
    available_books = total_books - total_issued

    connection.close()

    return render_template(
        "index.html",
        total_books=total_books,
        total_students=total_students,
        total_issued=total_issued,
        available_books=available_books
    )


# View Books + Search
@app.route("/books")
def books():

    search = request.args.get("search")

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    if search:
        cursor.execute(
            "SELECT * FROM books WHERE LOWER(title) LIKE LOWER(?)",
            ("%" + search + "%",)
        )
    else:
        cursor.execute("SELECT * FROM books")

    books = cursor.fetchall()

    connection.close()

    return render_template("books.html", books=books)


# Add Book Page
@app.route("/add_book")
def add_book():
    return render_template("add_book.html")

@app.route("/students")
def students():

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    connection.close()

    return render_template("students.html", students=students)

@app.route("/add_student")
def add_student():
    return render_template("add_student.html")

@app.route("/issue_book")
def issue_book():

    if "user" not in session:
        return redirect("/login")

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    # Get all students
    cursor.execute("SELECT id, name FROM students")
    students = cursor.fetchall()

    # Get only available books
    cursor.execute("""
        SELECT id, title
        FROM books
        WHERE id NOT IN (
            SELECT book_id FROM issued_books
        )
    """)
    books = cursor.fetchall()

    connection.close()

    return render_template(
        "issue_book.html",
        students=students,
        books=books
    )


# Save Book
@app.route("/save_book", methods=["POST"])
def save_book():

    title = request.form["title"]
    author = request.form["author"]
    category = request.form["category"]

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO books(title, author, category) VALUES (?, ?, ?)",
        (title, author, category)
    )

    connection.commit()
    connection.close()

    return redirect("/books")


# Delete Book
@app.route("/delete_book/<int:id>")
def delete_book(id):

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM books WHERE id = ?", (id,))

    connection.commit()
    connection.close()

    return redirect("/books")


# Edit Book Page
@app.route("/edit_book/<int:id>")
def edit_book(id):

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM books WHERE id = ?", (id,))
    book = cursor.fetchone()

    connection.close()

    return render_template("edit_book.html", book=book)


# Update Book
@app.route("/update_book/<int:id>", methods=["POST"])
def update_book(id):

    title = request.form["title"]
    author = request.form["author"]
    category = request.form["category"]

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE books SET title=?, author=?, category=? WHERE id=?",
        (title, author, category, id)
    )

    connection.commit()
    connection.close()

    return redirect("/books")

# Save Student
@app.route("/save_student", methods=["POST"])
def save_student():

    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO students(name, email, phone) VALUES (?, ?, ?)",
        (name, email, phone)
    )

    connection.commit()
    connection.close()

    return redirect("/students")

# Delete Student
@app.route("/delete_student/<int:id>")
def delete_student(id):

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM students WHERE id = ?", (id,))

    connection.commit()
    connection.close()

    return redirect("/students")

# Edit Student
@app.route("/edit_student/<int:id>")
def edit_student(id):

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()

    connection.close()

    return render_template("edit_student.html", student=student)

# Update Student
@app.route("/update_student/<int:id>", methods=["POST"])
def update_student(id):

    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE students SET name=?, email=?, phone=? WHERE id=?",
        (name, email, phone, id)
    )

    connection.commit()
    connection.close()

    return redirect("/students")

# Save Issued Book
@app.route("/save_issue", methods=["POST"])
def save_issue():

    student_id = request.form["student_id"]
    book_id = request.form["book_id"]
    issue_date = request.form["issue_date"]

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO issued_books(student_id, book_id, issue_date)
        VALUES (?, ?, ?)
        """,
        (student_id, book_id, issue_date)
    )

    connection.commit()
    connection.close()

    return redirect("/issued_books")

# View Issued Books
@app.route("/issued_books")
def issued_books():

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            issued_books.id,
            students.name,
            books.title,
            issued_books.issue_date
        FROM issued_books
        JOIN students ON students.id = issued_books.student_id
        JOIN books ON books.id = issued_books.book_id
    """)

    issued = cursor.fetchall()

    connection.close()

    return render_template("issued_books.html", issued=issued)

# Return Book
@app.route("/return_book/<int:id>")
def return_book(id):

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM issued_books WHERE id=?",
        (id,)
    )

    connection.commit()
    connection.close()

    return redirect("/issued_books")

if __name__ == "__main__":
    app.run(debug=True)