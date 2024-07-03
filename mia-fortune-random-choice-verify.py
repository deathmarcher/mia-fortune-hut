#!/usr/bin/env python3

import random
import time

def weighted_random_choice(items):
    total = sum(item['probability'] for item in items)
    r = round(random.uniform(0, total), 2)
    upto = 0
    for item in items:
        upto += item['probability']
        if round(upto, 2) >= round(r, 2):
            return item
    assert False, "Shouldn't get here"

def main():
    items = [
        {"item_name": "Fire Crystal", "quantity": 10, "probability": 1.59},
        {"item_name": "Fire Crystal", "quantity": 5, "probability": 3.17},
        {"item_name": "Charm Design", "quantity": 3, "probability": 3.17},
        {"item_name": "Charm Design", "quantity": 1, "probability": 3.17},
        {"item_name": "100 Gems", "quantity": 5, "probability": 3.17},
        {"item_name": "100 Gems", "quantity": 1, "probability": 3.17},
        {"item_name": "100 Enhancement XP Component", "quantity": 3, "probability": 3.17},
        {"item_name": "100 Enhancement XP Component", "quantity": 1, "probability": 3.25},
        {"item_name": "3h General Speedup", "quantity": 1, "probability": 3.17},
        {"item_name": "10,000 Hero XP", "quantity": 2, "probability": 3.17},
        {"item_name": "1h General Speedup", "quantity": 1, "probability": 3.17},
        {"item_name": "1h Construction Speedup", "quantity": 1, "probability": 3.17},
        {"item_name": "1h Training Speedup", "quantity": 1, "probability": 3.17},
        {"item_name": "1h Research Speedup", "quantity": 1, "probability": 3.17},
        {"item_name": "100K Meat", "quantity": 1, "probability": 9.52},
        {"item_name": "100K Wood", "quantity": 1, "probability": 9.52},
        {"item_name": "100K Coal", "quantity": 1, "probability": 9.52},
        {"item_name": "100K Iron", "quantity": 1, "probability": 9.52},
        {"item_name": "5m General Speedup", "quantity": 3, "probability": 4.76},
        {"item_name": "5m Construction Speedup", "quantity": 3, "probability": 4.76},
        {"item_name": "5m Training Speedup", "quantity": 3, "probability": 4.76},
        {"item_name": "5m Research Speedup", "quantity": 3, "probability": 4.76}
    ]

    # Number of times to select an item
    num_selections = 10000000

    # Dictionary to store the counts of each item selected
    item_counts = {f"{item['item_name']} x{item['quantity']}": 0 for item in items}

    start_time = time.time()
    next_print_time = start_time + 2

    # Simulate the selection process
    for i in range(1, num_selections + 1):
        selected_item = weighted_random_choice(items)
        item_key = f"{selected_item['item_name']} x{selected_item['quantity']}"
        item_counts[item_key] += 1

        # Print progress every 2 seconds
        current_time = time.time()
        if current_time >= next_print_time:
            elapsed_time = current_time - start_time
            progress = i / num_selections
            remaining_time = elapsed_time * (1 - progress) / progress
            print(f"Progress: {progress * 100:.2f}% - Estimated Time Remaining: {remaining_time:.2f} seconds")
            next_print_time = current_time + 2

    # Calculate the observed probabilities
    observed_probabilities = {item: count / num_selections * 100 for item, count in item_counts.items()}

    # Print the results
    print("Item Name and Quantity | Expected Probability | Observed Probability | Difference")
    print("---------------------------------------------------------------")
    for item in items:
        item_key = f"{item['item_name']} x{item['quantity']}"
        expected_probability = item['probability']
        observed_probability = observed_probabilities[item_key]
        difference = observed_probability - expected_probability
        print(f"{item_key:20} | {expected_probability:19} | {observed_probability:19.2f} | {difference:10.2f}")

if __name__ == "__main__":
    main()

