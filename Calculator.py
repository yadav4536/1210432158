from flask import Flask, request, jsonify
import requests
from collections import deque
from time import time

app = Flask(__name__)

# Configuration
WINDOW_SIZE = 10
API_URL = "https://number/{numberid}"  # Replace with the actual API endpoint

# Global storage
numbers = deque(maxlen=WINDOW_SIZE)
numbers_set = set()
window_prev_state = []

def fetch_numbers(number_id):
    try:
        response = requests.get(f"{API_URL}/{number_id}", timeout=0.5)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        return None

def calculate_average(num_list):
    return sum(num_list) / len(num_list) if num_list else 0

@app.route('/numbers/<number_id>', methods=['GET'])
def average_calculator(number_id):
    global window_prev_state

    if number_id not in ['p', 'f', 'e', 'r']:
        return jsonify({"error": "Invalid number ID"}), 400

    # Fetch new numbers
    new_numbers = fetch_numbers(number_id)
    if new_numbers is None:
        return jsonify({"error": "Failed to fetch numbers"}), 500

    # Remove duplicates and update storage
    new_numbers = [num for num in new_numbers if num not in numbers_set]
    numbers_set.update(new_numbers)
    
    for num in new_numbers:
        if len(numbers) == WINDOW_SIZE:
            oldest_number = numbers.popleft()
            numbers_set.remove(oldest_number)
        numbers.append(num)
    
    # Prepare response data
    window_curr_state = list(numbers)
    avg = calculate_average(window_curr_state)
    
    response = {
        "windowPrevState": window_prev_state,
        "windowCurrState": window_curr_state,
        "numbers": new_numbers,
        "avg": round(avg, 2)
    }
    
    # Update previous state
    window_prev_state = window_curr_state.copy()

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000, threaded=True)
