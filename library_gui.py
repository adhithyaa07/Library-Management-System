import tkinter as tk
from tkinter import ttk, messagebox
from library_db import (
    init_db, add_book, view_books, add_member, view_members,
    issue_book, return_book, view_issued_books,
    delete_book, delete_member
)


# ---------- Books Tab ----------

def build_books_tab(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Books")

    tk.Label(frame, text="Title").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    title_entry = tk.Entry(frame, width=25)
    title_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame, text="Author").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    author_entry = tk.Entry(frame, width=25)
    author_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame, text="Total Copies").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    copies_entry = tk.Entry(frame, width=25)
    copies_entry.grid(row=2, column=1, padx=10, pady=5)

    books_listbox = tk.Listbox(frame, width=60, height=12)
    books_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def refresh():
        books_listbox.delete(0, tk.END)
        for b in view_books():
            book_id, title, author, total, available = b
            books_listbox.insert(
                tk.END,
                f"ID {book_id} | {title} by {author} | {available}/{total} available"
            )

    def handle_add():
        title = title_entry.get()
        author = author_entry.get()
        copies = copies_entry.get()

        if not title or not author or not copies:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        try:
            copies = int(copies)
        except ValueError:
            messagebox.showerror("Error", "Total copies must be a number.")
            return

        add_book(title, author, copies)
        title_entry.delete(0, tk.END)
        author_entry.delete(0, tk.END)
        copies_entry.delete(0, tk.END)
        refresh()

    tk.Button(frame, text="Add Book", command=handle_add).grid(row=3, column=0, columnspan=2, pady=10)

    refresh()
    return refresh  # so other tabs can trigger a refresh here if needed


# ---------- Members Tab ----------

def build_members_tab(notebook):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Members")

    tk.Label(frame, text="Name").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    name_entry = tk.Entry(frame, width=25)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame, text="Email").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    email_entry = tk.Entry(frame, width=25)
    email_entry.grid(row=1, column=1, padx=10, pady=5)

    members_listbox = tk.Listbox(frame, width=60, height=12)
    members_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def refresh():
        members_listbox.delete(0, tk.END)
        for m in view_members():
            member_id, name, email = m
            members_listbox.insert(tk.END, f"ID {member_id} | {name} | {email}")

    def handle_add():
        name = name_entry.get()
        email = email_entry.get()

        if not name:
            messagebox.showerror("Error", "Name is required.")
            return

        add_member(name, email)
        name_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        refresh()

    tk.Button(frame, text="Add Member", command=handle_add).grid(row=2, column=0, columnspan=2, pady=10)

    refresh()
    return refresh

    def handle_delete():
        selected = members_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Select a member from the list first.")
            return

        text = members_listbox.get(selected[0])
        member_id = int(text.split("|")[0].replace("ID", "").strip())

        delete_member(member_id)
        refresh()

    tk.Button(frame, text="Delete Selected", command=handle_delete).grid(row=2, column=0, columnspan=2, pady=5)


# ---------- Issue/Return Tab ----------

def build_issue_return_tab(notebook, refresh_books):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Issue / Return")

    tk.Label(frame, text="Book ID").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    book_id_entry = tk.Entry(frame, width=15)
    book_id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame, text="Member ID").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    member_id_entry = tk.Entry(frame, width=15)
    member_id_entry.grid(row=1, column=1, padx=10, pady=5)

    issued_listbox = tk.Listbox(frame, width=60, height=12)
    issued_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def refresh():
        issued_listbox.delete(0, tk.END)
        for title, member_name, issue_date in view_issued_books():
            issued_listbox.insert(tk.END, f"{title} -> {member_name} (issued {issue_date})")

    def get_ids():
        book_id = book_id_entry.get()
        member_id = member_id_entry.get()
        if not book_id or not member_id:
            messagebox.showerror("Error", "Enter both Book ID and Member ID.")
            return None
        try:
            return int(book_id), int(member_id)
        except ValueError:
            messagebox.showerror("Error", "IDs must be numbers.")
            return None

    def handle_issue():
        ids = get_ids()
        if ids is None:
            return
        issue_book(*ids)
        refresh()
        refresh_books()  # update available_copies shown on the Books tab

    def handle_return():
        ids = get_ids()
        if ids is None:
            return
        return_book(*ids)
        refresh()
        refresh_books()

    tk.Button(frame, text="Issue Book", command=handle_issue).grid(row=2, column=0, pady=10)
    tk.Button(frame, text="Return Book", command=handle_return).grid(row=2, column=1, pady=10)

    refresh()
    def handle_delete():
        selected = books_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Select a book from the list first.")
            return

    # The listbox text looks like "ID 3 | Peagasus by Pegasus | 3/3 available"
    # We pull the ID back out of that text.
        text = books_listbox.get(selected[0])
        book_id = int(text.split("|")[0].replace("ID", "").strip())

        delete_book(book_id)
        refresh()

    tk.Button(frame, text="Delete Selected", command=handle_delete).grid(row=3, column=0, columnspan=2, pady=5)

# ---------- Main Window ----------

def main():
    init_db()

    window = tk.Tk()
    window.title("Library Management System")
    window.geometry("500x480")

    notebook = ttk.Notebook(window)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)

    refresh_books = build_books_tab(notebook)
    build_members_tab(notebook)
    build_issue_return_tab(notebook, refresh_books)

    window.mainloop()


if __name__ == "__main__":
    main()
