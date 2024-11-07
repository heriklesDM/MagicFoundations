import json
import numpy as np
import matplotlib.pyplot as plt

# Load the JSON results from the file
def load_results_from_json(file_name="simulation_results.json"):
    """Loads the simulation results from a JSON file."""
    with open(file_name, "r") as f:
        return json.load(f)

# Initialize global toggle dictionary for each card type
toggle_state = {
    'common'             : True,
    'uncommon'           : True,
    'rare'               : True,
    'mythic'             : True,
    'borderless_common'  : True,
    'borderless_uncommon': True,
    'borderless_rare'    : True,
    'borderless_mythic'  : True,
    'special_guest'      : True,
    'character_land'     : True,
    'dual_land'          : True,
    'regular_frame_land' : True
}

# Plot the simulation results with toggles for each card type
def plot_results(results):
    """Plots the average rounds with standard deviation for each card type."""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create a dictionary to store the line objects for toggling
    lines = {}
    labels = []

    # Lists to store all x and y values for scaling
    all_x_vals = []
    all_avg_vals = []

    # Loop through each card type in the results
    for card_type, milestones in results.items():
        # Check if this card type is toggled on in the global state
        if not toggle_state[card_type]:  # Skip the card type if it's toggled off
            continue
        
        # Only plot card types that are toggled on
        x_vals = sorted([int(target) for target in milestones.keys()])  # Ensure x_vals are integers
        avg_vals = [milestones[str(target)]["average"] for target in x_vals]  # Get averages for each milestone
        std_devs = [milestones[str(target)]["deviation"] for target in x_vals]  # Get standard deviation

        # Add values to all_x_vals and all_avg_vals to later determine axis limits
        all_x_vals.extend(x_vals)
        all_avg_vals.extend(avg_vals)

        # Plot each card type with error bars for standard deviation
        line, = ax.plot(x_vals, avg_vals, label=f"{card_type} - avg", marker='o')
        ax.fill_between(x_vals, np.subtract(avg_vals, std_devs), np.add(avg_vals, std_devs), alpha=0.2)
        lines[card_type] = line
        labels.append(card_type)

    # Set the title, labels, and grid
    ax.set_title("Average Number of Booster Packs to get all cards (with Standard Deviation)")
    ax.set_xlabel("Number of Distinct Cards")
    ax.set_ylabel("Number of Booster Packs")
    ax.legend(title="Card Types", loc="upper right")
    ax.grid(True)

    # Dynamic x-axis and y-axis scaling based on toggled data
    # Set the x-axis limit to the maximum of all x values
    ax.set_xticks(np.arange(1, max(all_x_vals) + 1, 1))  # Ensure x-ticks are integers
    ax.set_xlim(0, max(all_x_vals))  # Set x-axis limit to the maximum x-value across visible card types
    
    # Set the y-axis limits to the minimum and maximum of the average values across all visible card types
    ax.set_ylim(min(all_avg_vals) - 5, max(all_avg_vals) + 500)  # Add some padding for better visibility

    # Show the plot with all lines and the ability to toggle them
    plt.tight_layout()
    plt.show()

# Main function to load and plot the results
def main():
    # Load the results from the JSON file
    results = load_results_from_json()

    # Plot the results
    plot_results(results)

if __name__ == "__main__":
    main()
