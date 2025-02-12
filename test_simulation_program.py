# Copyright 2020, Brigham Young University-Idaho. All rights reserved.

from simulation_program import (
    Individual,
    create_population,
    move_individual,
    calculate_distance,
    count_states,
    run_simulation,
    process_results
)
from math import isclose
from pytest import approx
import random
import math
import pandas as pd
import pytest


def test_create_population():
    """Verify that create_population works correctly.
    It should create a list of individuals with the correct population size and initial infected count.
    """
    parameters = {
        "population_size": 100,
        "initial_infected": 10,
        "grid_size": 50,
        "movement_rate": 5,
        "infection_distance": 5,
        "p_transmission": 0.3,
        "infection_duration": 10,
        "p_death": 0.02,
        "simulation_steps": 10
    }
    population = create_population(parameters)
    # Verify that population is a list with the correct number of individuals.
    assert isinstance(population, list), (
        f"create_population should return a list but returned a {type(population)}"
    )
    assert len(population) == parameters["population_size"], (
        f"Expected population size {parameters['population_size']} but got {len(population)}"
    )
    # Verify that the number of initially infected individuals is correct.
    infected_count = sum(1 for person in population if person.state == "infected")
    assert infected_count == parameters["initial_infected"], (
        f"Expected {parameters['initial_infected']} infected individuals but got {infected_count}"
    )


def test_move_individual():
    """Verify that move_individual moves an individual within grid boundaries."""
    parameters = {"movement_rate": 5, "grid_size": 100}
    person = Individual(50, 50)
    random.seed(42)  # Fix seed for reproducibility
    moved_person = move_individual(person, parameters)
    # Check that the new x and y coordinates are within the boundaries [0, grid_size].
    assert 0 <= moved_person.x <= parameters["grid_size"], (
        f"Person's x coordinate {moved_person.x} is out of bounds"
    )
    assert 0 <= moved_person.y <= parameters["grid_size"], (
        f"Person's y coordinate {moved_person.y} is out of bounds"
    )


def test_calculate_distance():
    """Verify that calculate_distance returns the correct Euclidean distance."""
    person1 = Individual(0, 0)
    person2 = Individual(3, 4)
    distance = calculate_distance(person1, person2)
    expected_distance = 5.0
    # Using math.isclose or pytest.approx to check for floating-point equality.
    assert isclose(distance, expected_distance, rel_tol=1e-5), (
        f"Expected distance {expected_distance} but got {distance}"
    )


def test_count_states():
    """Verify that count_states correctly counts the state of a small, predefined population."""
    # Create a small population with known states.
    population = [
        Individual(0, 0, "susceptible"),
        Individual(0, 0, "infected"),
        Individual(0, 0, "recovered"),
        Individual(0, 0, "dead"),
        Individual(0, 0, "infected")
    ]
    counts = count_states(population)
    expected_counts = {"susceptible": 1, "infected": 2, "recovered": 1, "dead": 1}
    assert counts == expected_counts, (
        f"Expected counts {expected_counts} but got {counts}"
    )


def test_run_simulation():
    """Verify that run_simulation runs for the correct number of time steps and returns valid results."""
    parameters = {
        "population_size": 50,
        "initial_infected": 5,
        "grid_size": 100,
        "movement_rate": 1,
        "infection_distance": 2,
        "p_transmission": 0.5,
        "infection_duration": 5,
        "p_death": 0.1,
        "simulation_steps": 10
    }
    random.seed(42)  # Set seed for reproducibility
    results = run_simulation(parameters)
    expected_steps = parameters["simulation_steps"] + 1  # Including initial state
    assert len(results) == expected_steps, (
        f"Expected {expected_steps} steps but got {len(results)}"
    )
    # Verify each result contains all required state keys.
    for record in results:
        for key in ["susceptible", "infected", "recovered", "dead"]:
            assert key in record, (
                f"Record {record} is missing key '{key}'"
            )


def test_process_results():
    """Verify that process_results converts simulation results into a pandas DataFrame."""
    simulation_results = [
        {"susceptible": 95, "infected": 5, "recovered": 0, "dead": 0},
        {"susceptible": 90, "infected": 7, "recovered": 3, "dead": 0},
        {"susceptible": 85, "infected": 5, "recovered": 7, "dead": 3}
    ]
    df = process_results(simulation_results)
    assert isinstance(df, pd.DataFrame), (
        f"process_results should return a pandas DataFrame but returned {type(df)}"
    )
    # Verify that the DataFrame has the same number of rows as simulation_results.
    assert df.shape[0] == len(simulation_results), (
        f"Expected {len(simulation_results)} rows but got {df.shape[0]}"
    )
    # Verify that the DataFrame contains the expected columns.
    for col in ["susceptible", "infected", "recovered", "dead"]:
        assert col in df.columns, f"DataFrame is missing the column '{col}'"


# Run the tests when this file is executed directly.
pytest.main(["-v", "--tb=line", "-rN", __file__])
