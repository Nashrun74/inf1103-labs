# Functions

def load_inventory():
    orders = []

    try:
        with open("inventory.txt", "r") as file:           # reads file
            for line in file:
                order_data = line.strip().split(",")        # split nicely

                if len(order_data) == 3:
                    order = {
                        "order_id": int(order_data[0].strip()),
                        "product_name": order_data[1].strip(),
                        "quantity": int(order_data[2].strip())
                    }

                    orders.append(order)    # appends in list

    except FileNotFoundError:
        # Create sample orders if the file does not exist
        orders = [                                              # if file not found inputs the first 3 pre-determined values
            {"order_id": 1001, "product_name": "Wireless Mouse", "quantity": 2},
            {"order_id": 1002, "product_name": "Keyboard", "quantity": 1},
            {"order_id": 1003, "product_name": "USB Cable", "quantity": 3}
        ]

        save_inventory(orders) # save to inventory

    return orders


def save_inventory(orders):
    with open("inventory.txt", "w") as file:
        for order in orders:
            file.write(
                f"{order['order_id']}, "
                f"{order['product_name']}, "
                f"{order['quantity']}\n"
            )


def display_inventory(orders):          # displays inventory
    print("Current Orders:\n")

    for order in orders:
        print(
            f"{order['order_id']}, "
            f"{order['product_name']}, "
            f"{order['quantity']}"
        )


def add_order(orders):
    # user inputs
    product_name = input("\nEnter Product Name: ")
    quantity = int(input("Enter Quantity: "))

    # Generate the next order ID as must be unique
    if len(orders) > 0:
        new_order_id = max(
            order["order_id"] for order in orders
        ) + 1
    else:
        new_order_id = 1001     # sets it as first order id 

    # Create the new order
    new_order = {
        "order_id": new_order_id,
        "product_name": product_name,
        "quantity": quantity
    }

    # Add the order to the list
    orders.append(new_order)

    # Display the new order
    print("\nNew Order Added:")
    print(
        f"{new_order['order_id']},"
        f"{new_order['product_name']},"
        f"{new_order['quantity']}"
    )

    # Save updated orders
    save_inventory(orders)

    print("\nOrder successfully saved to inventory.txt")


# Main program

orders = load_inventory()
# print(orders)

display_inventory(orders)

add_order(orders)