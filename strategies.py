strategies = [
    {
        "name": "Strategy 1: Refresh on finding wish reward or reveal cost > 4",
        "logic": lambda event_state, data: (
            "end" if event_state['tokens'] < event_state['round_state']['reveal_cost'] and event_state['tokens'] < event_state['round_state']['refresh_cost'] else
            "refresh" if event_state['round_state']['wish_reward_found'] and event_state['round_state']['reveal_cost'] > 4 else
            "reveal"
        )
    },
    {
        "name": "Strategy 2: Refresh on reveal cost > 5 if no Essence Stones left",
        "logic": lambda event_state, data: (
            "end" if event_state['tokens'] < event_state['round_state']['reveal_cost'] and event_state['tokens'] < event_state['round_state']['refresh_cost'] else
            "refresh" if event_state['round_state']['reveal_cost'] > 5 and not any(
                reward['name'] == "Essence Stones" for reward in event_state['round_state']['current_rewards'] if reward not in event_state['round_state']['revealed_rewards']
            ) else
            "reveal"
        )
    },
    {
        "name": "Strategy 3: Reveal always",
        "logic": lambda event_state, data: (
            "end" if event_state['tokens'] < event_state['round_state']['reveal_cost'] and event_state['tokens'] < event_state['round_state']['refresh_cost'] else
            "reveal"
        )
    },
    {
        "name": "Strategy 4: Reveal if Multiplier in remaining rewards",
        "logic": lambda event_state, data: (
            "end" if event_state['tokens'] < event_state['round_state']['reveal_cost'] and event_state['tokens'] < event_state['round_state']['refresh_cost'] else
            "reveal" if any(
                reward['name'] == "Multiplier" for reward in event_state['round_state']['current_rewards'] if reward not in event_state['round_state']['revealed_rewards']
            ) else
            "refresh"
        )
    },
    {
        "name": "Strategy 5: Refresh if no wanted items in remaining rewards",
        "logic": lambda event_state, data: (
            "end" if event_state['tokens'] < event_state['round_state']['reveal_cost'] and event_state['tokens'] < event_state['round_state']['refresh_cost'] else
            "refresh" if not any(
                reward['name'] in ["Fire Crystals", "Charm Designs", "Enhancement XP Component", "Essence Stones"]
                for reward in event_state['round_state']['current_rewards'] if reward not in event_state['round_state']['revealed_rewards']
            ) else
            "reveal"
        )
    },
    {
        "name": "Strategy 6: Reveal if reveal cost < 10, otherwise refresh",
        "logic": lambda event_state, data: (
            "end" if event_state['tokens'] < event_state['round_state']['reveal_cost'] and event_state['tokens'] < event_state['round_state']['refresh_cost'] else
            "reveal" if event_state['round_state']['reveal_cost'] < 10 else
            "refresh"
        )
    },
    {
        "name": "Strategy 7: Refresh on finding wish reward or reveal cost > 3",
        "logic": lambda event_state, data: (
            "end" if event_state['tokens'] < event_state['round_state']['reveal_cost'] and event_state['tokens'] < event_state['round_state']['refresh_cost'] else
            "refresh" if event_state['round_state']['wish_reward_found'] and event_state['round_state']['reveal_cost'] > 3 else
            "reveal"
        )
    }
]
