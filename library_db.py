import sqlite3

def init_db():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            total_copies INTEGER NOT NULL,
            available_copies INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            issue_date TEXT NOT NULL,
            return_date TEXT,
            FOREIGN KEY (book_id) REFERENCES books(id),
            FOREIGN KEY (member_id) REFERENCES members(id)
        )
    """)

    conn.commit()
    conn.close()

init_db()
"""conn = sqlite3.connect("library.db")
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
conn.close()"""
def add_book(title, author, total_copies):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO books (title, author, total_copies, available_copies)
        VALUES (?, ?, ?, ?)
    """, (title, author, total_copies, total_copies))

    conn.commit()
    conn.close()
    print("Book added successfully!")
def view_books():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()

    conn.close()
    return rows
def add_member(name, email):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO members (name, email)
        VALUES (?, ?)
    """, (name, email))

    conn.commit()
    conn.close()
    print("Member added successfully!")


def view_members():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM members")
    rows = cursor.fetchall()

    conn.close()
    return rows

from datetime import date

def issue_book(book_id, member_id):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    # Step 1: check availability
    cursor.execute("SELECT available_copies FROM books WHERE id = ?", (book_id,))
    result = cursor.fetchone()

    if result is None:
        print("Book not found.")
        conn.close()
        return

    available = result[0]
    if available <= 0:
        print("No copies available right now.")
        conn.close()
        return

    # Step 2: record the issue
    today = date.today().isoformat()
    cursor.execute("""
        INSERT INTO issues (book_id, member_id, issue_date, return_date)
        VALUES (?, ?, ?, NULL)
    """, (book_id, member_id, today))

    # Step 3: reduce available copies
    cursor.execute("""
        UPDATE books SET available_copies = available_copies - 1
        WHERE id = ?
    """, (book_id,))

    conn.commit()
    conn.close()
    print("Book issued successfully!")
def return_book(book_id, member_id):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM issues
        WHERE book_id = ? AND member_id = ? AND return_date IS NULL
    """, (book_id, member_id))
    result = cursor.fetchone()

    if result is None:
        print("No matching active issue found.")
        conn.close()
        return

    issue_id = result[0]
    today = date.today().isoformat()

    cursor.execute("UPDATE issues SET return_date = ? WHERE id = ?", (today, issue_id))
    cursor.execute("UPDATE books SET available_copies = available_copies + 1 WHERE id = ?", (book_id,))

    conn.commit()
    conn.close()
    print("Book returned successfully!")
def view_issued_books():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT books.title, members.name, issues.issue_date
        FROM issues
        JOIN books ON issues.book_id = books.id
        JOIN members ON issues.member_id = members.id
        WHERE issues.return_date IS NULL
    """)
    rows = cursor.fetchall()

    conn.close()
    return rows
def delete_book(book_id):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()


def delete_member(member_id):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
    conn.commit()
    conn.close()
if __name__ == "__main__":
    init_db()
    print(view_books())
    print(view_members())
