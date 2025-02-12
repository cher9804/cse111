import random
import math
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------
# Define a class for individuals.
# ---------------------------------
class Individual:
    def __init__(self, x, y, state="susceptible"):
        """
        Initializes an individual in the simulation.

        Parameters:
            x (float): The x-coordinate of the individual.
            y (float): The y-coordinate of the individual.
            state (str): The health state of the individual.
                         Options are "susceptible", "infected", "recovered", "dead".
        """
        self.x = x
        self.y = y
        self.state = state
        self.days_infected = 0  # Counts how many time steps the individual has been infected

# -----------------------------------------------------
# Function: create_population
# Creates an initial population with random positions,
# and infects a specified number of individuals.
# -----------------------------------------------------
def create_population(parameters):
    """
    Creates the initial population of individuals with random positions.

    Parameters:
        parameters (dict): A dictionary of simulation parameters.

    Returns:
        list: A list of Individual objects.
    """
    population = []
    pop_size = parameters["population_size"]
    grid_size = parameters["grid_size"]
    initial_infected = parameters["initial_infected"]

    # Create all individuals with random positions
    for i in range(pop_size):
        x = random.uniform(0, grid_size)
        y = random.uniform(0, grid_size)
        population.append(Individual(x, y, state="susceptible"))

    # Infect a random subset of individuals
    infected_indices = random.sample(range(pop_size), initial_infected)
    for idx in infected_indices:
        population[idx].state = "infected"
        population[idx].days_infected = 0

    return population

# -----------------------------------------------------
# Function: move_individual
# Moves an individual randomly within the grid, obeying boundaries.
# -----------------------------------------------------
def move_individual(individual, parameters):
    """
    Moves an individual randomly within the grid boundaries.

    Parameters:
        individual (Individual): The individual to move.
        parameters (dict): Simulation parameters including movement_rate and grid_size.

    Returns:
        Individual: The moved individual.
    """
    movement_rate = parameters["movement_rate"]
    grid_size = parameters["grid_size"]

    # Only move individuals that are alive (not dead)
    if individual.state != "dead":
        dx = random.uniform(-movement_rate, movement_rate)
        dy = random.uniform(-movement_rate, movement_rate)
        # Update position and ensure it stays within bounds
        individual.x = max(0, min(grid_size, individual.x + dx))
        individual.y = max(0, min(grid_size, individual.y + dy))
    return individual

# -----------------------------------------------------
# Function: calculate_distance
# Returns the Euclidean distance between two individuals.
# -----------------------------------------------------
def calculate_distance(ind1, ind2):
    """
    Calculates the Euclidean distance between two individuals.

    Parameters:
        ind1 (Individual): The first individual.
        ind2 (Individual): The second individual.

    Returns:
        float: The distance between the two individuals.
    """
    return math.sqrt((ind1.x - ind2.x)**2 + (ind1.y - ind2.y)**2)

# -----------------------------------------------------
# Function: simulate_step
# Simulates one time step of the disease spread.
# -----------------------------------------------------
def simulate_step(population, parameters):
    """
    Simulates one time step:
      1. Moves all individuals.
      2. Checks for infections: if a susceptible is close to an infected, they may become infected.
      3. Updates infected individuals: increases days_infected and changes state to recovered or dead when appropriate.

    Parameters:
        population (list): List of Individual objects.
        parameters (dict): Dictionary of simulation parameters.

    Returns:
        list: The updated population after one time step.
    """
    p_transmission = parameters["p_transmission"]
    infection_distance = parameters["infection_distance"]
    infection_duration = parameters["infection_duration"]
    p_death = parameters["p_death"]

    # 1. Move all individuals
    for individual in population:
        move_individual(individual, parameters)

    # 2. Check for new infections
    for individual in population:
        if individual.state == "susceptible":
            # Check all infected individuals for proximity
            for other in population:
                if other.state == "infected":
                    if calculate_distance(individual, other) <= infection_distance:
                        # Infect with probability p_transmission
                        if random.random() < p_transmission:
                            individual.state = "infected"
                            individual.days_infected = 0
                            break  # No need to check other infected individuals

    # 3. Update the state of infected individuals
    for individual in population:
        if individual.state == "infected":
            individual.days_infected += 1
            # After the infection duration, determine outcome
            if individual.days_infected >= infection_duration:
                if random.random() < p_death:
                    individual.state = "dead"
                else:
                    individual.state = "recovered"

    return population

# -----------------------------------------------------
# Function: count_states
# Counts the number of individuals in each state.
# -----------------------------------------------------
def count_states(population):
    """
    Counts how many individuals are in each state.

    Parameters:
        population (list): List of Individual objects.

    Returns:
        dict: A dictionary with keys "susceptible", "infected", "recovered", "dead"
              and their corresponding counts.
    """
    counts = {"susceptible": 0, "infected": 0, "recovered": 0, "dead": 0}
    for individual in population:
        counts[individual.state] += 1
    return counts

# -----------------------------------------------------
# Function: run_simulation
# Runs the simulation for a set number of time steps.
# -----------------------------------------------------
def run_simulation(parameters):
    """
    Runs the disease simulation over a number of time steps and records the state counts.

    Parameters:
        parameters (dict): Simulation parameters.

    Returns:
        list: A list of dictionaries, each representing the state counts at a time step.
    """
    population = create_population(parameters)
    simulation_steps = parameters["simulation_steps"]
    results = []

    # Record the initial state
    results.append(count_states(population))
    # Run the simulation for the defined number of steps
    for step in range(simulation_steps):
        population = simulate_step(population, parameters)
        results.append(count_states(population))
    return results

# -----------------------------------------------------
# Function: process_results
# Converts the simulation results into a pandas DataFrame.
# -----------------------------------------------------
def process_results(simulation_results):
    """
    Processes the simulation results into a pandas DataFrame for analysis and visualization.

    Parameters:
        simulation_results (list): List of state count dictionaries for each time step.

    Returns:
        pandas.DataFrame: A DataFrame with time steps as the index and state counts as columns.
    """
    df = pd.DataFrame(simulation_results)
    df.index.name = "Time Step"
    return df

# -----------------------------------------------------
# Function: visualize_data
# Uses matplotlib to create a line chart of the simulation results.
# -----------------------------------------------------
def visualize_data(df):
    """
    Visualizes the simulation data using matplotlib.

    Parameters:
        df (pandas.DataFrame): DataFrame containing state counts over time.

    Creates a line chart for each state (susceptible, infected, recovered, dead).
    """
    plt.figure(figsize=(12, 8))
    plt.plot(df.index, df["susceptible"], label="Susceptible", marker="o")
    plt.plot(df.index, df["infected"], label="Infected", marker="o")
    plt.plot(df.index, df["recovered"], label="Recovered", marker="o")
    plt.plot(df.index, df["dead"], label="Dead", marker="o")
    plt.xlabel("Time Step")
    plt.ylabel("Number of Individuals")
    plt.title("Disease Spread Simulation Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# -----------------------------------------------------
# Main function to run the complete simulation.
# -----------------------------------------------------
def main():
    """
    Main function that:
      1. Defines simulation parameters.
      2. Runs the simulation.
      3. Processes and prints the results.
      4. Visualizes the simulation data.
    """
    # Define simulation parameters
    parameters = {
        "population_size": 200,      # Total number of individuals
        "initial_infected": 5,       # Number of initially infected individuals
        "grid_size": 100,            # The grid spans from 0 to grid_size in both x and y directions
        "movement_rate": 5,          # Maximum distance an individual can move per time step
        "infection_distance": 5,     # Distance threshold for infection to occur
        "p_transmission": 0.3,       # Probability that an infection occurs if within the threshold
        "infection_duration": 10,    # Number of time steps an individual remains infected before recovery/death
        "p_death": 0.02,             # Probability of death once the infection duration is reached
        "simulation_steps": 50       # Total number of simulation steps to run
    }

    # Run the simulation
    simulation_results = run_simulation(parameters)

    # Process the results into a DataFrame for easier analysis and visualization
    df_results = process_results(simulation_results)

    # Print the simulation results (first few rows)
    print("Simulation Results (first 10 time steps):")
    print(df_results.head(10))

    # Visualize the simulation data
    visualize_data(df_results)

# -----------------------------------------------------
# Entry point of the program.
# -----------------------------------------------------
if __name__ == "__main__":
    main()
