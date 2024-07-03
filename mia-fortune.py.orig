#!/usr/bin/env python3

import json
import random
import argparse
import time
from collections import defaultdict

def load_data(json_file):
    with open(json_file, 'r') as file:
        return json.load(file)

def initialize_game(data, wish_reward, tokens):
    rewards_pool = data['prize_pools']
    wish_reward_item = next((item for item in data['wish_rewards'] if item['name'] == wish_reward), None)
    current_rewards = random.sample([item for pool in rewards_pool for item in pool['items']], 9) + [wish_reward_item]
    random.shuffle(current_rewards)
    collected_rewards = {f"{item['name']} x{item['quantity']}": 0 for pool in rewards_pool for item in pool['items']}
    collected_rewards.update({f"{item['name']} x{item['quantity']}": 0 for item in data['wish_rewards']})
    return {
        "current_rewards": current_rewards,
        "revealed_rewards": [None] * 10,
        "collected_rewards": collected_rewards,
        "tokens": tokens,
        "reveal_cost": 1,
        "refresh_cost": 15,
        "progress": 0,
        "progress_milestones": data['progress_rewards'],
        "wish_reward_found": False,
        "wish_reward": wish_reward
    }

def print_centered(text, width):
    print(text.center(width))

def print_progress_bar(progress, total, width):
    filled_length = int(width * progress // total)
    bar = '=' * filled_length + '>' + '_' * (width - filled_length - 1)
    return bar

def generate_table(data, headers):
    col_widths = [max(len(str(item)) for item in col) for col in zip(*data)]
    col_widths = [max(width, len(header)) for width, header in zip(col_widths, headers)]
    row_format = " | ".join(["{:<" + str(width) + "}" for width in col_widths])
    table = "+" + "+".join(["-" * (width + 2) for width in col_widths]) + "+\n"
    table += "| " + row_format.format(*headers) + " |\n"
    table += "+" + "+".join(["-" * (width + 2) for width in col_widths]) + "+\n"
    for row in data:
        table += "| " + row_format.format(*row) + " |\n"
    table += "+" + "+".join(["-" * (width + 2) for width in col_widths]) + "+\n"
    return table

def print_game_state(game_state):
    terminal_width = 80

    # Title
    title = "+---------------------+\n|   Mia's Fortune Hut  |\n+---------------------+\n"
    print_centered(title, terminal_width)

    # Progress Bar
    progress_bar = print_progress_bar(game_state["progress"], 750, terminal_width - 20)
    print(f"Progress: |{progress_bar}| {game_state['progress']}")

    # Milestones
    milestones = game_state['progress_milestones']
    milestone_data = [[str(milestone['milestone']), milestone['rewards']] for milestone in milestones]
    milestone_table = generate_table(milestone_data, ["Milestone", "Rewards"])
    print(milestone_table)

    # Collected Rewards
    collected_data = [[name, str(quantity)] for name, quantity in game_state["collected_rewards"].items()]
    collected_table = generate_table(collected_data, ["Collected Reward", "Quantity"])
    print(collected_table)

    # Possible Rewards
    possible_data = [[str(i + 1), reward["name"], str(reward["quantity"])] for i, reward in enumerate(game_state["current_rewards"])]
    possible_table = generate_table(possible_data, ["Index", "Possible Reward", "Quantity"])

    # Revealed Rewards
    revealed_data = [[str(i + 1), reward["name"] if reward else "???" ] for i, reward in enumerate(game_state["revealed_rewards"])]
    revealed_table = generate_table(revealed_data, ["Index", "Revealed Reward"])

    print(f"\n{possible_table}\n{revealed_table}\n")

    # Tokens, Reveal Cost, and Refresh Cost
    print(f"Tokens: {game_state['tokens']}  Reveal Cost: {game_state['reveal_cost']}  Refresh Cost: {game_state['refresh_cost']}\n")

def weighted_random_choice(items):
    total = sum(item['probability'] for item in items)
    r = random.uniform(0, total)
    upto = 0
    for item in items:
        if upto + item['probability'] >= r:
            return item
        upto += item['probability']
    assert False, "Shouldn't get here"

def simulate_game(game_state, strategy, verbose):
    global data
    while game_state['tokens'] >= game_state['reveal_cost'] or game_state['tokens'] >= game_state['refresh_cost']:
        if verbose:
            print_game_state(game_state)
            time.sleep(2)
        
        if game_state['wish_reward_found'] or game_state['refresh_cost'] >= strategy['max_cost_to_reveal']:
            if game_state['tokens'] < game_state['refresh_cost']:
                break
            game_state = initialize_game(data, game_state['wish_reward'], game_state['tokens'] - game_state['refresh_cost'])
            continue
        
        if game_state['tokens'] < game_state['reveal_cost']:
            break
        
        if not any(reward and reward['name'] in strategy['target_items'] for reward in game_state['revealed_rewards']):
            if game_state['tokens'] < game_state['refresh_cost']:
                break
            game_state = initialize_game(data, game_state['wish_reward'], game_state['tokens'] - game_state['refresh_cost'])
            continue

        while True:
            index = random.randint(0, 9)
            if not game_state['revealed_rewards'][index]:
                break

        reward = game_state['current_rewards'][index]
        game_state['revealed_rewards'][index] = reward
        game_state['tokens'] -= game_state['reveal_cost']
        game_state['reveal_cost'] += 1

        if reward['name'] == game_state['wish_reward']:
            game_state['wish_reward_found'] = True
            game_state['refresh_cost'] = 0

        game_state['collected_rewards'][f"{reward['name']} x{reward['quantity']}"] += reward['quantity']
        game_state['progress'] += 1

        # Debug print to see if rewards are being collected
        if verbose:
            print(f"Collected reward: {reward['name']} x{reward['quantity']}")

def run_simulation(data, wish_reward, tokens, simulation_numbers, rounds, verbose):
    results = defaultdict(lambda: defaultdict(float))
    for sim_number in simulation_numbers:
        strategy = SIMULATIONS[sim_number - 1]
        for _ in range(rounds):
            game_state = initialize_game(data, wish_reward, tokens)
            simulate_game(game_state, strategy, verbose)
            for item, quantity in game_state['collected_rewards'].items():
                results[sim_number][item] += quantity / rounds

    return results

def print_simulation_results(results):
    for sim_number, collected_rewards in results.items():
        print(f"\nSimulation {sim_number}: {SIMULATIONS[sim_number - 1]['name']}")
        collected_data = [[item, f"{quantity:.1f}"] for item, quantity in sorted(collected_rewards.items(), key=lambda x: -x[1])]
        collected_table = generate_table(collected_data, ["Collected Reward", "Average Quantity"])
        print(collected_table)

SIMULATIONS = [
    {
        "name": "Strategy 1: Refresh on finding wish reward or refresh cost >= 6",
        "max_cost_to_reveal": 6,
        "target_items": ["Fire Crystal", "Charm Design", "100 Gems"]
    },
    {
        "name": "Strategy 2: Refresh on finding wish reward or refresh cost >= 7",
        "max_cost_to_reveal": 7,
        "target_items": ["Fire Crystal", "Charm Design", "100 Gems"]
    }
]

def main():
    global data
    parser = argparse.ArgumentParser(description='Simulate Mia\'s Fortune Hut game.')
    parser.add_argument('-c', '--config', required=True, help='Path to the JSON config file.')
    parser.add_argument('-t', '--tokens', type=int, required=True, help='Initial number of tokens.')
    parser.add_argument('-a', '--action', required=True, choices=['interactive', 'simulation'], help='Action mode.')
    parser.add_argument('-s', '--simulation', type=int, nargs='+', help='Simulation number(s) to run.')
    parser.add_argument('-r', '--rounds', type=int, help='Number of rounds for the simulation.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode.')

    args = parser.parse_args()

    data = load_data(args.config)
    simulation_numbers = args.simulation

    if args.action == 'interactive':
        print("Choose your Wish Reward from the following:")
        for i, reward in enumerate(data['wish_rewards']):
            print(f"{i + 1}. {reward['name']} x{reward['quantity']}")
        
        while True:
            try:
                choice = int(input("Enter the number of your choice: ")) - 1
                if choice < 0 or choice >= len(data['wish_rewards']):
                    raise ValueError
                wish_reward = data['wish_rewards'][choice]['name']
                break
            except ValueError:
                print("Invalid choice. Please try again.")

        game_state = initialize_game(data, wish_reward, args.tokens)

        while True:
            print_game_state(game_state)
            action = input("Enter 'r' to reveal a reward, 'f' to refresh the round, 'c' to show collected rewards, or 'h' to show history: ")

            if action == 'r':
                if game_state['tokens'] < game_state['reveal_cost']:
                    print("Not enough tokens to reveal a reward.")
                    continue
                
                while True:
                    index = random.randint(0, 9)
                    if not game_state['revealed_rewards'][index]:
                        break

                reward = game_state['current_rewards'][index]
                game_state['revealed_rewards'][index] = reward
                game_state['tokens'] -= game_state['reveal_cost']
                game_state['reveal_cost'] += 1

                if reward['name'] == wish_reward:
                    game_state['wish_reward_found'] = True
                    game_state['refresh_cost'] = 0

                game_state['collected_rewards'][f"{reward['name']} x{reward['quantity']}"] += reward['quantity']
                game_state['progress'] += 1

            elif action == 'f':
                if game_state['tokens'] < game_state['refresh_cost']:
                    print("Not enough tokens to refresh the round.")
                    continue

                game_state = initialize_game(data, wish_reward, game_state['tokens'] - game_state['refresh_cost'])

            elif action == 'c':
                collected_data = [[name, str(quantity)] for name, quantity in game_state["collected_rewards"].items()]
                collected_table = generate_table(collected_data, ["Collected Reward", "Quantity"])
                print(collected_table)

            elif action == 'h':
                # Implement history functionality if needed
                pass

    elif args.action == 'simulation':
        print("Choose your Wish Reward from the following:")
        for i, reward in enumerate(data['wish_rewards']):
            print(f"{i + 1}. {reward['name']} x{reward['quantity']}")
        
        while True:
            try:
                choice = int(input("Enter the number of your choice: ")) - 1
                if choice < 0 or choice >= len(data['wish_rewards']):
                    raise ValueError
                wish_reward = data['wish_rewards'][choice]['name']
                break
            except ValueError:
                print("Invalid choice. Please try again.")

        results = run_simulation(data, wish_reward, args.tokens, simulation_numbers, args.rounds, args.verbose)
        print_simulation_results(results)

if __name__ == "__main__":
    main()
