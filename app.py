from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize menu and orders as empty lists (will be used as dictionaries later)
menu = []
orders = []

# Helper function to find a dish by its ID
def find_dish(dish_id):
    for dish in menu:
        if dish['id'] == dish_id:
            return dish
    return None

# Helper function to find an order by its ID
def find_order(order_id):
    for order in orders:
        if order['id'] == order_id:
            return order
    return None

# Route to add a new dish to the menu
@app.route('/add_dish', methods=['POST'])
def add_dish():
    data = request.get_json()
    dish_id = data['id']
    dish_name = data['name']
    price = float(data['price'])
    availability = data['availability'].lower() == 'yes'

    # Check if the dish ID already exists in the menu
    if find_dish(dish_id):
        return jsonify({'message': 'Dish ID already exists. Please use a different ID.'}), 400

    # Add the new dish to the menu
    menu.append({
        'id': dish_id,
        'name': dish_name,
        'price': price,
        'availability': availability
    })

    return jsonify({'message': 'Dish added successfully.'}), 200

# Route to remove a dish from the menu
@app.route('/remove_dish/<string:dish_id>', methods=['DELETE'])
def remove_dish(dish_id):
    dish = find_dish(dish_id)
    if dish:
        menu.remove(dish)
        return jsonify({'message': 'Dish removed successfully.'}), 200
    else:
        return jsonify({'message': 'Dish not found.'}), 404

# Route to take a new order
@app.route('/take_order', methods=['POST'])
def take_order():
    data = request.get_json()
    customer_name = data['customer_name']
    dish_ids = data['dish_ids']

    # Check if all dishes in the order are available
    for dish_id in dish_ids:
        dish = find_dish(dish_id)
        if not dish or not dish['availability']:
            return jsonify({'message': 'Invalid order. Please check dish availability.'}), 400

    # Assign a unique order ID
    order_id = len(orders) + 1

    # Set the initial order status as 'received'
    status = 'received'

    # Add the new order to the orders list
    orders.append({
        'id': order_id,
        'customer_name': customer_name,
        'dish_ids': dish_ids,
        'status': status
    })

    return jsonify({'message': 'Order placed successfully.'}), 200

# Route to update the status of an order
@app.route('/update_order/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()
    new_status = data['status']

    # Find the order
    order = find_order(order_id)
    if not order:
        return jsonify({'message': 'Order not found.'}), 404

    # Update the order status
    order['status'] = new_status

    return jsonify({'message': 'Order status updated successfully.'}), 200

# Route to retrieve all orders
@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders), 200

if __name__ == '__main__':
    app.run(debug=True)
