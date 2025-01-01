import numpy as np
from tqdm import tqdm
from models.ant import Ant
from itertools import product
from algorithm.aco import ACO
from utils.constants import jobs 
from utils.method.data_treatment import create_matches

def find_optimal_path(jobs, workers, alpha=3.875, beta=1, evap_coeff=0.5, Q=jobs, iterations=50, verbose=0):
    """
    Executes the ACO function multiple times to find the best path with the lowest total duration.
    
    :param jobs: List of jobs.
    :param matches: List of Match objects.
    :param ants: List of Ant objects.
    :param alpha: Pheromone importance.
    :param beta: Heuristic importance.
    :param evap_coeff: Pheromone evaporation coefficient.
    :param Q: Constant for pheromone deposition.
    :param iterations: Number of times to run the ACO function.
    :return: A tuple containing the optimal path and the lowest total duration found.
    """
    best_path = None
    lowest_duration = float('inf')

    for i in range(iterations):
        matches = create_matches(jobs,workers,0.1)    
        ants = []
        for j in range(1, 4):
            ants.append(Ant(id=j))
        # Run the ACO algorithm
        optimal_path, total_duration = ACO(jobs, workers, matches, ants, alpha, beta, evap_coeff, Q)

        # Check if the current run's duration is the lowest
        if total_duration < lowest_duration:
            lowest_duration = total_duration
            best_path = optimal_path
        if verbose:
            print(f"Iteration {i+1}: Duration={total_duration}, Best Duration={lowest_duration}")
    return best_path, lowest_duration


def fine_tune_ACO(jobs, workers, initial_pheromones, num_ants_list, alpha_values, beta_values, evap_coeffs, Q_values, max_iterations=1000, tolerance=1e-5):
    """
    Fine-tunes the ACO algorithm by testing all combinations of the given parameter values.
    
    :param jobs: List of job objects.
    :param workers: List of worker objects.
    :param initial_pheromones: List of initial pheromone levels to test.
    :param num_ants_list: List of numbers of ants to test.
    :param alpha_values: List of alpha values to test.
    :param beta_values: List of beta values to test.
    :param evap_coeffs: List of evaporation coefficients to test.
    :param Q_values: List of Q values to test.
    :param max_iterations: Maximum number of iterations for each ACO run.
    :param tolerance: Convergence tolerance for each ACO run.
    :return: Sorted list of results with total duration and corresponding parameters.
    """
    # Initialize a list to store results
    results = []
   
    # Calculate the total number of combinations for tqdm
    total_combinations = len(initial_pheromones) * len(num_ants_list) * len(alpha_values) * len(beta_values) * len(evap_coeffs) * len(Q_values)

    # Generate all combinations of the parameter values
    for initial_pheromone, num_ants, alpha, beta, evap_coeff, Q in tqdm(product(initial_pheromones, num_ants_list, alpha_values, beta_values, evap_coeffs, Q_values), total=total_combinations, desc="Fine-tuning parameters"):
        
        # Create matches for the current initial pheromone level
        matches = create_matches(jobs, workers, initial_pheromone)
       
        # Create ants for the current number of ants
        ants = [Ant(id=i) for i in range(1, num_ants + 1)]
       
        # Run the ACO algorithm with the current combination of parameters
        optimal_path, total_duration = ACO(jobs, matches, ants, alpha, beta, evap_coeff, Q, max_iterations, tolerance, max_iterations/2)
       
        # Store the result with parameters for sorting later
        results.append({
            'total_duration': total_duration,
            'parameters': {
                'initial_pheromone': initial_pheromone,
                'num_ants': num_ants,
                'alpha': alpha,
                'beta': beta,
                'evap_coeff': evap_coeff,
                'Q': Q
            }
        })

    # Sort results by total duration in ascending order
    results.sort(key=lambda x: x['total_duration'])

    # Print sorted results
    for result in results:
        params = result['parameters']
        print(f"Total Duration: {result['total_duration']} | Parameters: Initial Pheromone: {params['initial_pheromone']}, "
              f"Num Ants: {params['num_ants']}, Alpha: {params['alpha']}, Beta: {params['beta']}, "
              f"Evap Coeff: {params['evap_coeff']}, Q: {params['Q']}")

    return results

# Define the parameters based on provided ranges and scaling method
def define_parameter_sets(jobs, workers):
    # Number of jobs (nodes) used to scale Q
    N = len(jobs)
    
    # Define parameter sets
    initial_pheromones = np.linspace(0.1, 1.0, 5).tolist()  # Initial pheromone level τ₀ from 0.1 to 1.0
    num_ants_list = [int(x) for x in np.linspace(N, 2 * N, 10).tolist()]  # Number of ants from N to 2N
    alpha_values = np.linspace(0.5, 5, 5).tolist()  # Alpha (α) values from 0.5 to 5
    beta_values = np.linspace(1, 10, 5).tolist()  # Beta (β) values from 1 to 10
    evap_coeffs = np.linspace(0.1, 0.9, 5).tolist()  # Evaporation coefficient (ρ) from 0.1 to 0.9

    # Q values scaled by path length (N) with k ranging from 1 to 5
    Q_values = [k * N for k in range(1, 6)]

    # Combine parameter sets for fine-tuning
    return initial_pheromones, num_ants_list, alpha_values, beta_values, evap_coeffs, Q_values