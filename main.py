# Simple Online Shopping System

products = {
    1: ("Shirt", 500),
    2: ("Shoes", 1200),
    3: ("Watch", 800),
    4: ("Bag", 700)
}

cart = []
total = 0

while True:
    print("\n---- Online Shopping ----")
    print("1. Show Products")
    print("2. Add to Cart")
    print("3. View Cart")
    print("4. Checkout")
    print("5. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        print("\nAvailable Products:")
        for key, value in products.items():
            print(key, value[0], "₹", value[1])

    elif choice == 2:
        item = int(input("Enter product number: "))
        if item in products:
            cart.append(products[item])
            print(products[item][0], "added to cart")
        else:
            print("Invalid product")

    elif choice == 3:
        print("\nYour Cart:")
        for item in cart:
            print(item[0], "₹", item[1])

    elif choice == 4:
        total = sum(item[1] for item in cart)
        print("\nTotal Amount: ₹", total)
        print("Thank you for shopping!")
        break

    elif choice == 5:
        print("Exited")
        break
