"""
Disease Spread Simulation with GUI

This program simulates the spread of a disease through a population.
It tracks individuals moving in a grid and updates their health state
("susceptible", "infected", "recovered", or "dead") according to
various parameters. Simulation results are processed into a pandas DataFrame,
visualized with matplotlib, and optionally controlled via a tkinter GUI.
"""

# ---------------------------
# Module Imports
# ---------------------------
import random
import math
import pandas as pd
import matplotlib.pyplot as plt

# For the GUI
import tkinter as tk
from tkinter import ttk, messagebox

# ---------------------------
# Simulation Classes and Functions
# ---------------------------
class Individual:
    def __init__(self, x, y, state="susceptible"):
        """
        Represents an individual in the simulation.
        
        Parameters:
            x (float): The x-coordinate.
            y (float): The y-coordinate.
            state (str): The health state ("susceptible", "infected", "recovered", "dead").
        """
        self.x = x
        self.y = y
        self.state = state
        self.days_infected = 0  # Counts time steps since infection


def create_population(parameters):
    """
    Creates the initial population with random positions and a few infected individuals.
    
    Parameters:
        parameters (dict): Contains keys 'population_size', 'initial_infected', and 'grid_size'.
    
    Returns:
        list: A list of Individual objects.
    """
    population = []
    pop_size = parameters["population_size"]
    grid_size = parameters["grid_size"]
    initial_infected = parameters["initial_infected"]

    # Create individuals at random positions.
    for i in range(pop_size):
        x = random.uniform(0, grid_size)
        y = random.uniform(0, grid_size)
        population.append(Individual(x, y, state="susceptible"))
    
    # Randomly infect a subset of individuals.
    infected_indices = random.sample(range(pop_size), initial_infected)
    for idx in infected_indices:
        population[idx].state = "infected"
        population[idx].days_infected = 0

    return population


def move_individual(individual, parameters):
    """
    Moves an individual randomly within the grid boundaries.
    
    Parameters:
        individual (Individual): The individual to move.
        parameters (dict): Contains keys 'movement_rate' and 'grid_size'.
    
    Returns:
        Individual: The moved individual.
    """
    movement_rate = parameters["movement_rate"]
    grid_size = parameters["grid_size"]

    # Only move if the individual is alive.
    if individual.state != "dead":
        dx = random.uniform(-movement_rate, movement_rate)
        dy = random.uniform(-movement_rate, movement_rate)
        individual.x = max(0, min(grid_size, individual.x + dx))
        individual.y = max(0, min(grid_size, individual.y + dy))
    return individual


def calculate_distance(ind1, ind2):
    """
    Calculates the Euclidean distance between two individuals.
    
    Parameters:
        ind1, ind2 (Individual): The individuals to compare.
    
    Returns:
        float: The distance.
    """
    return math.sqrt((ind1.x - ind2.x)**2 + (ind1.y - ind2.y)**2)


def simulate_step(population, parameters):
    """
    Performs a single simulation time step:
      1. Moves all individuals.
      2. Checks if susceptible individuals become infected by nearby infected individuals.
      3. Updates infected individuals by increasing infection duration and determining recovery or death.
    
    Parameters:
        population (list): List of Individual objects.
        parameters (dict): Contains keys such as 'p_transmission', 'infection_distance',
                           'infection_duration', and 'p_death'.
    
    Returns:
        list: The updated population.
    """
    p_transmission = parameters["p_transmission"]
    infection_distance = parameters["infection_distance"]
    infection_duration = parameters["infection_duration"]
    p_death = parameters["p_death"]

    # 1. Move each individual.
    for individual in population:
        move_individual(individual, parameters)

    # 2. For each susceptible individual, check for nearby infected individuals.
    for individual in population:
        if individual.state == "susceptible":
            for other in population:
                if other.state == "infected":
                    if calculate_distance(individual, other) <= infection_distance:
                        if random.random() < p_transmission:
                            individual.state = "infected"
                            individual.days_infected = 0
                            break  # No need to check further once infected.

    # 3. Update infected individuals.
    for individual in population:
        if individual.state == "infected":
            individual.days_infected += 1
            if individual.days_infected >= infection_duration:
                if random.random() < p_death:
                    individual.state = "dead"
                else:
                    individual.state = "recovered"

    return population


def count_states(population):
    """
    Counts the number of individuals in each state.
    
    Parameters:
        population (list): List of Individual objects.
    
    Returns:
        dict: A dictionary with counts for "susceptible", "infected", "recovered", and "dead".
    """
    counts = {"susceptible": 0, "infected": 0, "recovered": 0, "dead": 0}
    for individual in population:
        counts[individual.state] += 1
    return counts


def run_simulation(parameters):
    """
    Runs the entire simulation for a set number of time steps.
    
    Parameters:
        parameters (dict): Simulation parameters including "simulation_steps".
    
    Returns:
        list: A list of dictionaries recording the state counts at each time step.
    """
    population = create_population(parameters)
    simulation_steps = parameters["simulation_steps"]
    results = []

    # Record the initial state.
    results.append(count_states(population))
    for step in range(simulation_steps):
        population = simulate_step(population, parameters)
        results.append(count_states(population))
    return results


def process_results(simulation_results):
    """
    Converts simulation results (list of state dictionaries) into a pandas DataFrame.
    
    Parameters:
        simulation_results (list): The simulation data.
    
    Returns:
        pandas.DataFrame: DataFrame with time steps as the index.
    """
    df = pd.DataFrame(simulation_results)
    df.index.name = "Time Step"
    return df


def visualize_data(df):
    """
    Visualizes simulation results using matplotlib.
    
    Parameters:
        df (pandas.DataFrame): The processed simulation results.
    
    Displays a line chart of state counts over time.
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


def main():
    """
    Main function to run the simulation from the command line.
    It sets up the simulation parameters, runs the simulation, prints the results,
    and displays a visualization.
    """
    parameters = {
        "population_size": 200,      # Total number of individuals
        "initial_infected": 5,       # Initially infected individuals
        "grid_size": 100,            # The grid's size (0 to 100 for both x and y)
        "movement_rate": 5,          # Maximum movement per time step
        "infection_distance": 5,     # Distance threshold for infection
        "p_transmission": 0.3,       # Probability of infection upon contact
        "infection_duration": 10,    # Time steps until recovery or death
        "p_death": 0.02,             # Probability of death after infection
        "simulation_steps": 50       # Total simulation steps
    }
    simulation_results = run_simulation(parameters)
    df_results = process_results(simulation_results)
    print("Simulation Results (first 10 time steps):")
    print(df_results.head(10))
    visualize_data(df_results)


# ---------------------------
# Graphical User Interface (GUI)
# ---------------------------
def build_gui():
    """
    Builds and runs a simple tkinter GUI for the simulation.
    
    The GUI allows the user to enter:
        - Population Size
        - Initial Infected
        - Simulation Steps
    
    When the 'Run Simulation' button is clicked, the simulation is executed,
    the final state counts are displayed, and the simulation is visualized.
    """
    def run_simulation_gui():
        try:
            # Retrieve values from the GUI input fields.
            population_size = int(population_entry.get())
            initial_infected = int(infected_entry.get())
            simulation_steps = int(steps_entry.get())
            
            # Define parameters (some values are fixed for simplicity).
            parameters = {
                "population_size": population_size,
                "initial_infected": initial_infected,
                "grid_size": 100,
                "movement_rate": 5,
                "infection_distance": 5,
                "p_transmission": 0.3,
                "infection_duration": 10,
                "p_death": 0.02,
                "simulation_steps": simulation_steps
            }
            # Run the simulation and process the results.
            simulation_results = run_simulation(parameters)
            df_results = process_results(simulation_results)
            # Display final state counts in a message box.
            messagebox.showinfo("Simulation Complete",
                                f"Simulation ran for {simulation_steps} steps.\n"
                                f"Final state counts:\n{df_results.iloc[-1].to_dict()}")
            # Visualize the simulation results.
            visualize_data(df_results)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Create the main window.
    root = tk.Tk()
    root.title("Disease Simulation GUI")

    # Create labels and entry fields for simulation parameters.
    ttk.Label(root, text="Population Size:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    population_entry = ttk.Entry(root)
    population_entry.grid(row=0, column=1, padx=5, pady=5)
    population_entry.insert(0, "200")

    ttk.Label(root, text="Initial Infected:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    infected_entry = ttk.Entry(root)
    infected_entry.grid(row=1, column=1, padx=5, pady=5)
    infected_entry.insert(0, "5")

    ttk.Label(root, text="Simulation Steps:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    steps_entry = ttk.Entry(root)
    steps_entry.grid(row=2, column=1, padx=5, pady=5)
    steps_entry.insert(0, "50")

    # Button to run the simulation.
    run_button = ttk.Button(root, text="Run Simulation", command=run_simulation_gui)
    run_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

    # Start the GUI event loop.
    root.mainloop()


# ---------------------------
# Entry Point
# ---------------------------
if __name__ == "__main__":
    # Uncomment one of the following lines depending on which mode you want to run:
    
    # To run the simulation in command-line mode (with matplotlib visualization):
    main()
    
    # To run the simulation using the graphical user interface (GUI):
    build_gui()
