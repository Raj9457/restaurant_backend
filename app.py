from flask import Flask, request, jsonify

app = Flask(__name__)

# Initializing menu and orders
menu = []
orders = []
order_id = 1


@app.route('/')
def welcome():
    return "Welcome to Zesty Zomato!"

# Route to add a new dish to the menu
@app.route('/menu', methods=['POST'])
def add_dish():
    data = request.get_json()
    dish = {
        'id': len(menu) + 1,
        'name': data['name'],
        'price': data['price'],
        'availability': True
    }
    menu.append(dish)
    return jsonify({'message': 'Dish added successfully'})

# Route to remove a dish from the menu
@app.route('/menu/<int:dish_id>', methods=['DELETE'])
def remove_dish(dish_id):
    dish = next((d for d in menu if d['id'] == dish_id), None)
    if dish:
        menu.remove(dish)
        return jsonify({'message': 'Dish removed successfully'})
    else:
        return jsonify({'message': 'Dish not found'})

# Route to update the availability of a dish
@app.route('/menu/<int:dish_id>', methods=['PUT'])
def update_availability(dish_id):
    dish = next((d for d in menu if d['id'] == dish_id), None)
    if dish:
        dish['availability'] = request.get_json()['availability']
        return jsonify({'message': 'Dish availability updated successfully'})
    else:
        return jsonify({'message': 'Dish not found'})

# Route to get the menu
@app.route('/menu', methods=['GET'])
def get_menu():
    return jsonify(menu)

# Route to take a new order
@app.route('/order', methods=['POST'])
def take_order():
    data = request.get_json()
    order_dishes = data['dishes']
    order = {
        'id': order_id,
        'customer_name': data['customer_name'],
        'dishes': []
    }
    for dish_id in order_dishes:
        dish = next((d for d in menu if d['id'] == dish_id and d['availability']), None)
        if dish:
            order['dishes'].append(dish)
        else:
            return jsonify({'message': f'Dish with ID {dish_id} not found or not available'})
    orders.append(order)
    order_id += 1
    return jsonify({'message': 'Order taken successfully'})

# Route to update the status of an order
@app.route('/order/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    order = next((o for o in orders if o['id'] == order_id), None)
    if order:
        new_status = request.get_json()['status']
        order['status'] = new_status
        return jsonify({'message': 'Order status updated successfully'})
    else:
        return jsonify({'message': 'Order not found'})

# Route to get all orders
@app.route('/order', methods=['GET'])
def get_orders():
    return jsonify(orders)

if __name__ == '__main__':
    app.run(debug=False, port=8080)
