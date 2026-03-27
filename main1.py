import tkinter as tk
from tkinter import messagebox

# Product Data
products = {
    "Shirt": 500,
    "Shoes": 1200,
    "Watch": 800,
    "Bag": 700
}

cart = []

# Functions
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

# GUI Window
root = tk.Tk()
root.title("Online Shopping System")
root.geometry("500x400")

# Labels
tk.Label(root, text="Products", font=("Arial", 14)).pack()
product_list = tk.Listbox(root, height=6)
product_list.pack()

# Buttons
tk.Button(root, text="Show Products", command=show_products).pack(pady=5)
tk.Button(root, text="Add to Cart", command=add_to_cart).pack(pady=5)
tk.Button(root, text="View Cart", command=view_cart).pack(pady=5)

# Cart List
tk.Label(root, text="Cart", font=("Arial", 14)).pack()
cart_list = tk.Listbox(root, height=6)
cart_list.pack()

# Checkout Button
tk.Button(root, text="Checkout", command=checkout).pack(pady=10)

root.mainloop()
