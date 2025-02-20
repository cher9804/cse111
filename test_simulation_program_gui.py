from simulation_program_gui import (
    Individual,
    create_population,
    move_individual,
    calculate_distance,
    simulate_step,
    count_states,
    run_simulation,
    process_results,
    main
)
from math import isclose
from pytest import approx
import random
import math
import pandas as pd
import pytest

# ---------------------------
# Test for create_population
# ---------------------------
def test_create_population():
    """Verify that create_population correctly creates the population.
    
    It should create a list of individuals with the specified population size
    and the correct number of initially infected individuals.
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
    assert isinstance(population, list), (
        f"Expected a list but got {type(population)}"
    )
    assert len(population) == parameters["population_size"], (
        f"Expected {parameters['population_size']} individuals but got {len(population)}"
    )
    infected_count = sum(1 for person in population if person.state == "infected")
    assert infected_count == parameters["initial_infected"], (
        f"Expected {parameters['initial_infected']} infected individuals but got {infected_count}"
    )

# ---------------------------
# Test for move_individual
# ---------------------------
def test_move_individual():
    """Verify that move_individual moves an individual within grid boundaries."""
    parameters = {"movement_rate": 5, "grid_size": 100}
    person = Individual(50, 50)
    random.seed(42)  # Fix seed for reproducibility
    moved_person = move_individual(person, parameters)
    assert 0 <= moved_person.x <= parameters["grid_size"], (
        f"Person's x coordinate {moved_person.x} is out of bounds"
    )
    assert 0 <= moved_person.y <= parameters["grid_size"], (
        f"Person's y coordinate {moved_person.y} is out of bounds"
    )

# ---------------------------
# Test for calculate_distance
# ---------------------------
def test_calculate_distance():
    """Verify that calculate_distance returns the correct Euclidean distance."""
    person1 = Individual(0, 0)
    person2 = Individual(3, 4)
    distance = calculate_distance(person1, person2)
    expected_distance = 5.0  # 3-4-5 triangle
    assert isclose(distance, expected_distance, rel_tol=1e-5), (
        f"Expected distance {expected_distance} but got {distance}"
    )

# ---------------------------
# Test for simulate_step
# ---------------------------
def test_simulate_step():
    """Verify that simulate_step updates the population.
    
    To force state changes, use a small grid size, p_transmission = 1.0, and p_death = 0.0.
    """
    parameters = {
        "population_size": 20,
        "initial_infected": 3,
        "grid_size": 10,          # Small grid to force proximity
        "movement_rate": 5,
        "infection_distance": 10, # Cover the small grid
        "p_transmission": 1.0,    # Force infection
        "infection_duration": 3,
        "p_death": 0.0,           # Avoid death for testing
        "simulation_steps": 1
    }
    population = create_population(parameters)
    states_before = [ind.state for ind in population]
    new_population = simulate_step(population, parameters)
    states_after = [ind.state for ind in new_population]
    assert len(new_population) == parameters["population_size"], (
        f"Expected population size {parameters['population_size']} but got {len(new_population)}"
    )
    # If any susceptible were present, they should change state due to forced transmission.
    if "susceptible" in states_before:
        assert states_after != states_before, "No state changes detected in simulate_step"

# ---------------------------
# Test for count_states
# ---------------------------
def test_count_states():
    """Verify that count_states correctly counts each state in a small population."""
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

# ---------------------------
# Test for run_simulation
# ---------------------------
def test_run_simulation():
    """Verify that run_simulation runs the correct number of time steps and returns valid results."""
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
    random.seed(42)
    results = run_simulation(parameters)
    expected_steps = parameters["simulation_steps"] + 1  # initial state plus each step
    assert len(results) == expected_steps, (
        f"Expected {expected_steps} records but got {len(results)}"
    )
    for record in results:
        for key in ["susceptible", "infected", "recovered", "dead"]:
            assert key in record, f"Record {record} is missing key '{key}'"

# ---------------------------
# Test for process_results
# ---------------------------
def test_process_results():
    """Verify that process_results converts simulation results into a pandas DataFrame."""
    simulation_results = [
        {"susceptible": 95, "infected": 5, "recovered": 0, "dead": 0},
        {"susceptible": 90, "infected": 7, "recovered": 3, "dead": 0},
        {"susceptible": 85, "infected": 5, "recovered": 7, "dead": 3}
    ]
    df = process_results(simulation_results)
    assert isinstance(df, pd.DataFrame), (
        f"Expected a pandas DataFrame but got {type(df)}"
    )
    assert df.shape[0] == len(simulation_results), (
        f"Expected {len(simulation_results)} rows but got {df.shape[0]}"
    )
    for col in ["susceptible", "infected", "recovered", "dead"]:
        assert col in df.columns, f"DataFrame is missing column '{col}'"

# ---------------------------
# Test for main() function
# ---------------------------
def test_main(monkeypatch, capsys):
    """
    Verify that main() runs without error.
    
    Monkeypatch plt.show to prevent the plot from displaying, and capture printed output.
    """
    from simulation_program import main
    # Override plt.show to do nothing
    monkeypatch.setattr("simulation_program.plt.show", lambda: None)
    # Run main() and capture output.
    main()
    captured = capsys.readouterr().out
    assert "Simulation Results (first 10 time steps):" in captured, (
        "Expected printed output from main() not found."
    )


# Run the tests when this file is executed directly.
pytest.main(["-v", "--tb=line", "-rN", __file__])
