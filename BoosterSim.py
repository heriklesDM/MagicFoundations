import random
from concurrent.futures import ProcessPoolExecutor, as_completed
from collections import defaultdict
import json
import numpy as np
import os

MAX_ROUNDS = 1000

# Constants for new parameters
COMMON_CARD_COUNT = 80
UNCOMMON_CARD_COUNT = 100
RARE_CARD_COUNT = 60
MYTHIC_CARD_COUNT = 20
BORDERLESS_COMMON_COUNT = 2
BORDERLESS_UNCOMMON_COUNT = 8
BORDERLESS_RARE_COUNT = 43
BORDERLESS_MYTHIC_COUNT = 17
SPECIAL_GUEST_CARD_COUNT = 10
CHARACTER_LAND_COUNT = 10
DUAL_LAND_COUNT = 10
REGULAR_FRAME_LAND_COUNT = 10

# Probability distributions for different stacks
STACK_2_COMMON_PROBABILITY = 0.985  # 98.5% common, 1.5% special guest
STACK_3_PROBABILITIES = {
    "rare": 0.78,
    "mythic": 0.128,
    "borderless_rare": 0.077,
    "borderless_mythic": 0.015
}
STACK_4_PROBABILITIES = {
    "common": 0.167,
    "uncommon": 0.583,
    "rare": 0.163,
    "mythic": 0.026,
    "borderless_rare": 0.016,
    "borderless_mythic": 0.003,
    "borderless_common": 0.018,
    "borderless_uncommon": 0.024
}
STACK_5_PROBABILITIES = {
    "character_land": 0.25,
    "dual_land": 0.50,
    "regular_frame_land": 0.25
}

# Define the ID ranges for all card types
CARD_ID_RANGES = {
    "common": range(1, COMMON_CARD_COUNT + 1),
    "uncommon": range(101, 101 + UNCOMMON_CARD_COUNT),
    "rare": range(201, 201 + RARE_CARD_COUNT),
    "mythic": range(301, 301 + MYTHIC_CARD_COUNT),
    "borderless_common": range(401, 401 + BORDERLESS_COMMON_COUNT),
    "borderless_uncommon": range(501, 501 + BORDERLESS_UNCOMMON_COUNT),
    "borderless_rare": range(601, 601 + BORDERLESS_RARE_COUNT),
    "borderless_mythic": range(701, 701 + BORDERLESS_MYTHIC_COUNT),
    "special_guest": range(801, 801 + SPECIAL_GUEST_CARD_COUNT),
    "character_land": range(901, 901 + CHARACTER_LAND_COUNT),
    "dual_land": range(1001, 1001 + DUAL_LAND_COUNT),
    "regular_frame_land": range(1101, 1101 + REGULAR_FRAME_LAND_COUNT)
}

# Function to simulate a draw from Stack 1 (6 commons)
# Function to simulate a draw from Stack 1 (6 commons)
def draw_from_stack1():
    """Simulates a draw of 6 common cards"""
    # Return the list of 6 common cards and the card type as a tuple
    return random.sample(CARD_ID_RANGES["common"], 6), "common"

# Function to simulate a draw from Stack 2 (1 card, 98.5% common, 1.5% special guest)
def draw_from_stack2():
    """Simulates a draw from Stack 2 with 98.5% common, 1.5% special guest"""
    if random.random() < STACK_2_COMMON_PROBABILITY:
        # Return the card ID and the card type as a tuple
        return random.choice(CARD_ID_RANGES["common"]), "common"
    else:
        # Return the card ID and the card type as a tuple
        return random.choice(CARD_ID_RANGES["special_guest"]), "special_guest"

# Function to simulate a draw from Stack 3 (1 card with given chances)
def draw_from_stack3():
    """Simulates a draw from Stack 3 (rare, mythic, borderless rare, borderless mythic)"""
    category = random.choices(
        population=list(STACK_3_PROBABILITIES.keys()),
        weights=list(STACK_3_PROBABILITIES.values()),
        k=1
    )[0]
    # Return the card ID and the card type as a tuple
    return random.choice(CARD_ID_RANGES[category]), category

# Function to simulate a draw from Stack 4 (draw twice from the stack with multiple chances)
def draw_from_stack4():
    """Simulates a draw from Stack 4 (common, uncommon, rare, mythic, borderless)"""
    categories = random.choices(
        population=list(STACK_4_PROBABILITIES.keys()),
        weights=list(STACK_4_PROBABILITIES.values()),
        k=2  # Two draws
    )
    # Return a list of card IDs and their respective card types as tuples
    return [
        (random.choice(CARD_ID_RANGES[category]), category) for category in categories
    ], categories

# Function to simulate a draw from Stack 5 (character land, dual land, regular frame land)
def draw_from_stack5():
    """Simulates a draw from Stack 5 (character land, dual land, regular frame land)"""
    category = random.choices(
        population=list(STACK_5_PROBABILITIES.keys()),
        weights=list(STACK_5_PROBABILITIES.values()),
        k=1
    )[0]
    # Return the card ID and the card type as a tuple
    return random.choice(CARD_ID_RANGES[category]), category

# Function to simulate all draws until all milestones are reached
def simulate_draws_until_targets():
    """Simulates card draws from all stacks until all target milestones are reached"""
    unique_cards = {card_type: set() for card_type in CARD_ID_RANGES.keys()}  # Track unique cards for all types
    rounds = 0
    milestones = defaultdict(dict)  # Store milestones for each card type

    while True:
        # Draw from all stacks
        commons, _ = draw_from_stack1()  # List of 6 common cards
        unique_cards["common"].update(commons)  # Add all common cards to the pool
        
        special_guest_card, card_type_2 = draw_from_stack2()  # Draw 1 card, check its type
        if card_type_2 == "common":
            unique_cards["common"].add(special_guest_card)  # Add common card to common pool
        else:
            unique_cards["special_guest"].add(special_guest_card)  # Add special guest card to its pool
        
        uncommons = draw_from_stack3()  # Draw 3 uncommons
        unique_cards["uncommon"].update(uncommons)  # Add uncommons to the pool
        
        rare_card, card_type_3 = draw_from_stack3()  # Draw from Stack 3
        unique_cards[card_type_3].add(rare_card)  # Add the drawn card to the appropriate pool
        
        drawn_stack4, categories_stack4 = draw_from_stack4()  # Draw twice from Stack 4
        for card, category in zip(drawn_stack4, categories_stack4):
            unique_cards[category].add(card)  # Add cards to the respective categories
        
        character_land_card, card_type_5 = draw_from_stack5()  # Draw from Stack 5
        unique_cards[card_type_5].add(character_land_card)  # Add land cards to their pool
        
        # Increment the round counter
        rounds += 1
        
        # Check and store milestones for each card type
        all_completed = True
        for card_type, card_range in CARD_ID_RANGES.items():
            for target in range(1, len(card_range) + 1):
                if len(unique_cards[card_type]) >= target and milestones[card_type].get(target) is None:
                    milestones[card_type][target] = rounds
                if milestones[card_type].get(target) is None:
                    all_completed = False
        
        # If all milestones are completed, stop the simulation
        if all_completed:
            break

    return milestones

# Function to run the simulation with multiprocessing
def run_monte_carlo_simulation():
    """Runs the Monte Carlo simulation with multiprocessing to speed up the simulation"""
    results = defaultdict(lambda: defaultdict(list))
    num_cores = os.cpu_count()  # Use all available CPU cores

    # Use ProcessPoolExecutor for multiprocessing
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        future_to_round = {executor.submit(simulate_draws_until_targets): i for i in range(10000)}

        for future in as_completed(future_to_round):
            result = future.result()
            for card_type, milestones in result.items():
                for target, rounds in milestones.items():
                    results[card_type][target].append(rounds)

    # Compute averages, medians, and standard deviations
    final_results = defaultdict(dict)
    for card_type, milestones in results.items():
        for target, values in milestones.items():
            final_results[card_type][target] = {
                "average": np.mean(values),
                "median": np.median(values),
                "deviation": np.std(values)
            }

    return final_results

# Save results to a JSON file
def save_results_to_json(results):
    """Saves simulation results to a JSON file"""
    with open("simulation_results.json", "w") as f:
        json.dump(results, f, indent=4)

# Run the simulation and save results
results = run_monte_carlo_simulation()
save_results_to_json(results)
