# Functions
def get_valid_input():
    failed_attempts = 0
    while True:
        stock = input("Enter stock quantity (or 'quit' to exit): ")

        if stock.lower() == "quit":
            return "quit", failed_attempts

        if stock.isdigit():                                         # Only positive integers
            return int(stock), failed_attempts
        
        print("Invalid input! Please enter a positive integer.")
        failed_attempts += 1


def process_delivery(current_total, new_value):
    result = current_total + new_value
    return result


def calculate_tax(amount):
    tax = amount * 0.10
    return tax


def generate_report(total_units, failed_attempts):
    print("\n--- Final Report ---")
    print("Total Deliveries Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)


# Main program
inventory_total = 0
total_deliveries = 0
failed_attempts = 0

while True:
    result, input_failure = get_valid_input()
    failed_attempts += input_failure

    if result == "quit":
        break


    # Process the valid delivery
    inventory_total = process_delivery(inventory_total, result)
    if inventory_total > 500:
                print("ALERT: Overstock! Inventory exceeds 500 units.")
                failed_attempts += 1
                inventory_total -= result
                continue
    
    # Calculate tax for the delivery
    tax = calculate_tax(result)

    # Update delivery counter
    total_deliveries += 1

    print("Delivery accepted:", result)
    print("Tax for this delivery: $", tax)
    print("Current inventory total:", inventory_total)

# Generate final report
generate_report(total_deliveries, failed_attempts)