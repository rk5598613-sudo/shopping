import tkinter as tk
from tkinter import messagebox
import sqlite3

# ---------------- DATABASE ----------------
conn = sqlite3.connect("users.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
conn.commit()

# ---------------- LOGIN WINDOW ----------------
def login_window():
    login = tk.Tk()
    login.title("Login - KNR Stylo Hub")
    login.geometry("1600x1500")

    tk.Label(login, text="Login", font=("Arial", 16)).pack(pady=10)

    username = tk.Entry(login)
    username.pack(pady=5)
    username.insert(0, "Username")

    password = tk.Entry(login, show="*")
    password.pack(pady=5)
    password.insert(0, "Password")

    def login_user():
        cur.execute("SELECT * FROM users WHERE username=? AND password=?",
                    (username.get(), password.get()))
        if cur.fetchone():
            messagebox.showinfo("Success", "Login Successful")
            login.destroy()
            main_app()
        else:
            messagebox.showerror("Error", "Invalid Details")

    def register_user():
        cur.execute("INSERT INTO users VALUES (?, ?)",
                    (username.get(), password.get()))
        conn.commit()
        messagebox.showinfo("Success", "Registered Successfully")

    tk.Button(login, text="Login", command=login_user).pack(pady=5)
    tk.Button(login, text="Register", command=register_user).pack(pady=5)

    login.mainloop()

# ---------------- MAIN APP ----------------
def main_app():
    root = tk.Tk()
    root.title("KNR Stylo Hub - Shopping")
    root.geometry("800x600")

    # Product Data
    products = {
        "Shirt": 500,
        "Shoes": 1200,
        "Watch": 800,
        "Bag": 700
    }

    cart = []

    def show_products():
        product_list.delete(0, tk.END)
        for item, price in products.items():
            product_list.insert(tk.END, f"{item} - ₹{price}")

    def add_to_cart():
        selected = product_list.curselection()
        if selected:
            item = product_list.get(selected)
            name = item.split(" - ")[0]
            cart.append((name, products[name]))
            messagebox.showinfo("Success", f"{name} added to cart")
        else:
            messagebox.showwarning("Warning", "Select a product")

    def view_cart():
        cart_list.delete(0, tk.END)
        for item in cart:
            cart_list.insert(tk.END, f"{item[0]} - ₹{item[1]}")

    def checkout():
        total = sum(item[1] for item in cart)
        messagebox.showinfo("Bill", f"Total Amount: ₹{total}\nThank you for shopping!")
        cart.clear()
        cart_list.delete(0, tk.END)

    # GUI Elements
    tk.Label(root, text="KNR Stylo Hub", font=("Arial", 20, "bold")).pack(pady=10)

    tk.Label(root, text="Products", font=("Arial", 14)).pack()
    product_list = tk.Listbox(root, height=8, width=50)
    product_list.pack(pady=5)

    tk.Button(root, text="Show Products", command=show_products).pack(pady=5)
    tk.Button(root, text="Add to Cart", command=add_to_cart).pack(pady=5)
    tk.Button(root, text="View Cart", command=view_cart).pack(pady=5)

    tk.Label(root, text="Your Cart", font=("Arial", 14)).pack(pady=10)
    cart_list = tk.Listbox(root, height=8, width=50)
    cart_list.pack(pady=5)

    tk.Button(root, text="Checkout", command=checkout, bg="green", fg="white").pack(pady=10)

    root.mainloop()

# Start with login
login_window()

